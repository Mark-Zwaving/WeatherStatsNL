# -*- coding: utf-8 -*-
'''PTrint daysvalues to screen'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.3.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config, view.icon as icon
import knmi.view.fix as fix
import knmi.model.daydata as daydata
import view.translate as tr
import view.txt as txt

def ents( day ):
    stn   = day[daydata.STN]
    ymd   = day[daydata.YYYYMMDD]
    dummy = config.knmi_dayvalues_dummy_val
    ddvec = False if day[daydata.DDVEC] == dummy else fix.ent(day[daydata.DDVEC], daydata.entities[daydata.DDVEC])
    fhvec = False if day[daydata.FHVEC] == dummy else fix.ent(day[daydata.FHVEC], daydata.entities[daydata.FHVEC])
    fg    = False if day[daydata.FG]    == dummy else fix.ent(day[daydata.FG],  daydata.entities[daydata.FG])
    fhx   = False if day[daydata.FHX]   == dummy else fix.ent(day[daydata.FHX], daydata.entities[daydata.FHX])
    fhxh  = False if day[daydata.FHXH]  == dummy else fix.ent(day[daydata.FHXH], daydata.entities[daydata.FHXH])
    fhn   = False if day[daydata.FHN]   == dummy else fix.ent(day[daydata.FHN], daydata.entities[daydata.FHN])
    fhnh  = False if day[daydata.FHNH]  == dummy else fix.ent(day[daydata.FHNH], daydata.entities[daydata.FHNH])
    fxx   = False if day[daydata.FXX]   == dummy else fix.ent(day[daydata.FXX], daydata.entities[daydata.FXX])
    fxxh  = False if day[daydata.FXXH]  == dummy else fix.ent(day[daydata.FXXH], daydata.entities[daydata.FXXH])
    tg    = False if day[daydata.TG]    == dummy else fix.ent(day[daydata.TG], daydata.entities[daydata.TG])
    tn    = False if day[daydata.TN]    == dummy else fix.ent(day[daydata.TN], daydata.entities[daydata.TN])
    tnh   = False if day[daydata.TNH]   == dummy else fix.ent(day[daydata.TNH], daydata.entities[daydata.TNH])
    tx    = False if day[daydata.TX]    == dummy else fix.ent(day[daydata.TX], daydata.entities[daydata.TX])
    txh   = False if day[daydata.TXH]   == dummy else fix.ent(day[daydata.TXH], daydata.entities[daydata.TXH])
    t10n  = False if day[daydata.T10N]  == dummy else fix.ent(day[daydata.T10N], daydata.entities[daydata.T10N])
    t10nh = False if day[daydata.T10NH] == dummy else fix.ent(day[daydata.T10NH], daydata.entities[daydata.T10NH])
    sq    = False if day[daydata.SQ]    == dummy else fix.ent(day[daydata.SQ], daydata.entities[daydata.SQ])
    sp    = False if day[daydata.SP]    == dummy else fix.ent(day[daydata.SP], daydata.entities[daydata.SP])
    q     = False if day[daydata.Q]     == dummy else fix.ent(day[daydata.Q], daydata.entities[daydata.Q])
    dr    = False if day[daydata.DR]    == dummy else fix.ent(day[daydata.DR], daydata.entities[daydata.DR])
    rh    = False if day[daydata.RH]    == dummy else fix.ent(day[daydata.RH], daydata.entities[daydata.RH])
    rhx   = False if day[daydata.RHX]   == dummy else fix.ent(day[daydata.RHX], daydata.entities[daydata.RHX])
    rhxh  = False if day[daydata.RHXH]  == dummy else fix.ent(day[daydata.RHXH], daydata.entities[daydata.RHXH])
    pg    = False if day[daydata.PG]    == dummy else fix.ent(day[daydata.PG], daydata.entities[daydata.PG])
    px    = False if day[daydata.PX]    == dummy else fix.ent(day[daydata.PX], daydata.entities[daydata.PX])
    pxh   = False if day[daydata.PXH]   == dummy else fix.ent(day[daydata.PXH], daydata.entities[daydata.PXH])
    pn    = False if day[daydata.PN]    == dummy else fix.ent(day[daydata.PN], daydata.entities[daydata.PN])
    pnh   = False if day[daydata.PNH]   == dummy else fix.ent(day[daydata.PNH], daydata.entities[daydata.PNH])
    vvn   = False if day[daydata.VVN]   == dummy else fix.ent(day[daydata.VVN], daydata.entities[daydata.VVN])
    vvnh  = False if day[daydata.VVNH]  == dummy else fix.ent(day[daydata.VVNH], daydata.entities[daydata.VVNH])
    vvx   = False if day[daydata.VVX]   == dummy else fix.ent(day[daydata.VVX], daydata.entities[daydata.VVX])
    vvxh  = False if day[daydata.VVXH]  == dummy else fix.ent(day[daydata.VVXH], daydata.entities[daydata.VVXH])
    ng    = False if day[daydata.NG]    == dummy else fix.ent(day[daydata.NG], daydata.entities[daydata.NG])
    ug    = False if day[daydata.UG]    == dummy else fix.ent(day[daydata.UG], daydata.entities[daydata.UG])
    ux    = False if day[daydata.UX]    == dummy else fix.ent(day[daydata.UX], daydata.entities[daydata.UX])
    uxh   = False if day[daydata.UXH]   == dummy else fix.ent(day[daydata.UXH], daydata.entities[daydata.UXH])
    un    = False if day[daydata.UN]    == dummy else fix.ent(day[daydata.UN], daydata.entities[daydata.UN])
    unh   = False if day[daydata.UNH]   == dummy else fix.ent(day[daydata.UNH], daydata.entities[daydata.UNH])
    ev24  = False if day[daydata.EV24]  == dummy else fix.ent(day[daydata.EV24], daydata.entities[daydata.EV24])

    return ( stn, ymd, ddvec, fhvec, fg, fhx,
             fhxh, fhn, fhnh, fxx, fxxh, tg,
             tn, tnh, tx, txh, t10n, t10nh,
             sq, sp, q, dr, rh, rhx,
             rhxh, pg, px, pxh, pn, pnh,
             vvn, vvnh, vvx, vvxh, ng, ug,
             ux, uxh, un, unh, ev24 )

def txt_main(day):
    stn, ymd, ddvec, fhvec, fg, fhx,\
    fhxh, fhn, fhnh, fxx, fxxh, tg,\
    tn, tnh, tx, txh, t10n, t10nh,\
    sq, sp, q, dr, rh, rhx,\
    rhxh, pg, px, pxh, pn, pnh,\
    vvn, vvnh, vvx, vvxh, ng, ug,\
    ux, uxh, un, unh, ev24 = ents( day )

    txt, title1, title2, title3, main1, main2, main3 = '', '', '', '', '', '', ''

    title1 += txt.ent_to_titel('TX') if tx else ''
    title1 += txt.ent_to_titel('TG') if tg else ''
    title1 += txt.ent_to_titel('TN') if tn else ''
    title1 += txt.ent_to_titel('T10N') if t10n else ''
    title1 += txt.ent_to_titel('DDVEC') if ddvec else ''
    title1 += txt.ent_to_titel('FG') if fg else ''
    title1 += txt.ent_to_titel('RH') if rh else ''
    title1 += txt.ent_to_titel('SQ') if sq else ''
    title1 += txt.ent_to_titel('PG') if pg else ''
    title1 += txt.ent_to_titel('UG') if ug else ''

    title2 += txt.ent_to_titel('FXX') if fxx else ''
    title2 += txt.ent_to_titel('FHX') if fhx else ''
    title2 += txt.ent_to_titel('FHN') if fhn else ''
    title2 += txt.ent_to_titel('FHVEC') if fhvec else ''
    title2 += txt.ent_to_titel('DR') if dr else ''
    title2 += txt.ent_to_titel('SP') if sp else ''
    title2 += txt.ent_to_titel('Q') if q else ''
    title2 += txt.ent_to_titel('RHX') if rhx else ''
    title2 += txt.ent_to_titel('PX') if px else ''
    title2 += txt.ent_to_titel('PN') if pn else ''

    title3 += txt.ent_to_titel('VVX') if vvx else ''
    title3 += txt.ent_to_titel('VVN') if vvn else ''
    title3 += txt.ent_to_titel('NG') if ng else ''
    title3 += txt.ent_to_titel('UX') if ux else ''
    title3 += txt.ent_to_titel('UN') if un else ''
    title3 += txt.ent_to_titel('EV24') if ev24  else ''

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

def div( title=False, val=False, time=False ):
    val  =  val if  val != False else ''
    time = time if time != False else ''
    return f'''
            <div class="card col-11 col-xs-11 col-sm-11 col-md-6 col-lg-4 col-xl-3 mx-auto border-0">
                <div class="card-body">
                    <h6 class="card-title text-capitalize day_title">
                        {title}
                    </h4>
                    <div class="card-text day_data">
                        {val}
                        <br>
                        <small class="text-muted">{time}</small>
                    </div>
                </div>
            </div>
            '''.format( title, val, time )

def html_main(day):
    stn, ymd, ddvec, fhvec, fg, fhx, fhxh, fhn, fhnh, fxx, fxxh, tg, tn,\
    tnh, tx, txh, t10n, t10nh, sq, sp, q, dr, rh, rhx, rhxh, pg, px, pxh,\
    pn, pnh, vvn, vvnh, vvx, vvxh, ng, ug, ux, uxh, un, unh, ev24 = ents(day)

    # Add icons
    if tx: tx = f'{icon.tx} {tx}'
    if tg: tg = f'{icon.tg} {tg}'
    if tn: tn = f'{icon.tn} {tn}'
    if t10n:  t10n = f'{icon.t10n} {t10n}'
    if ddvec: ddvec = f'{icon.arro} {ddvec}'
    if fhvec: fhvec = f'{icon.wind} {fhvec}'
    if fg:  fg  = f'{icon.wind} {fg}'
    if fhx: fhx = f'{icon.wind} {fhx}'
    if fhn: fhn = f'{icon.wind} {fhn}'
    if fxx: fxx = f'{icon.wind} {fxx}'
    if vvn: vvn = f'{icon.bino} {vvn}'
    if vvx: vvx = f'{icon.bino} {vvx}'
    if sq: sq = f'{icon.sun} {sq}'
    if sp: sp = f'{icon.sun} {sp}'
    if  q: q  = f'{icon.radi} {q}'
    if rh: rh = f'{icon.umbr} {rh}'
    if dr: dr = f'{icon.umbr} {dr}'
    if rhx: rhx = f'{icon.umbr} {rhx}'
    if ux: ux = f'{icon.drop} {ux}'
    if un: un = f'{icon.drop} {un}'
    if ug: ug = f'{icon.drop} {ug}'
    if ng: ng = f'{icon.clou} {ng}'
    if pg: pg = f'{icon.pres} {pg}'
    if pn: pn = f'{icon.pres} {pn}'
    if px: px = f'{icon.pres} {px}'
    if ev24: ev24 = f'{icon.swea} {ev24}'

    main  = ''
    main += div( txt.ent_to_titel('TX'), tx, txh ) if tx else ''
    main += div( txt.ent_to_titel('TG'), tg, False ) if tg else ''
    main += div( txt.ent_to_titel('TN'), tn, tnh ) if tn else ''
    main += div( txt.ent_to_titel('T10N'), t10n, t10nh ) if t10n else ''
    main += div( txt.ent_to_titel('DDVEC'), ddvec, False ) if ddvec else ''
    main += div( txt.ent_to_titel('FG'), fg, False ) if fg else ''
    main += div( txt.ent_to_titel('RH'), rh, False ) if rh else ''
    main += div( txt.ent_to_titel('SQ'), sq, False ) if sq else ''
    main += div( txt.ent_to_titel('PG'), pg, False ) if pg else ''
    main += div( txt.ent_to_titel('UG'), ug, False ) if ug else ''

    main += div( txt.ent_to_titel('FXX'), fxx, fxxh ) if fxx else ''
    main += div( txt.ent_to_titel('FHVEC'), fhvec, False ) if fhvec else ''
    main += div( txt.ent_to_titel('FHX'), fhx, fhxh ) if fhx else ''
    main += div( txt.ent_to_titel('FHN'), fhn, fhnh ) if fhn else ''
    main += div( txt.ent_to_titel('SP'), sp, False ) if sp else ''
    main += div( txt.ent_to_titel('Q'), q, False ) if q else ''
    main += div( txt.ent_to_titel('DR'), dr, False ) if dr else ''
    main += div( txt.ent_to_titel('RHX'), rhx, rhxh ) if rhx else ''
    main += div( txt.ent_to_titel('PX'), px, pxh ) if px else ''
    main += div( txt.ent_to_titel('PN'), pn, pnh ) if pn else ''

    main += div( txt.ent_to_titel('VVN'), vvn, vvnh ) if vvn else ''
    main += div( txt.ent_to_titel('VVX'), vvx, vvxh ) if vvx else ''
    main += div( txt.ent_to_titel('NG'), ng, False ) if ng else ''
    main += div( txt.ent_to_titel('UX'), ux, uxh ) if ux else ''
    main += div( txt.ent_to_titel('UN'), un, unh ) if un else ''
    main += div( txt.ent_to_titel('EV24'), ev24, False ) if ev24 else ''

    return main
