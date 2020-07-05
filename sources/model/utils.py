# -*- coding: utf-8 -*-
'''Library for supportive divers functions'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.4"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config
import datetime, os
import view.translate as tr
from datetime import datetime
from dateutil import rrule
import numpy as np

def path( dir, file ):
    return os.path.abspath(os.path.join(dir, file))

def ymd_to_txt( ymd ):
    return datetime.strptime(str(ymd), "%Y%m%d").strftime('%A, %d %B %Y')

def now_act_for_file():
    txt =  datetime.now().strftime('%Y%m%d%H%M%S')
    return txt

def quit_menu(l):
    if np.array_equal(l,config.answer_quit):
        return True
    else:
        return False

# TODO testing
def add_zero_less_x(d, x):
    s = str(d)
    n = x - len(s)
    while n > 0:
        s = f'0{s}'
    return s

def add_zero_less_ten(d):
    if int(d) < 10:
        return f'0{d}'
    else:
        return f'{d}'

def add_zero_less_1000(d):
    s = str(d)
    n = len(s)
    if n == 1:
        return f'00{s}'
    elif n == 2:
        return f'0{s}'
    return s

def list_dates_range( sd, ed ):
    l = []
    sd = datetime.strptime(sd, '%Y%m%d')
    ed = datetime.strptime(ed, '%Y%m%d')
    for date in rrule.rrule( rrule.DAILY, dtstart=sd, until=ed ):
        l.append( date.strftime('%Y%m%d') )

    return l
