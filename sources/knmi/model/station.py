# -*- coding: utf-8 -*-
'''Library contains classes to store knmi data'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1.3"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, pathlib, config
import numpy as np

class Station:
    '''Class defines a KNMI weatherstation'''
    def __init__(self, wmo = ' ', place = ' ', province = ' ', info = ' '):
        self.wmo      = wmo
        self.place    = place
        self.province = province
        self.country  = 'Netherlands'
        self.info     = info

        self.dayvalues_skip_rows    = config.knmi_dayvalues_skip_rows
        self.dayvalues_dummy_val    = config.knmi_dayvalues_dummy_val
        self.dayvalues_empthy_val   = config.knmi_dayvalues_empthy_val
        self.dayvalues_notification = config.knmi_dayvalues_notification

        self.dir_dayvalues      = config.dir_thirdparty_knmi_dayvalues
        self.file_zip_dayvalues = os.path.join( self.dir_dayvalues, f'etmgeg_{self.wmo}.zip' )
        self.file_txt_dayvalues = os.path.join( self.dir_dayvalues, f'etmgeg_{self.wmo}.txt' )

        self.dayvalues_url      = config.knmi_dayvalues_url.format(self.wmo)

def name_in_list(name):
    n = name.lower()
    for s in config.stations.tolist():
        if s.place.lower() == n:
            return True
    return False

def wmo_in_list(wmo):
    for s in config.stations.tolist():
        if s.wmo == wmo:
            return True
    return False

def find_by_name( name ):
    n = name.lower()
    for s in config.stations.tolist():
        if s.place.lower() == n:
            return s
    return False

def find_by_wmo( wmo ):
    n = wmo.lower()
    for s in config.stations.tolist():
        if s.wmo.lower() == n:
            return s
    return False

def find_by_wmo_or_name(name_or_wmo):
    station_name = find_by_name( name_or_wmo )
    if station_name != False:
        return station_name

    station_wmo = find_by_wmo( name_or_wmo )
    if station_wmo != False:
        return station_wmo

    return False

def check_if_station_already_in_list( station, l ):
    for check in l:
        if check.wmo == station.wmo and check.place.lower() == station.place.lower():
            return True
    return False
