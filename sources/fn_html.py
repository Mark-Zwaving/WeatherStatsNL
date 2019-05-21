import config as c, datetime, datum as d

def pagina(title, style, content):
    return f'''<!DOCTYPE html>
    <html>
        <head>
            <title> {title} </title>
            <style> {style} </style>
        </head>
        <body>
        {content}
        <!-- Created by weerstats.py at {datetime.datetime.now()} //-->
        </body>
    </html>
    '''

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
