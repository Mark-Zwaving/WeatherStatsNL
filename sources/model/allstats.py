# -*- coding: utf-8 -*-
'''Library contains classes and functions for calculating summerstatistics'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.6"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config, numpy as np
import sources.control.fio as fio
import sources.model.utils as utils
import sources.model.stats as stats
import sources.model.daydata as daydata
import sources.view.fix as fix
import sources.view.log as log
import sources.view.html as html
import sources.view.icon as icon

class Stats:
    '''Class saves en stores summer statistics of a station in a given period'''
    def __init__(self, station, data ):
        self.station     = station
        self.data        = data
        self.ymd         = data[:,daydata.YYYYMMDD]
        self.p_start     = utils.f_to_s( self.ymd[ 0] )  # First day data
        self.p_end       = utils.f_to_s( self.ymd[-1] )  # Last day data
        self.period      = f'{self.p_start}-{self.p_end}'
        self.tg_ave      = stats.average(data,'TG')
        self.tx_max_sort = stats.sort( data, 'TX')
        self.tx_max      = self.tx_max_sort[0, daydata.ndx_ent('TX')]
        self.tg_max_sort = stats.sort( data, 'TG')
        self.tg_max      = self.tg_max_sort[0, daydata.ndx_ent('TG')]

        self.tn_max_sort = stats.sort( data, 'TN')
        self.tn_max      = self.tn_max_sort[0, daydata.ndx_ent('TN')]
        self.tx_min_sort = stats.sort( data, 'TX', reverse=True )
        self.tx_min      = self.tx_min_sort[0, daydata.ndx_ent('TX')]
        self.tg_min_sort = stats.sort( data, 'TG', reverse=True )
        self.tg_min      = self.tg_min_sort[0, daydata.ndx_ent('TG')]
        self.tn_min_sort = stats.sort( data, 'TN', reverse=True )
        self.tn_min      = self.tn_min_sort[0, daydata.ndx_ent('TN')]

        self.sq_sum      = stats.sum(data,'SQ') # Total sunshine hours
        self.sq_sort     = stats.sort(data, 'SQ')
        self.rh_sum      = stats.sum(data,'RH') # Total rain
        self.rh_sort     = stats.sort(data, 'RH')

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

        self.heat_ndx = stats.heat_ndx(data)
        self.days_heat_ndx = self.days_tg_gte_18
        self.hellmann = stats.hellmann(data)
        self.days_hellmann = self.days_tg_lt_0
        self.ijnsen = stats.ijnsen(data)
        self.frost_sum = stats.frost_sum(data)
        self.frost_sum_data = np.unique( np.concatenate( ( self.days_tn_lt_0,
                                                           self.days_tx_lt_0 ),
                                                           axis=0 ),
                                                           axis=0 )

def sort( l, pm = '+' ):
    l = np.array( sorted(np.array(l), key=lambda stats: stats.tg_ave) ).tolist() # Sort on average
    if pm == '+':
        l = l[::-1] # reverse

    return l

def calculate( stations, period, name=False, type='html' ):
    '''Function calculates all statistics'''
    colspan = 33

    # Make data list with station and summerstatistics
    allstats = list()
    for station in stations:
        log.console(f'Calculate statistics: {station.place}', True)
        ok, data = daydata.read( station )  # Get data stations
        if ok:
            days = daydata.period( data, period ) # Get days of period
            if days.size != 0: # Skip station
                allstats.append( Stats( station, days ) ) # Create summerstats object

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
                        {icon.weather_all()}
                        {table_title}
                        {icon.wave_square()}
                        {period}
                        {icon.cal_period()}
                    </th>
                </tr>
                <tr>
                    <th title="copyright data_notification"> </th>
                    <th> place {icon.home(size='fa-sm')} </th>
                    <th> province {icon.flag(size='fa-sm')} </th>
                    <th> period  {icon.cal_period(size='fa-sm')} </th>
                    <th title="Average temperature"> tg {icon.temp_half(size='fa-sm')} </th>
                    <th title="Highest maximum temperature"> tx {icon.arrow_up(size='fa-sm')} </th>
                    <th title="Highest average temperature"> tg {icon.arrow_up(size='fa-sm')} </th>
                    <th title="Highest minimum temperature"> tn {icon.arrow_up(size='fa-sm')} </th>
                    <th title="Lowest maximum temperature"> tx {icon.arrow_down(size='fa-sm')} </th>
                    <th title="Lowest average temperature "> tg {icon.arrow_down(size='fa-sm')} </th>
                    <th title="Lowest minumum temperature"> tn {icon.arrow_down(size='fa-sm')} </th>
                    <th title="Total hours of sunshine"> {icon.sun(size='fa-sm')} </th>
                    <th title="Total rain mm"> {icon.shower_heavy(size='fa-sm')} </th>
                    <th title="Heat index tg greater than 18 degrees celsius"> heat {icon.fire(size='fa-sm')} </th>
                    <th title="Warm days"> tx{icon.gte(size='fa-xs')}20 </th>
                    <th title="Summer days"> tx{icon.gte(size='fa-xs')}25 </th>
                    <th title="Tropical days"> tx{icon.gte(size='fa-xs')}30 </th>
                    <th title="High tropical days"> tx{icon.gte(size='fa-xs')}35 </th>
                    <th title="High tropical days"> tx{icon.gte(size='fa-xs')}40 </th>
                    <th title="Warm days on average"> tg{icon.gte(size='fa-xs')}18 </th>
                    <th title="Tropical nights"> tn{icon.gte(size='fa-xs')}20 </th>
                    <th title="Days with more than 10hour of sun">
                        {icon.sun(size='fa-xs')}{icon.gte(size='fa-xs')}10h
                    </th>
                    <th title="Days with more than 10 mm of rain">
                        {icon.shower_heavy(size='fa-xs')}{icon.gte(size='fa-xs')}10mm
                    </th>
                    <th title="Hellmann"> hmann {icon.icicles(size='fa-sm')}</th>
                    <th title="IJnsen"> ijnsen {icon.icicles(size='fa-sm')}</th>
                    <th title="Frost sum"> fsum {icon.icicles(size='fa-sm')}</th>
                    <th title="Days with maximum temperature below 0 degrees celsius"> tx{icon.lt(size='fa-xs')}0 </th>
                    <th title="Days with average temperature below 0 degrees celsius"> tg{icon.lt(size='fa-xs')}0 </th>
                    <th title="Days with minimum temperature below 0 degrees celsius"> tn{icon.lt(size='fa-xs')}0 </th>
                    <th title="Days with minimum temperature lower than -5 degrees celsius"> tn{icon.lt(size='fa-xs')}&minus;5 </th>
                    <th title="Days with minimum temperature lower than -10 degrees celsius"> tn{icon.lt(size='fa-xs')}&minus;10 </th>
                    <th title="Days with minimum temperature lower than -15 degrees celsius"> tn{icon.lt(size='fa-xs')}&minus;15 </th>
                    <th title="Days with minimum temperature lower than -20 degrees celsius"> tn{icon.lt(size='fa-xs')}&minus;20 </th>
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
                    <td title="{s.station.data_notification.lower()}">
                            {icon.copy_light(size='fa-xs')}
                    </td>
                    <td> <span class="val"> {s.station.place} </span> </td>
                    <td> <span class="val"> {s.station.province} </span> </td>
                    <td title="{period_txt}"> <span class="val"> {s.period} </span> </td>
                    <td>
                        <span class="val"> {tg_ave} </span>
                    </td>
                    <td>
                        <span class="val"> {tx_max} </span>
                        {html.table_days( s.tx_max_sort, 'TX', 'TXH' )}
                    </td>
                    <td>
                        <span class="val"> {tg_max} </span>
                        {html.table_days( s.tg_max_sort, 'TG' )}
                    </td>
                    <td>
                        <span class="val"> {tn_max} </span>
                        {html.table_days( s.tn_max_sort, 'TN', 'TNH' )}
                    </td>
                    <td>
                        <span class="val"> {tx_min} </span>
                        {html.table_days( s.tx_min_sort, 'TX', 'TXH' )}
                    </td>
                    <td>
                        <span class="val"> {tg_min} </span>
                        {html.table_days( s.tg_min_sort, 'TG' )}
                    </td>
                    <td>
                        <span class="val"> {tn_min} </span>
                        {html.table_days( s.tn_min_sort, 'TN', 'TNH' )}
                    </td>
                    <td>
                        <span class="val"> {sq_sum} </span>
                        {html.table_days( s.sq_sort , 'SQ' )}
                    </td>
                    <td>
                        <span class="val"> {rh_sum} </span>
                        {html.table_days( s.rh_sort, 'RH' )}
                    </td>
                    <td>
                        <span class="val"> {heat_ndx} </span>
                        {html.table_heat_ndx( s.days_heat_ndx, 'TG' )}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_20, axis=0)} </span>
                        {html.table_days_count(s.days_tx_gte_20, 'TX', 'TXH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_25, axis=0)} </span>
                        {html.table_days_count(s.days_tx_gte_25, 'TX', 'TXH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_30, axis=0)} </span>
                        {html.table_days_count(s.days_tx_gte_30, 'TX', 'TXH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_35, axis=0)} </span>
                        {html.table_days_count(s.days_tx_gte_35, 'TX', 'TXH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tx_gte_40, axis=0)} </span>
                        {html.table_days_count(s.days_tx_gte_40, 'TX', 'TXH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tg_gte_18, axis=0)} </span>
                        {html.table_days_count(s.days_tg_gte_18, 'TG' )}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_tn_gte_20, axis=0)} </span>
                        {html.table_days_count(s.days_tn_gte_20, 'TG' )}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_sq_gte_10, axis=0)} </span>
                        {html.table_days_count(s.days_sq_gte_10, 'SQ' )}
                    </td>
                    <td>
                        <span class="val"> {np.size(s.days_rh_gte_10, axis=0)} </span>
                        {html.table_days_count(s.days_rh_gte_10, 'RH' )}
                    </td>
                    <td>
                        <span class="val"> {hellmann} </span>
                        {html.table_hellmann( s.days_hellmann )}
                    </td>
                    <td>
                        <span class="val"> {ijnsen} </span>
                    </td>
                    <td>
                        <span class="val"> {f_sum} </span>
                        {html.table_frost_sum( s.frost_sum_data )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tx_lt_0, axis=0 )} </span>
                        {html.table_days_count( s.days_tx_lt_0, 'TX', 'TXH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tg_lt_0, axis=0 )} </span>
                        {html.table_days_count( s.days_tg_lt_0, 'TG' )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tn_lt_0, axis=0 )} </span>
                        {html.table_days_count( s.days_tn_lt_0, 'TN', 'TNH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tn_lt__5, axis=0 )} </span>
                        {html.table_days_count( s.days_tn_lt__5, 'TN', 'TNH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tn_lt__10, axis=0 )} </span>
                        {html.table_days_count( s.days_tn_lt__10, 'TN', 'TNH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tn_lt__15, axis=0 )} </span>
                        {html.table_days_count( s.days_tn_lt__15, 'TN', 'TNH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tn_lt__20, axis=0 )} </span>
                        {html.table_days_count( s.days_tn_lt__20, 'TN', 'TNH' )}
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
        fio.save(path, output) # Schrijf naar bestand

    return path
