# -*- coding: utf-8 -*-
'''Library for supportive divers functions'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.7'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config as cfg, datetime, os, re, math, random
import http.client as httplib, numpy as np
import view.translate as tr
import model.download as download
import model.read as read
import view.log as log
from datetime import datetime
from dateutil import rrule
from pytz import timezone

rnd_digit = lambda min,max  : random.randint(min, max)
file_path = lambda dir,file : os.path.join(dir, file)
mk_path   = lambda dir,file : os.path.abspath( file_path(dir, file) )

def var_dump( v ):
    print(id(v), type(v), v)

def is_empthy( answ ):
    if not answ or answ == '':
        return True
    else:
        return False

def has_internet(url=cfg.check_internet_url, timeout=0.1):
    ok = False
    connect = httplib.HTTPConnection(url, timeout=timeout)
    try:
        connect.request('HEAD', '/')
        connect.close()
    except Exception as e:
        pass
    else:
        ok = True

    return ok

def unique_list(l):
    unique = list()
    for el in l:
        if el not in unique:
            unique.append(el)
    return unique

# Fisher Yates Algorithm
def shuffle_list(l, level=1):
    max = len(l) - 1
    if max > 0:
        while level > 0:
            i = 0
            while i <= max:
                rnd = rnd_digit(0, max)  # Get random key

                # Swap values elements
                mem    = l[i]
                l[i]   = l[rnd]
                l[rnd] = mem

                i += 1  # Next element

            level -= 1
    return l

def rnd_from_list( l ):
    l = shuffle_list(l)  # Shuffle list
    rnd = rnd_digit( 0, len(l)-1 ) # Get a random number from list
    return l[rnd]

def s_to_bytes( s, charset, errors ):
    try:
        b = s.encode(encoding=charset, errors=errors)
    except Exception as e:
        log.console(f'Fail convert to bytes with charset {charset}\nError {e}', True)
    else:
        return b
    return s

def bytes_to_s( b, charset, errors ):
    try:
        s =  b.decode(encoding=charset, errors=errors)
    except Exception as e:
        log.console(f'Fail convert to string with charset {charset}.\nError:{e}', True)
    else:
        return s
    return b

def b_ascii_to_s( b ):
    s = bytes_to_s(b, 'ascii', 'ignore')
    return s

def download_and_read_file(url, file):
    ok, t = False, ''
    if has_internet():
        ok = download.file( url, file )
        if ok:
            ok, t = read.file(file)
    else:
        log.console('No internet connection...', True)

    return ok, t

def loc_date_now():
    dt_utc = datetime.now() # UTC propably
    tz = timezone(cfg.timezone)
    dt_loc = dt_utc.replace(tzinfo=tz)

    return dt_loc.now()

def isnan( f ):
    x = float(f)
    if math.isnan(x) or np.isnan(f):
        return True
    else:
        return False

def mk_name( base='x', period='x', stations=[], entities=[] ):
    st = base + '-' + period.replace('*', 'x')
    input(st)
    for s in stations:
        st += f'-{s.wmo}-'
    for e in entities:
        st += f'-{e}-'
    input(st)
    return st[:-1]

def mk_name_type( base='x', period='x', stations=[], entities=[], type='txt' ):
    return mk_name( base, period, stations, entities ) + f'.{type}'

def f_to_s( f ):
    return str(int(round(f)))

# Check and sanitize input
def clear( s ):
    s = re.sub('\n|\r|\t', '', s)
    s = re.sub('\s+', ' ', s)
    s = s.strip()
    return s

def make_query_txt_only(query):
    q = query.lower()
    q = q.replace('>=', ' ge ')
    q = q.replace('≥',  ' ge ')
    q = q.replace('<=', ' le ')
    q = q.replace('≤',  ' le ')
    q = q.replace('==', ' eq ')
    q = q.replace('!=', ' ne ')
    q = q.replace('<>', ' ne ')
    q = q.replace('!=', ' ne ')
    q = q.replace('>',  ' gt ')
    q = q.replace('<',  ' lt ')
    q = q.replace('||', ' or ')
    q = q.replace('&&', ' and ')

    return clear(q)

def ymd_to_txt( ymd ):
    ymd = ymd if type(ymd) is str else f_to_s(ymd)
    return datetime.strptime(ymd, '%Y%m%d').strftime('%A, %d %B %Y')

def now_act_for_file():
    txt =  datetime.now().strftime('%Y%m%d%H%M%S')
    return txt

def quit_menu(el):
    if np.array_equal(el, cfg.answer_quit):
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
