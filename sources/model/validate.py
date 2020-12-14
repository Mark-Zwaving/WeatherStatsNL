'''Library contains functions for validation'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.5"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import datetime, config
import sources.view.console as console
import sources.view.translate as tr
import sources.view.txt as vt

def yyyymmdd( ymd ):
    '''Function validates date'''
    ok = False
    ymd = str(ymd)
    console.log(f'Validate {ymd}')
    if  len(ymd) != 8:
        console.log('Date has wrong length. Use format of yyyymmdd with length is 8')
    elif not ymd.isdigit():
        console.log('Date has wrong chars. Date must only contain digits')
    else:
        try:
            y, m, d = int(ymd[:4]), int(ymd[4:6]), int(ymd[6:8])
            date = datetime.datetime(y, m, d)
        except Exception as e:
            console.log(vt.error('Validate', e))
        else:
            # Geen datum in de toekomst
            if date > datetime.datetime.now():
                console.log('Date is in the future. Try again later... ;-)')
            else:
                console.log(vt.succes('Validate'))
                ok = True
    return ok
