# -*- coding: utf-8 -*-
'''Library contains configuration options and a list with knmi stations'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, sys, numpy as np

# Config base maps
dir_app              =  os.path.dirname( os.path.abspath(__file__) )
dir_sources          =  os.path.abspath( os.path.join(dir_app, 'sources') )
dir_data             =  os.path.abspath( os.path.join(dir_app, 'data') )

dir_winterstats      = os.path.abspath( os.path.join(dir_data, 'winterstats' ) )
dir_summerstats      = os.path.abspath( os.path.join(dir_data, 'summerstats' ) )
dir_dayvalues        = os.path.abspath( os.path.join(dir_data, 'dayvalues' ) )
dir_search4days      = os.path.abspath( os.path.join(dir_data, 'search4days' ) )
dir_allstats         = os.path.abspath( os.path.join(dir_data, 'allstats' ) )
dir_thirdparty       = os.path.abspath( os.path.join(dir_data, 'thirdparty') )
dir_img              = os.path.abspath( os.path.join(dir_data, 'images' ) )
dir_pdf              = os.path.abspath( os.path.join(dir_data, 'pdf' ) )
dir_txt              = os.path.abspath( os.path.join(dir_data, 'text' ) )
dir_forecasts        = os.path.abspath( os.path.join(dir_data, 'forecasts' ) )
dir_templates        = os.path.abspath( os.path.join(dir_data, 'templates') )
dir_period           = os.path.abspath( os.path.join(dir_data, 'period') )
dir_static           = os.path.abspath( os.path.join(dir_data, 'static') )

dir_dayvalues_zip   = os.path.abspath( os.path.join(dir_dayvalues, 'zip' ) )
dir_dayvalues_txt   = os.path.abspath( os.path.join(dir_dayvalues, 'txt' ) )
dir_forecasts_txt   = os.path.abspath( os.path.join(dir_forecasts, 'txt' ) )
dir_templates_html  = os.path.abspath( os.path.join(dir_templates, 'html') )
dir_period_img      = os.path.abspath( os.path.join(dir_period, 'images') )

dir_view             =  os.path.abspath( os.path.join(dir_sources, 'view') )
dir_control          =  os.path.abspath( os.path.join(dir_sources, 'control') )
dir_model            =  os.path.abspath( os.path.join(dir_sources, 'model') )

# Give language for app. Under contruction.
# 'NL' for Netherlands/Dutch, 'EN' for English, Default is English
language  = 'EN'  # Select language
translate = True  # Translation active or not
# Default output type file. 'html'for html file.  'cmd' for commandline
# 'txt' for a text file. Only html is available at this moment
default_output = 'html'
timezone = 'Europe/Amsterdam'  # Set the time zone
help_info = True  # If True al (extra) info is shown
no_data_given = '...' # Replacement for no output
check_internet_url = 'www.google.com'  # Url to check for an internet connection
climate_period = '1981-2010' # The years/period for the calculations of climate averages

data_comment_sign = '#'

# Set Debugging on or of for development. TODO
debug = False  # Code will stop after executing some parts
log   = True   # Print all to screen

# Urls weather forecasts knmi
knmi_ftp_pub = 'ftp://ftp.knmi.nl/pub_weerberichten/'
knmi_forecast_global_url   = f'{knmi_ftp_pub}basisverwachting.txt'
knmi_forecast_model_url    = f'{knmi_ftp_pub}guidance_meerdaagse.txt'
knmi_forecast_guidance_url = f'{knmi_ftp_pub}guidance_modelbeoordeling.txt'
# List for WeatherStations
knmi_dayvalues_url          = r'https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_{0}.zip'
knmi_dayvalues_notification = 'SOURCE meteorological data: ROYAL NETHERLANDS METEOROLOGICAL INSTITUTE (KNMI)'
knmi_dayvalues_skip_header  = 49
knmi_dayvalues_skip_footer  = 0
knmi_dayvalues_dummy_val    = 99999999
knmi_dayvalues_missing_val  = '     '
knmi_dayvalues_delimiter    = ','
 # For 'rh', 'rhx', 'sq' sometimes value is -1, that means meaurement value is below 0.05.
 # Give replacement value for -1 here
knmi_dayvalues_low_measure_val = 0.025

knmi_data_format   = 'knmi' # used for data format
created_by_notification = 'Created by WeatherstatsNL at %s'

# Buienradar JSON data url
buienradar_json_data = 'https://data.buienradar.nl/2.0/feed/json'
# Select places to show with actual measurements. -1 for all
buienradar_json_places = [
    'Leeuwarden', 'Vlissingen', 'De Bilt', 'Groningen',
    'Maastricht', 'Nieuw Beerta', 'Twente', 'Arnhem',
    'Arcen', 'Eindhoven', 'Woensdrecht', 'Rotterdam',
    'Voorschoten', 'Lelystad', 'Hoorn Terschelling', 'Berkhout'
]
#  Possible options for buienradar places
#  'Arcen', 'Arnhem', 'Berkhout', 'Cadzand', 'De Bilt', 'Eindhoven', 'Ell', 'Euro platform',
#  'Gilze Rijen', 'Goes', 'Groningen', 'Hansweert', 'Heino', 'Herwijnen', 'Hoek van Holland',
#  'Hoorn Terschelling', 'Houtribdijk', 'Huibertgat', 'IJmond', 'IJmuiden', 'LE Goeree',
#  'Leeuwarden', 'Lelystad', 'Lopik-Cabauw', 'Maastricht', 'Nieuw Beerta', 'Oosterschelde',
#  'Rotterdam', 'Rotterdam Geulhaven Schaar', 'Stavenisse', 'Stavoren', 'Texelhors', 'Tholen',
#  'Twente', 'Vlieland', 'Vlissingen', 'Volkel', 'Voorschoten', 'Westdorpe', 'Wijk aan Zee',
#  'Woensdrecht', 'Zeeplatform F-3', 'Zeeplatform K13'
buienradar_json_cols = 4 # Colums for the data

knmi_json_data_10min = 'ftp://ftp.knmi.nl/pub_weerberichten/tabel_10Min_data.json'
# Select places to show with actual measurements. -1 for all
knmi_json_places = [
    'Den Helder', 'Vlissingen', 'De Bilt', 'Nieuw Beerta',
    'Terschelling', 'Leeuwarden', 'Twente', 'Wilhelminadorp',
    'Arcen', 'Eindhoven', 'Woensdrecht', 'Rotterdam',
    'Voorschoten', 'Berkhout', 'Hoogeveen', 'Maastricht-Aachen Airport'
]
# Possible options for knmi places
# 'Lauwersoog', 'Nieuw Beerta', 'Terschelling', 'Vlieland', 'Leeuwarden', 'Stavoren',
# 'Houtribdijk', 'Hoogeveen', 'Heino', 'Twente', 'Deelen', 'Hupsel', 'Herwijnen', 'Marknesse',
# 'De Bilt', 'Cabauw', 'Den Helder', 'Texelhors', 'Berkhout', 'IJmuiden', 'Wijk aan Zee',
# 'Voorschoten', 'Rotterdam', 'Hoek van Holland', 'Wilhelminadorp', 'Vlissingen', 'Westdorpe',
# 'Woensdrecht', 'Volkel', 'Eindhoven', 'Ell', 'Arcen', 'Maastricht-Aachen Airport'
knmi_json_cols = 4 # Colums for the data

# Not all data is correct or available
# Give here the allowed percentage of missed data in a given time period
allowed_perc_data_errors = 10

# Give a max number for preventing possible html files becoming very large
html_popup_table_cnt_rows = 25 # -1 for all rows

# Give a max number for preventing possible html files becoming very large
html_popup_table_val_10 = 20 # -1 for all rows

# Remove white from html source code
html_strip_output = True

fl_max = sys.float_info.min # Minimum possible value
fl_min = sys.float_info.max # Maximum possible value

# Plotting default values
plot_default      = 'n'  # Use of default values (below) ? Or add values at runtime ?
plot_show         = 'n'  # Show the plot directly -> matplotlib.show(). yess (y) or no (n)
plot_tight_layout = 'n'  # Use of matplotlib.tight_layout(). yess (y) or no (n)
# Plot resolutions default.
# Example month -> width 1600 x height 900. More days need more width
plot_width        = 1280 # Width (px) plotted image
plot_height       =  720 # Height (px) plotted image
# Images dpi (dots per inches) for printing on paper
plot_dpi          =  100 # Higher will increase de point size. Make width/height higher too
plot_image_type   = 'png'
plot_graph_type   = 'line'  # bar or line
plot_line_width   =  1      # Width line
plot_line_style   = 'solid'  # Linestyle
plot_marker_size  =  3      # Dot sizes
plot_marker_type  =  'o'    # Type marker
plot_cummul_val   = 'n'     # Cummulative values. yess (y) or no (n)
plot_climate_ave  = 'n'     # Adding climate averages to plot. yess (y) or no (n)
plot_min_max_ave_period  = 'y'     # Adding climate averages to plot. yess (y) or no (n)
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
plot_marker_txt   = 'y'  # Markertext. yess (y) or no (n)
plot_marker_color = '#333333'
plot_marker_font  = { 'family'  : 'consolas',
                      'weight'  : 'normal',
                      'size'    : 'small',
                      'variant' : 'small-caps' }
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
plot_legend_loc       = 'upper right'
plot_legend_fontsize  = 'small'
plot_legend_facecolor = None
plot_legend_shadow    = False
plot_legend_frameon   = False
plot_legend_fancybox  = False

# Asked for char
answer_quit = ['q', 'quit', 'stop']
answer_yes  = ['yes', 'y', 'yess', 'j', 'ok', 'oke', 'oké', 'ja']
answer_no   = ['no', 'n', 'nope', 'nee']
