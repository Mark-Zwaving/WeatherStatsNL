# -*- coding: utf-8 -*-
'''Library contains functions for building html and css ouput'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config as c, datetime, dates as d, fn, calc_stats as stat
import calc_sommerstats as cs, knmi

def pagina(title, style, content):
    return f'''<!-- Created by WeatherstatsNL at {datetime.datetime.now()} //-->
    <!DOCTYPE html>
    <html>
        <head>
            <title> {title} </title>
            <meta charset="UTF-8">
            <meta name="author" content="WeatherstatsNL">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style> {style} </style>
            <link rel="stylesheet" type="text/css" href="css/default_1.css">
            <link rel="stylesheet" type="text/css" href="css/default_2.css">
            <script src="js/default_1.js"></script>
            <script src="js/default_2.js"></script>
        </head>
        <body>
            <header>
                <!-- here you can add your own menu //-->
            </header>
            <article>
                {content}
            </article>
            <footer>
                <!-- here you can add your own footer //-->
            </footer>
        </body>
    </html>
    '''

def div_entity( title, data, time = '' ):
    return f'''
        <div class="entity">
            <div class="title">
                {title}
            </div>
            <div class="data">
                {data}
                {time}
            </div>
        </div>
    '''

def div_hour( data ):
    return f'''
        <div class="hour">
            {data}
        </div>
    '''

def div_entities( day_values ):
    d = day_values
    html = '<div id="container">'

    if d.TX is not d.empthy:
        t = div_hour( fn.fix(d.TXH,"TXH") ) if d.TXH is not d.empthy else ''
        html += div_entity( 'Maximum temperature', fn.fix(d.TX,"TX"), t)
    if d.TG is not d.empthy:
        html += div_entity( 'Mean temperature', fn.fix(d.TG,"TG") )
    if d.TN is not d.empthy:
        t = div_hour( fn.fix(d.TNH,"TNH") ) if d.TNH is not d.empthy else ''
        html += div_entity( 'Minimum temperature', fn.fix(d.TN,"TN"), t)
    if d.T10N is not d.empthy:
        t = div_hour( fn.fix(d.T10NH,"T10NH") ) if d.T10NH is not d.empthy else ''
        html += div_entity( 'Minimum temperature (10cm)', fn.fix(d.T10N,"T10N"), t)

    if d.DDVEC is not d.empthy:
        html += div_entity( 'Wind direction', fn.fix(d.DDVEC,"DDVEC") )
    if d.SQ is not d.empthy:
        html += div_entity( 'Sunshine duration (hourly)', fn.fix(d.SQ,"SQ") )
    if d.PG is not d.empthy:
        html += div_entity( 'Mean pressure', fn.fix(d.PG,"PG") )
    if d.UG is not d.empthy:
        html += div_entity( 'Mean atmospheric humidity', fn.fix(d.UG,"UG") )

    if d.FG is not d.empthy:
        html += div_entity( 'Mean windspeed (daily)', fn.fix(d.FG,"FG") )
    if d.SP is not d.empthy:
        html += div_entity( 'Sunshine duration (maximum potential)', fn.fix(d.SP,"SP") )
    if d.NG is not d.empthy:
        html += div_entity( 'Mean cloud cover', fn.fix(d.NG,"NG") )
    if d.RH is not d.empthy:
        html += div_entity( 'Precipitation amount', fn.fix(d.RH,"RH") )

    if d.FXX is not d.empthy:
        t = div_hour( fn.fix(d.FXXH,"FXXH") ) if d.FXXH is not d.empthy else ''
        html += div_entity( 'Maximum wind (gust)', fn.fix(d.FXX,"FXX"), t)
    if d.Q is not d.empthy:
        html += div_entity( 'Radiation (global)', fn.fix(d.Q,"Q") )
    if d.EV24 is not d.empthy:
        html += div_entity( 'Evapotranspiration (potential)', fn.fix(d.EV24,"EV24") )
    if d.DR is not d.empthy:
        html += div_entity( 'Precipitation duration', fn.fix(d.DR,"DR") )

    if d.FHVEC is not d.empthy:
        html += div_entity( 'Mean windspeed (vector)', fn.fix(d.FHVEC,"FHVEC") )
    if d.UX is not d.empthy:
        t = div_hour( fn.fix(d.UXH,"UXH") ) if d.UXH is not d.empthy else ''
        html += div_entity( 'Maximum humidity', fn.fix(d.UX,"UX"), t )
    if d.PX is not d.empthy:
        t = div_hour( fn.fix(d.PXH,"PXH") ) if d.PXH is not d.empthy else ''
        html += div_entity( 'Maximum pressure (hourly)', fn.fix(d.PX,"PX"), t )
    if d.RHX is not d.empthy:
        t = div_hour( fn.fix(d.RHXH,"RHXH") ) if d.RHXH is not d.empthy else ''
        html += div_entity( 'Maximum precipitation (hourly)', fn.fix(d.RHX,"RHX"), t )

    if d.FHX is not d.empthy:
        t = div_hour( fn.fix(d.FHXH,"FHXH") ) if d.FHXH is not d.empthy else ''
        html += div_entity( 'Maximum mean windspeed (hourly)', fn.fix(d.FHX,"FHX"), t )
    if d.VVX is not d.empthy:
        t = div_hour( fn.fix(d.VVXH,"VVXH") ) if d.VVXH is not d.empthy else ''
        html += div_entity( 'Maximum visibility', fn.fix(d.VVX,"VVX"), t )
    if d.PN is not d.empthy:
        t = div_hour( fn.fix(d.PNH,"PNH") ) if d.PNH is not d.empthy else ''
        html += div_entity( 'Minimum pressure (hourly)', fn.fix(d.PN,"PN"), t )
    if d.UN is not d.empthy:
        t = div_hour( fn.fix(d.UNH,"UNH") ) if d.UNH is not d.empthy else ''
        html += div_entity( 'Minimum humidity', fn.fix(d.UN,"UN"), t )

    if d.FHN is not d.empthy:
        t = div_hour( fn.fix(d.FHNH,"FHNH") ) if d.FHNH is not d.empthy else ''
        html += div_entity( 'Minimum mean windspeed (hourly)', fn.fix(d.FHN,"FHN"), t)
    if d.VVN is not d.empthy:
        t = div_hour( fn.fix(d.VVNH,"VVNH") ) if d.VVNH is not d.empthy else ''
        html += div_entity( 'Minimum visibility', fn.fix(d.VVN,"VVN"), t )

    html += '</div>'

    return html

def table_count(l, max):
    html = ''
    if l:
        if max is not 0:
            l.reverse() # Last count is last. Make first
            cnt = len(l)
            max = cnt if max == -1 else max # -1 for all!
            end = cnt if max > cnt else max # check bereik
            html += '<table class="popup">'
            html += '<thead><tr><th>datum</th><th>tijd</th><th>waarde</th>'
            html += '<th>eis</th><th>aantal</th></tr></thead>'
            html += '<tbody>'

            for e in l[:end]:
                sdt = d.Datum(e.datum).tekst()
                val = fn.rm_s( fn.fix( e.waarde, e.ent ) )
                eis = fn.rm_s( fn.fix( e.eis, e.ent ) )
                t_ent = knmi.ent_to_t_ent( e.ent )
                tme = fn.rm_s(fn.fix(e.tijd, t_ent)) if t_ent is not False else '.'
                html += f'<tr><td title="{sdt}">{e.datum}</td><td>{tme}</td>'\
                        f'<td>{val}</td><td>{e.oper}{eis}</td><td>{e.tel}</td></tr>'

            html += '</tbody>'
            html += '</table>'

    return html

def table_extremes(l, max):
    html = ''
    if l:
        if max is not 0:
            l.reverse() # Most extreme is last. Make first
            cnt = len(l)
            max = cnt if max == -1 else max # -1 for all!
            end = cnt if max > cnt else max # check bereik
            html += '<table class="popup">'
            html += '<thead><tr><th>datum</th><th>value</th><th>time</th><tr></thead>'
            html += '<tbody>'

            for e in l[:end]:
                sdt  = d.Datum( e.datum ).tekst()
                val = fn.rm_s( fn.fix( e.extreem, e.ent) )
                t_ent = knmi.ent_to_t_ent( e.ent )
                tme = fn.rm_s(fn.fix(e.tijd, t_ent)) if t_ent is not False else '.'
                html += f'<tr><td title="{sdt}">{e.datum}</td><td>{val}</td><td>{tme}</td></tr>'

            html += '</tbody>'
            html += '</table>'

    return html

def table_hellmann ( l, max ):
    html = ''
    if l:
        if max is not 0:
            l.reverse()
            cnt = len(l)
            max = cnt if max == -1 else max # -1 for all!
            end = cnt if max > cnt else max # check bereik
            html += '<table class="popup">'
            html += '<thead><tr><th>datum</th><th>getal</th><th>totaal</th><th>aantal</th></tr></thead>'
            html += '<tbody>'

            for e in l[:end]:
                sdt = d.Datum(e.datum).tekst()
                get = fn.rm_s(fn.fix(e.getal, 'hellmann'))
                som = fn.rm_s(fn.fix(e.som, 'hellmann'))
                html += f'<tr><td title="{sdt}">{e.datum}</td><td>{get}</td>'
                html += f'<td>{som}</td><td>{e.aantal}</td></tr>'

            html += '</tbody>'
            html += '</table>'

    return html

def table_heat_ndx( l, max ):
    html = ''
    if l:
        if max is not 0:
            l.reverse()
            cnt = len(l)
            max = cnt if max == -1 else max # -1 for all!
            end = cnt if max > cnt else max # check bereik
            html += '<table class="popup">'
            html += '<thead><tr><th>datum</th><th>tg</th><th>getal</th>'
            html += '<th>totaal</th><th>aantal</th></tr></thead>'
            html += '<tbody>'

            for e in l[:end]:
                sdt = d.Datum(e.datum).tekst()
                tg  = fn.rm_s(fn.fix(e.tg, 'tg'))
                get = fn.rm_s(fn.fix(e.getal, 'heat_ndx'))
                som = fn.rm_s(fn.fix(e.totaal, 'heat_ndx'))
                html += f'<tr><td title="{sdt}">{e.datum}</td><td>{tg}</td>'
                html += f'<td>{get}</td><td>{som}</td><td>{e.aantal}</td></tr>'

            html += '</tbody>'
            html += '</table>'

    return html

def table_list_heatwave_days( l, max ):
    html = ''
    if l:
        if max is not 0:
            l.reverse()
            cnt = len(l)
            max = cnt if max == -1 else max # -1 for all!
            end = cnt if max > cnt else max # check bereik
            html += '''<table class="popup">
                       <thead>
                       <tr><th>datum</th><th>∑warmte</th><th>∑dag</th>
                           <th>warmte</th><th>tx</th><th>tg</th><th>tn</th></tr>
                       </thead>
                       <tbody>'''
            cnt = len(l[:end])
            for e in l[:end]:
                sdt = d.Datum(e.YYYYMMDD).tekst()
                tx  = fn.rm_s(fn.fix(e.TX, 'tx'))
                tn  = fn.rm_s(fn.fix(e.TN, 'tn'))
                tg  = fn.rm_s(fn.fix(e.TG, 'tg'))

                # Migt be buggy tg < 18 will cause a error
                l_act = l[:cnt]
                tot_warm = fn.rm_s(fn.fix(cs.warmte_getal(l_act)['getal'],'heat_ndx')) # Calculate total warmth ndx at this moment
                g_warm = fn.rm_s(fn.fix(stat.get_heat_ndx_of_etm_geg(e),'heat_ndx'))

                html += f'''<tr>
                            <td title="{sdt}">{e.YYYYMMDD}</td><td>{tot_warm}</td>
                            <td>{cnt}</td><td>{g_warm}</td><td>{tx}</td><td>{tg}</td>
                            <td>{tn}</td>
                            </tr>'''

                cnt -= 1 # Less one day for next

            html += '</tbody>'
            html += '</table>'

    return html


def table_heatwaves( l, max ):
    html = ''
    if l:
        if max is not 0:
            cnt = len(l)
            max = cnt if max == -1 else max # -1 for all!
            end = cnt if max > cnt else max # check bereik
            html += '<table class="popup">'
            html += '<thead><tr><th>datum</th><th>tx</th><th>tg</th>'
            html += '<th>tn</th><th>sq</th><th>rh</th></tr></thead>'
            html += '<tbody>'

            for e in l[:end]:
                sdt = d.Datum(e.YYYYMMDD).tekst()
                tx = fn.fix(e.TX,"tx")
                tg = fn.rm_s(fn.fix(e.TG,"tg"))
                tn = fn.rm_s(fn.fix(e.TN,"tn"))
                sq = fn.rm_s(fn.fix(e.SQ,'sq'))
                rs = fn.rm_s(fn.fix(e.RS,'rs'))
                html += f'<tr><td title="{sdt}">{e.datum}</td><td title="Maximum temperatuur">{tx}</td>'
                html += f'<td title="Gemiddelde temperatuur">{tg}</td><td title="Minimum temperatuur">{tn}</td>'
                html += f'<td title="Aantal uren zon">{sq}</td><td title="Aantal mm regen">{rs}</td></tr>'

            html += '</tbody>'
            html += '</table>'

    return html
