# -*- coding: utf-8 -*-
'''Library contains classes and functions for calculating summerstatistics'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.6"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config
import numpy as np
import control.io as io
import model.utils as utils
import model.stats as stats
import model.daydata as daydata
import view.fix as fix
import view.log as log
import view.html as html

class Stats:
    '''Class saves en stores summer statistics of a station in a given period'''
    def __init__(self, station, data ):
        self.station  = station
        self.data     = data
        self.ymd      = data[:,daydata.YYYYMMDD]
        self.p_start  = utils.f_to_s( self.ymd[ 0] )  # First day data
        self.p_end    = utils.f_to_s( self.ymd[-1] )  # Last day data
        self.period   = f'{self.p_start}-{self.p_end}'
        self.tg_ave   = stats.average(data,'TG')
        self.tx_max   = stats.max(data,'TX')
        self.tg_max   = stats.max(data,'TG')
        self.tn_max   = stats.max(data,'TN')
        self.tx_min   = stats.min(data,'TX')
        self.tg_min   = stats.min(data,'TG')
        self.tn_min   = stats.min(data,'TN')
        self.sq_sum   = stats.sum(data,'SQ') # Total sunshine hours
        self.rh_sum   = stats.sum(data,'RH') # Total rain
        self.heat_ndx = stats.heat_ndx(data)
        self.hellmann = stats.hellmann(data)
        self.ijnsen   = stats.ijnsen(data)
        self.frost_sum = stats.frost_sum(data)

        # Days lists
        self.days_tx_lt_0   = stats.terms_days(data,'TX','<',  0)
        self.days_tg_lt_0   = stats.terms_days(data,'TG','<',  0)
        self.days_tn_lt_0   = stats.terms_days(data,'TN','<',  0)
        self.days_tn_lt__5  = stats.terms_days(data,'TN','<', -5)
        self.days_tn_lt__10 = stats.terms_days(data,'TN','<',-10)
        self.days_tn_lt__15 = stats.terms_days(data,'TN','<',-15)
        self.days_tn_lt__20 = stats.terms_days(data,'TN','<',-20)
        self.days_tx_gte_20 = stats.terms_days(data,'TX','≥',20) # Warm days
        self.days_tx_gte_25 = stats.terms_days(data,'TX','≥',25) # Summer days
        self.days_tx_gte_30 = stats.terms_days(data,'TX','≥',30) # Tropical days
        self.days_tx_gte_35 = stats.terms_days(data,'TX','≥',35) # Tropical days
        self.days_tx_gte_40 = stats.terms_days(data,'TX','≥',40) # Tropical days
        self.days_tg_gte_18 = stats.terms_days(data,'TG','≥',18) # Warmte getal dag
        self.days_tg_gte_20 = stats.terms_days(data,'TG','≥',20) # Warme gemiddelde
        self.days_tn_gte_20 = stats.terms_days(data,'TN','≥',20) # Tropical nights
        self.days_sq_gte_10 = stats.terms_days(data,'SQ','≥',10) # Sunny days > 10 hours
        self.days_rh_gte_10 = stats.terms_days(data,'RH','≥',10) # Rainy days > 10mm

def sort( l, pm = '+' ):
    l = np.array( sorted(l, key=lambda stats: stats.tg_ave) ) # Sort on average
    if pm == '+':
        l = l[::-1] # reverse

    return l

def calculate( stations, period, name=False, type='html' ):
    '''Function calculates all statistics'''
    colspan = 32
    popup_rows = config.max_rows_table_popup

    # Make data list with station and summerstatistics
    allstats = np.array( [] )
    for station in stations:
        log.console(f'Calculate statistics: {station.place}', True)
        ok, data = daydata.read( station )  # Get data stations
        if ok:
            days = daydata.period( data, period ) # Get days of period
            if days.size != 0: # Skip station
                allstats = np.append( allstats, Stats( station, days ) ) # Create summerstats object

    log.console(f'\nPreparing output: {type}', True)

    # Update name if there is none yet
    if not name:
        name = utils.mk_name('all-statistics', period)

    # Make path if it is a html or txt file
    path = ''
    if   type == 'html': dir = config.dir_html_allstats
    elif type ==  'txt': dir = config.dir_txt_allstats
    path = utils.mk_path(dir, f'{name}.{type}')

    # Sort on TG
    allstats = sort( allstats, '+' )

    # Make output
    title, main, footer = '', '', ''

    # Maak content op basis van type uitvoer html of text
    # Maak titel
    table_title = 'All statistics '
    if type in ['txt','cmd']:
        s = ' '
        title += f'{table_title} {period}\n'
        title += f'PLACE{s:15} '
        title += f'PROVINCE{s:7} '
        title += f'PERIOD{s:11} '
        title += f'TG{s:5} '
        title += f'WARMTH '
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
                        <i class="fas fa-cloud-sun-rain"></i>
                        {table_title}
                        <i class="fas fa-calculator"></i>
                        {period}
                        <i class="far fa-calendar-alt"></i>
                    </th>
                </tr>
                <tr>
                    <th> place <i class="fas fa-home fa-sm"></i></th>
                    <th> province <i class="fab fa-font-awesome-flag fa-sm"></i> </th>
                    <th> period  <i class="far fa-calendar-alt fa-sm"></i></th>
                    <th title="Average temperature"> tg <i class="fas fa-thermometer-half fa-sm"></i> </th>
                    <th title="Highest maximum temperature"> tx <i class="fas fa-arrow-up fa-sm"></i> </th>
                    <th title="Highest average temperature"> tg <i class="fas fa-arrow-up fa-sm"></i> </th>
                    <th title="Highest minimum temperature"> tn <i class="fas fa-arrow-up fa-sm"></i> </th>
                    <th title="Lowest maximum temperature"> tx <i class="fas fa-arrow-down fa-sm"></i> </th>
                    <th title="Lowest average temperature "> tg <i class="fas fa-arrow-down fa-sm"></i> </th>
                    <th title="Lowest minumum temperature"> tn <i class="fas fa-arrow-down fa-sm"></i> </th>
                    <th title="Total hours of sunshine"> <i class="fas fa-sun fa-sm"></i> </th>
                    <th title="Total rain mm"> <i class="fas fa-cloud-showers-heavy fa-sm"></i> </th>

                    <th title="Heat index tg greater than 18 degrees celsius"> heat <i class="fas fa-fire-alt fa-sm"></i> </th>
                    <th title="Warm days"> tx<i class="fas fa-greater-than-equal fa-xs"></i>20 </th>
                    <th title="Summer days"> tx<i class="fas fa-greater-than-equal fa-xs"></i>25 </th>
                    <th title="Tropical days"> tx<i class="fas fa-greater-than-equal fa-xs"></i>30 </th>
                    <th title="High tropical days"> tx<i class="fas fa-greater-than-equal fa-xs"></i>35 </th>
                    <th title="High tropical days"> tx<i class="fas fa-greater-than-equal fa-xs"></i>40 </th>
                    <th title="Warm days on average"> tg<i class="fas fa-greater-than-equal fa-xs"></i>18 </th>
                    <th title="Tropical nights"> tn<i class="fas fa-greater-than-equal fa-xs"></i>20 </th>
                    <th title="Days with more than 10hour of sun"> <i class="fas fa-sun fa-xs"></i><i class="fas fa-greater-than-equal fa-xs"></i>10h</th>
                    <th title="Days with more than 10 mm of rain"> <i class="fas fa-cloud-showers-heavy fa-xs"></i><i class="fas fa-greater-than-equal fa-xs"></i>10mm</th>

                    <th title="Hellmann"> hmann <i class="fas fa-icicles fa-sm"></i></th>
                    <th title="IJnsen"> ijnsen <i class="fas fa-icicles fa-sm"></i></th>
                    <th title="Frost sum"> fsum <i class="fas fa-icicles fa-sm"></i></th>
                    <th title="Days with maximum temperature below 0 degrees celsius"> tx<i class="fas fa-less-than fa-xs"></i>0 </th>
                    <th title="Days with average temperature below 0 degrees celsius"> tg<i class="fas fa-less-than fa-xs"></i>0 </th>
                    <th title="Days with minimum temperature below 0 degrees celsius"> tn<i class="fas fa-less-than fa-xs"></i>0 </th>
                    <th title="Days with minimum temperature lower than -5 degrees celsius"> tn<i class="fas fa-less-than fa-xs"></i>&minus;5 </th>
                    <th title="Days with minimum temperature lower than -10 degrees celsius"> tn<i class="fas fa-less-than fa-xs"></i>&minus;10 </th>
                    <th title="Days with minimum temperature lower than -15 degrees celsius"> tn<i class="fas fa-less-than fa-xs"></i>&minus;15 </th>
                    <th title="Days with minimum temperature lower than -20 degrees celsius"> tn<i class="fas fa-less-than fa-xs"></i>&minus;20 </th>
                </tr>
            </thead>
            <tbody>
            '''

    # Walkthrough all cities
    for s in allstats:
        log.console(f'Make {type} output for: {s.station.place}', True)
        heat_ndx = fix.ent( s.heat_ndx, 'heat_ndx' )
        tg_ave   = fix.ent( s.tg_ave, 'tg' )
        tx_max   = fix.ent( s.tx_max, 'tx' )
        tg_max   = fix.ent( s.tg_max, 'tg' )
        tn_max   = fix.ent( s.tn_max, 'tn' )
        tx_min   = fix.ent( s.tx_min, 'tx' )
        tg_min   = fix.ent( s.tg_min, 'tg' )
        tn_min   = fix.ent( s.tn_min, 'tn' )
        hellmann = fix.ent( s.hellmann, 'hellmann' )
        ijnsen   = fix.ent( s.ijnsen, 'ijnsen' )
        f_sum    = fix.ent( s.frost_sum, 'frost_sum' )
        sq_sum   = fix.ent( s.sq_sum, 'SQ' )
        rh_sum   = fix.ent( s.rh_sum, 'RH' )

        if type in ['txt','cmd']:
            main += f'{s.station.place:<21} '
            main += f'{s.station.province:<16} '
            main += f'{s.station.period:<18} '
            main += f'{tg_ave:<7} '
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
            period_txt = f'{utils.ymd_to_txt(s.p_start)} - {utils.ymd_to_txt(s.p_end)}'
            main += f'''
                <tr>
                    <td> <span class="val"> {s.station.place} </span> </td>
                    <td> <span class="val"> {s.station.province} </span> </td>
                    <td title="{period_txt}"> <span class="val"> {s.period} </span> </td>
                    <td> <span class="val"> {tg_ave} </span> </td>
                    <td> <span class="val"> {tx_max} </span> </td>
                    <td> <span class="val"> {tg_max} </span> </td>
                    <td> <span class="val"> {tn_max} </span> </td>
                    <td> <span class="val"> {tx_min} </span> </td>
                    <td> <span class="val"> {tg_min} </span> </td>
                    <td> <span class="val"> {tn_min} </span> </td>
                    <td> <span class="val"> {sq_sum} </span> </td>
                    <td> <span class="val"> {rh_sum} </span> </td>
                    <td> <span class="val"> {heat_ndx} </span> </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_20, axis=0)} </span>
                        {html.table_count(s.days_tx_gte_20, 'TX', 'TXH', popup_rows)}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_25, axis=0)} </span>
                        {html.table_count(s.days_tx_gte_25, 'TX', 'TXH', popup_rows)}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_30, axis=0)} </span>
                        {html.table_count(s.days_tx_gte_30, 'TX', 'TXH', popup_rows)}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_35, axis=0)} </span>
                        {html.table_count(s.days_tx_gte_35, 'TX', 'TXH', popup_rows)}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_40, axis=0)} </span>
                        {html.table_count(s.days_tx_gte_40, 'TX', 'TXH', popup_rows)}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tg_gte_18, axis=0)} </span>
                        {html.table_count(s.days_tg_gte_18, 'TG', '', popup_rows)}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tn_gte_20, axis=0)} </span>
                        {html.table_count(s.days_tn_gte_20, 'TG', '', popup_rows)}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_sq_gte_10, axis=0)} </span>
                        {html.table_count(s.days_sq_gte_10, 'SQ', '', popup_rows)}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_rh_gte_10, axis=0)} </span>
                        {html.table_count(s.days_rh_gte_10, 'RH', '', popup_rows)}
                    </td>
                    <td> <span class="val"> {hellmann} </span> </td>
                    <td> <span class="val"> {ijnsen} </span> </td>
                    <td> <span class="val"> {f_sum} </span> </td>
                    <td>
                        <span class="val"> {np.size( s.days_tx_lt_0, axis=0 )} </span>
                        {html.table_count( s.days_tx_lt_0, 'TX', 'TXH', popup_rows )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tg_lt_0, axis=0 )} </span>
                        {html.table_count( s.days_tg_lt_0, 'TG', '', popup_rows )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tn_lt_0, axis=0 )} </span>
                        {html.table_count( s.days_tn_lt_0, 'TN', 'TNH', popup_rows )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tn_lt__5, axis=0 )} </span>
                        {html.table_count( s.days_tn_lt__5, 'TN', 'TNH', popup_rows )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tn_lt__10, axis=0 )} </span>
                        {html.table_count( s.days_tn_lt__10, 'TN', 'TNH', popup_rows )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tn_lt__15, axis=0 )} </span>
                        {html.table_count( s.days_tn_lt__15, 'TN', 'TNH', popup_rows )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tn_lt__20, axis=0 )} </span>
                        {html.table_count( s.days_tn_lt__20, 'TN', 'TNH', popup_rows )}
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
        page.strip     =  True
        page.set_path(dir, f'{name}.html')
        # Styling
        page.add_css_file(dir='./../static/css/', name='table-statistics.css')
        page.add_css_file(dir='./../static/css/', name='default.css')
        page.add_css_file(dir='./css/', name='allstats.css')
        # Scripting
        page.add_script_file(dir='./js/', name='allstats.js')
        page.add_script_file(dir='./../static/js/', name='sort-col.js')
        page.add_script_file(dir='./../static/js/', name='default.js')

        page.save()

    elif type == 'txt':
        io.save(path, output) # Schrijf naar bestand

    return path
