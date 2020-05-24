'''Library contains functions for validation'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.5"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import datetime, config
import view.log as log
import view.translate as tr

def yyyymmdd( ymd ):
    '''Function validates date'''
    ok = False
    ymd = str(ymd)
    if  len(ymd) != 8:
        log.console(f'Date: {ymd} has wrong length.')
        log.console(tr.txt('Use format of yyyymmdd with length is 8'))
    elif not ymd.isdigit():
        log.console(f'Date: {ymd} has wrong chars.')
        log.console(tr.txt('Date must only contain digits'))
    else:
        try:
            y, m, d = int(ymd[:4]), int(ymd[4:6]), int(ymd[6:8])
            date = datetime.datetime(y, m, d)
        except Exception as e:
            log.console(f"Error: {ymd} {e}")
        else:
            # Geen datum in de toekomst
            if date > datetime.datetime.now():
                log.console(f'Date: {ymd} is in the future.')
                log.console(tr.txt('Maybe try again later ;-)'))
            else:
                ok = True
    if ok:
        log.console(f"Date {ymd} is oké!")

    return ok
