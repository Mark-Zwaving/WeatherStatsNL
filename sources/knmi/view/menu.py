# -*- coding: utf-8 -*-
'''Functions for menu '''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.2"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import view.log as log
import view.translate as tr
import control.ask as ask

def error_no_stations_found():
    #
    log.header('No weatherstations found !', True )
    log.console('Add one or more weatherstations in config.py', True )
    log.footer('Press a key to quit...', True )
    input('...')

def main_menu():
    log.header('MAIN MENU', True )
    log.console('\tChoose one of the following options\n', True )
    log.console('\t   1) Download all data dayvalues knmi stations', True )
    log.console('\t   2) Download one or more dayvalues(s) data knmi stations', True )
    log.console('\t   3) Dayvalues', True )
    log.console('\t   4) Winterstatistics', True )
    log.console('\t   5) Cold waves', True )
    log.console('\t   6) Summerstatistics', True )
    log.console('\t   7) Heatwaves', True )
    log.console('\t   8) Allround statistics summer and winter', True )
    log.console('\t   9) Extremes', True )
    log.console('\t  10) Images', True )
    log.console("\n\tPress 'q' or 'Q' to quit...", True )
    log.footer('Your choice is ?', True )
    choice = ask.ask(' ? ')  # Make a choice

    return choice
