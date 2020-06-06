# -*- coding: utf-8 -*-
'''Library contains classes and functions to calculate winterstatistics'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.7.3'
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
        self.date_start = data[ 0, daydata.YYYYMMDD] # First day data
        self.date_end   = data[-1, daydata.YYYYMMDD] # Last day data
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

        # Entities list from days
        self.ent_tx_lt_0   = daydata.list_ent( self.days_tx_lt_0, 'TX' )
        self.ent_tg_lt_0   = daydata.list_ent( self.days_tg_lt_0, 'TG' )
        self.ent_tn_lt_0   = daydata.list_ent( self.days_tn_lt_0, 'TN' )
        self.ent_tn_lt__5  = daydata.list_ent( self.days_tn_lt__5, 'TN' )
        self.ent_tn_lt__10 = daydata.list_ent( self.days_tn_lt__10, 'TN' )
        self.ent_tn_lt__15 = daydata.list_ent( self.days_tn_lt__15, 'TN' )
        self.ent_tn_lt__20 = daydata.list_ent( self.days_tn_lt__20, 'TN' )
        self.ent_hellmann  = self.ent_tg_lt_0

        # Counts days
        self.cnt_tx_lt_0   = self.ent_tx_lt_0.size
        self.cnt_tg_lt_0   = self.ent_tg_lt_0.size
        self.cnt_tn_lt_0   = self.ent_tn_lt_0.size
        self.cnt_tn_lt__5  = self.ent_tn_lt__5.size
        self.cnt_tn_lt__10 = self.ent_tn_lt__10.size
        self.cnt_tn_lt__15 = self.ent_tn_lt__15.size
        self.cnt_tn_lt__20 = self.ent_tn_lt__20.size

        # Sum
        self.sum_hellmann  = abs(stats.sum(self.days_tg_lt_0, 'TG'))

def sort( l, ent, pm = '+' ):
    l = np.array( sorted(l, key=lambda stats: stats.sum_hellmann) ) # Sort on hellmann
    if pm == '+':
        l = l[::-1] # reverse

    return l

def calculate( stations, sd, ed, name=False, type='html' ):
    '''Function to calculate winterstatistics'''
    log.console(f'Preparing output...')

    # Make data list with station and stats
    winter = np.array( [] )
    for station in stations:
        log.console(f'Read and calculate statistics: {station.place}', True)
        ok, data = daydata.read( station )  # Get data stations
        if ok:
            period = stats.period( data, sd, ed ) # Get days of period
            winter = np.append( winter, Stats( station, period ) ) # Create winterstats object

    # Update name if there is none yet
    if not name:
        name = f'winter-statistics-{sd}-{ed}'

    # Make path if it is a html or txt file
    path = ''
    if type in ['html','txt']:
        if type == 'html':
            dir = config.dir_html_winterstats
        elif type == 'txt':
            dir = config.dir_txt_winterstats

        path = utils.path(dir, f'{name}.{type}')

    # Sort on hellmann
    winter = sort( winter, '+' )

    # Make output
    title, main, footer = '', '', ''

    # Head of txt of console
    if type in [ 'txt', 'cmd' ]:
        title += f'PLAATS{s:17} PROVINCIE         PERIODE{s:11} TG{s:5} '
        title += 'HELLMANN TX MIN  TG MIN  TN MIN  TX<0  TG<0  TN<0  TN<-5  '
        title += 'TX<-10 TX<-15 TX<-20\n'

    if type == 'html':
        table_title = name.replace('-', ' ').replace('_', ' ')
        title += f'<table>\n<thead>\n<tr><th colspan="15">{table_title}</th></tr>\n'
        title += '<tr>\n'
        title += '<th> plaats </th>\n'
        title += '<th> provincie </th>\n'
        title += '<th> periode </th>\n'
        title += '<th> tg </th>\n'
        title += '<th> hellmann </th>\n'
        title += '<th title="Koudste dag"> tx min </th>\n'
        title += '<th title="Koudste gemiddelde"> tg min </th>\n'
        title += '<th title="Koudste minimum"> tn min </th>\n'
        title += '<th title="IJsdagen"> tx&lt;0 </th>\n'
        title += '<th title="Hellmanndagen"> tg&lt;0 </th>\n'
        title += '<th title="Vorstdagen"> tn&lt;0 </th>\n'
        title += '<th title="Dagen met matige vorst"> tn&lt;-5 </th>\n'
        title += '<th title="Dagen met strenge vorst"> tn&lt;-10 </th>\n'
        title += '<th title="Dagen met zeer strenge vorst"> tn&lt;-15 </th>\n'
        title += '<th title="Dagen met zeer strenge vorst"> tn&lt;-20 </th>\n'
        title += '</tr>\n</thead>\n'
        title += '<tbody>'

    # Calculate values
    for s in winter:
        log.console(f'Make output: {s.station.place}', True)
        tg_gem    = fix.ent( s.tg_gem, 'TG' )
        tx_min    = fix.ent( s.tx_min, 'TX' )
        tg_min    = fix.ent( s.tg_min, 'TG' )
        tn_min    = fix.ent( s.tn_min, 'TN' )
        hellmann  = fix.ent( s.sum_hellmann, 'hellmann' )  # hellmann

        if type == 'html':
            period_txt = f'{utils.ymd_to_txt(s.date_start)} - {utils.ymd_to_txt(s.date_end)}'
            # TODO the extension html tables
            main += '<tr>'
            main += f'<td> {s.station.place} </td>'
            main += f'<td> {s.station.province} </td>'
            main += f'<td title="{period_txt}"> {s.period} </td>'
            main += f'<td> {tg_gem} </td>'
            main += f'<td> {hellmann} </td>'
            main += f'<td> {tx_min} </td>'
            main += f'<td> {tg_min} </td>'
            main += f'<td> {tn_min} </td>'
            main += f'<td> {s.cnt_tx_lt_0} </td>'
            main += f'<td> {s.cnt_tg_lt_0} </td>'
            main += f'<td> {s.cnt_tn_lt_0} </td>'
            main += f'<td> {s.cnt_tn_lt__5} </td>'
            main += f'<td> {s.cnt_tn_lt__10} </td>'
            main += f'<td> {s.cnt_tn_lt__15} </td>'
            main += f'<td> {s.cnt_tn_lt__20} </td>'
            main += '</tr>'

        elif type in ['txt','cmd']:
            main += f'{s.station.place:<23} {s.station.province:17} '
            main += f'{s.station.period:18} {tg_gem:7} {hellmann:^8} '
            main += f'{tx_min:<7} {tg_min:<7} {tn_min:<7} {s.cnt_tx_lt_0:^5} '
            main += f'{s.cnt_tg_lt_0:^5} {s.cnt_tn_lt_0:^5} {s.cnt_tn_lt__5:^6} '
            main += f'{s.cnt_tn_lt__10:^6} {s.cnt_tn_lt__15:^6} {s.cnt_tn_lt__20:^6} \n'

    # Close of main, footer
    notification = stations[0].dayvalues_notification
    if type in ['txt','cmd']:
        footer += notification
    elif type == 'html':
        footer += '</tbody>\n'
        footer += '<tfoot>\n'
        footer += '<tr>\n<td colspan="15">\n'
        footer += notification
        footer += '</td>\n</tr>\n'
        footer += '</tfoot>\n'
        footer += '</table>\n'

    # Write to file or console
    output = f'{title}\n{main}\n{footer}'
    if type == 'cmd':
        log.console( output, True )
    elif type == 'html':
        page           =  html.Template()
        page.title     =  table_title
        page.header    =  table_title
        page.main      =  output
        page.file_path =  path

        page.add_css_file('./css/', 'table-statistics.css')
        page.add_script_file('./js/', 'sort_col.js') # TODO
        page.save()
    elif type == 'txt':
        io.save(path, output) # Schrijf naar bestand

    return path
