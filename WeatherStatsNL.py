# -*- coding: utf-8 -*-
'''WeatherStatsNL calculates weather statistics for dutch cities with data from the knmi'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.1.0'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

# Import libraries
import config
import view.log as log
import view.menu as menu

# Main programm
if __name__== '__main__':
    log.header( 'Welcome to WeatherStatsNL', True )
    if config.stations.size == 0:
        menu.error_no_stations_found()
    else:
        menu.main_menu()

    log.footer('Good bye', True )
