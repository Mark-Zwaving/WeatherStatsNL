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
import view.log as log
import view.html as html
import model.utils as utils
import control.io as io
import knmi.model.stats as stats
import knmi.model.daydata as daydata
import knmi.view.fix as fix
import numpy as np

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

        # Days lists
        self.days_tx_lt_0   = stats.terms_days( data, 'TX', '<',   0 )
        self.days_tg_lt_0   = stats.terms_days( data, 'TG', '<',   0 )
        self.days_tn_lt_0   = stats.terms_days( data, 'TN', '<',   0 )
        self.days_tn_lt__5  = stats.terms_days( data, 'TN', '<',  -5 )
        self.days_tn_lt__10 = stats.terms_days( data, 'TN', '<', -10 )
        self.days_tn_lt__15 = stats.terms_days( data, 'TN', '<', -15 )
        self.days_tn_lt__20 = stats.terms_days( data, 'TN', '<', -20 )
        self.days_hellmann  = self.days_tg_lt_0
        self.sum_hellmann   = abs( stats.sum( self.days_tg_lt_0, 'TG' ) )

def sort( l, ent, pm = '+' ):
    l = np.array( sorted(l, key=lambda stats: stats.sum_hellmann) ) # Sort on hellmann
    if pm == '+': l = l[::-1] # reverse

    return l

def calculate( stations, period, name, type='html' ):
    '''Function to calculate winterstatistics'''
    log.console(f'Preparing output...')
    colspan = 15

    # Make data list with station and stats
    winter = np.array( [] )
    for station in stations:
        log.console(f'Read and calculate statistics: {station.place}', True)
        ok, data = daydata.read( station )  # Get data stations
        if ok:
            days = daydata.period( data, period ) # Get days of period
            winter = np.append( winter, Stats( station, days ) ) # Create winterstats object

    log.console(f'Preparing winterstats, output type is {type}', True)

    # Update name if there is none yet
    if not name:
        name = utils.mk_name('winterstatistics', period)

    # Make path if it is a html or txt file
    path = ''
    if type in ['html','txt']:
        if type == 'html':
            dir = config.dir_html_winterstats
        elif type ==  'txt':
            dir = config.dir_txt_winterstats

        path = utils.mk_path(dir, f'{name}.{type}')

    # Sort on hellmann
    winter = sort( winter, '+' )

    # Make output
    title, main, footer = '', '', ''

    # Head of txt of console
    table_title = name.replace('-', ' ')
    if type in [ 'txt', 'cmd' ]:
        title += f'{table_title} \n'
        title += f'PLAATS{s:17} '
        title += f'PROVINCIE{s:8} '
        title += f'PERIODE{s:11} '
        title += f'TG{s:5} '
        title += 'HELLMANN TX MIN  TG MIN  TN MIN  TX<0  TG<0  TN<0  TN<-5  '
        title += 'TX<-10 TX<-15 TX<-20\n'

    if type == 'html':
        title += f'''
              <table>
              <thead><tr><th colspan="{colspan}">{table_title}</th></tr>
                  <tr>
                      <th> plaats </th>
                      <th> provincie </th>
                      <th> periode </th>
                      <th> tg </th>
                      <th> hellmann </th>
                      <th title="Koudste dag"> tx min </th>
                      <th title="Koudste gemiddelde"> tg min </th>
                      <th title="Koudste minimum"> tn min </th>
                      <th title="IJsdagen"> tx&lt;0 </th>
                      <th title="Hellmanndagen"> tg&lt;0 </th>
                      <th title="Vorstdagen"> tn&lt;0 </th>
                      <th title="Dagen met matige vorst"> tn&lt;-5 </th>
                      <th title="Dagen met strenge vorst"> tn&lt;-10 </th>
                      <th title="Dagen met zeer strenge vorst"> tn&lt;-15 </th>
                      <th title="Dagen met zeer strenge vorst"> tn&lt;-20 </th>
                  </tr>
              </thead>
              <tbody>
                  '''

    # Calculate values
    for s in winter:
        log.console(f'Working on: {s.station.place}', True)

        tg_gem    = fix.ent( s.tg_gem, 'TG' )
        tx_min    = fix.ent( s.tx_min, 'TX' )
        tg_min    = fix.ent( s.tg_min, 'TG' )
        tn_min    = fix.ent( s.tn_min, 'TN' )
        hellmann  = fix.ent( s.sum_hellmann, 'hellmann' )  # hellmann

        if type == 'html':
            period_txt = f'{utils.ymd_to_txt(s.date_start)} - {utils.ymd_to_txt(s.date_end)}'
            # TODO the extension html tables
            main += f'''
                <tr>
                    <td> {s.station.place} </td>
                    <td> {s.station.province} </td>
                    <td title="{period_txt}"> {s.period} </td>
                    <td> {tg_gem} </td>
                    <td> {hellmann} </td>
                    <td> {tx_min} </td>
                    <td> {tg_min} </td>
                    <td> {tn_min} </td>
                    <td> {s.days_tx_lt_0.size} </td>
                    <td> {s.days_tg_lt_0.size} </td>
                    <td> {s.days_tn_lt_0.size} </td>
                    <td> {s.days_tn_lt__5.size} </td>
                    <td> {s.days_tn_lt__10.size} </td>
                    <td> {s.days_tn_lt__15.size} </td>
                    <td> {s.days_tn_lt__20.size} </td>
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
            main += f'{s.days_tx_lt_0.size:^5} '
            main += f'{s.days_tg_lt_0.size:^5} '
            main += f'{s.days_tn_lt_0.size:^5} '
            main += f'{s.days_tn_lt__5.size:^6} '
            main += f'{s.days_tn_lt__10.size:^6} '
            main += f'{s.days_tn_lt__15.size:^6} '
            main += f'{s.days_tn_lt__20.size:^6} \n'

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
        page.header    =  table_title
        page.main      =  output
        page.footer    =  ''
        page.file_path =  path
        page.add_css_file('./css/', 'table-statistics.css')
        page.add_script_file('./js/', 'sort_col.js') # TODO
        page.save()

    elif type == 'txt':
        io.save(path, output) # Schrijf naar bestand

    return path
