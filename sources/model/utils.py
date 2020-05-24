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

path = lambda dir, file : os.path.abspath(os.path.join(dir,file))

ymd_to_txt = lambda ymd : datetime.date(int(ymd[:4]),int(ymd[4:6]),int(ymd[6:8])).strftime('%A, %d %B %Y')

now_act_for_file = lambda : datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
