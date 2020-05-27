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
