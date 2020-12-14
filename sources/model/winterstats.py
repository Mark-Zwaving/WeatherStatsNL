# -*- coding: utf-8 -*-
'''Library contains classes and functions to calculate winterstatistics'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.7.4'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config
import numpy as np
import sources.view.console as console
import sources.view.html as vhtml
import sources.view.fix as fix
import sources.view.icon as icon
import sources.control.fio as fio
import sources.model.utils as utils
import sources.model.stats as stats
import sources.model.daydata as daydata

class Stats:
    '''Class stores and saves winter statistics of a station in a given period'''
    def __init__(self, station, data ):
        self.station = station
        self.data    = data
        self.ymd     = data[:,daydata.YYYYMMDD]
        self.date_s  = utils.f_to_s( self.ymd[0]  )  # First day data
        self.date_e  = utils.f_to_s( self.ymd[-1] )  # Last day data
        self.period  = f'{self.date_s}-{self.date_e}'

        # Average calculations
        self.tg_gem = stats.average( data, 'TG' )

        # Min extremes
        self.tx_min_sort = stats.sort( data, 'TX', reverse=True )
        self.tx_min      = self.tx_min_sort[0, daydata.ndx_ent('TX')]
        self.tg_min_sort = stats.sort( data, 'TG', reverse=True )
        self.tg_min      = self.tg_min_sort[0, daydata.ndx_ent('TG')]
        self.tn_min_sort = stats.sort( data, 'TN', reverse=True )
        self.tn_min      = self.tn_min_sort[0, daydata.ndx_ent('TN')]

        self.rh_sort = stats.sort( data, 'RH' )
        self.rh_sum  = stats.sum( data, 'RH' )
        self.sq_sort = stats.sort( data, 'SQ' )
        self.sq_sum  = stats.sum( data, 'SQ' )

        # Days lists
        self.days_tx_lt_0   = stats.terms_days( data, 'TX', '<',   0 )
        self.days_tg_lt_0   = stats.terms_days( data, 'TG', '<',   0 )
        self.days_tn_lt_0   = stats.terms_days( data, 'TN', '<',   0 )
        self.days_tn_lt__5  = stats.terms_days( data, 'TN', '<',  -5 )
        self.days_tn_lt__10 = stats.terms_days( data, 'TN', '<', -10 )
        self.days_tn_lt__15 = stats.terms_days( data, 'TN', '<', -15 )
        self.days_tn_lt__20 = stats.terms_days( data, 'TN', '<', -20 )

        self.days_hellmann  = self.days_tg_lt_0
        self.sum_hellmann   = stats.hellmann( data )
        self.frost_sum      = stats.frost_sum( data )
        self.frost_sum_data = self.days_tn_lt_0 # All days with a T < 0
        self.ijnsen         = stats.ijnsen( data )

def sort( l, ent, pm = '+' ):
    l = np.array( sorted(np.array(l), key=lambda stats: stats.sum_hellmann) ).tolist() # Sort on hellmann
    if pm == '+':
        l = l[::-1] # reverse

    return l

def calculate( stations, period, name, type='html' ):
    '''Function to calculate winterstatistics'''
    console.log(f'Preparing output...')
    colspan = 20

    # Make data list with station and stats
    winter = list()
    for station in stations:
        console.log(f'Calculate statistics: {station.place}', True)
        ok, data = daydata.read( station )  # Get data stations
        if ok:
            days = daydata.period( data, period ) # Get days of period
            if days.size != 0:
                winter.append( Stats( station, days ) ) # Create winterstats object

    console.log(f'\nPreparing output: {type}', True)

    # Update name if there is none yet
    if not name:
        name = utils.mk_name('winterstatistics', period)

    # Make path if it is a html or txt file
    path = utils.mk_path( utils.mk_path(config.dir_winterstats, type),
                          f'{name}.{type}' )

    # Sort on hellmann
    winter = sort( winter, '+' )

    # Make output
    title, main, footer = '', '', ''

    # Head of txt of console
    table_title = 'Winter statistics '
    if type in [ 'txt', 'cmd' ]:
        title += f'{table_title} {period}\n'
        title += f'PLAATS{s:17} '
        title += f'PROVINCIE{s:8} '
        title += f'PERIODE{s:11} '
        title += f'TG{s:5} '
        title += 'HELLMANN TX MIN  TG MIN  TN MIN  TX<0  TG<0  TN<0  TN<-5  '
        title += 'TX<-10 TX<-15 TX<-20\n'

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
                    <th title="copyright data_notification"> &nbsp; </th>
                    <th> place {icon.home(size='fa-sm')}</th>
                    <th> province {icon.flag(size='fa-sm')}</th>
                    <th> period {icon.cal_period(size='fa-sm')}</th>
                    <th title="Average temperature"> tg {icon.temp_half(size='fa-sm')}</th>
                    <th title="Hellmann"> hmann {icon.icicles(size='fa-sm')}</th>
                    <th title="IJnsen"> ijnsen {icon.icicles(size='fa-sm')}</th>
                    <th title="Frost sum"> fsum {icon.icicles(size='fa-sm')}</th>
                    <th title="Coldest maximum temperature"> tx {icon.arrow_down(size='fa-sm')}</th>
                    <th title="Coldest average temperature "> tg {icon.arrow_down(size='fa-sm')}</th>
                    <th title="Coldest minumum temperature"> tn {icon.arrow_down(size='fa-sm')}</th>
                    <th title="Total hours sun"> {icon.sun(size='fa-sm')}</th>
                    <th title="Total mm rain"> {icon.shower_heavy(size='fa-sm')} </th>
                    <th title="Days with maximum temperature below 0 degrees celsius"> tx{icon.lt(size='fa-xs')}0 </th>
                    <th title="Days with average temperature below 0 degrees celsius"> tg{icon.lt(size='fa-xs')}0 </th>
                    <th title="Days with minimum temperature below 0 degrees celsius"> tn{icon.lt(size='fa-xs')}0 </th>
                    <th title="Days with temperature lower than -5 degrees celsius"> tn{icon.lt(size='fa-xs')}&minus;5 </th>
                    <th title="Days with temperature lower than -10 degrees celsius"> tn{icon.lt(size='fa-xs')}&minus;10 </th>
                    <th title="Days with temperature lower than -15 degrees celsius"> tn{icon.lt(size='fa-xs')}&minus;15 </th>
                    <th title="Days with temperature lower than -20 degrees celsius"> tn{icon.lt(size='fa-xs')}&minus;20 </th>
                  </tr>
              </thead>
              <tbody>
            '''
    # Calculate values
    for s in winter:
        console.log(f'Make {type} output for: {s.station.place}', True)

        tg_gem    = fix.ent( s.tg_gem, 'TG' )
        tx_min    = fix.ent( s.tx_min, 'TX' )
        tg_min    = fix.ent( s.tg_min, 'TG' )
        tn_min    = fix.ent( s.tn_min, 'TN' )
        hellmann  = fix.ent( s.sum_hellmann, 'hellmann' )
        f_sum     = fix.ent( s.frost_sum, 'frost_sum' )
        ijnsen    = fix.ent( s.ijnsen, 'ijnsen' )
        sq_sum    = fix.ent( s.sq_sum, 'SQ' )
        rh_sum    = fix.ent( s.rh_sum, 'RH' )

        if type == 'html':
            period_txt = f'{utils.ymd_to_txt(s.date_s)} - {utils.ymd_to_txt(s.date_e)}'
            # TODO the extension html tables
            main += f'''
                <tr class="row-data">
                    <td title="{s.station.data_notification.lower()}">
                            {icon.copy_light(size='fa-xs')}
                    </td>
                    <td> <span class="val"> {s.station.place} </span> </td>
                    <td> <span class="val"> {s.station.province} </span> </td>
                    <td title="{period_txt}"> <span class="val"> {s.period} </span> </td>
                    <td> <span class="val"> {tg_gem} </span> </td>
                    <td>
                        <span class="val"> {hellmann} </span>
                        {vhtml.table_hellmann( s.days_tg_lt_0 )}
                    </td>
                    <td>
                        <span class="val"> {ijnsen} </span>
                    </td>
                    <td>
                        <span class="val"> {f_sum} </span>
                        {vhtml.table_frost_sum( s.frost_sum_data )}
                    </td>
                    <td>
                        <span class="val"> {tx_min} </span>
                        {vhtml.table_days( s.tx_min_sort, 'TX', 'TXH' )}
                    </td>
                    <td>
                        <span class="val"> {tg_min} </span>
                        {vhtml.table_days( s.tg_min_sort, 'TG' )}
                    </td>
                    <td>
                        <span class="val"> {tn_min} </span>
                        {vhtml.table_days( s.tn_min_sort, 'TN', 'TNH' )}
                    </td>
                    <td>
                        <span class="val"> {sq_sum} </span>
                        {vhtml.table_days( s.sq_sort, 'SQ' )}
                    </td>
                    <td>
                        <span class="val"> {rh_sum} </span>
                        {vhtml.table_days( s.rh_sort, 'RH' )}

                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tx_lt_0, axis=0 )} </span>
                        {vhtml.table_days_count( s.days_tx_lt_0, 'TX', 'TXH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tg_lt_0, axis=0 )} </span>
                        {vhtml.table_days_count( s.days_tg_lt_0, 'TG' )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tn_lt_0, axis=0 )} </span>
                        {vhtml.table_days_count( s.days_tn_lt_0, 'TN', 'TNH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tn_lt__5, axis=0 )} </span>
                        {vhtml.table_days_count( s.days_tn_lt__5, 'TN', 'TNH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tn_lt__10, axis=0 )} </span>
                        {vhtml.table_days_count( s.days_tn_lt__10, 'TN', 'TNH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tn_lt__15, axis=0 )} </span>
                        {vhtml.table_days_count( s.days_tn_lt__15, 'TN', 'TNH' )}
                    </td>
                    <td>
                        <span class="val"> {np.size( s.days_tn_lt__20, axis=0 )} </span>
                        {vhtml.table_days_count( s.days_tn_lt__20, 'TN', 'TNH' )}
                    </td>
                </tr>
                '''

        elif type in ['txt','cmd']:
            main += f'{s.station.place:<23} '
            main += f'{s.station.province:17} '
            main += f'{s.station.period:18} '
            main += f'{tg_gem:7} '
            main += f'{hellmann:^8} '
            main += f'{tx_min:<7} '
            main += f'{tg_min:<7} '
            main += f'{tn_min:<7} '
            main += f'{np.size( s.days_tx_lt_0,   axis=0 ):^5} '
            main += f'{np.size( s.days_tg_lt_0,   axis=0 ):^5} '
            main += f'{np.size( s.days_tn_lt_0,   axis=0 ):^5} '
            main += f'{np.size( s.days_tn_lt__5,  axis=0 ):^6} '
            main += f'{np.size( s.days_tn_lt__10, axis=0 ):^6} '
            main += f'{np.size( s.days_tn_lt__15, axis=0 ):^6} '
            main += f'{np.size( s.days_tn_lt__20, axis=0 ):^6} \n'

    # Close of main, footer
    if type in ['txt','cmd']:
        footer += config.knmi_dayvalues_notification

    elif type == 'html':
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

    path_to_root = './../../' # Path to html root
    console.log('\nWrite/print results... ', True)

    # Write to file or console
    output = f'{title}\n{main}\n{footer}'
    if type == 'cmd':
        console.log( output, True )

    elif type == 'html':
        page           =  vhtml.Template()
        page.title     =  table_title
        page.main      =  output
        page.strip     =  True
        page.path_to_root = path_to_root
        page.file_path = path
        # Styling
        page.css_files = [ f'{path_to_root}winterstats/css/default.css',
                           f'{path_to_root}static/css/table-statistics.css',
                           f'{path_to_root}winterstats/css/winterstats.css' ]
        # Scripts
        page.script_files = [ f'{path_to_root}winterstats/js/winterstats.js',
                              f'{path_to_root}static/js/sort-col.js',
                              f'{path_to_root}static/js/default.js' ]
        page.save()

    elif type == 'txt':
        fio.save(path, output) # Schrijf naar bestand

    return path
