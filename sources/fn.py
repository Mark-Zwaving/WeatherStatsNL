# -*- coding: utf-8 -*-
'''Library contains casual functions for different purposes'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, threading, time, zipfile, config as c, write as w, convert as cvt
import knmi

def rm_double_space(s):
    if '  ' in s:
        while '  ' in s:
            s = s.replace('  ', ' ')
    return s

def rm_tab( s ):
    if '\t' in s:
        while '\t' in s:
            s = s.replace('\t', '')
    return s

def rm_ln( s ):
    if '\n' in s:
        while '\n' in s:
            s = s.replace('\n', '')
    return s

def rm_lr( s ):
    if '\r' in s:
        while '\r' in s:
            s = s.replace('\r', '')
    return s

def rm_s( s ):
    if ' ' in s:
        while ' ' in s:
            s = s.replace(' ', '')
    return s

def san( s ):
    '''Function sanitizes input for use'''
    s = rm_lr(rm_ln(rm_tab(rm_double_space(str(s))))).strip().lower()
    if s == '' or not s:
        #print('Invoer is leeg')
        return False
    else:
        return s

def fix( s, ent ):
    ent = ent.lower()

    if not s:
        return '.'

    temp = [ 'tx', 'tn', 'tg', 't10n' ]
    prec = [ 'ev24', 'rh', 'rhx' ]
    perc = [ 'ug', 'ux', 'un', 'sp' ]
    wind = [ 'fhvec','fg','fhx','fhn','fxx' ]
    hour = [ 'fhxh', 'fhnh', 'fxxh', 'tnh', 'txh', 'rhxh',
             'pxh', 'vvnh', 'vvxh', 'uxh', 'unh', 'pnh' ]
    hou6 = [ 't10nh' ]
    pres = [ 'pg', 'pn', 'px' ]
    duri = [ 'sq', 'dr' ]
    radi = [ 'q' ]
    dire = [ 'ddvec' ]
    octa = [ 'ng' ]
    view = [ 'vvn', 'vvx' ]
    indx = [ 'heat_ndx', 'hellmann']

    if   ent in indx: return f'{float(s)/10:0.1F}'
    elif ent in temp: return f'{float(s)/10:0.1F} °C'
    elif ent in pres: return f'{float(s)/10:0.1F} hPa'
    elif ent in radi: return f'{s} J/cm2'
    elif ent in perc: return f'{s} %'
    elif ent in hour: i2 = s; i1 = int(i2) - 1; return f'{i1}-{i2} uur'
    elif ent in hou6: i2 = s; i1 = int(i2) - 6; return f'{i1}-{i2} UT'
    elif ent in octa: return s
    elif ent in wind:
        ms = float(s) / 10
        bft = cvt.ms_to_bft(ms)
        return f'{ms:0.1F} m/s {bft}bft'

    elif ent in prec:
        return '<0.05' if s == '-1' else f'{float(s)/10:0.1F}' + ' mm'
    elif ent in duri:
        return '<0.05' if s == '-1' else f'{float(s)/10:0.1F}' + ' hour'
    elif ent in dire:
        if s == '0':
            return f'{s} variable'
        else:
            # From degrees to direction
            # Source: https://www.campbellsci.com/blog/convert-wind-directions
            ldir = [ 'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S',
                     'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N' ]
            indx = int( round( float(s) % 360 / 22.5, 0 ) + 1 )
            sdir = ldir[indx]
            return f'{s}° {sdir}'
    elif ent in view:
        if s == '0': return '<100 m'
        else:
            i = int(s)
            if i < 49:
                i2 = i + 1
                return f'{i*100}-{i2*100} m'
            elif i == 50:
                return '5-6 km'
            elif i <= 79:
                i1, i2 = i - 50, i - 49
                return f'{i1}-{i2} km'
            elif i <= 89:
                i1, i2 = i - 50, i - 45
                return f'{i1}-{i2} km'
            else:
                return '>70km'
    return s

def println(s):
    print(f'{s}{c.ln}')

def unzip( zip_dir, zip_file, unzip_file ):
    '''Functie unzipt een bestand. Returned True of False, gelukt of niet'''
    oke, lock_zip = False, threading.Lock()
    path, unzip = os.path.split(unzip_file)
    with lock_zip:
        start_ns = time.time_ns()
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip:
                zip.extract(unzip, zip_dir)
        except zipfile.BadZipfile as e:
            print(f"Unzipping file: '{zip_file}' failed")
            if c.log: print(f'{e.reason}{c.ln}{e.strerror}')
        else:
            print(f"Unzipping zipfile: '{zip_file}'")
            print(f"To file: '{unzip_file}' succesful")
            w.write_process_time_s('Time to unzip is: ', start_ns)
            oke = True
    return oke

def select_dates_from_list ( lijst_geg, start_datum, eind_datum ):
    '''Functie maakt een nieuwe lijst met gegevens op basis van begin- en einddatum'''
    l = []
    for geg in lijst_geg:
        if geg.YYYYMMDD >= start_datum and geg.YYYYMMDD <= eind_datum:
            l.append(geg)
    return l

def search_station( naam ):
    '''Functie vindtstation uit de lijst op basis van naam of wmonummer
       en returned de station of false als niks wordt gevonden'''
    naam = naam.lower()
    for station in c.lijst_stations:
        wmo, plaats = station.wmo, station.plaats.lower()
        if wmo == naam or plaats == naam:
            return station
    return False

def is_station_in_list(station, lijst):
    for check in lijst:
        if check.wmo == station.wmo and check.plaats == station.plaats:
            return True
    return False

def mk_path(dir, add):
    return os.path.abspath(os.path.join(dir, add))
