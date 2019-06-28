# -*- coding: utf-8 -*-
'''Library contains configuratino options and a list with knmi stations'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9.21"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

# Give language for app. Under contruction...
# 'NL' for Netherlands/Dutch, 'EN' for English, Default is English
language = 'EN'

# Not all data is correct or available
# Give here the allowed percentage of missed data in a given time period
allowed_perc_data_errors = 10

# Give a max number for preventing possible html files becoming very large
html_popup_table_max_rows = 25 # -1 for all rows

# Set Debugging on or of for development
debug = False

# Add dirs/files to weatherStats
import os, sys, pathlib

dir_app     =  os.path.dirname(os.path.abspath(__file__))
dir_sources =  os.path.abspath(os.path.join(dir_app, 'sources'))
dir_station =  os.path.abspath(os.path.join(dir_app, 'station'))
dir_data    =  os.path.abspath(os.path.join(dir_station, 'data'))
dir_html    =  os.path.abspath(os.path.join(dir_station, 'html'))
dir_txt     =  os.path.abspath(os.path.join(dir_station, 'txt'))
dir_css     =  os.path.abspath(os.path.join(dir_html, 'css'))
dir_js      =  os.path.abspath(os.path.join(dir_html, 'js'))
file_css_default1 =  os.path.abspath(os.path.join(dir_css,  'default_1.css'))
file_css_default2 =  os.path.abspath(os.path.join(dir_css,  'default_2.css'))
file_js_default1  =  os.path.abspath(os.path.join(dir_js, 'default_1.js'))
file_js_default2  =  os.path.abspath(os.path.join(dir_js, 'default_2.js'))

# Add dir_app and dir sources to system
for dir in [dir_app, dir_sources]:
    sys.path.append(dir)

# Check if map is there for use, if not make the map.
# Add the map to the system
for dir in [dir_station, dir_data, dir_txt, dir_html, dir_css, dir_js]:
    if not os.path.exists(dir):
        os.makedirs(dir)
    sys.path.append(dir)

for file in [file_css_default1, file_css_default1, file_js_default1, file_js_default1]:
    if not os.path.exists(file):
        pathlib.Path(file).touch()

# WeatherStations
import sources.station as station

# List for WeatherStations
lijst_stations = []# Add KNMI weatherstations
lijst_stations.append( station.KNMI('215', 'Voorschoten', 'Zuid-Holland', '') )
lijst_stations.append( station.KNMI('235', 'De Kooy', 'Noord-Holland', '') )
lijst_stations.append( station.KNMI('240', 'Schiphol', 'Noord-Holland', '') )
lijst_stations.append( station.KNMI('249', 'Berkhout', 'Noord-Holland', '') )
lijst_stations.append( station.KNMI('251', 'Hoorn Terschelling', 'Friesland', '') )
lijst_stations.append( station.KNMI('257', 'Wijk aan Zee', 'Noord-Holland', '') )
lijst_stations.append( station.KNMI('260', 'De Bilt', 'Utrecht', '') )
lijst_stations.append( station.KNMI('265', 'Soesterberg', 'Utrecht', '') )
lijst_stations.append( station.KNMI('267', 'Stavoren','Friesland', '') )
lijst_stations.append( station.KNMI('269', 'Lelystad','Flevoland', '') )
lijst_stations.append( station.KNMI('270', 'Leeuwarden','Friesland', '') )
lijst_stations.append( station.KNMI('273', 'Marknesse', 'Flevoland', '')  )
lijst_stations.append( station.KNMI('275', 'Deelen', 'Gelderland', '') )
lijst_stations.append( station.KNMI('277', 'Lauwersoog', 'Groningen', '') )
lijst_stations.append( station.KNMI('278', 'Heino', 'Overijssel', '') )
lijst_stations.append( station.KNMI('279', 'Hoogeveen', 'Drenthe', '') )
lijst_stations.append( station.KNMI('280', 'Eelde', 'Drenthe', '') )
lijst_stations.append( station.KNMI('283', 'Hupsel', 'Gelderland', '') )
lijst_stations.append( station.KNMI('286', 'Nieuw Beerta', 'Groningen', '') )
lijst_stations.append( station.KNMI('290', 'Twenthe', 'Overijssel', '') )
lijst_stations.append( station.KNMI('310', 'Vlissingen', 'Zeeland', '') )
lijst_stations.append( station.KNMI('319', 'Westdorpe', 'Zeeland', '') )
lijst_stations.append( station.KNMI('323', 'Wilhelminadorp', 'Zeeland', '') )
lijst_stations.append( station.KNMI('330', 'Hoek van Holland', 'Zuid-Holland', '') )
lijst_stations.append( station.KNMI('344', 'Rotterdam', 'Zuid-Holland', '') )
lijst_stations.append( station.KNMI('348', 'Cabauw Mast', 'Utrecht', '') )
lijst_stations.append( station.KNMI('350', 'Gilze-Rijen', 'Noord-Brabant', '') )
lijst_stations.append( station.KNMI('356', 'Herwijnen', 'Gelderland', '') )
lijst_stations.append( station.KNMI('370', 'Eindhoven', 'Noord-Brabant', '') )
lijst_stations.append( station.KNMI('375', 'Volkel', 'Noord-Brabant', '') )
lijst_stations.append( station.KNMI('377', 'Ell', 'Limburg', '') )
lijst_stations.append( station.KNMI('380', 'Maastricht', 'Limburg', '') )
lijst_stations.append( station.KNMI('391', 'Arcen', 'Limburg', '') )
# Non selected
#lijst_stations.append( station.KNMI('242', 'Vlieland', 'Friesland', '') )
#lijst_stations.append( station.KNMI('340', 'Woensdrecht', 'Noord-Brabant', '') )
#lijst_stations.append( station.KNMI('311', 'Hoofdplaat', 'Zeeland', '') )
#lijst_stations.append( station.KNMI('210', 'Valkenburg Zh', 'Zuid-Holland', '') )
#lijst_stations.append( station.KNMI('209', 'IJmond', 'Noord-Holland', '') )
#lijst_stations.append( station.KNMI('248', 'Wijdenes', 'Noord-Holland', '') )
#lijst_stations.append( station.KNMI('258', 'Houtribdijk', 'Noord-Holland', '') )
#lijst_stations.append( station.KNMI('225', 'IJmuiden', 'Noord-Holland', '') )
#lijst_stations.append( station.KNMI('285', 'Huibertgat', 'Groningen', '') )
#lijst_stations.append( station.KNMI('308', 'Cadzand', 'Zeeland', '') )
#lijst_stations.append( station.KNMI('312', 'Oosterschelde', 'Zeeland', '') )
#lijst_stations.append( station.KNMI('313', 'Vlakte van De Raan', 'Zeeland', '') )
#lijst_stations.append( station.KNMI('331', 'Tholen', 'Noord-Brabant', '') )
#lijst_stations.append( station.KNMI('324', 'Stavenisse', 'Zeeland', '') )
#lijst_stations.append( station.KNMI('343', 'Rotterdam Geulhaven', 'Zuid-Holland', '') )
#lijst_stations.append( station.KNMI('315', 'Hansweert', 'Zeeland', '') )
#lijst_stations.append( station.KNMI('316', 'Schaar', 'Zeeland', '') )


# To add your own stations
# Note: To make you own data file. Keep knmi structure
# And '     ' <- 5 spaces, for empthy (=no data)
# KNMI DATA STRUCTURE
#  STN,YYYYMMDD,DDVEC,FHVEC,   FG,  FHX, FHXH,  FHN, FHNH,  FXX, FXXH,   TG,   TN,  TNH,
#   TX,  TXH, T10N,T10NH,   SQ,   SP,    Q,   DR,   RH,  RHX, RHXH,   PG,   PX,  PXH,
#   PN,  PNH,  VVN, VVNH,  VVX, VVXH,   NG,   UG,   UX,  UXH,   UN,  UNH, EV24

# For example how to make a new station
Borkum = station.Place('','')  # Make a Weatherstation
Borkum.place            =  ''  # Name of town/place
Borkum.province         =  ''  # Province
Borkum.country          =  ''  # Country
Borkum.info             =  ''  # Additional info
Borkum.file_etmgeg_zip  =  'X.zip'  # Local zip name <optional>
Borkum.file_etmgeg_txt  =  'X.txt'  # !Important. Programm reads data from this file
Borkum.url_etmgeg       =  'https://...'  # Download url for downloading data from the internet
Borkum.skip_lines       =  0        # Skip introduction texts lines in file
Borkum.notification     =  'SOURCE: ...'  # Put your copyright notifications

# Add weather station to list
#lijst_stations.append( Borkum )

# old
log   = False # log modus
ln, tab = os.linesep, "\t"
line = '----------' * 8
data_empthy = '     '
stop = 'q'

max_value_geg  =  sys.maxsize
min_value_geg  =  -sys.maxsize - 1
