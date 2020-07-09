# -*- coding: utf-8 -*-
'''Processes data dayvalues from the knmi'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__version__    =  "0.0.6"
__license__    =  "GNU Lesser General Public License (LGPL)"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, threading, time, numpy as np, urllib.request
import config
import view.log as log
import view.txt as view_txt
import view.translate as tr
from zipfile import ZipFile, BadZipfile
import model.validate as validate

# Dayvalues data KNMI / Keys for dayvalues
STN      =  0 # WMO number for nl weatherstation
YYYYMMDD =  1 # Date (YYYY=year MM=month DD=day)
DDVEC    =  2 # Vector mean wind direction in degrees (360=north, 90=east, 180=south, 270=west, 0=calm/variable)
FHVEC    =  3 # Vector mean windspeed (in 0.1 m/s)
FG       =  4 # Daily mean windspeed (in 0.1 m/s)
FHX      =  5 # Maximum hourly mean windspeed (in 0.1 m/s)
FHXH     =  6 # Hourly division in which FHX was measured
FHN      =  7 # Minimum hourly mean windspeed (in 0.1 m/s)
FHNH     =  8 # Hourly division in which FHN was measured
FXX      =  9 # Maximum wind gust (in 0.1 m/s)
FXXH     = 10 # Hourly division in which FXX was measured
TG       = 11 # Daily mean temperature in (0.1 degrees Celsius)
TN       = 12 # Minimum temperature (in 0.1 degrees Celsius)
TNH      = 13 # Hourly division in which TN was measured
TX       = 14 # Maximum temperature (in 0.1 degrees Celsius)
TXH      = 15 # Hourly division in which TX was measured
T10N     = 16 # Minimum temperature at 10 cm above surface (in 0.1 degrees Celsius)
T10NH    = 17 # 6-hourly division in which T10N was measured; 6=0-6 UT, 12=6-12 UT, 18=12-18 UT, 24=18-24 UT
SQ       = 18 # Sunshine duration (in 0.1 hour) calculated from global radiation (-1 for <0.05 hour)
SP       = 19 # Percentage of maximum potential sunshine duration
Q        = 20 # Global radiation (in J/cm2)
DR       = 21 # Precipitation duration (in 0.1 hour)
RH       = 22 # Daily precipitation amount (in 0.1 mm) (-1 for <0.05 mm)
RHX      = 23 # Maximum hourly precipitation amount (in 0.1 mm) (-1 for <0.05 mm)
RHXH     = 24 # Hourly division in which RHX was measured
PG       = 25 # Daily mean sea level pressure (in 0.1 hPa) calculated from 24 hourly values
PX       = 26 # Maximum hourly sea level pressure (in 0.1 hPa)
PXH      = 27 # Hourly division in which PX was measured
PN       = 28 # Minimum hourly sea level pressure (in 0.1 hPa)
PNH      = 29 # Hourly division in which PN was measured
VVN      = 30 # Minimum visibility; 0: <100 m, 1:100-200 m, 2:200-300 m,..., 49:4900-5000 m, 50:5-6 km, 56:6-7 km, 57:7-8 km,..., 79:29-30 km, 80:30-35 km, 81:35-40 km,..., 89: >70 km)
VVNH     = 31 # Hourly division in which VVN was measured
VVX      = 32 # Maximum visibility; 0: <100 m, 1:100-200 m, 2:200-300 m,..., 49:4900-5000 m, 50:5-6 km, 56:6-7 km, 57:7-8 km,..., 79:29-30 km, 80:30-35 km, 81:35-40 km,..., 89: >70 km)
VVXH     = 33 # Uurvak waarin VVX is gemeten / Hourly division in which VVX was measured
NG       = 34 # Mean daily cloud cover (in octants, 9=sky invisible)
UG       = 35 # Daily mean relative atmospheric humidity (in percents)
UX       = 36 # Maximum relative atmospheric humidity (in percents)
UXH      = 37 # Hourly division in which UX was measured
UN       = 38 # Minimum relative atmospheric humidity (in percents)
UNH      = 39 # Hourly division in which UN was measured
EV24     = 40 # Potential evapotranspiration (Makkink) (in 0.1 mm)

entities = np.array( [
    'STN', 'YYYYMMDD', 'DDVEC', 'FHVEC', 'FG', 'FHX', 'FHXH', 'FHN', 'FHNH', 'FXX',
    'FXXH', 'TG', 'TN', 'TNH', 'TX', 'TXH', 'T10N', 'T10NH', 'SQ', 'SP',
    'Q', 'DR', 'RH', 'RHX', 'RHXH', 'PG', 'PX', 'PXH', 'PN', 'PNH',
    'VVN', 'VVNH', 'VVX', 'VVXH', 'NG', 'UG', 'UX', 'UXH', 'UN', 'UNH',
    'EV24'
    ] )

lock = threading.Lock()

def is_ent( ent ):
    '''Check if a value is a dayvalue entity'''
    e  = ent.strip().upper()
    ok = e in entities
    return ok, e

def ndx_ent( ent ):
    '''Get index by text from the array entities'''
    e = ent.strip().upper()
    ndx, = np.where( entities == e )

    return ndx[0]

def ent_ndx( ndx ):
    '''Get text by index from array entities'''
    return entities[ndx]

def list_ent( data, ent ):
    ndx = ndx_ent(ent)
    return data[:,ndx]

def day( station, yyyymmdd ):
    '''Function return a list of the dayvalues'''
    ok, data = False, np.array([])
    if validate.yyyymmdd(yyyymmdd):  # Validate date
        ok, data = read(station)
        if ok: # Date is read fine
            ndx = ndx_ent('YYYYMMDD')
            ymd, s_ymd, e_ymd = int(yyyymmdd), data[0,ndx], data[-1,ndx]

            # Check ranges and correct anyway
            if ymd < s_ymd:
                ymd = s_ymd
                log.console(f'Date {s_ymd} out range of data. First available date {ymd} used.', True)
            elif ymd > s_ymd:
                ymd = e_ymd
                log.console(f'Date {e_ymd} out range of data. First available date {ymd} used.', True)

            data = data[np.where(data[:,ndx] == ymd)] # Get values correct date

    return ok, data[0]

def read( station ):
    '''Reads data dayvalues from the knmi into a list'''
    ok, file_name = False, station.file_txt_dayvalues

    with lock:
        try:
            data = np.genfromtxt( file_name, dtype=np.float64,
                                  delimiter=config.knmi_dayvalues_delimiter,
                                  filling_values=config.knmi_dayvalues_dummy_val,
                                  skip_header=config.knmi_dayvalues_skip_rows
                                  )
        except Exception as e:
            log.console(tr.txt('Failed to read') + f': {file_name}\n{e}' )
        else:
            log.console(tr.txt('Succes reading') + f': {file_name}')
            ok = True

    return ok, data

# Numpy methode didnt work. For now using normal list -> TODO
def update_minus_1( data ):
    l = data.tolist()
    low_val = config.knmi_dayvalues_low_measure_val
    ndx_rh  = ndx_ent('rh')
    ndx_rhx = ndx_ent('rhx')
    ndx_sq  = ndx_ent('sq')
    l_ndx   = [ ndx_rh, ndx_rhx, ndx_sq ]
    for x, row in enumerate(l):
        for y, kol in enumerate(row):
            if kol == -1.0 and (y in l_ndx):
                data[x,y] = low_val

    return data

def period( data, sdate, edate ):
    '''Function selects days by start and end dates'''
    # Select values period
    date_s, date_e = float(sdate),  float(edate)
    ymd = data[:,ndx_ent('YYYYMMDD')] # Get dates array
    sel = np.where( (ymd >= date_s) & (ymd <= date_e) ) # Get selected keys for correct dates
    data = data[sel] # Make new array based on the selected days
    data = update_minus_1( data ) # Update low values

    return data

def read_stations_period( stations, symd, eymd ):
    data = np.array([])
    for station in stations:
        ok, ds = read(station)
        if ok:
            new = period( ds, symd, eymd )
            data = new if data.size == 0 else np.concatenate( (data, new) )

    return data

def unzip( station ):
    ok  = False
    zip = station.file_zip_dayvalues
    txt = station.file_txt_dayvalues
    dir = station.dir_dayvalues
    ts  = time.time_ns()
    with lock:
        try:
            log.console( f'Unzip: {zip}\nTo: {txt}')
            with ZipFile(zip, 'r') as z:
                z.extractall(dir)
        except BadZipfile as e:
            log.console(tr.txt('Failed to unzip file') + ': {zip}\n{e}')
        else:
            log.console(f'Unzip successful')
            log.console(view_txt.process_time_ext('Time to unzip', time.time_ns()-ts))
            ok = True

    return ok

def download ( station ):
    '''Function downloads etmgeg file from knmi.nl'''
    ok   = False
    zip  = station.file_zip_dayvalues
    url  = station.dayvalues_url
    ts   = time.time_ns()
    with lock:
        log.console(f'Download: {url}\nTo: {zip}')
        try:
            response = urllib.request.urlretrieve( url, zip )
        except urllib.error.URLError as e:
            log.console(tr.txt('Download failed') + f': {url}\n{e}')
        else:
            log.console(tr.txt('Dowload successful'))
            log.console(view_txt.process_time_ext(tr.txt('Time to download'), time.time_ns()-ts))
            ok = True

    return ok

def process_data( station ):
    '''Function processes (downloading en unzipping) a data file'''
    ok = download(station)
    print('')
    if ok:
        ok = unzip(station)
        print('')

    return ok

def process_all():
    '''Function processes (downloading en unzipping) files from the selected stations'''
    for station in config.stations:
        process_data( station )
