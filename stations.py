# -*- coding: utf-8 -*-
''' Library contains class to store knmi data
    Here you can make your own data list
    Function for handlin stationsdata
'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.1.8'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config
import os, numpy as np
import sources.model.utils as utils

class Station:
    '''Class defines a (knmi) weatherstation'''
    def __init__(self, wmo = ' ', place = ' ', province = ' ', country='', info = ' ', format='knmi', ):
        self.wmo      = wmo
        self.place    = place
        self.province = province
        self.state    = province
        self.country  = country
        self.info     = info

        self.data_format        = config.knmi_data_format     # For data standards
        self.data_skip_header   = config.knmi_dayvalues_skip_header
        self.data_skip_footer   = config.knmi_dayvalues_skip_footer
        self.data_dummy_val     = config.knmi_dayvalues_dummy_val
        self.data_missing       = config.knmi_dayvalues_missing_val
        self.data_notification  = config.knmi_dayvalues_notification
        self.data_delimiter     = config.knmi_dayvalues_delimiter
        self.data_dir           = config.dir_data_dayvalues
        self.data_zip_file      = f'etmgeg_{self.wmo}.zip'
        self.data_txt_file      = f'etmgeg_{self.wmo}.txt'
        self.data_zip_path      = os.path.join(self.data_dir, self.data_zip_file)
        self.data_txt_path      = os.path.join(self.data_dir, self.data_txt_file)
        self.data_url           = config.knmi_dayvalues_url.format(self.wmo)
        self.data_comments_sign = config.data_comment_sign
        self.data_dayvalues_txt_path = self.data_txt_path # Unused, yet
        self.data_download      = True

# Make list with stations
list = []
# Add KNMI weatherstations
# Extended example ie Maastricht,
Maastricht = Station('380', 'Maastricht', 'Limburg', 'Netherlands')  # Create Station
Maastricht.data_skip_header  = config.knmi_dayvalues_skip_header  # (=49, KNMI)
Maastricht.data_dummy_val    = config.knmi_dayvalues_dummy_val
Maastricht.data_empthy_val   = config.knmi_dayvalues_missing_val
Maastricht.data_notification = config.knmi_dayvalues_notification
Maastricht.data_format       = config.knmi_data_format
Maastricht.data_zip_path     = os.path.join( Maastricht.data_dir, 'etmgeg_380.zip' )
Maastricht.data_txt_path     = os.path.join( Maastricht.data_dir, 'etmgeg_380.txt' )
Maastricht.data_dayvalus_url  = r'https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_380.zip'
list.append( Maastricht ) # Add to list

# For the rest the url and the files and the rest are automaticly updated
# Just put in the right WMO number for the station
list.append(Station('215', 'Voorschoten', 'Zuid-Holland', ''))
list.append(Station('235', 'De Kooy', 'Noord-Holland', ''))
list.append(Station('240', 'Schiphol', 'Noord-Holland', ''))
list.append(Station('249', 'Berkhout', 'Noord-Holland', ''))
list.append(Station('251', 'Hoorn Terschelling', 'Friesland', ''))
list.append(Station('257', 'Wijk aan Zee', 'Noord-Holland', ''))
list.append(Station('260', 'De Bilt', 'Utrecht', ''))
# list.append(Station('265', 'Soesterberg', 'Utrecht', '')) # Read error
list.append(Station('267', 'Stavoren','Friesland', ''))
list.append(Station('269', 'Lelystad','Flevoland', ''))
list.append(Station('270', 'Leeuwarden','Friesland', ''))
list.append(Station('273', 'Marknesse', 'Flevoland', ''))
list.append(Station('275', 'Deelen', 'Gelderland', ''))
list.append(Station('277', 'Lauwersoog', 'Groningen', ''))
list.append(Station('278', 'Heino', 'Overijssel', ''))
list.append(Station('279', 'Hoogeveen', 'Drenthe', ''))
list.append(Station('280', 'Eelde', 'Drenthe', ''))
list.append(Station('283', 'Hupsel', 'Gelderland', ''))
list.append(Station('286', 'Nieuw Beerta', 'Groningen', ''))
list.append(Station('290', 'Twenthe', 'Overijssel', ''))
list.append(Station('310', 'Vlissingen', 'Zeeland', ''))
list.append(Station('319', 'Westdorpe', 'Zeeland', ''))
list.append(Station('323', 'Wilhelminadorp', 'Zeeland', ''))
list.append(Station('330', 'Hoek van Holland', 'Zuid-Holland', ''))
list.append(Station('344', 'Rotterdam', 'Zuid-Holland', ''))
list.append(Station('348', 'Cabauw Mast', 'Utrecht', ''))
list.append(Station('350', 'Gilze-Rijen', 'Noord-Brabant', ''))
list.append(Station('356', 'Herwijnen', 'Gelderland', ''))
list.append(Station('370', 'Eindhoven', 'Noord-Brabant', ''))
list.append(Station('375', 'Volkel', 'Noord-Brabant', ''))
list.append(Station('377', 'Ell', 'Limburg', ''))
list.append(Station('391', 'Arcen', 'Limburg', ''))
list.append(Station('242', 'Vlieland', 'Friesland', ''))

# Below an example how to add your your (own) station
# Rules for your data file.
# 1. Keep knmi structure and order. So restructure data in a KNMI way
# 2. '     ' = 5 spaces or data_dummy_value = 99999 for unregistered data
#  KNMI DATA Structure:
#  STN,YYYYMMDD,DDVEC,FHVEC,   FG,  FHX, FHXH,  FHN, FHNH,  FXX, FXXH,   TG,   TN,  TNH,
#   TX,  TXH, T10N,T10NH,   SQ,   SP,    Q,   DR,   RH,  RHX, RHXH,   PG,   PX,  PXH,
#   PN,  PNH,  VVN, VVNH,  VVX, VVXH,   NG,   UG,   UX,  UXH,   UN,  UNH, EV24
# Borkum = Station()  # Create Station
# Borkum.wmo                    =  '-1'
# Borkum.place                  =  'Emden'
# Borkum.province               =  'Niedersaksen'
# Borkum.country                =  'Deutschland'
# Borkum.dayvalues_skip_rows    =  1
# Borkum.dayvalues_dummy_val    =  knmi_dayvalues_dummy_val
# Borkum.dayvalues_empthy_val   =  knmi_dayvalues_empthy_val
# Borkum.dayvalues_notification =  'source copyright @ Borkum'
# Borkum.dayvalues_dir_dayvalues =  os.path.join( dir_data, 'borkum' ) # ie. Create map borkum in the data map
# Borkum.dayvalues_file_zip      =  os.path.join( Borkum.dir_dayvalues, 'tag.zip' )
# Borkum.dayvalues_file_txt      =  os.path.join( Borkum.dir_dayvalues, 'tag.txt' )
# Borkum.data_url                =  r'https://my.borkum.de/data/tag.zip'
# list.append( Borkum ) # Add to list

# Sort station list on place name, using numpy
list = np.array( sorted( np.array(list), key=lambda station: station.place ) ).tolist()

################################################################################
# Functions
def from_wmo_to_station(wmo):
    if wmo_in_list(wmo):
        for station in list:
            if station.wmo == wmo:
                return station
    return False

def from_wmo_to_name(wmo, l=False):
    if wmo_in_list(wmo):
        if l == False:
            l = utils.only_existing_stations_in_map()
        for s in l:
            if s.wmo == wmo:
                return s.place
    return wmo

def from_wmo_to_province(wmo, l=False):
    if wmo_in_list(wmo):
        if l == False:
            l = utils.only_existing_stations_in_map()
        for s in l:
            if s.wmo == wmo:
                return s.province
    return wmo

def name_in_list(name, l=False):
    if name:
        n = name.lower()
        if l == False:
            l = utils.only_existing_stations_in_map()
        for s in l:
            if s.place.lower() == n:
                return True
    return False

def wmo_in_list(wmo, l=False):
    if wmo:
        if l == False:
            l = utils.only_existing_stations_in_map()
        for s in l:
            if s.wmo == wmo:
                return True
    return False

def find_by_name(name, l=False):
    if name:
        n = name.lower()
        if l == False:
            l = utils.only_existing_stations_in_map()
        for s in l:
            if s.place.lower() == n:
                return s
    return False

def find_by_wmo( wmo, l=False):
    if wmo:
        n = wmo.lower()
        if l == False:
            l = utils.only_existing_stations_in_map()
        for s in l:
            if s.wmo.lower() == n:
                return s
    return False

def find_by_wmo_or_name(name_or_wmo, l=False):
    if name_or_wmo:
        name = find_by_name( name_or_wmo, l )
        if name != False:
            return name

        wmo = find_by_wmo( name_or_wmo, l )
        if wmo != False:
            return wmo

    return False

def check_if_station_already_in_list( station, l ):
    for el in l:
        if el.wmo == station.wmo and check.place.lower() == station.place.lower():
            return True
    return False
