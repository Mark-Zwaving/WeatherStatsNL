# -*- coding: utf-8 -*-
'''Print daysvalues to screen'''
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
    stn   = str(int(day[daydata.STN]))
    ymd   = str(int(day[daydata.YYYYMMDD]))
    dummy = config.knmi_dayvalues_dummy_val
    ddvec = fix.ent(day[daydata.DDVEC], daydata.entities[daydata.DDVEC])
    fhvec = fix.ent(day[daydata.FHVEC], daydata.entities[daydata.FHVEC])
    fg    = fix.ent(day[daydata.FG],  daydata.entities[daydata.FG])
    fhx   = fix.ent(day[daydata.FHX], daydata.entities[daydata.FHX])
    fhxh  = fix.ent(day[daydata.FHXH], daydata.entities[daydata.FHXH])
    fhn   = fix.ent(day[daydata.FHN], daydata.entities[daydata.FHN])
    fhnh  = fix.ent(day[daydata.FHNH], daydata.entities[daydata.FHNH])
    fxx   = fix.ent(day[daydata.FXX], daydata.entities[daydata.FXX])
    fxxh  = fix.ent(day[daydata.FXXH], daydata.entities[daydata.FXXH])
    tg    = fix.ent(day[daydata.TG], daydata.entities[daydata.TG])
    tn    = fix.ent(day[daydata.TN], daydata.entities[daydata.TN])
    tnh   = fix.ent(day[daydata.TNH], daydata.entities[daydata.TNH])
    tx    = fix.ent(day[daydata.TX], daydata.entities[daydata.TX])
    txh   = fix.ent(day[daydata.TXH], daydata.entities[daydata.TXH])
    t10n  = fix.ent(day[daydata.T10N], daydata.entities[daydata.T10N])
    t10nh = fix.ent(day[daydata.T10NH], daydata.entities[daydata.T10NH])
    sq    = fix.ent(day[daydata.SQ], daydata.entities[daydata.SQ])
    sp    = fix.ent(day[daydata.SP], daydata.entities[daydata.SP])
    q     = fix.ent(day[daydata.Q], daydata.entities[daydata.Q])
    dr    = fix.ent(day[daydata.DR], daydata.entities[daydata.DR])
    rh    = fix.ent(day[daydata.RH], daydata.entities[daydata.RH])
    rhx   = fix.ent(day[daydata.RHX], daydata.entities[daydata.RHX])
    rhxh  = fix.ent(day[daydata.RHXH], daydata.entities[daydata.RHXH])
    pg    = fix.ent(day[daydata.PG], daydata.entities[daydata.PG])
    px    = fix.ent(day[daydata.PX], daydata.entities[daydata.PX])
    pxh   = fix.ent(day[daydata.PXH], daydata.entities[daydata.PXH])
    pn    = fix.ent(day[daydata.PN], daydata.entities[daydata.PN])
    pnh   = fix.ent(day[daydata.PNH], daydata.entities[daydata.PNH])
    vvn   = fix.ent(day[daydata.VVN], daydata.entities[daydata.VVN])
    vvnh  = fix.ent(day[daydata.VVNH], daydata.entities[daydata.VVNH])
    vvx   = fix.ent(day[daydata.VVX], daydata.entities[daydata.VVX])
    vvxh  = fix.ent(day[daydata.VVXH], daydata.entities[daydata.VVXH])
    ng    = fix.ent(day[daydata.NG], daydata.entities[daydata.NG])
    ug    = fix.ent(day[daydata.UG], daydata.entities[daydata.UG])
    ux    = fix.ent(day[daydata.UX], daydata.entities[daydata.UX])
    uxh   = fix.ent(day[daydata.UXH], daydata.entities[daydata.UXH])
    un    = fix.ent(day[daydata.UN], daydata.entities[daydata.UN])
    unh   = fix.ent(day[daydata.UNH], daydata.entities[daydata.UNH])
    ev24  = fix.ent(day[daydata.EV24], daydata.entities[daydata.EV24])

    return ( stn, ymd, ddvec, fhvec, fg, fhx,
             fhxh, fhn, fhnh, fxx, fxxh, tg,
             tn, tnh, tx, txh, t10n, t10nh,
             sq, sp, q, dr, rh, rhx,
             rhxh, pg, px, pxh, pn, pnh,
             vvn, vvnh, vvx, vvxh, ng, ug,
             ux, uxh, un, unh, ev24 )
