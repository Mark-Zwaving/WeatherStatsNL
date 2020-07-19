# -*- coding: utf-8 -*-
'''Processes data dayvalues from the knmi'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__version__    =  "0.1.0"
__license__    =  "GNU Lesser General Public License (LGPL)"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config
import os, threading, time, urllib.request, calendar
import numpy as np, array
from zipfile import ZipFile, BadZipfile
from datetime import datetime
import model.validate as validate
import model.utils as utils
import view.log as log
import view.txt as view_txt
import view.translate as tr

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
    ndx, = np.where( (entities == e) )

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
            data = np.genfromtxt( file_name,
                                  dtype=np.float64,
                                  delimiter=config.knmi_dayvalues_delimiter,
                                  missing_values=config.knmi_dayvalues_missing_val,
                                  filling_values=np.nan,
                                  skip_header=config.knmi_dayvalues_skip_rows,
                                  usemask=True
                                  )
        except Exception as e:
            log.console(tr.txt('Failed to read') + f': {file_name}\n{e}' )
        else:
            # log.console(tr.txt('Succes reading') + f': {file_name}')
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

def sel_tuple(l):
    '''Function puts keys in a where clausule tuple'''
    return ( (array.array(l), np.int64), )

def check_periode( per ):
    '''Function checks if a period is valuable'''
    per = per.replace(' ','')  # No spaces
    now = datetime.now()  # Date now
    yn  = now.strftime('%Y')
    mn  = now.strftime('%m')
    dn  = now.strftime('%d')

    # Make start and a end date
    sp, ep = '', ''
    if per.find('-') == -1: #  No '-' in period given
        yp = per[0:4]
        mp = per[4:6]
        dp = per[6:8]

        # if int(yp) > int(yn) || int(per) > int(f'{yn}{mn}{dn}'):
        #     return False

        # OPTION YYYYMMDD   Get only one day in a year
        if per.isdigit():
            return True
        # OPTION ********  All the data
        elif per == '*'*8:
            return True
        # OPTION ****      This actual whole year
        elif per == '****':
            return True
        # OPTION **        This actual whole month
        elif per == '**':
            return True
        # OPTION YYYY****   Get whole year
        elif yp.isdigit() and f'{mp}{dp}' == '****':
            return True
        # OPTION YYYYMM**   Get whole month in year
        elif f'{yp}{mp}'.isdigit() and f'{dp}' == '**':
            return True
        # ADVANCED OPTIONS for more different periods in a given period
        # OPTION ****MM**   Get months for every year
        elif f'{yp}{dp}' == '******' and mp.isdigit():
            return True
        # OPTION ****MMDD   Get days for every available year
        elif f'{yp}' == '****' and '{mp}{dp}'.isdigit():
            return True
    # Base period with a start and end date is given
    else:
        # Split in start and end-date
        s_per, e_per = per.split('-')

        # OPTION YYYYMMDD-YYYYMMDD  Get keys for the given periode
        if s_per.isdigit() and e_per.isdigit():
            return True
        else:
            # Split up in y , m , d
            ys, ye = s_per[0:4], e_per[0:4]
            ms, me = s_per[4:6], e_per[4:6]
            ds, de = s_per[6:8], e_per[6:8]

            # Normal period added
            if s_per.isdigit() and e_per.isdigit():
                return True

            # OPTION: YYYY****-YYYY****  A full year from startyear to endyear
            elif f'{ys}{ye}'.isdigit() and f'{ms}{ds}{me}{de}' == '*'*8:
                return True
            # OPTION: YYYYMDD-YYYYMM**  A full month + next months untill possible end
            elif s_per.isdigit() and f'{ye}{me}'.isdigit() and de == '**':
                return True

            # OPTION: 20100601-2020****  A full date untill a year or a end date -> now!
            elif s_per.isdigit() and ye.isdigit() and f'{me}{de}' == '*'*4:
                return True

            # More simple options later maybe

            # ADVANCED OPTIONS for more different periods in a given period
            # OPTION YYYYMMDD-YYYY*MMDD  A certain day in a year. From startyear to endyear.
            elif s_per.isdigit() and len(e_per) == 9 and e_per[4] == '*' and \
               ye.isdigit() and f'{ye}{e_per[5:9]}'.isdigit():
               return True

            # OPTION YYYYMMDD-YYYY*MMDD*  A certain period in a year. From startyear to endyear
            elif s_per.isdigit() and len(e_per) == 10 and \
               e_per[4] == '*' and e_per[9] == '*'  and s_per[5:9].isdigit():
               return True
            # TODO periods crossover years

            # OPTION YYYYMM**-YYYYMM** A full 1 month in an year. From startyear to endyear
            elif f'{ys}{ms}{ye}{me}'.isdigit() and f'{ds}{de}' == '****' and \
               f'{ys}{ms}' == f'{ye}{me}':
               return True

    return False

def sel_keys_days ( ymd, per ):
    # Get the dates array
    y0  = utils.f_to_s(ymd[ 0])[:4]
    yz  = utils.f_to_s(ymd[-1])[:4]
    per = per.replace(' ','')  # No spaces
    now = datetime.now()  # Date now
    yn  = now.strftime('%Y')
    mn  = now.strftime('%m')
    dn  = now.strftime('%d')
    sel = np.array([])  # Array with selected keys
    keys = []  # Empthy keys array to fill with found keys

    # Make start and a end date
    sp, ep = '', ''
    if per.find('-') == -1: #  No '-' in period given
        yp = per[0:4]
        mp = per[4:6]
        dp = per[6:8]

        # OPTION YYYYMMDD   Get only one day in a year
        if per.isdigit():
            sel = np.where( (ymd == float(per)) )
            return sel

        # OPTION ********  All the data
        elif per == '*'*8: # All time
            sp = ymd[ 0]
            ep = ymd[-1]

        # OPTION ****      This actual whole year
        elif per == '****':
            sp = f'{yn}0101'
            ep = f'{yn}{mn}{dn}'

        # OPTION **        This actual whole month
        elif per == '**':
            sp = f'{yn}{mn}01'
            ep = f'{yn}{mn}{dn}'

        # OPTION YYYY****   Get whole year
        elif yp.isdigit() and f'{mp}{dp}' == '****':
            sp = f'{yp}0101'
            ep = f'{yp}1231'

        # OPTION YYYYMM**   Get whole month in year
        elif f'{yp}{mp}'.isdigit() and f'{dp}' == '**':
            dd = calendar.monthrange(int(yp), int(mp))[1]  # num_days
            # Is it the actual month in the actual year? Then actual day
            if mp == mn and yp == yn: dd = dn
            sp = f'{yp}{mp}01'
            ep = f'{yp}{mp}{dd}'

        # ADVANCED OPTIONS for more different periods in a given period
        # OPTION ****MM**   Get months for every year
        elif f'{yp}{dp}' == '******' and mp.isdigit():
            years = range(int(y0), int(yz)+1)
            for y in years:
                m_per = f'{y}{mp}**'
                k = sel_keys_days( ymd, m_per )[0]
                if k.size != 0:
                    keys = np.concatenate((keys, k))
            return sel_tuple(keys)

        # OPTION ****MMDD   Get days for every available year
        elif f'{yp}' == '****' and '{mp}{dp}'.isdigit():
            years = range(int(y0), int(yz)+1)
            for y in years:
                k = sel_keys_days(ymd, f'{y}{mp}{dp}')[0]
                if k.size != 0:
                    keys = np.concatenate((keys, k))

            return sel_tuple(keys)

    # Base period with a start and end date is given
    else:
        # Split in start and end-date
        s_per, e_per = per.split('-')

        # OPTION YYYYMMDD-YYYYMMDD  Get keys for the given periode
        if s_per.isdigit() and e_per.isdigit():
            sp = s_per
            ep = e_per
        else:
            # Split up in y , m , d
            ys, ye = s_per[0:4], e_per[0:4]
            ms, me = s_per[4:6], e_per[4:6]
            ds, de = s_per[6:8], e_per[6:8]

            # Correct years for the wildcard option: ****1225-****1225
            if ys == '****':
                ys = y0  # First possible year
            if ye == '****':
                ye = yz  # Last possible year

            # OPTION: YYYY****-YYYY****  A full year from startyear to endyear
            elif f'{ys}{ye}'.isdigit() and f'{ms}{ds}{me}{de}' == '*'*8:
                days = calendar.monthrange(int(ye), int(mn))[1]  # num_days
                mmdd = f'{mn}{days}' if ye == yn else '1231'
                sp = f'{ys}{ms}{ds}'
                ep = f'{ye}{mmdd}'

            # OPTION: YYYYMMDD-YYYYMM**  A full month + next months untill possible end
            elif s_per.isdigit() and f'{ye}{me}'.isdigit() and de == '**':
                days = calendar.monthrange(int(ye), int(me))[1]  # num_days
                dd  = dn if f'{ye}{me}' == f'{yn}{mn}' else days
                sp  = f'{ys}{ms}{ds}'
                ep  = f'{ye}{me}{dd}'

            # OPTION: 20100601-2020****  A full date untill a year or a end date -> now!
            elif s_per.isdigit() and ye.isdigit() and f'{me}{de}' == '*'*4:
                days = calendar.monthrange(int(ye), int(me))[1]  # num_days
                mmdd = f'{mn}{dn}' if ys == ye else f'{me}{days}'
                sp = f'{ys}{ms}{ds}'
                ep = f'{ye}{mmdd}'

            # More simple options later maybe

            # ADVANCED OPTIONS for more different periods in a given period
            # OPTION YYYYMMDD-YYYY*MMDD  A certain day in a year. From startyear to endyear.
            elif s_per.isdigit() and len(e_per) == 9 and e_per[4] == '*' and \
               ye.isdigit() and f'{ye}{e_per[5:9]}'.isdigit():
                md    = f'{ms}{ds}'
                years = range(int(ys), int(ye)+1)
                for y in years:
                    k = sel_keys_days(ymd, f'{y}{md}')[0]
                    sel = np.concatenate((sel, k)) if np.size(sel) != 0 else k
                # tup = sel_tuple( keys )
                return sel

            # OPTION YYYYMMDD-YYYY*MMDD*  A certain period in a year. From startyear to endyear
            elif s_per.isdigit() and len(e_per) == 10 and \
               e_per[4] == '*' and e_per[9] == '*'  and s_per[5:9].isdigit():

                s_md, e_md = f'{ms}{ds}', f'{e_per[5:9]}'
                years = range(int(ys), int(ye)+1)
                for y in years:
                    keys = sel_keys_days(ymd, f'{y}{s_md}-{y}{e_md}')
                    sel = np.concatenate((sel, keys)) if sel[0].size != 0 else keys

                return sel
            # TODO periods crossover years

            # OPTION YYYYMM**-YYYYMM** A full 1 month in an year. From startyear to endyear
            elif f'{ys}{ms}{ye}{me}'.isdigit() and f'{ds}{de}' == '****' and \
               f'{ys}{ms}' == f'{ye}{me}':
                years = range(int(ys),int(ye)+1)
                for y in years:
                    keys = sel_keys_days(ymd, f'{y}{ms}**')
                    if keys.size != 0:
                        sel = np.concatenate( (sel, keys) ) # Add keys to total list

                return sel

    # Search for wanted date keys
    # print('SP', sp, 'EP', ep)
    sp = float(sp)
    ep = float(ep)
    sel = np.where( (ymd >= sp) & (ymd <= ep) )
    return sel

def period( data, per ):
    '''Function selects days by start and end dates'''
    ymd  = data[:, YYYYMMDD]   # Get the dates array
    sel  = sel_keys_days ( ymd, per )  # Get the keys list
    data = update_minus_1( data[sel] )    # Update/correct values -1
    return data

def read_station_period ( station, per ):
    ok, data = read(station)
    if ok: data = period( data, per )
    return ok, data

def read_stations_period( stations, per ):
    data = np.array([])
    for station in stations:
        log.console(f'Read station {station.place}', True)
        ok, data_station = read_station_period ( station, per )
        if ok:
            data = data_station if data.size == 0 else np.concatenate( (data, data_station) )

    return data

def unzip( station ):
    ok  = False
    zip = station.file_zip_dayvalues
    txt = station.file_txt_dayvalues
    dir = station.dir_dayvalues
    ts  = time.time_ns()
    with lock:
        try:
            log.console( f'Unzip {zip}')
            with ZipFile(zip, 'r') as z:
                z.extractall(dir)
        except BadZipfile as e:
            log.console(tr.txt('Failed to unzip file') + ': {zip}\n{e}')
        else:
            txt = f'Unzip successful, time to unzip is '
            log.console(view_txt.process_time_ext(txt, time.time_ns()-ts))
            ok = True

    return ok

def download ( station ):
    '''Function downloads etmgeg file from knmi.nl'''
    ok   = False
    zip  = station.file_zip_dayvalues
    url  = station.dayvalues_url
    ts   = time.time_ns()
    with lock:
        log.console(f'Download {url}')
        try:
            response = urllib.request.urlretrieve( url, zip )
        except urllib.error.URLError as e:
            log.console(tr.txt('Download failed') + f': {url}\n{e}')
        else:
            txt = 'Download successful, time to download is '
            log.console(view_txt.process_time_ext(txt, time.time_ns()-ts))
            ok = True

    return ok

def process_data( station ):
    '''Function processes (downloading en unzipping) a data file'''
    log.console(f'Process data for station: {station.place}')
    ok = download(station)
    if ok:
        ok = unzip(station)
        print('')

    return ok

def process_all():
    '''Function processes (downloading en unzipping) files from the selected stations'''
    for station in config.stations:
        process_data( station )
