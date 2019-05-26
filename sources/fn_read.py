# -*- coding: utf-8 -*-
'''Library contains a function to read from a file and returns a object with the
data of a date'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, threading, urllib, urllib.request, urllib.error, zipfile
import config as c, knmi, write as w
import datetime, time, math, locale

def get_knmi_etmgeg_by_station_and_date ( station, yyyymmdd ):
    '''Function: gets the weatherdata from a station at a given date'''
    if c.log:
        print(f'''
Function:get_knmi_etmgeg_by_station_and_date('{station}','{yyyymmdd}')\nFile:etmgeg.py
        ''')
    oke = False
    knmi_etmgeg = []
    sid = station.wmo + ', ' + station.plaats
    lock_read = threading.Lock()
    with lock_read:
        if c.log:
            print(f"Read data station: '{sid}'")
            print(f"Filenames: '{station.file_etmgeg_txt}'")
        try:
            with open(station.file_etmgeg_txt, 'r') as f: # Lees file in array
                data_file = f.readlines()
        except IOError as e:
            if c.log:s
                print(f"Failed to read data from file: '{station.file_etmgeg_txt}' ")
                print(f'{e.reason}{c.ln}{e.strerror}')
        else:
            print(f"Read data from station: '{sid}' succesful !")
            if c.log:
                print(f"Data first date: '{data_file[station.skip_lines]}")
                print(f"Data last date: {data_file[-1]}")
            # Make list with knmi data
            for el in range( station.skip_lines, len(data_file) ):
                knmi_etmgeg.append( knmi.Etmgeg(data_file[el]) )

            oke = True

    return knmi_etmgeg if oke else False;
