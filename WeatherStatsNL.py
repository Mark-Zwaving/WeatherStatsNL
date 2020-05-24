# -*- coding: utf-8 -*-
'''WeatherStatsNL calculates weather statistics for dutch cities
from the data from the knmi'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.5"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os

# Import libraries
import config
import knmi.model.daydata as  daydata
import knmi.model.stats as stats
import knmi.control.menu as control_menu
import knmi.view.menu as view_menu
import knmi.view.fix as fix
import view.log as log

# Main programm
if __name__== "__main__":

    log.header('Welcome to WeatherStatsNL', True)
    if config.stations.size == 0:
        view_menu.error_no_stations_found()
    else:
        while True:  # Main menu
            choice = view_menu.main_menu( )
            if choice in config.answer_quit:
                break
            else:
                control_menu.menu_choices( choice )

    log.footer('Good bye', True )

    # print('dir_app', config.dir_app)
    # print('dir_data', config.dir_data)
    # print('dir_knmi', config.dir_knmi)
    # print('file_zip', daydata.file_zip)
    # print('file_txt', daydata.file_txt)
    # print('data_url', daydata.data_url)
    # print('data_source', daydata.data_source)
    # print('data_skip_rows', daydata.data_skip_rows)
    # print('data_dummy_val', daydata.data_dummy_val)
    # input('?')
    # log.console('MAIN MENU')
    #
    # sd, ed = 20200401, 20200430
    #
    # ok, data = daydata.read( '280' )
    # data = stats.period( data, sd, ed )
    #
    # max = fix.ent(stats.max( data, 'TX' ), 'TX')
    # min = fix.ent(stats.min( data, 'TN' ), 'TN')
    # ave = fix.ent(stats.average( data, 'TG' ), 'TG')
    # som = fix.ent(stats.sum( data, 'RH' ), 'RH')
    #
    # log.console( f'Maximum TX: {max}' )
    # log.console( f'Minimum TN: {min}' )
    # log.console( f'Average TG: {ave}' )
    # log.console( f'Rainsum RH: {som}' )
