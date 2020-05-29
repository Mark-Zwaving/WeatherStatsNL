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
    log.header('No weatherstations found !', True )
    log.console('Add one or more weatherstations in config.py', True )
    log.footer('Press a key to quit...', True )
    input('...')

def main_menu():
    log.header('MAIN MENU', True )
    log.console('\tDOWNLOAD DATA', True )
    log.console('\t\t1) Download all data dayvalues knmi stations', True )
    log.console('\t\t2) Download one or more dayvalues(s) data knmi stations', True )
    print(' ')
    log.console('\tDAYVALUES AND PERIODS', True )
    log.console('\t\t3) Dayvalues', True )
    log.console('\t\t4) Period graphs', True )
    print(' ')
    log.console('\tSTATISTICS TABLES', True )
    log.console('\t\t5) Winterstatistics', True )
    log.console('\t\t6) Summerstatistics', True )
    log.console('\t\t7) Heatwaves', True )
    log.console('\t\t8) Winter- and summerstatistics', True )
    log.console('\t\t9) Extremes', True )
    print(' ')
    log.console('\tChoose one of the following options: 1, 2, 3 ... 9', True )
    log.console("\tPress 'q' or 'Q' to quit...", True )
    log.footer('Your choice is ?', True )
    choice = ask.ask(' ? ', False)  # Make a choice

    return choice
