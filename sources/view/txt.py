# -*- coding: utf-8 -*-
'''Library contains functions for writing output to screen or to a file'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.7"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import math, time, re
import numpy as np
import sources.model.daydata as daydata
import sources.model.utils as utils
import sources.view.log as log

def error(t, err):
    t = f'{t} failed.\nError {err}'
    return t

def succes(t):
    t = f'{t} success.'
    return t

def clean_up( t ):
    t = t.strip()
    t = re.sub(r'(\n\n)\n+', '\n\n', t)
    t = re.sub('\t|  ', ' ', t)
    return t

def padding( t, align='center', spaces=35):
    pad = spaces - len(t)
    if pad < 0:
        pad = 0

    res = f'{t:{pad}}'
    if   align == 'center': res = f'{t:^{pad}}'
    elif align == 'left':   res = f'{t:{pad}}'
    elif align == 'right':  res = f'{t:>{pad}}'

    return res

def enter_default(default):
    return f'Press <enter> for default (={default})'

def enter_back_to_main():
    return "Press 'q' to go back to the main menu... "

def ent_to_title(ent):
    e = ent.strip().upper()
    if   e == 'TX': return 'Maximum temperature'
    elif e == 'TG': return 'Mean temperature'
    elif e == 'TN': return 'Minimum temperature'
    elif e == 'T10N': return 'Minimum temperature (10cm)'
    elif e == 'DDVEC': return 'Wind direction'
    elif e == 'FG': return 'Mean windspeed (daily)'
    elif e == 'RH': return 'Precipitation amount'
    elif e == 'SQ': return 'Sunshine duration (hourly)'
    elif e == 'PG': return 'Mean pressure'
    elif e == 'UG': return 'Mean atmospheric humidity'
    elif e == 'FXX': return 'Maximum wind (gust)'
    elif e == 'FHVEC': return 'Mean windspeed (vector)'
    elif e == 'FHX': return 'Maximum mean windspeed (hourly)'
    elif e == 'FHN': return 'Minimum mean windspeed (hourly)'
    elif e == 'SP': return 'Sunshine duration (maximum potential)'
    elif e == 'Q': return 'Radiation (global)'
    elif e == 'DR': return 'Precipitation duration'
    elif e == 'RHX': return 'Maximum precipitation (hourly)'
    elif e == 'PX': return 'Maximum pressure (hourly)'
    elif e == 'PN': return 'Minimum pressure (hourly)'
    elif e == 'VVN': return 'Minimum visibility'
    elif e == 'VVX': return 'Maximum visibility'
    elif e == 'NG': return 'Mean cloud cover'
    elif e == 'UX': return 'Maximum humidity'
    elif e == 'UN': return 'Minimum humidity'
    elif e == 'EV24': return 'Evapotranspiration (potential)'
    return e

def optionlist( npl, sep=',', col_cnt = False, col_spaces = False ):
    # Possible update none values
    max_len, max_char = 0, 60
    for e in npl:
        char_len = len( str(e) )
        if char_len > max_len:
            max_len = char_len

    # Update the values
    if col_cnt == False: col_cnt = math.floor( max_char / max_len )
    if col_spaces == False or col_spaces < max_len: col_spaces = max_len

    # Make txt list with colls en newlines
    txt, n, max = '', 1, npl.size
    for e in npl:
        txt += f'{e:{col_spaces}}'
        txt += f'{sep} ' if n % col_cnt != 0 and n != max else '\n' # comma or newline
        n   += 1

    return txt

def dayvalues_entities( sep=',', kol = False, kol_width = False ):
    '''Functions prints a list with available entities'''
    l = daydata.entities
    for rem in np.array( [ 'FHXH', 'FHNH', 'FXXH', 'TNH', 'TXH', 'T10NH',\
                           'RHXH', 'PXH',  'PNH', 'VVNH', 'VVXH',  'UXH',\
                           'UNH' ] ):
        l = l[l != rem] # Remove time ent

    txt = optionlist( l, '', kol, kol_width )
    return txt

def knmi_stations(l, kol = 4, kol_width = 20):
    '''Functions prints list with available knmi stations'''
    content, cnt = '', len(l) # not a np list
    for i in range(cnt):
        station = l[i]
        content += f'{station.wmo} {station.place:{kol_width}}'
        content += '\n' if (i+1) == cnt or (i+1) % kol == 0 else '' # comma or newline

    return content

def txt_main( day ):
    stn, ymd, ddvec, fhvec, fg, fhx,\
    fhxh, fhn, fhnh, fxx, fxxh, tg,\
    tn, tnh, tx, txh, t10n, t10nh,\
    sq, sp, q, dr, rh, rhx,\
    rhxh, pg, px, pxh, pn, pnh,\
    vvn, vvnh, vvx, vvxh, ng, ug,\
    ux, uxh, un, unh, ev24 = ents( day )

    txt, title1, title2, title3, main1, main2, main3 = '', '', '', '', '', '', ''

    title1 += ent_to_title('TX') if tx else ''
    title1 += ent_to_title('TG') if tg else ''
    title1 += ent_to_title('TN') if tn else ''
    title1 += ent_to_title('T10N') if t10n else ''
    title1 += ent_to_title('DDVEC') if ddvec else ''
    title1 += ent_to_title('FG') if fg else ''
    title1 += ent_to_title('RH') if rh else ''
    title1 += ent_to_title('SQ') if sq else ''
    title1 += ent_to_title('PG') if pg else ''
    title1 += ent_to_title('UG') if ug else ''

    title2 += ent_to_title('FXX') if fxx else ''
    title2 += ent_to_title('FHX') if fhx else ''
    title2 += ent_to_title('FHN') if fhn else ''
    title2 += ent_to_title('FHVEC') if fhvec else ''
    title2 += ent_to_title('DR') if dr else ''
    title2 += ent_to_title('SP') if sp else ''
    title2 += ent_to_title('Q') if q else ''
    title2 += ent_to_title('RHX') if rhx else ''
    title2 += ent_to_title('PX') if px else ''
    title2 += ent_to_title('PN') if pn else ''

    title3 += ent_to_title('VVX') if vvx else ''
    title3 += ent_to_title('VVN') if vvn else ''
    title3 += ent_to_title('NG') if ng else ''
    title3 += ent_to_title('UX') if ux else ''
    title3 += ent_to_title('UN') if un else ''
    title3 += ent_to_title('EV24') if ev24  else ''

    main1 = ''
    main1 += tx if tx else ''
    main1 += tg if tg else ''
    main1 += tn if tn else ''
    main1 += t10n  if t10n  else ''
    main1 += ddvec if ddvec else ''
    main1 += fg    if fg    else ''
    main1 += rh    if rh    else ''
    main1 += sq    if sq    else ''
    main1 += pg    if pg    else ''
    main1 += ug    if ug    else ''

    main2 += fhvec if fhvec else ''
    main2 += fhx   if fhx   else ''
    main2 += fhn   if fhn   else ''
    main2 += fxx   if fxx   else ''
    main2 += sp    if sp    else ''
    main2 += q     if q     else ''
    main2 += dr    if dr    else ''
    main2 += rhx   if rhx   else ''
    main2 += px    if px    else ''
    main2 += pn    if pn    else ''

    main3 += vvn   if vvn   else ''
    main3 += vvx   if vvx   else ''
    main3 += ng    if ng    else ''
    main3 += ux    if ux    else ''
    main3 += un    if un    else ''
    main3 += ev24  if ev24  else ''

    txt += f'{title1}\n{main1}\n'
    txt += f'{title2}\n{main2}\n'
    txt += f'{title3}\n{main3}\n'

    return f'{txt}\n'

def process_time_ext(t='', delta_ns=0):
    '''Function gives a time string from nano seconds till days '''
    dag_sec, uur_sec, min_sec = 86400, 3600, 60
    delta_sec = delta_ns / 1000000000

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
    if dag > 0: t += str(dag) + (' days '    if dag > 1 else ' day ')
    if uur > 0: t += str(uur) + (' hours '   if uur > 1 else ' hour ')
    if min > 0: t += str(min) + (' minutes ' if min > 1 else ' minute ')

    smile = utils.add_zero_less_1000(mill)
    if sec > 0:
        t += f'{sec}.{smile} ' + ('second ' if sec == 1 else 'seconds ')
    else:
        t += f'0.{smile} second '

    # if micr > 0: txt += f'{micr} {"microseconds" if micr>1 else "microsecond"} '
    # if nano > 0: txt += f'{nano} {"nanoseconds" if nano>1 else "nanosecond"} '

    return t

def process_time(t='', st=time.time_ns()):
    delta = time.time_ns() - st
    t = process_time_ext(t, delta)
    return t
