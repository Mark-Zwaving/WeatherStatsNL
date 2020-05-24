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
html_popup_table_max_rows = -1 # -1 for all rows

# Set Debugging on or of for development
debug = False

# Add dirs/files to weatherStats
import os, sys, pathlib

# Application maps
dir_app      = os.path.dirname(os.path.abspath(__file__))
dir_sources  = os.path.abspath(os.path.join(dir_app, 'sources'))
dir_data     = os.path.abspath(os.path.join(dir_app, 'data'))

# Add dir_app and dir sources to system
for dir in [dir_app, dir_sources, dir_data]: sys.path.append(dir)

# Source map now available
import station

# List for WeatherStations
knmi_stn = []# Add KNMI weatherstations
knmi_stn.append( station.KNMI('215', 'Voorschoten', 'Zuid-Holland', '') )
knmi_stn.append( station.KNMI('235', 'De Kooy', 'Noord-Holland', '') )
knmi_stn.append( station.KNMI('240', 'Schiphol', 'Noord-Holland', '') )
knmi_stn.append( station.KNMI('249', 'Berkhout', 'Noord-Holland', '') )
knmi_stn.append( station.KNMI('251', 'Hoorn Terschelling', 'Friesland', '') )
knmi_stn.append( station.KNMI('257', 'Wijk aan Zee', 'Noord-Holland', '') )
knmi_stn.append( station.KNMI('260', 'De Bilt', 'Utrecht', '') )
knmi_stn.append( station.KNMI('265', 'Soesterberg', 'Utrecht', '') )
knmi_stn.append( station.KNMI('267', 'Stavoren','Friesland', '') )
knmi_stn.append( station.KNMI('269', 'Lelystad','Flevoland', '') )
knmi_stn.append( station.KNMI('270', 'Leeuwarden','Friesland', '') )
knmi_stn.append( station.KNMI('273', 'Marknesse', 'Flevoland', '')  )
knmi_stn.append( station.KNMI('275', 'Deelen', 'Gelderland', '') )
knmi_stn.append( station.KNMI('277', 'Lauwersoog', 'Groningen', '') )
knmi_stn.append( station.KNMI('278', 'Heino', 'Overijssel', '') )
knmi_stn.append( station.KNMI('279', 'Hoogeveen', 'Drenthe', '') )
knmi_stn.append( station.KNMI('280', 'Eelde', 'Drenthe', '') )
knmi_stn.append( station.KNMI('283', 'Hupsel', 'Gelderland', '') )
knmi_stn.append( station.KNMI('286', 'Nieuw Beerta', 'Groningen', '') )
knmi_stn.append( station.KNMI('290', 'Twenthe', 'Overijssel', '') )
knmi_stn.append( station.KNMI('310', 'Vlissingen', 'Zeeland', '') )
knmi_stn.append( station.KNMI('319', 'Westdorpe', 'Zeeland', '') )
knmi_stn.append( station.KNMI('323', 'Wilhelminadorp', 'Zeeland', '') )
knmi_stn.append( station.KNMI('330', 'Hoek van Holland', 'Zuid-Holland', '') )
knmi_stn.append( station.KNMI('344', 'Rotterdam', 'Zuid-Holland', '') )
knmi_stn.append( station.KNMI('348', 'Cabauw Mast', 'Utrecht', '') )
knmi_stn.append( station.KNMI('350', 'Gilze-Rijen', 'Noord-Brabant', '') )
knmi_stn.append( station.KNMI('356', 'Herwijnen', 'Gelderland', '') )
knmi_stn.append( station.KNMI('370', 'Eindhoven', 'Noord-Brabant', '') )
knmi_stn.append( station.KNMI('375', 'Volkel', 'Noord-Brabant', '') )
knmi_stn.append( station.KNMI('377', 'Ell', 'Limburg', '') )
knmi_stn.append( station.KNMI('380', 'Maastricht', 'Limburg', '') )
knmi_stn.append( station.KNMI('391', 'Arcen', 'Limburg', '') )
knmi_stn.append( station.KNMI('242', 'Vlieland', 'Friesland', '') )
# Non selected
#knmi_stn.append( station.KNMI('340', 'Woensdrecht', 'Noord-Brabant', '') )
#knmi_stn.append( station.KNMI('311', 'Hoofdplaat', 'Zeeland', '') )
#knmi_stn.append( station.KNMI('210', 'Valkenburg Zh', 'Zuid-Holland', '') )
#knmi_stn.append( station.KNMI('209', 'IJmond', 'Noord-Holland', '') )
#knmi_stn.append( station.KNMI('248', 'Wijdenes', 'Noord-Holland', '') )
#knmi_stn.append( station.KNMI('258', 'Houtribdijk', 'Noord-Holland', '') )
#knmi_stn.append( station.KNMI('225', 'IJmuiden', 'Noord-Holland', '') )
#knmi_stn.append( station.KNMI('285', 'Huibertgat', 'Groningen', '') )
#knmi_stn.append( station.KNMI('308', 'Cadzand', 'Zeeland', '') )
#knmi_stn.append( station.KNMI('312', 'Oosterschelde', 'Zeeland', '') )
#knmi_stn.append( station.KNMI('313', 'Vlakte van De Raan', 'Zeeland', '') )
#knmi_stn.append( station.KNMI('331', 'Tholen', 'Noord-Brabant', '') )
#knmi_stn.append( station.KNMI('324', 'Stavenisse', 'Zeeland', '') )
#knmi_stn.append( station.KNMI('343', 'Rotterdam Geulhaven', 'Zuid-Holland', '') )
#knmi_stn.append( station.KNMI('315', 'Hansweert', 'Zeeland', '') )
#knmi_stn.append( station.KNMI('316', 'Schaar', 'Zeeland', '') )


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
#knmi_stn.append( Borkum )

# old
log   = False # log modus
ln, tab = os.linesep, "\t"
line = '----------' * 8
data_empthy = '     '
stop = 'q'

max_value_geg  =  sys.maxsize
min_value_geg  =  -sys.maxsize - 1

# Put here your selected colors. Use only hexa colors.
# See also file ./html/hexa-colors.html to select colors
hexa_colors = [
      '#6b8e23','#ff00ff','#00ff00','#daa520','#5f9ea0','#ff0000','#e9967a',
      '#0000ee','#458b74','#6495ed','#00cdcd','#b03060','#191970','#8b795e',
      '#9b30ff','#cd4f39','#ffa54f','#eeee00','#00b159','#ffc425','#00aedb',
      '#f47835','#d41243','#8ec127','#dbf84a','#02d2d5','#fde600','#4a4b4b',
      '#0000FF','#BDB76B','#556B2F','#1E90FF','#9ACD32','#CD5C5C','#32CD32',
      '#BA55D3','#9370DB','#C71585','#808000','#663399','#2E8B57','#6A5ACD',
      '#a200ff','#fd3b00','#0f3766','#0b6623','#267068','#971757','#8a9f95',
      '#bda1a1','#5b1515','#b7acdf','#fcb8f8','#e6a5c4','#b6d38c','#f3ea9d',
      '#A52A2A','#E9967A','#0000ee','#00008b','#8a2be2','#8b2323','#7fff00',
      '#cd661d','#6495ed','#00ffff','#8b8878','#006400','#cd6600','#006400',
      '#00bfff','#ff3030','#228b22','#ffd700','#00ff00','#cdc673','#add8e6',
      '#20b2aa','#20b2aa','#cd00cd','#66cdaa','#c71585','#698b22',
      '#cd6889','#a020f0','#436eee'
]
'''
#faebd7,#cdc0b0,#8b8378,#76eec6,#838b8b,#ffe4c4,#eed5b7,#cdb79e,#000000,#ffebcd,#0000ee,#a52a2a,#8b2323,#deb887,#ffd39b,#cdaa7d,#8b7355,#5f9ea0,#98f5ff,#7ac5cd,#7fff00,#66cd00,#d2691e,#cd661d,#ff7f50,#ff7256,#6495ed,#eee8cd,#cdc8b1,#8b8878,#00cdcd,#008b8b,#ffb90f,#556b2f,#bcee68,#ff7f00,#ee7600,#8b4500,#b23aee,#9a32cd,#68228b,#8fbc8f,#c1ffc1,#b4eeb4,#9bcd9b,#483d8b,#97ffff,#79cdcd,#9400d3,#ff1493,#cd1076,#00bfff,#00b2ee,#009acd,#696969,#1c86ee,#1874cd,#104e8b,#ff3030,#fffaf0,#dcdcdc,#eec900,#8b7500,#daa520,#cd9b1d,#8b6914,#030303,#1c1c1c,#1f1f1f,#212121,#242424,#292929,#2e2e2e,#050505,#363636,#383838,#3b3b3b,#3d3d3d,#404040,#424242,#454545,#474747,#4a4a4a,#080808,#4d4d4d,#4f4f4f,#525252,#575757,#595959,#5e5e5e,#636363,#0a0a0a,#666666,#696969,#6e6e6e,#707070,#7a7a7a,#0d0d0d,#7f7f7f,#828282,#858585,#878787,#8c8c8c,#919191,#9e9e9e,#a3a3a3,#a8a8a8,#121212,#c4c4c4,#d1d1d1,#d6d6d6,#e0e0e0,#171717,#e8e8e8,#ededed,#f2f2f2,#fafafa,#00ff00,#00cd00,#adff2f,#e0eee0,#ff6eb4,#ee6363,#8b3a3a,#eeeee0,#8b8b83,#fff68f,#e6e6fa,#eee0e5,#8b8386,#fffacd,#cdc9a5,#eedd82,#bfefff,#9ac0cd,#f08080,#d1eeee,#7a8b8b,#eedc82,#8b814c,#d3d3d3,#ffaeb9,#cd8c95,#ffa07a,#cd8162,#20b2aa,#b0e2ff,#8db6cd,#8470ff,#b0c4de,#bcd2ee,#6e7b8b,#eeeed1,#8b8b7a,#faf0e6,#ee00ee,#8b008b,#ff34b3,#cd2990,#66cdaa,#0000cd,#e066ff,#b452cd,#9370db,#9f79ee,#5d478b,#7b68ee,#48d1cc,#191970,#ffe4e1,#cdb7b5,#ffe4b5,#eecfa1,#8b795e,#fdf5e6,#c0ff3e,#698b22,#ee9a00,#8b5a00,#ee4000,#8b2500,#ff83fa,#cd69c9,#8b4789,#eee8aa,#9aff9a,#7ccd7c,#afeeee,#aeeeee,#668b8b,#ff82ab,#ee799f,#8b475d,#ffdab9,#eecbad,#ffb5c5,#cd919e,#8b636c,#dda0dd,#eeaeee,#8b668b,#a020f0,#663399,#912cee,#7d26cd,#ff0000,#ee0000,#8b0000,#ffc1c1,#cd9b9b,#8b6969,#4876ff,#436eee,#27408b,#8b4513,#fa8072,#ff8c69,#ee8262,#f4a460,#4eee94,#43cd80,#2e8b57,#fff5ee,#8b8682,#a0522d,#ff8247,#ee7942,#cd6839,#8b4726,#87ceeb,#87ceff,#7ec0ee,#6ca6cd,#6a5acd,#836fff,#7a67ee,#473c8b,#708090,#c6e2ff,#b9d3ee,#9fb6cd,#6c7b8b,#fffafa,#cdc9c9,#8b8989,#00ff7f,#00ee76,#008b45,#63b8ff,#5cacee,#4f94cd,#36648b,#ffa54f,#ee9a49,#cd853f,#eed2ee,#cdb5cd,#8b7b8b,#ff6347,#ee5c42,#40e0d0,#00f5ff,#00e5ee,#00c5cd,#00868b,#ee82ee,#d02090,#ff3e96,#ee3a8c,#cd3278,#f5deb3,#ffe7ba,#eed8ae,#cdba96,#8b7e66,#ffffff,#f5f5f5,#ffff00,#eeee00,#cdcd00,#8b8b00
'''

# Create maps and files for saving data
dir_html                  = os.path.abspath(os.path.join(dir_app,  'html'))
dir_html_allstats         = os.path.abspath(os.path.join(dir_html, 'allstats'))
dir_html_winterstats      = os.path.abspath(os.path.join(dir_html, 'winterstats'))
dir_html_coldwaves        = os.path.abspath(os.path.join(dir_html, 'coldwaves'))
dir_html_summerstats      = os.path.abspath(os.path.join(dir_html, 'summerstats'))
dir_html_heatwaves        = os.path.abspath(os.path.join(dir_html, 'heatwaves'))
dir_html_extremes         = os.path.abspath(os.path.join(dir_html, 'extremes'))
dir_html_dayvalues        = os.path.abspath(os.path.join(dir_html, 'dayvalues'))

dir_html_css              = os.path.abspath(os.path.join(dir_html, 'css')) # Extra
dir_html_allstats_css     = os.path.abspath(os.path.join(dir_html_allstats,    'css'))
dir_html_winterstats_css  = os.path.abspath(os.path.join(dir_html_winterstats, 'css'))
dir_html_coldwaves_css    = os.path.abspath(os.path.join(dir_html_coldwaves,   'css'))
dir_html_summerstats_css  = os.path.abspath(os.path.join(dir_html_summerstats, 'css'))
dir_html_heatwaves_css    = os.path.abspath(os.path.join(dir_html_heatwaves,   'css'))
dir_html_extremes_css     = os.path.abspath(os.path.join(dir_html_extremes,    'css'))
dir_html_dayvalues_css    = os.path.abspath(os.path.join(dir_html_dayvalues,   'css'))

dir_html_js               = os.path.abspath(os.path.join(dir_html, 'js'))  # Extra
dir_html_dayvalues_js     = os.path.abspath(os.path.join(dir_html_dayvalues,   'js'))
dir_html_allstats_js      = os.path.abspath(os.path.join(dir_html_allstats,    'js'))
dir_html_winterstats_js   = os.path.abspath(os.path.join(dir_html_winterstats, 'js'))
dir_html_coldwaves_js     = os.path.abspath(os.path.join(dir_html_coldwaves,   'js'))
dir_html_summerstats_js   = os.path.abspath(os.path.join(dir_html_summerstats, 'js'))
dir_html_heatwaves_js     = os.path.abspath(os.path.join(dir_html_heatwaves,   'js'))
dir_html_extremes_js      = os.path.abspath(os.path.join(dir_html_extremes,    'js'))
dir_html_dayvalues_js     = os.path.abspath(os.path.join(dir_html_dayvalues,   'js'))

file_css_default1         = 'default_1.css'
file_css_default2         = 'default_2.css'
file_js_default1          = 'default_1.js'
file_js_default2          = 'default_2.js'

dir_text                  = os.path.abspath(os.path.join(dir_app,  'text'))
dir_text_allstats         = os.path.abspath(os.path.join(dir_text, 'allstats'))
dir_text_winterstats      = os.path.abspath(os.path.join(dir_text, 'winterstats'))
dir_text_coldwaves        = os.path.abspath(os.path.join(dir_text, 'coldwaves'))
dir_text_summerstats      = os.path.abspath(os.path.join(dir_text, 'summerstats'))
dir_text_heatwaves        = os.path.abspath(os.path.join(dir_text, 'heatwaves'))
dir_text_extremes         = os.path.abspath(os.path.join(dir_text, 'extremes'))
dir_text_dayvalues        = os.path.abspath(os.path.join(dir_text, 'dayvalues'))

dir_images                = os.path.abspath(os.path.join(dir_app,    'images'))
dir_images_allstats       = os.path.abspath(os.path.join(dir_images, 'allstats'))
dir_images_winterstats    = os.path.abspath(os.path.join(dir_images, 'winterstats'))
dir_images_coldwaves      = os.path.abspath(os.path.join(dir_images, 'coldwaves'))
dir_images_summerstats    = os.path.abspath(os.path.join(dir_images, 'summerstats'))
dir_images_heatwaves      = os.path.abspath(os.path.join(dir_images, 'heatwaves'))
dir_images_extremes       = os.path.abspath(os.path.join(dir_images, 'extremes'))
dir_images_dayvalues      = os.path.abspath(os.path.join(dir_images, 'dayvalues'))

# Check if map exists, if not create it and add map to the system
dir_all = [dir_data,

           dir_html,
           dir_html_allstats, dir_html_winterstats, dir_html_coldwaves,
           dir_html_summerstats, dir_html_heatwaves, dir_html_extremes,
           dir_html_dayvalues,

           dir_html_css,
           dir_html_allstats_css, dir_html_winterstats_css, dir_html_coldwaves_css,
           dir_html_summerstats_css, dir_html_heatwaves_css, dir_html_extremes_css,
           dir_html_dayvalues_css,

           dir_html_js,
           dir_html_allstats_js, dir_html_winterstats_js, dir_html_coldwaves_js,
           dir_html_summerstats_js,dir_html_heatwaves_js, dir_html_extremes_js,
           dir_html_dayvalues_js,

           dir_text,
           dir_text_allstats, dir_text_winterstats, dir_text_coldwaves,
           dir_text_summerstats, dir_text_heatwaves, dir_text_extremes,
           dir_text_dayvalues,

           dir_images,
           dir_images_allstats, dir_images_winterstats, dir_images_coldwaves,
           dir_images_summerstats, dir_images_heatwaves, dir_images_extremes,
           dir_images_dayvalues
           ]
for dir in dir_all:
    if not os.path.exists(dir):
        os.makedirs(dir)
    sys.path.append(dir)

# Create css en js files for adding css and js to the html pages
dir_css = [dir_html_allstats_css, dir_html_winterstats_css, dir_html_coldwaves_css,
           dir_html_summerstats_css, dir_html_heatwaves_css, dir_html_extremes_css,
           dir_html_css ]
dir_js  = [dir_html_allstats_js, dir_html_winterstats_js, dir_html_coldwaves_js,
           dir_html_summerstats_js, dir_html_heatwaves_js, dir_html_extremes_js,
           dir_html_js ]

files_css = [ file_css_default1, file_css_default2 ]
files_js  = [ file_js_default1, file_js_default2 ]

for dir in dir_css:
    for css in files_css:
        file = os.path.abspath(os.path.join(dir, css))
        if not os.path.exists(file):
            pathlib.Path(file).touch()

for dir in dir_js:
    for js in files_js:
        file = os.path.abspath(os.path.join(dir, js))
        if not os.path.exists(file):
            pathlib.Path(file).touch()
