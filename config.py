# -*- coding: utf-8 -*-
'''Library contains configuration options and a list with knmi stations'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.8"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

# Application maps
import os, sys, numpy as np
dir_app       = os.path.dirname( os.path.abspath(__file__) )
dir_sources   = os.path.abspath( os.path.join(dir_app, 'sources') )
dir_view      = os.path.abspath( os.path.join(dir_app, 'view') )
dir_control   = os.path.abspath( os.path.join(dir_app, 'control') )
dir_data      = os.path.abspath( os.path.join(dir_app, 'data') )
dir_knmi      = os.path.abspath( os.path.join(dir_data, 'knmi' ) )
dir_data_txt  = os.path.abspath( os.path.join(dir_data, 'text' ) )
dir_data_html = os.path.abspath( os.path.join(dir_data, 'html' ) )
dir_data_template       = os.path.abspath( os.path.join(dir_data, 'templates' ) )
dir_data_txt_dayvalues  = os.path.abspath( os.path.join(dir_data_txt, 'dayvalues' ) )
dir_data_html_dayvalues = os.path.abspath( os.path.join(dir_data_html, 'dayvalues' ) )

# Give language for app. Under contruction...
# 'NL' for Netherlands/Dutch, 'EN' for English, Default is English
language  = 'NL'  # Select language
translate = True  # Translation active or not

# Add KNMI stations for user

# List for WeatherStations
from sources.knmi.model.station import Station
knmi_data_url              = r'https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_{0}.zip'
knmi_data_notification     = 'BRON: KONINKLIJK NEDERLANDS METEOROLOGISCH INSTITUUT (KNMI)'
knmi_data_skip_rows_etmgeg = 49
knmi_data_dummy_val        = 99999
knmi_data_empthy_val       = '     '
knmi_data_delimiter        = ','

# List with stations
stations = np.array([])
# Add KNMI weatherstations
# Extended example ie Maastricht
Maastricht = Station()  # Create Station
Maastricht.wmo               = '380'
Maastricht.place             = 'Maastricht'
Maastricht.province          = 'Limburg'
Maastricht.country           = 'Netherlands'
Maastricht.data_skip_rows    = knmi_data_skip_rows_etmgeg  # (=49, KNMI)
Maastricht.data_dummy_val    = knmi_data_dummy_val
Maastricht.data_empthy_val   = knmi_data_empthy_val
Maastricht.data_notification = knmi_data_notification
Maastricht.dir_etmgeg        = os.path.join( dir_knmi, 'etmgeg' )
Maastricht.file_zip_etmgeg   = os.path.join( Maastricht.dir_etmgeg, 'etmgeg_380.zip' )
Maastricht.file_txt_etmgeg   = os.path.join( Maastricht.dir_etmgeg, 'etmgeg_380.txt' )
Maastricht.data_url          = r'https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_380.zip'
stations = np.append( stations, Maastricht ) # Add to list

# For the rest the url and the files and the rest are automaticly updated
# Just put in the right WMO number for the station
stations = np.append(stations, Station('215', 'Voorschoten', 'Zuid-Holland', ''))
stations = np.append(stations, Station('235', 'De Kooy', 'Noord-Holland', ''))
stations = np.append(stations, Station('240', 'Schiphol', 'Noord-Holland', ''))
stations = np.append(stations, Station('249', 'Berkhout', 'Noord-Holland', ''))
stations = np.append(stations, Station('251', 'Hoorn Terschelling', 'Friesland', ''))
stations = np.append(stations, Station('257', 'Wijk aan Zee', 'Noord-Holland', ''))
stations = np.append(stations, Station('260', 'De Bilt', 'Utrecht', ''))
stations = np.append(stations, Station('265', 'Soesterberg', 'Utrecht', ''))
stations = np.append(stations, Station('267', 'Stavoren','Friesland', ''))
stations = np.append(stations, Station('269', 'Lelystad','Flevoland', ''))
stations = np.append(stations, Station('270', 'Leeuwarden','Friesland', ''))
stations = np.append(stations, Station('273', 'Marknesse', 'Flevoland', ''))
stations = np.append(stations, Station('275', 'Deelen', 'Gelderland', ''))
stations = np.append(stations, Station('277', 'Lauwersoog', 'Groningen', ''))
stations = np.append(stations, Station('278', 'Heino', 'Overijssel', ''))
stations = np.append(stations, Station('279', 'Hoogeveen', 'Drenthe', ''))
stations = np.append(stations, Station('280', 'Eelde', 'Drenthe', ''))
stations = np.append(stations, Station('283', 'Hupsel', 'Gelderland', ''))
stations = np.append(stations, Station('286', 'Nieuw Beerta', 'Groningen', ''))
stations = np.append(stations, Station('290', 'Twenthe', 'Overijssel', ''))
stations = np.append(stations, Station('310', 'Vlissingen', 'Zeeland', ''))
stations = np.append(stations, Station('319', 'Westdorpe', 'Zeeland', ''))
stations = np.append(stations, Station('323', 'Wilhelminadorp', 'Zeeland', ''))
stations = np.append(stations, Station('330', 'Hoek van Holland', 'Zuid-Holland', ''))
stations = np.append(stations, Station('344', 'Rotterdam', 'Zuid-Holland', ''))
stations = np.append(stations, Station('348', 'Cabauw Mast', 'Utrecht', ''))
stations = np.append(stations, Station('350', 'Gilze-Rijen', 'Noord-Brabant', ''))
stations = np.append(stations, Station('356', 'Herwijnen', 'Gelderland', ''))
stations = np.append(stations, Station('370', 'Eindhoven', 'Noord-Brabant', ''))
stations = np.append(stations, Station('375', 'Volkel', 'Noord-Brabant', ''))
stations = np.append(stations, Station('377', 'Ell', 'Limburg', ''))
stations = np.append(stations, Station('391', 'Arcen', 'Limburg', ''))
stations = np.append(stations, Station('242', 'Vlieland', 'Friesland', ''))

# Below an example how to add your your (own) station
# Rules for your data file.
# 1. Keep knmi structure and order. So restructure data in a KNMI way
# 2. '     ' = 5 spaces or data_dummy_value = 99999 for unregistered data
#  KNMI DATA Structure:
#  STN,YYYYMMDD,DDVEC,FHVEC,   FG,  FHX, FHXH,  FHN, FHNH,  FXX, FXXH,   TG,   TN,  TNH,
#   TX,  TXH, T10N,T10NH,   SQ,   SP,    Q,   DR,   RH,  RHX, RHXH,   PG,   PX,  PXH,
#   PN,  PNH,  VVN, VVNH,  VVX, VVXH,   NG,   UG,   UX,  UXH,   UN,  UNH, EV24
# Borkum = Station()  # Create Station
# Borkum.wmo               = '-1'
# Borkum.place             = 'Emden'
# Borkum.province          = 'Niedersaksen'
# Borkum.country           = 'Deutschland'
# Borkum.data_skip_rows    = 1
# Borkum.data_dummy_val    = knmi_data_dummy_val
# Borkum.data_empthy_val   = knmi_data_empthy_val
# Borkum.data_notification = 'source copyright @ Borkum'
# Borkum.dir_etmgeg        = os.path.join( dir_data, 'borkum' ) # ie. Create map borkum in data map
# Borkum.file_zip_etmgeg   = os.path.join( Borkum.dir_etmgeg, 'tag.zip' )
# Borkum.file_txt_etmgeg   = os.path.join( Borkum.dir_etmgeg, 'tag.txt' )
# Borkum.data_url          = r'https://my.borkum.de/data/tag.zip'
# stations = np.append( stations, Borkum ) # Add to list

# Sort station list on place name
stations = np.array(sorted( stations, key=lambda station: station.place ))

# Not all data is correct or available
# Give here the allowed percentage of missed data in a given time period
allowed_perc_data_errors = 10

# Give a max number for preventing possible html files becoming very large
html_popup_table_max_rows = -1 # -1 for all rows

# Set Debugging on or of for development
debug = False
log   = True

# Asked for char
answer_quit = ['q','Q']
answer_yes  = ['y','Y']
answer_no   = ['n','N']

# Add dir_app and dir sources to system
for dir in [dir_app, dir_sources, dir_data, dir_knmi]:
    sys.path.append(dir)
