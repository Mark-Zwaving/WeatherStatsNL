# -*- coding: utf-8 -*-
'''Library for supportive divers functions'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import datetime
import view.translate as tr

def path( dir, file):
    return os.path.abspath(os.path.join(dir,file))

def from_yyyymmdd_to_txt(ymd):
    d = datetime.date( int(ymd[:4]), int(ymd[4:6]), int(ymd[6:8]) )
    day_name  = tr.txt(d.strftime('%A'))
    date_day  = tr.txt(d.strftime('%d'))
    monthname = tr.txt(d.strftime('%B'))
    year      = d.strftime('%B')

    return f'{day_name}, {date_day} {monthname} {year}'
