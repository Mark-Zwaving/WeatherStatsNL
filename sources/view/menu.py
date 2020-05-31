# -*- coding: utf-8 -*-
'''Functions for menu '''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.2"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config
import view.log as log
import view.translate as tr
import control.ask as ask
import knmi.control.menu as control_menu

menu = [
    [ 'DOWNLOAD DATA', [
            [ 'Download all data dayvalues knmi stations',
               control_menu.process_knmi_dayvalues_all ],
            [ 'Download one or more dayvalues(s) data knmi stations',
               control_menu.process_knmi_dayvalues_selected ]
        ]
    ],
    [ 'DAYVALUES AND PERIODS', [
            [ 'Dayvalues', control_menu.get_dayvalues_by_date ],
            [ 'Select days', control_menu.select_days ],
            [ 'Period graphs', control_menu.graph_period ]
        ]
    ],
    [ 'STATISTICS TABLES', [
            [ 'Winterstatistics', control_menu.table_winterstats ],
            [ 'Summerstatistics', control_menu.table_zomerstats  ],
            [ 'Heatwaves', control_menu.table_heatwaves ],
            [ 'Winter- and summerstatistics', control_menu.table_allstats ],
            [ 'Extremes', control_menu.table_allextremes ]
        ]
    ]
]

def error_no_stations_found():
    log.header('No weatherstations found !', True )
    log.console('Add one or more weatherstations in config.py', True )
    log.footer('Press a key to quit...', True )
    input('...')

def main_menu():
    while True:  # Main menu
        n = 1
        log.header('MAIN MENU', True )
        for el in menu:
            log.console(f'\t{el[0]}', True)
            for option in el[1]:
                title, fn = option[0], option[1]
                log.console(f'\t\t{n}) {title}' ,True)
                n += 1
            print('')

        log.console(f'\tChoose one of the following options: 1, 2, 3 ... {n-1}', True )
        log.console("\tPress 'q' or 'Q' to quit...", True )

        log.footer('Your choice is ?', True )
        choice = ask.ask(' ? ', False)  # Make a choice

        if choice in config.answer_quit:
            break
        else:
            c, n = int(choice), 1
            for el in menu:
                for option in el[1]:
                    print(n)
                    if n == c:
                        print( n, c )
                        option[1]()
                        break
                        break
                    n += 1
