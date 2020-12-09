# -*- coding: utf-8 -*-
'''Functions for menu '''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.8"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config, threading
import sources.model.utils as utils
import sources.view.log as log
import sources.view.translate as tr
import sources.control.ask as ask
import sources.control.menu as cmenu

menu = [
    [ 'DOWNLOAD DATA',
        [ [ 'Download all dayvalues knmi stations', cmenu.process_knmi_dayvalues_all ],
          [ 'Download one or more dayvalues knmi stations', cmenu.process_knmi_dayvalues_selected ]
          ]
    ],
    [ 'FORECASTS',
        [ [ 'Weather (knmi, dutch)', cmenu.process_weather_knmi_global ],
          [ 'Weather (buienradar, dutch)', cmenu.process_weather_buienradar_global ],
          [ 'Model evaluation (knmi, dutch)', cmenu.process_weather_knmi_model ],
          [ 'Medium-term (knmi, dutch)', cmenu.process_weather_knmi_guidance ]
          ]
    ],
    [ 'CURRENT WEATHER',
        [ [ 'Stations NL (buienradar, dutch)', cmenu.process_weather_buienradar_current ],
          [ 'Stations NL (knmi, dutch)', cmenu.process_weather_knmi_current ]
        ]
    ],
    [ 'DAYVALUES AND PERIODS',
        [ [ 'Dayvalues', cmenu.get_dayvalues_by_date ],
          [ 'Search for days', cmenu.search_for_days ],
          [ 'Period graphs', cmenu.graph_period ]
          ]
    ],
    [ 'STATISTICS TABLES',
        [ [ 'Winter statistics', cmenu.table_winterstats ],
          [ 'Summer statistics', cmenu.table_summerstats ],
          [ 'Winter & summer statistics', cmenu.table_allstats ]
        # [ 'Heatwaves TODO', cmenu.table_heatwaves ],
        # [ 'Coldwaves TODO', cmenu.table_coldwaves ]
        ]
    ]
]

def check_menu_options():
    '''If no internet, skip download part'''
    ok_web, ok_data, loc_menu = False, False, menu
    # Check internet
    if not utils.has_internet():
        loc_menu = loc_menu[3:] # Update menu. Skip download options menu
    else:
        ok_web = True

    if utils.is_data_map_empthy():
        loc_menu = loc_menu[:-2] # Update menu. Skip data handling options menu
    else:
        ok_data = True

    return ok_web, ok_data, loc_menu

def error_no_stations_found():
    log.header('No weatherstations found in configuration file !', True )
    log.console('Add one or more weatherstations in config.py', True )
    log.footer('Press a key to quit...', True )
    input('...')

def fn_exec( choice, loc_menu ):
    n = 1
    for title in loc_menu:
        for option in title[1]:
            if n == choice:
                option[1]()
            n += 1

def main_menu():
    while True:  # Main menu
        ok_web, ok_data, loc_menu = check_menu_options()
        num = 1
        log.header('MAIN MENU', True )

        for el in loc_menu:
            title, options = el[0], el[1]
            log.console(f'\t{title}', True)
            for option in options:
                title, fn = option[0], option[1]
                log.console(f'\t\t{num}) {title}', True)
                num += 1
            print('')

        if ok_data == False and ok_web == False:
            t  = '\tNo internet and no data! Not much can be done now.\n'
            t += '\tFirst.  Try to have a working internet connection.\n'
            t += '\tSecond. Press a key to reload the menu or restart the application.\n'
            t += '\tThird.  Download weatherdata from the download options in the menu.'
            log.console(t, True)
            log.footer("\tPress a key to reload menu or press 'q' to quit...", True )
            answ = ask.ask(' ? ')
            if answ in config.answer_quit:
                break
            else:
                answ = False
        else:
            if ok_web == False:
                t = '\tNo internet connection. Get an working internet connection for more menu options.'
                log.console(t, True )
            elif ok_data == False:
                t = '\tNo data found. Download the weather data (option 1 & 2) for more menu options.'
                log.console(t, True )

            log.console(f'\tChoose one of the following options: 1...{num-1}', True )
            log.footer('Your choice is ? ', True )
            answ = ask.ask(' ? ')  # Make a choice

        if not answ:
            continue
        elif answ in config.answer_quit:
            break
        else:
            try:
                choice = int(answ)
            except ValueError:
                log.console(f'\nOption "{answ}" unknown...', True ) # Input was not a number
            else:
                if choice in range( 1, num ):
                    fn_exec(choice, loc_menu)
                else:
                    log.console(f'\nOption "{answ}" out of reach', True )
