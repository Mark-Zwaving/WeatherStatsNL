# -*- coding: utf-8 -*-
'''Library for supportive divers functions'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.3"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import datetime, os
import view.translate as tr
from datetime import datetime
from dateutil import rrule

def path( dir, file ):
    return os.path.abspath(os.path.join( dir, file ))

def ymd_to_txt( ymd ):
    y = int(ymd[:4])
    m = int(ymd[4:6])
    d = int(ymd[6:8])
    txt = datetime.date(y,m,d.strftime('%A, %d %B %Y'))

    return txt

def now_act_for_file():
    return datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

def add_zero_less_ten(d):
    if int(d) < 10:
        return f'0{d}'
    else:
        return f'{d}'

def list_dates_range( sd, ed ):
    l = []
    start = datetime.strptime(sd, '%Y%m%d')
    ends  = datetime.strptime(ed, '%Y%m%d')
    for date in rrule.rrule( rrule.DAILY, dtstart=start, until=ends ):
        l.append( date.strftime('%Y%m%d') )

    return l
