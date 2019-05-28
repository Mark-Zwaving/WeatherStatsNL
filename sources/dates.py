''' Library contains a class to handle dates'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import datetime, config as cfg

class Datum():
    def __init__(self, yyyymmdd):
        if cfg.language == 'NL':
            self.maanden = ['januari', 'februari', 'maart', 'april', 'mei', 'juni',
            'juli', 'augustus', 'september', 'oktober', 'november', 'december']
            self.dagen = ['maandag','dinsdag','woensdag','donderdag', 'vrijdag',
                          'zaterdag','zondag']

        else: # DEFAULT EN
            self.maanden = ['january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'oktober', 'november', 'december']
            self.dagen = ['monday','tuesday','wednesday','thursday', 'friday',
                          'saturday','sunday']

        self.y, self.m, self.d = int(yyyymmdd[:4]), int(yyyymmdd[4:6]), int(yyyymmdd[6:8])
        self.datum = datetime.date(self.y, self.m, self.d)

    def weekdag(self): return self.dagen[self.datum.weekday()]
    def maand(self):   return self.maanden[self.datum.month-1]
    def yyyy(self):    return str(self.y)
    def mm(self):      return str(self.m) if self.m > 9 else "0%i" % self.m
    def dd(self):      return str(self.d) if self.d > 9 else "0%i" % self.d
    def tekst(self):   return f'{self.weekdag()}, {self.dd()} {self.maand()} {self.yyyy()}'

def cnt_days(ymd_s, ymd_e):
    ys, ms, ds = ymd_s[:4], ymd_s[4:6], ymd_s[6:8]
    ye, me, de = ymd_e[:4], ymd_e[4:6], ymd_e[6:8]

    d0 = datetime.date( int(ys), int(ms), int(ds) )
    d1 = datetime.date( int(ye), int(me), int(de) )

    delta = (d1 - d0).days
    return delta
