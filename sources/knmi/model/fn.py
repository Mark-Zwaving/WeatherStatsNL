# -*- coding: utf-8 -*-
'''Library contains casual functions for different purposes'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, threading, time, zipfile
import config
import knmi.model.daydata as daydata

# Some quick,short functions
div_10       = lambda s:        f'{float(s)/10:0.1F}'
div_10_add   = lambda s,a:      f'{div_10(s)}{a}'
mk_path      = lambda dir,add:  os.path.abspath( os.path.join( dir, add ) )

def find_knmi_station( id ):
    '''Function searches for station in the list if found in list then return
       the station else False'''
    id = id.lower()
    for station in config.stations:
        if id in [station.wmo, station.place.lower()]:
            return station

    return False # Station not found

def is_station_in_list(station, lijst):
    for check in lijst:
        if check.wmo == station.wmo and check.place.lower() == station.place.lower():
            return True

    return False

def get_list_X_from_list_EtmGeg(l, ent):
    '''Gets a list with values based on ent [TX,TN,...]'''
    res = []
    for etm in l:
        el = station.etmgeg(etm, ent)
        res.append(el)

    return res
