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

def div_day_entity( station, title, val, ent, t_val, t_ent ):
    if val == station.empthy:
        return ''
    else:
        val, time = fn.fix(val, ent), ''
        if t_val not in [station.empthy, '']:
            time = div_hour(fn.fix(t_val, t_ent))

        return f'''
            <div class="entity">
                <div class="title">
                    {title}
                </div>
                <div class="data">
                    {val}
                    {time}
                </div>
            </div>
        '''

    return ''

def div_hour( data ):
    return f'''
        <div class="hour">
            {data}
        </div>
    '''

def html_dayvalues( station, day_values ):
    d, s = day_values, station
    html  = '<div id="container">'
    html += div_day_entity( s, 'Maximum temperature', d.TX,'TX',d.TXH,'TXH' )
    html += div_day_entity( s, 'Gemiddelde temperature', d.TG,'TG','','' )
    html += div_day_entity( s, 'Minimum temperature', d.TN,'TN',d.TNH,'TNH' )
    html += div_day_entity( s, 'Minimum temperature (10cm)', d.T10N,'TN',d.T10NH,'TNH' )
    html += div_day_entity( s, 'Wind direction', d.DDVEC,'DDVEC','','' )
    html += div_day_entity( s, 'Sunshine duration (hourly)',d.SQ,'SQ','','' )
    html += div_day_entity( s, 'Mean pressure', d.PG,'PG','','' )
    html += div_day_entity( s, 'Mean atmospheric humidity', d.UG,'UG','','' )
    html += div_day_entity( s, 'Mean windspeed (daily)', d.FG,'FG','','' )
    html += div_day_entity( s, 'Sunshine duration (maximum potential)', d.SP,'SP','','' )
    html += div_day_entity( s, 'Mean cloud cover', d.NG,'NG','','' )
    html += div_day_entity( s, 'Precipitation amount', d.RH,'RH','','' )
    html += div_day_entity( s, 'Maximum wind (gust)', d.FXX,'FXX',d.FXXH,'FXXH' )
    html += div_day_entity( s, 'Radiation (global)', d.Q,'Q','','' )
    html += div_day_entity( s, 'Evapotranspiration (potential)', d.EV24,'EV24','','' )
    html += div_day_entity( s, 'Precipitation duration', d.DR,'DR','','' )
    html += div_day_entity( s, 'Mean windspeed (vector)', d.FHVEC,'FHVEC','','' )
    html += div_day_entity( s, 'Maximum wind (gust)', d.FXX,'FXX',d.FXXH,'FXXH' )
    html += div_day_entity( s, 'Maximum humidity', d.UX,'UX',d.UXH,'UXH' )
    html += div_day_entity( s, 'Maximum pressure (hourly)', d.PX,'PX',d.PXH,'PXH' )
    html += div_day_entity( s, 'Maximum precipitation (hourly)', d.RHX,'RHX',d.RHXH,'RHXH' )
    html += div_day_entity( s, 'Maximum mean windspeed (hourly)', d.FHX,'FHX',d.FHXH,'FHXH' )
    html += div_day_entity( s, 'Maximum visibility', d.VVX,'VVX',d.VVXH,'VVXH' )
    html += div_day_entity( s, 'Minimum pressure (hourly)', d.PN,'PN',d.PNH,'PNH' )
    html += div_day_entity( s, 'Minimum humidity', d.UN,'UN',d.UNH,'UNH' )
    html += div_day_entity( s, 'Minimum mean windspeed (hourly)', d.FHN,'FHN',d.FHNH,'FHNH' )
    html += div_day_entity( s, 'Minimum visibility', d.VVN,'VVN',d.VVNH,'VVNH' )
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
                t_ent = knmi.ent_to_t_ent( e.ent )
                eis = fn.div_10(e.eis)
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
                html += f'<tr><td title="{sdt}">{e.datum}</td><td>{som}</td>'
                html += f'<td>{get}</td><td>{e.aantal}</td></tr>'

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
            warm_sum = stat.warmte_getal(l)['getal'] # Total heat ndx
            html += '''<table class="popup">
                       <thead>
                       <tr><th>datum</th><th>∑dag</th><th>∑warmte</th>
                           <th>warmte</th><th>tx</th><th>tg</th><th>tn</th></tr>
                       </thead>
                       '''

            for e in l[:end]:
                sdt = d.Datum(e.YYYYMMDD).tekst()
                tx  = fn.rm_s(fn.fix(e.TX, 'tx'))
                tn  = fn.rm_s(fn.fix(e.TN, 'tn'))
                tg  = fn.rm_s(fn.fix(e.TG, 'tg'))

                tot_warm = fn.rm_s(fn.fix(warm_sum,'heat_ndx'))
                act_warm = stat.get_heat_ndx_of_etm_geg(e)
                g_warm = fn.rm_s(fn.fix(act_warm,'heat_ndx'))

                html += f'''<tr>
                            <td title="{sdt}">{e.YYYYMMDD}</td><td>{cnt}</td>
                            <td>{tot_warm}</td><td>{g_warm}</td><td>{tx}</td>
                            <td>{tg}</td><td>{tn}</td>
                            </tr>
                        '''

                # Minus act day heatndx for the total heatndx of the day before
                warm_sum -= act_warm
                cnt -= 1

            html += '</tbody>'
            html += '</table>'

    return html
