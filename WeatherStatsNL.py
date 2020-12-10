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
import config, sys, stations
import sources.view.log as log
import sources.view.menu as menu

# Add dir (from this) app to system path, if not already there.
if config.dir_app not in sys.path:
    sys.path.append(config.dir_app)

# Main programm
if __name__== '__main__':
    log.console('\nWelcome to WeatherStatsNL', True )
    if len(stations.list) == 0:
        menu.error_no_stations_found()
    else:
        menu.main_menu()

    log.console('\nGood bye', True )
