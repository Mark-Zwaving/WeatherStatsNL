# -*- coding: utf-8 -*-
'''Library for supportive divers functions'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.7'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config, stations, datetime, os, re, math, random, threading
import http.client as httplib, numpy as np
from datetime import datetime
from dateutil import rrule
from pytz import timezone
import sources.control.fio as fio
import sources.view.console as console
import sources.view.translate as tr

rnd_digit = lambda min,max  : random.randint(min, max)
file_path = lambda dir,file : os.path.join(dir, file)
mk_path   = lambda dir,file : os.path.abspath( file_path(dir, file) )

def s_in_list(s, l):
    for el in l:
        if str(s).lower() == el.lower():
            return True
    return False

def is_yes(s):
    ok = s_in_list(s, config.answer_yes)
    return ok

def is_no(s):
    ok = s_in_list(s, config.answer_no)
    return ok

def is_quit(s):
    ok = s_in_list(s, config.answer_quit)
    return ok

def var_dump( v ):
    print(id(v), type(v), v)

def is_empthy( val ):
    ok = False
    if not val:
        ok = True

    return ok

def is_nan( val ):
    ok = False
    try:
        if val != val:
            ok = True
        elif val == np.isnan:
            ok = True
        elif np.isnan(val):
            ok = True
        elif math.isnan(val):
            ok = True
    except Exception as e:
        pass

    return ok

def is_float( val ):
    ok = True
    try:
        if val is None:
            ok = False
        elif is_nan(val):
            ok = False
        else:
            f = float(val)
    except Exception as e:
        console.log(f'Digit {val} is no float.')
        ok = False

    return ok

def has_internet(url=config.check_internet_url, timeout=0.1):
    ok = False
    with threading.Lock():
        connect = httplib.HTTPConnection(url, timeout=timeout)
        try:
            connect.request('HEAD', '/')
            connect.close()
        except Exception as e:
            pass
        else:
            ok = True

    return ok

def is_data_map_empthy():
    ok, dir = False, config.dir_dayvalues_txt
    with threading.Lock():
        if os.path.exists(dir):
            l = os.listdir(dir)
            if len(l) == 0:
                ok = True
            else:
                paths = [os.path.join(dir, el) for el in l]
                for station in stations.list:
                    if station.data_txt_path in paths:
                        ok = False
                        break
                else:
                    ok = True
    return ok

def only_existing_stations_in_map():
    l, dir = list(), config.dir_dayvalues_txt
    with threading.Lock():
        if os.path.exists(dir):
            paths = [os.path.join(dir, el) for el in os.listdir(dir)]
            for station in stations.list:
                if station.data_txt_path in paths:
                    l.append(station)
    return l

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
        console.log(f'Fail convert to bytes with charset {charset}\nError {e}', True)
    else:
        return b
    return s

def bytes_to_s( b, charset, errors ):
    try:
        s =  b.decode(encoding=charset, errors=errors)
    except Exception as e:
        console.log(f'Fail convert to string with charset {charset}.\nError:{e}', True)
    else:
        return s
    return b

def b_ascii_to_s( b ):
    s = bytes_to_s(b, 'ascii', 'ignore')
    return s

def b_utf8_to_s( b ):
    s = bytes_to_s(b, 'utf-8', 'ignore')
    return s

def download_and_read_file(url, file):
    ok, t = False, ''
    if has_internet():
        ok = fio.download( url, file )
        if ok:
            ok, t = fio.read(file)
    else:
        console.log('No internet connection...', True)

    return ok, t

def loc_date_now():
    dt = datetime.now() # UTC ?
    dt_loc = dt.replace(tzinfo=timezone(config.timezone)) # Now local

    return dt_loc.now() # return local

def now_for_file():
    t =  loc_date_now().strftime('%Y%m%d%H%M%S')
    return t

def now_created_notification():
    ds = loc_date_now().strftime('%A, %d %B %Y %H:%M')
    return config.created_by_notification % ds

def ymd_to_txt( ymd ):
    ymd = ymd if type(ymd) is str else f_to_s(ymd)
    return datetime.strptime(ymd, '%Y%m%d').strftime('%A, %d %B %Y')

def mk_name( base='x', period='x', places=[], entities=[] ):
    st = base + '-' + period.replace('*', 'x')
    for s in places:
        st += f'-{s.wmo}-'
    for e in entities:
        st += f'-{e}-'
    return st[:-1]

def mk_name_type( base='x', period='x', places=[], entities=[], type='txt' ):
    return mk_name( base, period, places, entities ) + f'.{type}'

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
    q = q.replace('ge',  ' ge ')
    q = q.replace('le',  ' le ')
    q = q.replace('eq',  ' eq ')
    q = q.replace('ne',  ' ne ')
    q = q.replace('gt',  ' gt ')
    q = q.replace('lt',  ' lt ')
    q = q.replace('or',  ' or ')
    q = q.replace('and', ' and ')
    q = q.replace('>=',  ' ge ')
    q = q.replace('≥',   ' ge ')
    q = q.replace('<=',  ' le ')
    q = q.replace('≤',   ' le ')
    q = q.replace('==',  ' eq ')
    q = q.replace('!=',  ' ne ')
    q = q.replace('<>',  ' ne ')
    q = q.replace('!=',  ' ne ')
    q = q.replace('>',   ' gt ')
    q = q.replace('<',   ' lt ')
    q = q.replace('||',  ' or ')
    q = q.replace('&&',  ' and ')

    return clear(q)

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
