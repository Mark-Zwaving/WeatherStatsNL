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
import view.log as log
import view.html as html
import view.fix as fix
import view.icon as icon
import control.io as io
import model.utils as utils
import model.stats as stats
import model.daydata as daydata

class Stats:
    '''Class stores and saves winter statistics of a station in a given period'''
    def __init__(self, station, data ):
        self.station    = station
        self.data       = data
        self.ymd        = data[:,daydata.YYYYMMDD]
        self.date_start = utils.f_to_s( self.ymd[0]  )  # First day data
        self.date_end   = utils.f_to_s( self.ymd[-1] )  # Last day data
        self.period     = f'{self.date_start}-{self.date_end}'

        # Average calculations
        self.tg_gem = stats.average( data, 'TG' )

        # Min extremes
        self.tx_min = stats.min( data, 'TX' )
        self.tg_min = stats.min( data, 'TG' )
        self.tn_min = stats.min( data, 'TN' )

        self.rh_sum = stats.sum( data, 'RH' )
        self.sq_sum = stats.sum( data, 'SQ' )

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
        self.frost_sum      = stats.frost_sum ( data )
        self.ijnsen         = stats.ijnsen( data )

def sort( l, ent, pm = '+' ):
    l = np.array( sorted(l, key=lambda stats: stats.sum_hellmann) ) # Sort on hellmann
    if pm == '+': l = l[::-1] # reverse

    return l

def calculate( stations, period, name, type='html' ):
    '''Function to calculate winterstatistics'''
    log.console(f'Preparing output...')
    colspan = 19
    popup_rows = config.max_rows_table_popup

    # Make data list with station and stats
    winter = np.array( [] )
    for station in stations:
        log.console(f'Calculate statistics: {station.place}', True)
        ok, data = daydata.read( station )  # Get data stations
        if ok:
            days = daydata.period( data, period ) # Get days of period
            if days.size != 0:
                winter = np.append( winter, Stats( station, days ) ) # Create winterstats object

    log.console(f'\nPreparing output: {type}', True)

    # Update name if there is none yet
    if not name:
        name = utils.mk_name('winterstatistics', period)

    # Make path if it is a html or txt file
    path = ''
    if type in ['html','txt']:
        if type == 'html':
            dir = config.dir_html_winterstats
        elif type == 'txt':
            dir = config.dir_txt_winterstats

        path = utils.mk_path(dir, f'{name}.{type}')

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
        log.console(f'Make {type} output for: {s.station.place}', True)

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
            period_txt = f'{utils.ymd_to_txt(s.date_start)} - {utils.ymd_to_txt(s.date_end)}'
            # TODO the extension html tables
            main += f'''
                <tr class="row-data">
                    <td> <span class="val"> {s.station.place} </span> </td>
                    <td> <span class="val"> {s.station.province} </span> </td>
                    <td title="{period_txt}"> <span class="val"> {s.period} </span> </td>
                    <td> <span class="val"> {tg_gem} </span> </td>
                    <td> <span class="val"> {hellmann} </span> </td>
                    <td> <span class="val"> {ijnsen} </span> </td>
                    <td> <span class="val"> {f_sum} </span> </td>
                    <td> <span class="val"> {tx_min} </span> </td>
                    <td> <span class="val"> {tg_min} </span> </td>
                    <td> <span class="val"> {tn_min} </span> </td>
                    <td> <span class="val"> {sq_sum} </span> </td>
                    <td> <span class="val"> {rh_sum} </span> </td>
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
        page.set_path( dir, f'{name}.html' )
        # Styling
        page.add_css_file(dir='./../static/css/', name='table-statistics.css')
        page.add_css_file(dir='./../static/css/', name='default.css')
        page.add_css_file(dir='./css/', name='winterstats.css')
        # Scripts
        page.add_script_file(dir='./js/', name='winterstats.js')
        page.add_script_file(dir='./../static/js/', name='sort-col.js')
        page.add_script_file(dir='./../static/js/', name='default.js')
        page.save()

    elif type == 'txt':
        io.save(path, output) # Schrijf naar bestand

    return path
