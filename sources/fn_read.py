# -*- coding: utf-8 -*-
'''Library contains functions for reading from files'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, threading, urllib, urllib.request, urllib.error, zipfile
import config as c, knmi, write as w
import datetime, time, math, locale

def get_list_day_values_by_station( station ):
    data = []
    name = station.file_etmgeg_txt
    lock = threading.Lock()
    with lock:
        try:
            with open(name, 'r') as f:
                data = f.readlines()
        except IOError as e:
            if c.log:
                print (f'''
    Read data from file: '{name}' failed"
    {c.ln}{e.reason}{c.ln}{e.strerror} ''')
        else:
            if c.log:
                print(f"Read data from file: '{name}' succesful")
            data = data[station.skip_lines:] # Only real data in list

    return data

def knmi_etmgeg_data ( station ):
    '''Functie lees alle daggegevens van een station en returned een lijst met de gegegevens'''
    if c.log: print("Functie: knmi_etmgeg_data ( station ) Bestand: 'fn.py'")

    etmgeg = []
    data = get_list_day_values_by_station( station )
    if data:
        for el in range(station.skip_lines, len(data)):
            etmgeg.append(knmi.Etmgeg(data[el]))

    return etmgeg

def get_string_day_values_by_station_and_date( station, yyyymmdd ):
    '''Function: gets the weatherdata from a station at a given date'''

    sid = f'{station.wmo} {station.plaats}'
    data = get_list_day_values_by_station(station)
    if data:
        for day in data:
            if day[6:14] == yyyymmdd:
                if c.log:
                    print(f"Read data station: {sid} at date: {yyyymmdd} succes!")
                return day

    if c.log:
        print(f"Read data station: {sid} failed !")

    return False

def get_knmi_etmgeg_by_station_and_date ( station, yyyymmdd ):
    '''Function: gets the weatherdata from a station at a given date'''

    day = get_string_day_values_by_station_and_date( station, yyyymmdd )
    if day:
        return knmi.Etmgeg( day )

    return False
