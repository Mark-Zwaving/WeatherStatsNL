import config as c, datetime, datum as d, fn

def pagina(title, style, content):
    return f'''<!DOCTYPE html>
    <html>
        <head>
            <title> {title} </title>
            <meta charset="UTF-8">
            <meta name="author" content="WeatherstatsNL">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style> {style} </style>
            <link rel="stylesheet" type="text/css" href="css/default.css">
            <script src="js/default.js"></script>
        </head>
        <body>
            <header>
                <!-- here you can add your own menu //-->
            </heeader>
            <article>
                {content}
            </article>
            <footer>
                <!-- here you can add your own footer //-->
            </footer>
        <!-- Created by WeatherstatsNL at {datetime.datetime.now()} //-->
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

def table_extremes ( l, x, p ):
    l.reverse()
    cnt = len(l); x = cnt if x > cnt else x # check bereik
    t  = '<table class="popup">'
    t += '<thead><tr><th>datum</th><th>waarde</th><th>tijd</th><tr></thead><tbody>'
    for e in l[:x]:
        t += f'<tr> <td title="{d.Datum(e.datum).tekst()}">{e.datum}</td> ' \
             f'<td>{e.extreem:0.1f}{p}</td> <td>{e.tijd}</td> </tr>'
    t += '</tbody></table>'
    return t

def table_hellmann ( l, x ):
    l.reverse()
    cnt = len(l); x = cnt if x > cnt else x # check bereik
    t  = '<table class="popup">'
    t += '<thead><tr><th>datum</th><th>getal</th><th>totaal</th><th>aantal</th></tr></thead>'
    t += '<tbody>'
    for e in l:
        t += f'<tr> <td title="{d.Datum(e.datum).tekst()}">{e.datum}</td> ' \
             f'<td>{e.getal:0.1f}</td> <td>{e.som:0.1f}</td> <td>{e.aantal}</td> </tr>'
    t += '</tbody></table>'
    return t

def table_warmte_getal( l, x ):
    l.reverse()
    cnt = len(l); x = cnt if x > cnt else x # check bereik
    t  = '<table class="popup">'
    t += '<thead><tr><th>datum</th><th>tg</th><th>getal</th>' \
         '<th>totaal</th><th>aantal</tr></thead><tbody>'
    for e in l:
        t += f'<tr> <td title="{d.Datum(e.datum).tekst()}">{e.datum}</td> ' \
             f'<td>{e.tg:0.1f}</td> <td>{e.getal:0.1f}</td> ' \
             f'<td>{e.totaal:0.1f}</td> <td>{e.aantal}</td></tr>'
    t += '</tbody></table>'
    return t

def table_count ( l, x, p ):
    l.reverse()
    cnt = len(l); x = cnt if x > cnt else x # check bereik
    t  = '<table class="popup">'
    t += '<thead><tr><th>datum</th><th>tijd</th><th>waarde</th>' \
         '<th>eis</th><th>aantal</th></tr></thead><tbody>'
    for e in l[:x]:
        t += f'<tr><td title="{d.Datum(e.datum).tekst()}">{e.datum}</td> ' \
             f'<td>{e.tijd}</td><td>{e.waarde:0.1f}{p}</td>' \
             f'<td>{e.oper}{e.val:0.1f}{p}</td><td>{e.tel}</td></tr>'
    t += '</tbody></table>'
    return t

def table_days_heat_waves( l, x ):
    cnt = len(l); x = cnt if x > cnt else x # check bereik
    h  = '<table class="popup">'
    h += '<thead><tr><th>datum</th><th>tx</th><th>tg</th><th>tn</th>' \
         '<th>sq</th><th>rh</th></tr></thead><tbody>'
    for e in l[:x]:
        h += f'<tr><td title="{d.Datum(e.YYYYMMDD).tekst()}">{e.datum}</td> ' \
             f'<td title="Maximum temperatuur">{e.TX:0.1f}°C</td>' \
             f'<td title="Gemiddelde temperatuur">{e.TG:0.1f}°C</td>' \
             f'<td title="Minimum temperatuur">{e.TN:0.1f}°C</td>' \
             f'<td title="Aantal uren zon">{e.SQ:0.1f}uur</td>' \
             f'<td title="Aantal mm regen">{e.RS:0.1f}mm</td></tr>'
    h += '</tbody></table>'
    return h


def css_day_values ():
    return '''
		* {
			margin: 0;
			padding: 0;
			border: 0;
		}
        body {
            color: gray;
            font: normal normal normal 0.9rem/1rem Calibri;
        }
        article {
            margin: 2rem;
			padding: 1rem;
            background: #eee;
            border: 1px solid gray;
            border-radius: 2rem;
        }
        header, footer {
            color: gray;
            font: normal normal normal 1.2rem/1rem Calibri;
			margin: 0.5rem 3rem;
        }
		header > h3 {
			letter-spacing: 0.1rem;
		}
        #container {
			margin: 0.5rem 1rem;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            grid-auto-rows: minmax(100px, auto);
            border: 1px solid gray;
            border-radius: 1rem;
            background-color: beige;
        }
        #container > .entity {
			margin: 1rem;
			padding:1rem;
            color: black;
            font: normal normal normal 0.9rem/1rem Calibri;
            border: 1px solid black;
            border-radius: 0.4rem;
            background-color: #eee;
			text-align: center;
			background-color: white;
        }
        #container > .entity > .title {
			margin: 0.2rem;
			letter-spacing: 0.1rem;
            font: normal normal normal 1rem/1rem Calibri;
        }
        #container > .entity > .data {
            font: bold normal normal 1.2rem/1rem Calibri;
        }
        #container > .entity > .data > .hour {
            font: normal normal normal 0.8rem/1rem Calibri;
        }
		footer {
            color: #777;
            font: normal normal normal 0.7rem/1rem Calibri;
		}
    '''

def style_winterstats_table ( ):
    return '''
        body { color: black; font: normal normal normal 0.9rem/1rem Calibri; }
        table { margin: 1rem auto; border-spacing: 4px; border-collapse: separate; }
        th { padding: 3px; text-transform: uppercase; }
        td { padding: 1px 4px; }
        thead tr:first-child th {
            color: #eeeeee; background: #777777;
            font-size: 1rem;
            text-transform: uppercase;
        }
		td:nth-child(1), td:nth-child(2) { font-style: italic }
		td:nth-child(n+3) { text-align: center; }
        tr:nth-child(odd) { background: #eeeeee; }
        tr:nth-child(even) { background: #dddddd; }
		tr:hover { background:beige; font-weight:bold }
        td:hover { font-weight:bold; cursor: pointer; color: green }
        .popup {
            position: absolute;
            display: inline-block;
            background: #777777;
            transition: opacity 500ms;
            visibility: hidden;
            opacity: 0;
            box-shadow: 0px 0px 2px 1px gray;
            border-spacing: 2px;
        }
        .popup th { padding: 1px 3px 0px 3px; }
        .popup td {
			color: black; font-style: normal; font-weight: normal;
            text-align: center; padding: 1px 2px 1px 2px;
        }
        td:hover .popup { visibility: visible; opacity: 1; }
        tfoot tr td {
            font-size: 0.8rem;
            color: #cccccc; background: none;
            text-transform: lowercase;
            font-style: italic;
        }
        tfoot tr td:hover { font-weight: normal; text-decoration: none; cursor: cursor; }
        sub { font-size: 0.5rem; }
    '''
