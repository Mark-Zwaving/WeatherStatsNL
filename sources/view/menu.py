# -*- coding: utf-8 -*-
'''Functions for menu '''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.3"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config, model.utils as utils
import view.log as log
import view.translate as tr
import control.ask as ask
import control.menu as control_menu

menu = [
    [ 'DOWNLOAD DATA', [
            [ 'Download all data dayvalues knmi stations',
               control_menu.process_knmi_dayvalues_all ],
            [ 'Download one or more dayvalues(s) data knmi stations',
               control_menu.process_knmi_dayvalues_selected ]
        ]
    ],
    [ 'FORECASTS', [
            [ 'Forecast weather (dutch)',
               control_menu.process_weather_knmi_global ],
            [ 'Forecast model (dutch)',
               control_menu.process_weather_knmi_model ],
            [ 'Forecast guidance (dutch)',
               control_menu.process_weather_knmi_guidance ]
        ]
    ],
    [ 'DAYVALUES AND PERIODS', [
            [ 'Dayvalues', control_menu.get_dayvalues_by_date ],
            [ 'Search for days', control_menu.search_for_days ],
            [ 'Period graphs', control_menu.graph_period ]
        ]
    ],
    [ 'STATISTICS TABLES', [
            [ 'Winter statistics', control_menu.table_winterstats ],
            [ 'Summer statistics', control_menu.table_summerstats  ],
            [ 'Winter & summer statistics', control_menu.table_allstats ]
            # [ 'Heatwaves TODO', control_menu.table_heatwaves ],
            # [ 'Coldwaves TODO', control_menu.table_coldwaves ]
        ]
    ]
]

def check_internet_menu():
    '''If no internet, skip download part'''
    loc_menu = menu
    if not utils.has_internet():
        loc_menu = loc_menu[2:] # Skip download
    return loc_menu

def error_no_stations_found():
    log.header('No weatherstations found !', True )
    log.console('Add one or more weatherstations in config.py', True )
    log.footer('Press a key to quit...', True )
    input('...')

def fn_exec( choice, loc_menu ):
    num = 1
    for title in loc_menu:
        for option in title[1]:
            if num == choice:
                option[1]()
            num += 1

def main_menu():
    loc_menu = check_internet_menu()
    while True:  # Main menu
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

        log.console(f'\tChoose one of the following options: 1...{num-1}', True )
        log.console("\tPress 'q' to quit...", True )
        log.footer('Your choice is ? ', True )

        answ = ask.ask(' ? ', False)  # Make a choice

        if answ in config.answer_quit:
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
