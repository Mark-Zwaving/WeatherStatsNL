# -*- coding: utf-8 -*-
'''Library contains functions for writing output to screen or to a file'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.3"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config, math, time
import view.txt as txt
import knmi.model.daydata as daydata

def ent_to_titel(ent):
    e = ent.strip().upper()
    if  e == 'TX': return tr.txt('Maximum temperature')
    elif e == 'TG': return tr.txt('Mean temperature')
    elif e == 'TN': return tr.txt('Minimum temperature')
    elif e == 'T10N': return tr.txt('Minimum temperature (10cm)')
    elif e == 'DDVEC': return tr.txt('Wind direction')
    elif e == 'FG': return tr.txt('Mean windspeed (daily)')
    elif e == 'RH': return tr.txt('Precipitation amount')
    elif e == 'SQ': return tr.txt('Sunshine duration (hourly)')
    elif e == 'PG': return tr.txt('Mean pressure')
    elif e == 'UG': return tr.txt('Mean atmospheric humidity')
    elif e == 'FXX': return tr.txt('Maximum wind (gust)')
    elif e == 'FHVEC': return tr.txt('Mean windspeed (vector)')
    elif e == 'FHX': return tr.txt('Maximum mean windspeed (hourly)')
    elif e == 'FHN': return tr.txt('Minimum mean windspeed (hourly)')
    elif e == 'SP': return tr.txt('Sunshine duration (maximum potential)')
    elif e == 'Q': return tr.txt('Radiation (global)')
    elif e == 'DR': return tr.txt('Precipitation duration')
    elif e == 'RHX': return tr.txt('Maximum precipitation (hourly)')
    elif e == 'PX': return tr.txt('Maximum pressure (hourly)')
    elif e == 'PN': return tr.txt('Minimum pressure (hourly)')
    elif e == 'VVN': return tr.txt('Minimum visibility')
    elif e == 'VVX': return tr.txt('Maximum visibility')
    elif e == 'NG': return tr.txt('Mean cloud cover')
    elif e == 'UX': return tr.txt('Maximum humidity')
    elif e == 'UN': return tr.txt('Minimum humidity')
    elif e == 'EV24': return tr.txt('Evapotranspiration (potential)')
    return e

def dayvalues_entities( kol = 7, kol_width = 9 ):
    '''Functions prints a list with available entities'''
    tel, txt, ents, max = 1, '', daydata.entities, len( daydata.entities )
    for ent in ents:
        text += ent
        if tel % kol_width == 0 and tel != max:
            txt += ', '
    return txt

def knmi_stations(l, kol = 4, kol_width = 20):
    '''Functions prints list with available knmi stations'''
    content, cnt = '', len(l)
    for i in range(cnt):
        station = l[i]
        if kol_width != ',':
            content += f'{station.wmo} {station.place:{kol_width}}'
            if (i+1) == cnt:
                content += '\n'
            elif (i+1) % kol == 0:
                content += '\n'
        else:
            content += f"{station.wmo} {station.place}"
            if (i+1) == cnt:
                content += '\n'
            elif (i+1) % kol == 0:
                content += ',\n'
            else:
                content += ', '

    return content

def process_time_ext(txt, t_ns):
    '''Function gives a time string from nano seconds till days '''
    dag_sec, uur_sec, min_sec = 86400, 3600, 60
    delta_sec = t_ns / 1000000000

    rest, total_sec = math.modf( delta_sec )
    rest, milli_sec = math.modf( rest * 1000 )
    rest, micro_sec = math.modf( rest * 1000 )
    rest, nano_sec  = math.modf( rest * 1000 )
    mill, micr, nano = int(milli_sec), int(micro_sec), int(nano_sec)

    # Calculate from seconds
    dag  = int(total_sec // dag_sec) # Calculate days
    rest = total_sec  % dag_sec      # Leftover seconds
    uur  = int(rest // uur_sec)      # Calculate hours
    rest = rest  % uur_sec           # Leftover seconds
    min  = int(rest // min_sec)      # Calculate minutes
    rest = rest  % min_sec           # Leftover seconds
    sec  = int(rest)                 # Calculate seconds

    # Make nice output. Give emthpy string if 0
    # Only print to screen when counted amount > 0
    txt += ': '
    if dag  > 0: txt += f'{dag} {"days" if dag>1 else "day"} '
    if uur  > 0: txt += f'{uur} {"hours" if uur>1 else "hour"} '
    if min  > 0: txt += f'{min} {"minutes" if min>1 else "minute"} '
    if sec  > 0: txt += f'{sec} {"seconds" if sec>1 else "second"} '
    if mill > 0: txt += f'{mill} {"milliseconds" if mill>1 else "millisecond"} '
    # if micr > 0: txt += f'{micr} {"microseconds" if micr>1 else "microsecond"} '
    # if nano > 0: txt += f'{nano} {"nanoseconds" if nano>1 else "nanosecond"} '

    return txt

def process_time_s( txt_start, start_ns ):
    return f'{txt_start} {(time.time_ns() - start_ns) / 1000000000:.4f} seconds'
