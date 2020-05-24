# -*- coding: utf-8 -*-
'''PTrint daysvalues to screen'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import numpy as np
import view.html as view_html
import model.utils as utils
import knmi.model.daydata as daydata
import knmi.model.dayvalues as model_day_values
import knmi.model.fix as fix
import config
import view.translate as tr

def ents( day ):
    stn   = day[daydata.STN]
    ymd   = day[daydata.YYYYMMDD]
    dummy = config.knmi_data_dummy_val
    ddvec = False if day[daydata.DDVEC] == dummy else fix.ent(day[daydata.DDVEC])
    fhvec = False if day[daydata.FHVEC] == dummy else fix.ent(day[daydata.FHVEC])
    fg    = False if day[daydata.FG]    == dummy else fix.ent(day[daydata.FG])
    fhx   = False if day[daydata.FHX]   == dummy else fix.ent(day[daydata.FHX])
    fhxh  = False if day[daydata.FHXH]  == dummy else fix.ent(day[daydata.FHXH])
    fhn   = False if day[daydata.FHN]   == dummy else fix.ent(day[daydata.FHN])
    fhnh  = False if day[daydata.FHNH]  == dummy else fix.ent(day[daydata.FHNH])
    fxx   = False if day[daydata.FXX]   == dummy else fix.ent(day[daydata.FXX])
    fxxh  = False if day[daydata.FXXH]  == dummy else fix.ent(day[daydata.FXXH])
    tg    = False if day[daydata.TG]    == dummy else fix.ent(day[daydata.TG])
    tn    = False if day[daydata.TN]    == dummy else fix.ent(day[daydata.TN])
    tnh   = False if day[daydata.TNH]   == dummy else fix.ent(day[daydata.TNH])
    tx    = False if day[daydata.TX]    == dummy else fix.ent(day[daydata.TX])
    txh   = False if day[daydata.TXH]   == dummy else fix.ent(day[daydata.TXH])
    t10n  = False if day[daydata.T10N]  == dummy else fix.ent(day[daydata.T10N])
    t10nh = False if day[daydata.T10NH] == dummy else fix.ent(day[daydata.T10NH])
    sq    = False if day[daydata.SQ]    == dummy else fix.ent(day[daydata.SQ])
    sp    = False if day[daydata.SP]    == dummy else fix.ent(day[daydata.SP])
    q     = False if day[daydata.Q]     == dummy else fix.ent(day[daydata.Q])
    dr    = False if day[daydata.DR]    == dummy else fix.ent(day[daydata.DR])
    rh    = False if day[daydata.RH]    == dummy else fix.ent(day[daydata.RH])
    rhx   = False if day[daydata.RHX]   == dummy else fix.ent(day[daydata.RHX])
    rhxh  = False if day[daydata.RHXH]  == dummy else fix.ent(day[daydata.RHXH])
    pg    = False if day[daydata.PG]    == dummy else fix.ent(day[daydata.PG])
    px    = False if day[daydata.PX]    == dummy else fix.ent(day[daydata.PX])
    pxh   = False if day[daydata.PXH]   == dummy else fix.ent(day[daydata.PXH])
    pn    = False if day[daydata.PN]    == dummy else fix.ent(day[daydata.PN])
    pnh   = False if day[daydata.PNH]   == dummy else fix.ent(day[daydata.PNH])
    vvn   = False if day[daydata.VVN]   == dummy else fix.ent(day[daydata.VVN])
    vvnh  = False if day[daydata.VVNH]  == dummy else fix.ent(day[daydata.VVNH])
    vvx   = False if day[daydata.VVX]   == dummy else fix.ent(day[daydata.VVX])
    vvxh  = False if day[daydata.VVXH]  == dummy else fix.ent(day[daydata.VVXH])
    ng    = False if day[daydata.NG]    == dummy else fix.ent(day[daydata.NG])
    ug    = False if day[daydata.UG]    == dummy else fix.ent(day[daydata.UG])
    ux    = False if day[daydata.UX]    == dummy else fix.ent(day[daydata.UX])
    uxh   = False if day[daydata.UXH]   == dummy else fix.ent(day[daydata.UXH])
    un    = False if day[daydata.UN]    == dummy else fix.ent(day[daydata.UN])
    unh   = False if day[daydata.UNH]   == dummy else fix.ent(day[daydata.UNH])
    ev24  = False if day[daydata.EV24]  == dummy else fix.ent(day[daydata.EV24])

    return ( stn, ymd, ddvec, fhvec, fg, fhx, fhxh, fhn, fhnh, fxx, fxxh, tg, tn,
             tnh, tx, txh, t10n, t10nh, sq, sp, q, dr, rh, rhx, rhxh, pg, px, pxh,
             pn, pnh, vvn, vvnh, vvx, vvxh, ng, ug, ux, uxh, un, unh, ev24 )

def text(day):
    stn, ymd, ddvec, fhvec, fg, fhx, fhxh, fhn, fhnh, fxx, fxxh, tg, tn,\
    tnh, tx, txh, t10n, t10nh, sq, sp, q, dr, rh, rhx, rhxh, pg, px, pxh,\
    pn, pnh, vvn, vvnh, vvx, vvxh, ng, ug, ux, uxh, un, unh, ev24 = ents(day)

    txt, title1, title2, title3, main1, main2, main3 = '', '', '', '', '', '', ''

    title1 += tr.txt('Maximum temperature') if tx else ''
    title1 += tr.txt('Mean temperature') if tg else ''
    title1 += tr.txt('Minimum temperature') if tn else ''
    title1 += tr.txt('Minimum temperature (10cm)') if t10n else ''
    title1 += tr.txt('Wind direction') if ddvec else ''
    title1 += tr.txt('Mean windspeed (daily)') if fg else ''
    title1 += tr.txt('Precipitation amount') if rh else
    title1 += tr.txt('Sunshine duration (hourly)') if sq else ''
    title1 += tr.txt('Mean pressure') if pg else ''
    title1 += tr.txt('Mean atmospheric humidity') if ug else ''

    title2 += tr.txt('Maximum wind (gust') if fxx else ''
    title2 += tr.txt('Maximum mean windspeed (hourly)') if fhx else ''
    title2 += tr.txt('Minimum mean windspeed (hourly)') if fhn else ''
    title2 += tr.txt('Mean windspeed (vector)') if fhvec else ''
    title2 += tr.txt('Precipitation duration') if dr else ''
    title2 += tr.txt('Sunshine duration (maximum potential)') if sp else ''
    title2 += tr.txt('Radiation (global)') if q else ''
    title2 += tr.txt('Maximum precipitation (hourly)') if rhx else ''
    title2 += tr.txt('Maximum pressure (hourly)') if px else ''
    title2 += tr.txt('Minimum pressure (hourly)') if pn else ''

    title3 += tr.txt('Maximum visibility') if vvx else ''
    title3 += tr.txt('Minimum visibility') if vvn else ''
    title3 += tr.txt('Mean cloud cover') if ng else ''
    title3 += tr.txt('Maximum humidity') if ux else ''
    title3 += tr.txt('Minimum humidity') if un else ''
    title3 += tr.txt('Evapotranspiration (potential)') if ev24  else ''

    main1 = ''
    main1 += tx    if tx    else ''
    main1 += tg    if tg    else ''
    main1 += tn    if tn    else ''
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

    txt += f'{title1\n{main1}\n}'
    txt += f'{title2\n{main2}\n}'
    txt += f'{title3\n{main3}\n}'

    return f'{txt}\n'

def div( title=False, val=False, time=False ):
    return f'''
            <div class="day_entity">
                <div class="day_title">
                    {title}
                </div>
                <div class="day_data">
                    {val} {time}
                </div>
            </div>
            '''.format( title, val if val else '', time if time else '' )

def html_main(station, day):
    stn, ymd, ddvec, fhvec, fg, fhx, fhxh, fhn, fhnh, fxx, fxxh, tg, tn,\
    tnh, tx, txh, t10n, t10nh, sq, sp, q, dr, rh, rhx, rhxh, pg, px, pxh,\
    pn, pnh, vvn, vvnh, vvx, vvxh, ng, ug, ux, uxh, un, unh, ev24 = ents(day)

    main  = ''
    main += div( tr.txt('Maximum temperature'), tx, txh ) if tx else ''
    main += div( tr.txt('Mean temperature'), tg, False ) if tg else ''
    main += div( tr.txt('Minimum temperature'), tn, tnh ) if tn else ''
    main += div( tr.txt('Minimum temperature (10cm)'), t10n, t10nh ) if t10n else ''
    main += div( tr.txt('Wind direction'), ddvec, False ) if ddvec else ''
    main += div( tr.txt('Mean windspeed (daily)'), fg, False ) if fg else ''
    main += div( tr.txt('Precipitation amount'), rh, False ) if rh else ''
    main += div( tr.txt('Sunshine duration (hourly)'), sq, False ) if sq else ''
    main += div( tr.txt('Mean pressure'), pg, False ) if pg else ''
    main += div( tr.txt('Mean atmospheric humidity'), ug, False ) if ug else ''

    main += div( tr.txt('Maximum wind (gust'), fxx, fxxh ) if fxx else ''
    main += div( tr.txt('Mean windspeed (vector)'), fhvec, False ) if fhvec else ''
    main += div( tr.txt('Maximum mean windspeed (hourly)'), fhx, fhxh ) if fhx else ''
    main += div( tr.txt('Minimum mean windspeed (hourly)'), fhn, fhnh ) if fhn else ''
    main += div( tr.txt('Sunshine duration (maximum potential)'), sp, False ) if sp else ''
    main += div( tr.txt('Radiation (global)'), q, False ) if q else ''
    main += div( tr.txt('Precipitation duration'), dr, False ) if dr else ''
    main += div( tr.txt('Maximum precipitation (hourly)'), rhx, rhxh ) if rhx else ''
    main += div( tr.txt('Maximum pressure (hourly)'), px, pxh ) if px else ''
    main += div( tr.txt('Minimum pressure (hourly)'), pn, pnh ) if pn else ''

    main += div( tr.txt('Minimum visibility'), vvn, vvnh ) if vvn else ''
    main += div( tr.txt('Maximum visibility'), vvx, vvxh ) if vvx else ''
    main += div( tr.txt('Mean cloud cover'), ng, False ) if ng else ''
    main += div( tr.txt('Maximum humidity'), ux, uxh ) if ux else ''
    main += div( tr.txt('Minimum humidity'), un, unh ) if un else ''
    main += div( tr.txt('Evapotranspiration (potential)'), ev24, False ) if ev24  else ''

    return main
