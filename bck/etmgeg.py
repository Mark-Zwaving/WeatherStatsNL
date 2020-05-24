# -*- coding: utf-8 -*-
'''WeatherStatsNL calculates weather statistics for day values from the data
   from the knmi'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__version__    =  "0.1"
__license__    =  "GNU Lesser General Public License (LGPL)"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, threading, time, urllib, log, numpy as np

data_skip_rows = 49
data_dummy_val = 99999
dir_app  = os.getcwd()
dir_file = os.path.dirname( os.path.abspath(__file__) )
dir_data = os.path.dirname( os.path.join( base_dir_app , '/data/knmi/etmgeg/' ) )
file_zip = os.path.join( base_dir_data, 'etmgeg_{0}.zip' )
file_txt = os.path.join( base_dir_data, 'etmgeg_{0}.txt' )
data_url = r'https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_{0}.zip'


def read( stn, skip=skip_rows ):
    # https://www.datacamp.com/community/tutorials/python-numpy-tutorial
    # loadtxt() minder handig
    data = np.genfromtxt( filename, dtype=np.int32, delimiter=',',
                          filling_values=data_dummy_val, skip_header=data_skip_rows
                          )
    return data


def unzip( stn ):
    oke  = False
    lock = threading.Lock()
    zip = file_zip % stn
    txt = file_txt % stn
    ts  = time.time_ns()
    with lock:
        try:
            with zipfile.ZipFile(zip) as z:
                z.extract(txt)
        except zipfile.BadZipfile as e:
            log.console(f"Failed to unzip file: '{zip_file}'\n{e}")
        else:
            t_txt = write_process_time_ns('Time to unzip ', t_st)
            log.console( f"Unzip: '{zip}'\nTo file: '{txt}' succesful\n{t_txt}" )
            oke = True

    return oke

def download ( stn ):
    '''Function downloads etmgeg file from knmi.nl'''
    oke  = False
    lock = threading.Lock()
    file = data_url % stn
    url  = data_url % stn
    t_st = time.time_ns()
    with lock:
        log.console( f"Start downloading: '{url}'\n To: '{file}'" )
        try:
            response = urllib.request.urlretrieve( url, file )
        except urllib.error.URLError as e:
            log.console( f"Failed to download: '{url}'\n {e.reason}\n {e.strerror}" )
        else:
            t_txt = write_process_time_ns('Time to download ', t_st)
            log.console( f"Dowload: '{data_url}' succesful !\n{t_txt}" )
            oke = True

    return oke

def proces_data( stn ):
    ok = download(stn)
    if ok:
        ok = unzip(stn)
    return ok
