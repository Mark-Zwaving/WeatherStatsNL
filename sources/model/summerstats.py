# -*- coding: utf-8 -*-
'''Library contains classes and functions for calculating summerstatistics'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9.6"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config
import numpy as np
import view.log as log
import view.html as html
import view.fix as fix
import control.io as io
import model.utils as utils
import model.stats as stats
import model.daydata as daydata

class Stats:
    '''Class saves en stores summer statistics of a station in a given period'''
    def __init__(self, station, data ):
        self.station    = station
        self.data       = data
        self.ymd        = data[:,daydata.YYYYMMDD]
        self.date_start = utils.f_to_s( self.ymd[ 0] )  # First day data
        self.date_end   = utils.f_to_s( self.ymd[-1] )  # Last day data
        self.period     = f'{self.date_start}-{self.date_end}'

        self.tg_gem = stats.average(data,'TG') # Avergae TG
        self.tx_max = stats.max(data,'TX') # Highest TX
        self.tg_max = stats.max(data,'TG') # Highest TG
        self.tn_max = stats.max(data,'TN') # Highest TN
        self.sq_tot = stats.sum(data,'SQ') # Total sunshine hours
        self.rh_tot = stats.sum(data,'RH') # Total rain
        self.heat_ndx = stats.heat_ndx(data)

        self.days_tx_gte_20 = stats.terms_days(data,'TX','≥',20) # Warm days
        self.days_tx_gte_25 = stats.terms_days(data,'TX','≥',25) # Summer days
        self.days_tx_gte_30 = stats.terms_days(data,'TX','≥',30) # Tropical days
        self.days_tx_gte_35 = stats.terms_days(data,'TX','≥',35) # Tropical days
        self.days_tg_gte_18 = stats.terms_days(data,'TG','≥',18) # Warmte getal dag
        self.days_tg_gte_20 = stats.terms_days(data,'TG','≥',20) # Warme gemiddelde
        self.days_tn_gte_20 = stats.terms_days(data,'TN','≥',20) # Tropical nights
        self.days_sq_gte_10 = stats.terms_days(data,'SQ','≥',10) # Sunny days > 10 hours
        self.days_rh_gte_10 = stats.terms_days(data,'RH','≥',10) # Rainy days > 10mm

def sort( l, pm = '+' ):
    l = np.array( sorted(l, key=lambda stats: stats.heat_ndx) ) # Sort on heat index
    if pm == '+':
        l = l[::-1] # reverse

    return l



def calculate( stations, period, name=False, type='html' ):
    '''Function calculates summer statistics'''
    colspan = 18
    popup_rows = config.max_rows_table_popup

    # Make data list with station and summerstatistics
    summer = np.array( [] )
    for station in stations:
        log.console(f'Read and calculate statistics: {station.place}', True)
        ok, data = daydata.read( station )  # Get data stations
        if ok:
            days = daydata.period( data, period ) # Get days of period
            if days.size != 0: # Skip station
                summer = np.append( summer, Stats( station, days ) ) # Create summerstats object

    log.console(f'Preparing output: {type}', True)

    # Update name if there is none yet
    if not name:
        name = utils.mk_name('summerstatistics', period)

    # Make path if it is a html or txt file
    path = ''
    if type == 'html':
        dir = config.dir_html_winterstats
    elif type ==  'txt':
        dir = config.dir_txt_winterstats
    path = utils.mk_path(dir, f'{name}.{type}')

    log.console(f'Preparing summerstats, output type is {type}', True)

    # Sort on TG
    summer = sort( summer, '+' )

    # Make output
    title, main, footer = '', '', ''

    # Maak content op basis van type uitvoer html of text
    # Maak titel
    table_title = name.replace('-', ' ')
    if type in ['txt','cmd']:
        s = ' '
        title += f'{table_title} \n'
        title += f'PLAATS{s:15} '
        title += f'PROVINCIE{s:7} '
        title += f'PERIODE{s:11} '
        title += f'TG{s:5} '
        title += f'∑WARMTE '
        title += 'TX MAX  '
        title += 'TG MAX  '
        title += 'TN MAX  '
        title += 'TX≥20 '
        title += 'TX≥25 '
        title += 'TX≥30 '
        title += 'TX≥35 '
        title += 'TG≥20 '
        title += 'TG≥18 '
        title += 'TN≥20 '
        title += 'ZON≥10 '
        title += 'ZON{s:6} '
        title += 'REGEN≥10 '
        title += 'REGEN\n'

    if type == 'html':
        title += f'''
            <table>
            <thead>
                <tr>
                    <th colspan="{colspan}"> {table_title} </th>
                </tr>
                <tr>
                    <th> plaats </th>
                    <th> provincie </th>
                    <th> periode </th>
                    <th> tg </th>
                    <th title="Warmte getal"> heat ndx </th>
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
        heat_ndx = fix.ent( s.heat_ndx, 'heat_ndx' )
        tg_gem   = fix.ent( s.tg_gem, 'tg' )
        tx_max   = fix.ent( s.tx_max, 'tx' )
        tg_max   = fix.ent( s.tg_max, 'tg' )
        tn_max   = fix.ent( s.tn_max, 'tn' )
        rh_tot   = fix.ent( s.rh_tot, 'rh' )
        sq_tot   = fix.ent( s.sq_tot, 'sq' )

        if type in ['txt','cmd']:
            main += f'{s.station.place:<21} '
            main += f'{s.station.province:<16} '
            main += f'{s.station.period:<18} '
            main += f'{tg_gem:<7} '
            main += f'{heat_ndx:<7} '
            main += f'{tx_max:<7} '
            main += f'{tg_max:<7} '
            main += f'{tn_max:<7} '
            main += f'{tx_gte_20:^6} '
            main += f'{tx_gte_25:^6} '
            main += f'{tx_gte_30:^6} '
            main += f'{tx_gte_35:^6} '
            main += f'{tg_gte_20:^6} '
            main += f'{tg_gte_18:^6} '
            main += f'{tn_gte_20:^6} '
            main += f'{sq_gte_10:^7} '
            main += f'{sq_tot:<10} '
            main += f'{rh_gte_10:^9} '
            main += f'{rh_tot:<11} '

        if type == 'html':
            period_txt = f'{utils.ymd_to_txt(s.date_start)} - {utils.ymd_to_txt(s.date_end)}'
            main += f'''
                <tr>
                    <td> <span class="val"> {s.station.place} </span> </td>
                    <td> <span class="val"> {s.station.province} </span> </td>
                    <td title="{period_txt}"> <span class="val"> {s.period} </span> </td>
                    <td> <span class="val"> {tg_gem} </span> </td>
                    <td> <span class="val"> {heat_ndx} </span> </td>
                    <td> <span class="val"> {tx_max} </span> </td>
                    <td> <span class="val"> {tg_max} </span> </td>
                    <td> <span class="val"> {tn_max}  </span> </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_20)} </span>
                        {html.table_count(s.days_tx_gte_20, 'TX', 'TXH', popup_rows)}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_25)} </span>
                        {html.table_count(s.days_tx_gte_25, 'TX', 'TXH', popup_rows)}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_30)} </span>
                        {html.table_count(s.days_tx_gte_30, 'TX', 'TXH', popup_rows)}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_35)} </span>
                        {html.table_count(s.days_tx_gte_35, 'TX', 'TXH', popup_rows)}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tg_gte_20)} </span>
                        {html.table_count(s.days_tg_gte_20, 'TG', '', popup_rows)}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tg_gte_18)} </span>
                        {html.table_count(s.days_tg_gte_18, 'TG', '', popup_rows)}
                    </td>
                    <td>
                        <span class="val"> {sq_tot} </span>
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_sq_gte_10)} </span>
                        {html.table_count(s.days_sq_gte_10, 'SQ', '', popup_rows)}
                    </td>
                    <td>
                        <span class="val"> {rh_tot} </span>
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_rh_gte_10)} </span>
                        {html.table_count(s.days_rh_gte_10, 'RH', '', popup_rows)}
                    </td>
                </tr>
                '''


    if type in ['txt','cmd']:
        footer += config.knmi_dayvalues_notification

    if type == 'html':
        footer += f'''
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="{colspan}">
                        {config.knmi_dayvalues_notification}
                    </td>
                </tr>
            </tfoot>
            </table>
        '''

    # Write to file or console
    output = f'{title}\n{main}\n{footer}'
    if type == 'cmd':
        log.console( output, True )

    elif type == 'html':
        page           =  html.Template()
        page.title     =  table_title
        page.main      =  output
        page.set_path(dir, f'{name}.html')
        page.add_css_file(name='table-statistics.css')
        page.add_css_file(name='default.css')
        page.add_css_file(dir='./css/', name='summerstats.css')
        page.add_script_file(dir='./js/', name='sort-col.js')
        page.add_script_file(name='default.js')
        page.add_script_file(dir='./js/', name='summerstats.js')

        page.save()

    elif type == 'txt':
        io.save(path, output) # Schrijf naar bestand

    return path