# -*- coding: utf-8 -*-
'''Library contains configuration options and a list with knmi stations'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

# Application maps
import os, sys, numpy as np
from sources.model.station import Station

# Config base maps
dir_app              =  os.path.dirname( os.path.abspath(__file__) )
dir_sources          =  os.path.abspath( os.path.join(dir_app, 'sources') )
dir_view             =  os.path.abspath( os.path.join(dir_app, 'view') )
dir_control          =  os.path.abspath( os.path.join(dir_app, 'control') )
dir_model            =  os.path.abspath( os.path.join(dir_app, 'model') )
dir_data             =  os.path.abspath( os.path.join(dir_app, 'data') )

dir_txt              =  os.path.abspath( os.path.join(dir_data, 'text' ) )
dir_html             =  os.path.abspath( os.path.join(dir_data, 'html' ) )
dir_img              =  os.path.abspath( os.path.join(dir_data, 'images' ) )
dir_knmi             =  os.path.abspath( os.path.join(dir_data, 'knmi' ) )
dir_thirdparty       =  os.path.abspath( os.path.join(dir_data, 'thirdparty') )

dir_knmi_dayvalues   =  os.path.abspath( os.path.join(dir_knmi, 'dayvalues' ) )
dir_img_dayvalues    =  os.path.abspath( os.path.join(dir_img, 'dayvalues' ) )
dir_img_period       =  os.path.abspath( os.path.join(dir_img, 'period' ) )
dir_txt_dayvalues    =  os.path.abspath( os.path.join(dir_txt, 'dayvalues' ) )

dir_html_templates   =  os.path.abspath( os.path.join(dir_html, 'templates' ) )
dir_html_dayvalues   =  os.path.abspath( os.path.join(dir_html, 'dayvalues' ) )
dir_html_winterstats =  os.path.abspath( os.path.join(dir_html, 'winterstats' ) )
dir_html_summerstats =  os.path.abspath( os.path.join(dir_html, 'summerstats' ) )
dir_html_allstats    =  os.path.abspath( os.path.join(dir_html, 'allstats' ) )
dir_html_search_for_days =  os.path.abspath( os.path.join(dir_html, 'search-for-days'))
dir_txt_winterstats  =  os.path.abspath( os.path.join(dir_txt, 'winterstats' ) )
dir_thirdparty_css   =  os.path.abspath( os.path.join(dir_thirdparty, 'css') )
dir_thirdparty_js    =  os.path.abspath( os.path.join(dir_thirdparty, 'js') )

# Add dir_app and dir sources to system
for dir in [ dir_app, dir_sources ]:
    sys.path.append(dir)

# Give language for app. Under contruction...
# 'NL' for Netherlands/Dutch, 'EN' for English, Default is English
language  = 'NL'  # Select language
translate = True  # Translation active or not
no_data_given = '...'
help_info = True
check_internet_url = 'www.google.com'


# The years/period for the calculations of climate averages
climate_period = '1990-2019'

# List for WeatherStations
knmi_dayvalues_url          = r'https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_{0}.zip'
knmi_dayvalues_notification = 'BRON meteorologische gegevens: KONINKLIJK NEDERLANDS METEOROLOGISCH INSTITUUT (KNMI)'
knmi_dayvalues_skip_rows    = 49
knmi_dayvalues_dummy_val    = 99999999
knmi_dayvalues_missing_val  = '     '
knmi_dayvalues_delimiter    = ','
 # For 'rh', 'rhx', 'sq' sometimes value is -1, that means meaurement value is below 0.05.
 # Give replacement value for -1 here
knmi_dayvalues_low_measure_val = 0.025

# List with stations
stations = np.array([])
# Add KNMI weatherstations
# Extended example ie Maastricht
Maastricht = Station()  # Create Station
Maastricht.wmo                    = '380'
Maastricht.place                  = 'Maastricht'
Maastricht.province               = 'Limburg'
Maastricht.country                = 'Netherlands'
Maastricht.dayvalues_skip_rows    = knmi_dayvalues_skip_rows  # (=49, KNMI)
Maastricht.dayvalues_dummy_val    = knmi_dayvalues_dummy_val
Maastricht.dayvalues_empthy_val   = knmi_dayvalues_missing_val
Maastricht.dayvalues_notification = knmi_dayvalues_notification
Maastricht.dir_dayvalues          = dir_knmi_dayvalues
Maastricht.file_zip_dayvalues     = os.path.join( Maastricht.dir_dayvalues, 'etmgeg_380.zip' )
Maastricht.file_txt_dayvalues     = os.path.join( Maastricht.dir_dayvalues, 'etmgeg_380.txt' )
Maastricht.dayvalues_url          = r'https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_380.zip'
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
# stations = np.append(stations, Station('265', 'Soesterberg', 'Utrecht', '')) # Read error
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
# Borkum.wmo                    =  '-1'
# Borkum.place                  =  'Emden'
# Borkum.province               =  'Niedersaksen'
# Borkum.country                =  'Deutschland'
# Borkum.dayvalues_skip_rows    =  1
# Borkum.dayvalues_dummy_val    =  knmi_dayvalues_dummy_val
# Borkum.dayvalues_empthy_val   =  knmi_dayvalues_empthy_val
# Borkum.dayvalues_notification =  'source copyright @ Borkum'
# Borkum.dir_dayvalues          =  os.path.join( dir_data, 'borkum' ) # ie. Create map borkum in the data map
# Borkum.file_zip_dayvalues     =  os.path.join( Borkum.dir_dayvalues, 'tag.zip' )
# Borkum.file_txt_dayvalues     =  os.path.join( Borkum.dir_dayvalues, 'tag.txt' )
# Borkum.data_url               =  r'https://my.borkum.de/data/tag.zip'
# stations = np.append( stations, Borkum ) # Add to list

# Sort station list on place name
stations = np.array( sorted( stations, key=lambda station: station.place ) )

# Not all data is correct or available
# Give here the allowed percentage of missed data in a given time period
allowed_perc_data_errors = 10

# Give a max number for preventing possible html files becoming very large
html_popup_table_max_rows = -1 # -1 for all rows

# Set Debugging on or of for development
debug = False
log   = True

# Plotting default values
default_values = 'no' # Use of default values (below) ? Or add values at runtime ?
plot_width     = 1280 # Width plotted image
plot_height    =  720 # Height plotted image
# Images dpi (dots per inches) for printing on paper
plot_dpi         =  100 # Higher will increase de point size. Make width/height higher too
plot_image_type  = 'png'
plot_graph_type  = 'line'  # bar or line
plot_line_width  =  1      # Width line
plot_line_style  = 'solid'  # Linestyle
plot_marker_size =  3      # Dot sizes
plot_marker_type =  'o'    # Type marker
plot_cummul_val  = 'n'     # Cummulative values
plot_climate_ave = 'n'     # Adding climate averages to plot
plot_clima_line_style  = 'dotted'
plot_clima_line_width  = 1
plot_clima_marker_type = '.'
plot_clima_marker_size = 1


# Base Style Plotting
# 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight',
# 'ggplot', 'grayscale', 'seaborn-bright', 'seaborn-colorblind',
# 'seaborn-dark-palette', 'seaborn-dark', 'seaborn-darkgrid',
# 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper',
# 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks',
# 'seaborn-white', 'seaborn-whitegrid', 'seaborn', 'Solarize_Light2',
# 'tableau-colorblind10'
plt_style = False #'fivethirtyeight' # Set to False for no default styling

# Style for marker texts
plot_marker_txt   = 'y'  # Select 'y' for markertext or 'n' for no
plot_marker_color = '#333333'
plot_marker_font  = { 'family'  : 'consolas',
                      'weight'  : 'normal',
                      'size'    : 'small',
                      'variant' : 'small-caps'
                    }
plot_marker_horizontalalignment = 'center'
plot_marker_verticalalignment = 'top'
plot_marker_alpha = 0.9

# Style grid in plot
plot_grid_on        = True  # True for a grid or False for no grid
plot_grid_color     = '#cccccc'
plot_grid_linestyle = 'dotted'
plot_grid_linewidth = 1

# Style titel
plot_title_color = '#333333'
plot_title_font  = { 'family'  : 'consolas',
                     'weight'  : 'bold',
                     'size'    : '14',
                     'variant' : 'normal'
                    }

# Style xlabel
plot_xlabel_text    = 'DATES'
plot_xlabel_color   = '#333333'
plot_xlabel_font    = { 'family'  : 'consolas',
                        'weight'  : 'normal',
                        'size'    : '12',
                        'variant' : 'small-caps'
                      }

# Style ylabel
plot_ylabel_color = '#333333'
plot_ylabel_font  = { 'family'  : 'consolas',
                      'weight'  : 'normal',
                      'size'    : '11',
                      'variant' : 'small-caps'
                    }

# Style values/dates on the x-as
plot_xas_color   = '#777777'
plot_xas_font    = { 'family'  : 'consolas',
                     'weight'  : 'normal',
                     'size'    : '10',
                     'variant' : 'small-caps'
                    }
plot_xas_rotation = 40

# Style legend
plot_legend_loc       = 'best'
plot_legend_fontsize  = 'small'
plot_legend_facecolor = None
plot_legend_shadow    = False
plot_legend_frameon   = False
plot_legend_fancybox  = False

# Statistics table max rows in popup for automaticly generated in statistics pages
max_rows_table_popup = 10
strip_html_output    = True

# Asked for char
answer_quit = np.array(['q', 'quit'])
answer_yes  = np.array(['yes', 'y', 'j', 'ok', 'oke', 'oké'])
answer_no   = np.array(['no', 'n', 'nope'])

#
