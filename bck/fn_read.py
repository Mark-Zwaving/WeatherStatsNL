# -*- coding: utf-8 -*-
'''Library contains functions for reading from files'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import threading, config as c, knmi, write as w, fn
import numpy as np

def get_string_css_from_file( name ):
    file = fn.mk_path(c.dir_html_css, name)
    lock = threading.Lock()
    data = ' '
    with lock:
        try:
            with open(file, 'r') as f:
                data = f.read().replace('\n', '')
        except IOError as e:
            if c.log:
                print(f"Read css data from file: {name} failed")
                print(f"{c.ln}{e.reason}{c.ln}{e.strerror}")
        else:
            if c.log:
                print(f"Read css data from file: {name} succesful")

    return data

# Using numpy
def get_list_dayvalues_from_station( station ):
    l_data = [] # Use numpy
    lock = threading.Lock()
    with lock:
        try:
            l_data = np.loadtxt( station.file_etmgeg_txt,
                                 dtype=np.int32, delimiter=',',
                                 skiprows=station.skip_lines )
        except IOError as e:
            if c.log:
                print(f"Read data from file: {name} failed")
                print(f"{c.ln}{e.reason}{c.ln}{e.strerror}")
        else:
            if c.log:
                print(f"Read data from file: {name} succesful")

    return l_data


def get_list_day_values_by_station( station ):
    data, fname = [], station.file_etmgeg_txt
    lock = threading.Lock()
    with lock:
        try:
            with open(fname, 'r') as f:
                data = f.readlines()
        except IOError as e:
            if c.log:
                print(f"Read data from file: {name} failed")
                print(f"{c.ln}{e.reason}{c.ln}{e.strerror}")
        else:
            if c.log:
                print(f"Read data from file: {name} succesful")
            data = data[station.skip_lines:] # Only real data in list

    return data

def get_list_knmi_etmgeg_data ( station ):
    '''Functie lees alle daggegevens van een station en returned een lijst met de gegegevens'''
    if c.log:
        print("Functie: knmi_etmgeg_data ( station ) Bestand: 'fn.py'")

    etmgeg = []
    data = get_list_day_values_by_station( station )
    if data:
        for el in range(station.skip_lines, len(data)):
            etmgeg.append(knmi.Etmgeg(data[el]))

    return etmgeg

def knmi_etmgeg_data ( station ): # Old function, for delete later
    return get_list_knmi_etmgeg_data ( station )

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

def get_dayvalues_from_station_by_date( station, yyyymmdd ):
    l_days = get_list_day_values_by_station( station )
    if l_days:
        for day in l_days:
            if day[6:14] == yyyymmdd:
                return knmi.Etmgeg( day )

    return False

def get_list_dayvalues_from_station_in_period ( station, s_date_start, s_date_end ):
    '''Functie gives dayvalues from a station within two given dates'''
    l_complete, l_period = get_list_knmi_etmgeg_data ( station ), []
    i_start, i_end = int(s_date_start), int(s_date_end)
    if l_complete:
        for day in l_complete:
            if int(day.YYYYMMDD) >= i_start and int(day.YYYYMMDD) <= i_end:
                l_period.append(day)

    return l_period
