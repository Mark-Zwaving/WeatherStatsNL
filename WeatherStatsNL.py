# -*- coding: utf-8 -*-
'''WeatherStatsNL calculates weather statistics for dutch cities
from the data from the knmi'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.9"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os

# Import libraries
import config
import knmi.model.daydata as  daydata
import knmi.model.stats as stats
import knmi.control.menu as control_menu
import knmi.view.fix as fix
import view.log as log
import view.menu as view_menu

# Main programm
if __name__== "__main__":
    log.header( 'Welcome to WeatherStatsNL', True )
    if config.stations.size == 0:
        view_menu.error_no_stations_found()
    else:
        choice = view_menu.main_menu()

    log.footer('Good bye', True )
