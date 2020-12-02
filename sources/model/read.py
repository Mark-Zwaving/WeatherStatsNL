# -*- coding: utf-8 -*-
'''Functions to read text'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.5"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import threading, codecs
import view.log as log

def file( path ):
    t, ok = '', False
    log.console(f'Read file: {path}', True)

    with threading.Lock():
        try:
            with open(path, mode='r') as f:
                t = f.read()
        except Exception as e:
            log.console(f'Fail reading file.\nError: {e}', True)
        else:
            log.console('Reading success.\n', True)
            ok = True

    return ok, t
