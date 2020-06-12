# -*- coding: utf-8 -*-
'''Library contains classes and functions for calculating summerstatistics'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9.3"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config as cfg, fn, fn_html as h, calc_stats as st, dates as d
import write as wr, ask, fn_read as r, knmi

class Stats:
    '''Class saves en stores summer statistics of a station in a given period'''
    def __init__(self, station, data ):
        self.station    = station
        self.data       = data
        self.date_start = data[ 0, daydata.YYYYMMDD] # First day data
        self.date_end   = data[-1, daydata.YYYYMMDD] # Last day data
        self.period     = f'{self.date_start}-{self.date_end}'

        self.tg_gem = stats.average(data,'TG') # Avergae TG
        self.tx_max = stats.max(data,'TX') # Highest TX
        self.tg_max = stats.max(data,'TG') # Highest TG
        self.tn_max = stats.max(data,'TN') # Highest TN
        self.sq_tot = stats.sum(data,'SQ') # Total sunshine hours
        self.rh_tot = stats.sum(data,'RH') # Total rain

        self.heat_ndx =  st.warmte_getal(etm_l)

        self.days_tx_gte_20 = stats.terms_days(data,'TX','≥',20) # Warm days
        self.days_tx_gte_25 = stats.terms_days(data,'TX','≥',25) # Summer days
        self.days_tx_gte_30 = stats.terms_days(data,'TX','≥',30) # Tropical days
        self.days_tx_gte_35 = stats.terms_days(data,'TX','≥',35) # Tropical days
        self.days_tg_gte_18 = stats.terms_days(data,'TG','≥',18) # Warmte getal dag
        self.days_tg_gte_20 = stats.terms_days(data,'TG','≥',20) # Warme gemiddelde
        self.days_tn_gte_20 = stats.terms_days(data,'TN','≥',20) # Tropical nights
        self.days_sq_gte_10 = stats.terms_days(data,'SQ','≥',10) # Sunny days > 10 hours
        self.days_rh_gte_10 = stats.terms_days(data,'RH','≥',10) # Rainy days > 10mm

        self.cnt_tx_gte_20 = self.days_tx_gte_20.size # Count Warm days
        self.cnt_tx_gte_25 = self.days_tx_gte_25.size # Count Summer days
        self.cnt_tx_gte_30 = self.days_tx_gte_30.size # Count Tropical days
        self.cnt_tx_gte_35 = self.days_tx_gte_35.size # Count Tropical days
        self.cnt_tg_gte_18 = self.days_tg_gte_18.size # Count Warmte getal dag
        self.cnt_tg_gte_20 = self.days_tg_gte_20.size # Count Warme gemiddelde
        self.cnt_tn_gte_20 = self.days_tn_gte_20.size # Count Tropical nights
        self.cnt_sq_gte_10 = self.days_sq_gte_10.size # Count Sunny days > 10 hours
        self.cnt_rh_gte_10 = self.days_sq_gte_10.size # Count Rainy days > 10mm

def sort( l, pm = '+' ):
    l = np.array( sorted(l, key=lambda stats: stats.heat_ndx) ) # Sort on heat index
    if pm == '+':
        l = l[::-1] # reverse

    return l

def calculate( stations, sd, ed, name=False, type='html' ):
    '''Function calculates summer statistics'''

    log.console(f'Preparing output...')
    max_rows = cfg.html_popup_table_max_rows

    # Make data list with station and summerstatistics
    summer = np.array( [] )
    for station in stations:
        log.console(f'Read and calculate statistics: {station.place}', True)
        ok, data = daydata.read( station )  # Get data stations
        if ok:
            period = stats.period( data, sd, ed ) # Get days of period
            summer = np.append( summer, Stats( station, period ) ) # Create summerstats object

    log.console(f'Preparing output: {type}', True)

    # Update name if there is none yet
    if not name:
        name = f'summer-statistics-{sd}-{ed}'

    # Make path if it is a html or txt file
    path = ''
    if type in ['html','txt']:
        if type == 'html':
            dir = config.dir_html_summerstats
        elif type == 'txt':
            dir = config.dir_txt_summerstats

        path = utils.path(dir, f'{name}.{type}')

    # Sort on TG
    summer = sort( summer, '+' )

    # Make output
    title, main, footer = '', '', ''


    fn.lnprintln(f'...Preparing output ({type})...')

    zomer_geg = sort_zomerstats_num(zomer_geg,'+') # Sorteer op tg

    # Maak content op basis van type uitvoer html of text
    # Maak titel
    if type in ['txt','cmd']:
        s = ' '
        content = f'PLAATS{s:15} PROVINCIE{s:7} PERIODE{s:11} TG      ∑WARMTE ' \
                  f'TX MAX  TG MAX  TN MAX  ∑TX≥20 ∑TX≥25 ∑TX≥30 ∑TX≥35 ' \
                  f'∑TG≥20 ∑TG≥18 ∑TN≥20 ∑ZON≥10 ∑ZON       ∑REGEN≥10 ∑REGEN  \n'

    if type == 'html':
        content  = f'''
        <table>
            <thead>
            <tr> <th colspan="18"> {title} </th> </tr>
            <tr>
                <th> plaats </th>
                <th> provincie </th>
                <th> periode </th>
                <th> tg </th>
                <th title="Warmte getal"> ∑warmte </th>
                <th title="Warmste dag"> tx max </th>
                <th title="Hoogste gemiddelde"> tg max </th>
                <th title="Hoogste minimum"> tn max </th>
                <th title="Aantal warme dagen"> ∑tx&ge;20 </th>
                <th title="Aantal zomers dagen"> ∑tx&ge;25 </th>
                <th title="Aantal tropische dagen"> ∑tx&ge;30 </th>
                <th title="Aantal tropische dagen"> ∑tx&ge;35 </th>
                <th title="Aantal tropennachten"> ∑tn&ge;20 </th>
                <th title="Warmte getal dagen"> tg&ge;18 </th>
                <th title="Totaal aantal uren zon"> ∑zon </th>
                <th title="Dagen met meer dan tien uur zon"> ∑zon&ge;10hour</th>
                <th title="Totaal aantal mm regen"> ∑regen </th>
                <th title="Dagen met meer dan tien mm regen"> ∑regen&ge;10mm</th>
            </tr>
            </thead>
            <tbody>
        '''

    # Walkthrough all cities
    for s in summer:
        log.console(f'For: {s.station.place}', True)
        warm = g.warmte_getal['getal']
        heat_ndx = fn.rm_s(fn.fix(warm, 'heat_ndx'))
        tg_gem   = fn.rm_s(fn.fix(g.tg_gem['gem'],'tg'))
        tx_max   = fn.rm_s(fn.fix(g.tx_max['max'],'tx'))
        tg_max   = fn.rm_s(fn.fix(g.tg_max['max'],'tg'))
        tn_max   = fn.rm_s(fn.fix(g.tn_max['max'],'tn'))
        rh_tot   = fn.rm_s(fn.fix(g.rh_tot['som'],'rh'))
        sq_tot   = fn.rm_s(fn.fix(g.sq_tot['som'],'sq'))
        tx_gte_20 = str(g.tx_gte_20['tel'])
        tx_gte_25 = str(g.tx_gte_25['tel'])
        tx_gte_35 = str(g.tx_gte_35['tel'])
        tx_gte_30 = str(g.tx_gte_30['tel'])
        tg_gte_18 = str(g.tg_gte_18['tel'])
        tn_gte_20 = str(g.tn_gte_20['tel'])
        tg_gte_20 = str(g.tg_gte_20['tel'])
        sq_gte_10 = str(g.sq_gte_10['tel'])
        rh_gte_10 = str(g.rh_gte_10['tel'])

        if type in ['txt','cmd']:
            content += f"{g.place:<21} {g.province:<16} {g.period:<18} " \
                       f"{tg_gem:<7} {heat_ndx:<7} {tx_max:<7} {tg_max:<7} " \
                       f"{tn_max:<7} {tx_gte_20:^6} {tx_gte_25:^6} {tx_gte_30:^6} " \
                       f"{tx_gte_35:^6} {tg_gte_20:^6} {tg_gte_18:^6} {tn_gte_20:^6} " \
                       f"{sq_gte_10:^7} {sq_tot:<10} {rh_gte_10:^9} {rh_tot:<11} \n"

        if type == 'html':
            date_txt = f"{d.Datum(g.date_start).tekst()} - {d.Datum(g.date_end).tekst()}"
            content += f'''
                <tr>
                    <td> {g.place} </td>
                    <td> {g.province} </td>
                    <td title="{date_txt}"> {g.period} </td>
                    <td> {tg_gem} </td>
                    <td> {heat_ndx} {h.table_heat_ndx(g.warmte_getal['lijst'], max_rows)} </td>
                    <td> {tx_max} {h.table_extremes(g.tx_max['lijst'][-1:], max_rows)} </td>
                    <td> {tg_max} {h.table_extremes(g.tg_max['lijst'][-1:], max_rows)} </td>
                    <td> {tn_max} {h.table_extremes(g.tn_max['lijst'][-1:], max_rows)} </td>
                    <td> {tx_gte_20} {h.table_count(g.tx_gte_20['lijst'], max_rows)} </td>
                    <td> {tx_gte_25} {h.table_count(g.tx_gte_25['lijst'], max_rows)} </td>
                    <td> {tx_gte_30} {h.table_count(g.tx_gte_30['lijst'], max_rows)} </td>
                    <td> {tx_gte_35} {h.table_count(g.tx_gte_35['lijst'], max_rows)} </td>
                    <td> {tg_gte_20} {h.table_count(g.tg_gte_20['lijst'], max_rows)} </td>
                    <td> {tg_gte_18} {h.table_count(g.tg_gte_18['lijst'], max_rows)} </td>
                    <td> {sq_tot} </td>
                    <td> {sq_gte_10} {h.table_count(g.sq_gte_10['lijst'], max_rows)} </td>
                    <td> {rh_tot} </td>
                    <td> {rh_gte_10} {h.table_count(g.rh_gte_10['lijst'], max_rows)} </td>
                </tr>
                '''

    if type in ['txt','cmd']:
        content += bronvermelding

    if type == 'html':
        content += f'''
            </tbody>
            <tfoot> <tr> <td colspan="18"> {bronvermelding} </td> </tr> </tfoot>
        </table>'''

        css = r.get_string_css_from_file( 'default-table-statistics.css' ) # Get css from file
        content = h.pagina(title, css, content) # Make html page
        content = fn.clean_s(content) # Remove unnecessary whitespace

    if type == 'cmd':
        fn.lnprintln(cfg.line + cfg.ln + content + cfg.ln + cfg.line)

    if type in ['html','txt']:
        file_name = fn.mk_path(path, name) # Make file name
        wr.write_to_file(file_name, content) # Schrijf naar bestand

    return file_name
