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
import sources.view.log as log
import sources.view.html as vhtml
import sources.view.fix as fix
import sources.view.icon as icon
import sources.control.fio as fio
import sources.model.utils as utils
import sources.model.stats as stats
import sources.model.daydata as daydata

class Stats:
    '''Class saves en stores summer statistics of a station in a given period'''
    def __init__(self, station, data ):
        self.station = station
        self.data    = data
        self.ymd     = data[:,daydata.YYYYMMDD]
        self.date_s  = utils.f_to_s(self.ymd[ 0])  # First day data
        self.date_e  = utils.f_to_s(self.ymd[-1])  # Last day data
        self.period  = f'{self.date_s}-{self.date_e}'

        self.tg_gem = stats.average(data,'TG') # Avergae TG
        self.tx_max_sort = stats.sort( data, 'TX')
        self.tx_max      = self.tx_max_sort[0, daydata.ndx_ent('TX')] # Get max is 1st in list
        self.tg_max_sort = stats.sort( data, 'TG')
        self.tg_max      = self.tg_max_sort[0, daydata.ndx_ent('TG')]
        self.tn_max_sort = stats.sort( data, 'TN')
        self.tn_max      = self.tn_max_sort[0, daydata.ndx_ent('TN')]

        self.sq_tot = stats.sum(data,'SQ') # Total sunshine hours
        self.sq_sort = stats.sort(data, 'SQ')
        self.rh_tot = stats.sum(data,'RH') # Total rain
        self.rh_sort = stats.sort( data, 'RH')

        self.days_tx_gte_20 = stats.terms_days(data,'TX','≥',20) # Warm days
        self.days_tx_gte_25 = stats.terms_days(data,'TX','≥',25) # Summer days
        self.days_tx_gte_30 = stats.terms_days(data,'TX','≥',30) # Tropical days
        self.days_tx_gte_35 = stats.terms_days(data,'TX','≥',35) # Tropical days
        self.days_tx_gte_40 = stats.terms_days(data,'TX','≥',40) # Extreme Tropical days
        self.days_tg_gte_18 = stats.terms_days(data,'TG','≥',18) # Warmte getal dag
        self.days_tg_gte_20 = stats.terms_days(data,'TG','≥',20) # Warme gemiddelde
        self.days_tn_gte_20 = stats.terms_days(data,'TN','≥',20) # Tropical nights
        self.days_sq_gte_10 = stats.terms_days(data,'SQ','≥',10) # Sunny days > 10 hours
        self.days_rh_gte_10 = stats.terms_days(data,'RH','≥',10) # Rainy days > 10mm

        self.heat_ndx = stats.heat_ndx(data)
        self.days_heat_ndx = self.days_tg_gte_18

def sort( l, pm = '+' ):
    l = np.array( sorted(np.array(l), key=lambda stats: stats.heat_ndx) ).tolist() # Sort on heat index
    if pm == '+':
        l = l[::-1] # reverse

    return l

def calculate( stations, period, name=False, type='html' ):
    '''Function calculates summer statistics'''
    colspan = 20

    # Make data list with station and summerstatistics
    summer = list()
    for station in stations:
        log.console(f'Calculate statistics: {station.place}', True)
        ok, data = daydata.read( station )  # Get data stations
        if ok:
            days = daydata.period( data, period ) # Get days of period
            if days.size != 0: # Skip station
                summer.append( Stats( station, days ) ) # Create summerstats object

    log.console(f'\nPreparing output: {type}', True)

    # Update name if there is none yet
    if not name:
        name = utils.mk_name('summerstatistics', period)

    # Make path if it is a html or txt file
    path = ''
    if type == 'html':
        dir = config.dir_html_summerstats
    elif type == 'txt':
        dir = config.dir_txt_summerstats
    path = utils.mk_path(dir, f'{name}.{type}')

    # Sort on TG
    summer = sort( summer, '+' )

    # Make output
    title, main, footer = '', '', ''

    # Maak content op basis van type uitvoer html of text
    # Maak titel
    table_title = 'Summer statistics '
    if type in ['txt','cmd']:
        s = ' '
        title += f'{table_title} {period}\n'
        title += f'PLAATS{s:15} '
        title += f'PROVINCIE{s:7} '
        title += f'PERIODE{s:11} '
        title += f'TG{s:5} '
        title += f'WARMTE '
        title += 'TX MAX  '
        title += 'TG MAX  '
        title += 'TN MAX  '
        title += 'TX≥20 '
        title += 'TX≥25 '
        title += 'TX≥30 '
        title += 'TX≥35 '
        title += 'TX≥40 '
        title += 'TG≥20 '
        title += 'TG≥18 '
        title += 'TN≥20 '
        title += 'ZON≥10 '
        title += 'ZON{s:6} '
        title += 'REGEN≥10 '
        title += 'REGEN\n'

    if type == 'html':
        title += f'''
            <table id="stats">
            <thead>
                <tr>
                    <th colspan="{colspan}">
                        {icon.weather_all()}
                        {table_title}
                        {icon.wave_square()}
                        {period}
                        {icon.cal_period()}
                    </th>
                </tr>
                <tr>
                    <th title="copyright data_notification"> </th>
                    <th> place {icon.home(size='fa-sm')}</th>
                    <th> province {icon.flag(size='fa-sm')}</th>
                    <th> period {icon.cal_period(size='fa-sm')}</th>
                    <th title="Average temperature"> tg {icon.temp_half(size='fa-sm')}</th>
                    <th title="Warmte getal"> heat {icon.fire(size='fa-sm')}</th>
                    <th title="Warmste dag"> tx {icon.arrow_up(size='fa-sm')}</th>
                    <th title="Hoogste gemiddelde"> tg {icon.arrow_up(size='fa-sm')}</th>
                    <th title="Hoogste minimum"> tn {icon.arrow_up(size='fa-sm')}</th>
                    <th title="Aantal warme dagen"> tx{icon.gte(size='fa-xs')}20 </th>
                    <th title="Aantal zomers dagen"> tx{icon.gte(size='fa-xs')}25 </th>
                    <th title="Aantal tropische dagen"> tx{icon.gte(size='fa-xs')}30 </th>
                    <th title="Aantal tropische dagen"> tx{icon.gte(size='fa-xs')}35 </th>
                    <th title="Aantal tropische dagen"> tx{icon.gte(size='fa-xs')}40 </th>
                    <th title="Aantal tropennachten"> tn{icon.gte(size='fa-xs')}20 </th>
                    <th title="Warmte getal dagen"> tg{icon.gte(size='fa-xs')}18 </th>
                    <th title="Totaal aantal uren zon"> {icon.sun(size='fa-sm')} </th>
                    <th title="Dagen met meer dan tien uur zon"> {icon.sun(size='fa-xs')}{icon.gte(size='fa-xs')}10h</th>
                    <th title="Totaal aantal mm regen">{icon.shower_heavy(size='fa-sm')}</th>
                    <th title="Dagen met meer dan tien mm regen"> {icon.shower_heavy(size='fa-xs')}{icon.gte(size='fa-xs')}10mm</th>
                </tr>
            </thead>
            <tbody>
            '''

    # Walkthrough all cities
    for s in summer:
        log.console(f'Make {type} output for: {s.station.place}', True)
        heat   = fix.ent( s.heat_ndx, 'heat_ndx' )
        tg_gem = fix.ent( s.tg_gem, 'tg' )
        tx_max = fix.ent( s.tx_max, 'tx' )
        tg_max = fix.ent( s.tg_max, 'tg' )
        tn_max = fix.ent( s.tn_max, 'tn' )
        rh_tot = fix.ent( s.rh_tot, 'rh' )
        sq_tot = fix.ent( s.sq_tot, 'sq' )

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
            period_txt = f'{utils.ymd_to_txt(s.date_s)} - {utils.ymd_to_txt(s.date_e)}'
            main += f'''
                    <td title="{s.station.data_notification.lower()}">
                            {icon.copy_light(size='fa-xs')}
                    </td>
                    <td> <span class="val"> {s.station.place} </span> </td>
                    <td> <span class="val"> {s.station.province} </span> </td>
                    <td title="{period_txt}"> <span class="val"> {s.period} </span> </td>
                    <td> <span class="val"> {tg_gem} </span> </td>
                    <td>
                        <span class="val"> {heat} </span>
                        {vhtml.table_days(s.days_heat_ndx, 'TG')}
                    </td>
                    <td>
                        <span class="val"> {tx_max} </span>
                        {vhtml.table_days( s.tx_max_sort, 'TX', 'TXH' )}
                    </td>
                    <td>
                        <span class="val"> {tg_max} </span>
                        {vhtml.table_days( s.tg_max_sort, 'TG' )}
                    </td>
                    <td>
                        <span class="val"> {tn_max}  </span>
                        {vhtml.table_days( s.tn_max_sort, 'TN', 'TNH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_20, axis=0)} </span>
                        {vhtml.table_days_count(s.days_tx_gte_20, 'TX', 'TXH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_25, axis=0)} </span>
                        {vhtml.table_days_count(s.days_tx_gte_25, 'TX', 'TXH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_30, axis=0)} </span>
                        {vhtml.table_days_count(s.days_tx_gte_30, 'TX', 'TXH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_35, axis=0)} </span>
                        {vhtml.table_days_count(s.days_tx_gte_35, 'TX', 'TXH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_40, axis=0)} </span>
                        {vhtml.table_days_count(s.days_tx_gte_40, 'TX', 'TXH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tn_gte_20, axis=0)} </span>
                        {vhtml.table_days_count(s.days_tn_gte_20, 'TG' )}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tg_gte_18, axis=0)} </span>
                        {vhtml.table_days_count(s.days_tg_gte_18, 'TG' )}
                    </td>
                    <td>
                        <span class="val"> {sq_tot} </span>
                        {vhtml.table_days( s.sq_sort, 'SQ' )}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_sq_gte_10, axis=0)} </span>
                        {vhtml.table_days_count(s.days_sq_gte_10, 'SQ', '' )}
                    </td>
                    <td>
                        <span class="val"> {rh_tot} </span>
                        {vhtml.table_days( s.rh_sort, 'RH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_rh_gte_10, axis=0)} </span>
                        {vhtml.table_days_count(s.days_rh_gte_10, 'RH', '' )}
                    </td>
                </tr>
                '''

    if type in ['txt','cmd']:
        footer += stations[0].data_notification

    if type == 'html':
        footer += f'''
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="{colspan}">
                        {utils.now_created_notification()}
                    </td>
                </tr>
            </tfoot>
            </table>
        '''

    log.console('\nWrite/print results... ', True)

    # Write to file or console
    output = f'{title}\n{main}\n{footer}'
    if type == 'cmd':
        log.console( output, True )

    elif type == 'html':
        page           =  vhtml.Template()
        page.title     =  table_title
        page.main      =  output
        page.strip     =  True
        page.set_path(dir, f'{name}.html')
        # Styling
        page.add_css_file(dir='./../static/css/', name='table-statistics.css')
        page.add_css_file(dir='./../static/css/', name='default.css')
        page.add_css_file(dir='./css/', name='summerstats.css')
        # Scripts
        page.add_script_file(dir='./js/', name='summerstats.js')
        page.add_script_file(dir='./../static/js/', name='sort-col.js')
        page.add_script_file(dir='./../static/js/', name='default.js')

        page.save()

    elif type == 'txt':
        fio.save(path, output) # Schrijf naar bestand

    return path
