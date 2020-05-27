# -*- coding: utf-8 -*-
'''Library contains functions for writing output to screen or to a file'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.4"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config, math, time
import view.txt as view_txt
import knmi.model.daydata as daydata
import view.translate as tr

def ent_to_title(ent):
    e = ent.strip().upper()
    if   e == 'TX': return tr.txt('Maximum temperature')
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
        txt += ent
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

def txt_main(day):
    stn, ymd, ddvec, fhvec, fg, fhx,\
    fhxh, fhn, fhnh, fxx, fxxh, tg,\
    tn, tnh, tx, txh, t10n, t10nh,\
    sq, sp, q, dr, rh, rhx,\
    rhxh, pg, px, pxh, pn, pnh,\
    vvn, vvnh, vvx, vvxh, ng, ug,\
    ux, uxh, un, unh, ev24 = ents( day )

    txt, title1, title2, title3, main1, main2, main3 = '', '', '', '', '', '', ''

    title1 += view_txt.ent_to_titel('TX') if tx else ''
    title1 += view_txt.ent_to_titel('TG') if tg else ''
    title1 += view_txt.ent_to_titel('TN') if tn else ''
    title1 += view_txt.ent_to_titel('T10N') if t10n else ''
    title1 += view_txt.ent_to_titel('DDVEC') if ddvec else ''
    title1 += view_txt.ent_to_titel('FG') if fg else ''
    title1 += view_txt.ent_to_titel('RH') if rh else ''
    title1 += view_txt.ent_to_titel('SQ') if sq else ''
    title1 += view_txt.ent_to_titel('PG') if pg else ''
    title1 += view_txt.ent_to_titel('UG') if ug else ''

    title2 += view_txt.ent_to_titel('FXX') if fxx else ''
    title2 += view_txt.ent_to_titel('FHX') if fhx else ''
    title2 += view_txt.ent_to_titel('FHN') if fhn else ''
    title2 += view_txt.ent_to_titel('FHVEC') if fhvec else ''
    title2 += view_txt.ent_to_titel('DR') if dr else ''
    title2 += view_txt.ent_to_titel('SP') if sp else ''
    title2 += view_txt.ent_to_titel('Q') if q else ''
    title2 += view_txt.ent_to_titel('RHX') if rhx else ''
    title2 += view_txt.ent_to_titel('PX') if px else ''
    title2 += view_txt.ent_to_titel('PN') if pn else ''

    title3 += view_txt.ent_to_titel('VVX') if vvx else ''
    title3 += view_txt.ent_to_titel('VVN') if vvn else ''
    title3 += view_txt.ent_to_titel('NG') if ng else ''
    title3 += view_txt.ent_to_titel('UX') if ux else ''
    title3 += view_txt.ent_to_titel('UN') if un else ''
    title3 += view_txt.ent_to_titel('EV24') if ev24  else ''

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
