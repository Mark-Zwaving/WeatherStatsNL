# -*- coding: utf-8 -*-
'''Library contains a log function'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.2"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import datetime, config
import sources.view.translate as tr
import sources.control.ask as ask

line = '#' * 80

def header ( txt='Header', log=config.log ):
    if log:
         print(f'\n{line}\n##  {tr.txt(txt)}\n{line}\n')

def footer ( txt='Footer', log=config.log ):
    if log:
        print(f'\n{line}\n##  {tr.txt(txt)}\n{line}\n')

def log ( txt='Console', log=config.log, debug=config.debug ):
    s = tr.txt(str(txt))
    if log:
        print(s)

    if debug:
        print(f'{datetime.datetime.now()} | {s}')
        ask.ask('Press a key to continue...', True)
