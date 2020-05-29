# -*- coding: utf-8 -*-
'''Library contains classes and functions to calculate winterstatistics'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.9.1'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'
import config
import knmi.model.stats as stats
import knmi.model.daydata as daydata
import model.utils as utils
import knmi.view.fix as fix
import view.html as html

class Stats:
    '''Class stores and saves winter statistics of a station in a given period'''
    def __init__(self, station, data ):
        self.station    = station
        self.data       = data
        self.date_start = data[0, daydata.YYYYMMDD]
        self.date_end   = data[-1, daydata.YYYYMMDD]
        self.period     = f'{self.date_start}-{self.date_end}'
        self.tg_gem     = stats.average( data, 'TG' )
        self.npl_hellmann, self.sum_hellmann = stats.hellmann( data )
        self.tx_min     = stats.min( data, 'TX' )
        self.tg_min     = stats.min( data, 'TG' )
        self.tn_min     = stats.min( data, 'TN' )
        self.npl_tx_lt_0  = stats.terms_days( data, 'TX', '<',   0 )
        self.cnt_tx_lt_0  = self.npl_tx_lt_0.size
        self.npl_tg_lt_0  = stats.terms_days( data, 'TX', '<',   0 )
        self.cnt_tg_lt_0  = stats.terms_days( data, 'TX', '<',   0 ).size

        self.npl_tn_lt_0  = stats.terms_days( data, 'TN', '<',   0 )
        self.npl_tn_lt_0  = stats.terms_days( data, 'TN', '<',   0 ).sixe
        self.tn_lt__5   = stats.terms_days( data, 'TN', '<',  -5 ).size
        self.tn_lt__10  = stats.terms_days( data, 'TN', '<', -10 ).size
        self.tn_lt__15  = stats.terms_days( data, 'TN', '<', -15 ).size
        self.tn_lt__20  = stats.terms_days( data, 'TN', '<', -20 ).size

def sort( l, ent, pm = '+' ):
    l = np.array( sorted(l, key=lambda stats: stats.hellmann) ) # Sort on hellmann
    if pm == '-':
        l[::-1] # reverse

    return l

def calculate( stations, sd, ed, name=False, type='html' ):
    '''Function to calculate winterstatistics'''
    log.console(f'Preparing output...')

    # Make data list with station and stats
    winter = np.array( [] )
    for station in stations:
        ok, data = daydata.read( station )  # Get data stations
        if ok:
            period = stats.period( data, sd, ed ) # Get days of period
            winter = np.append( winter, Stats( station, period ) ) # Create winterstats object

    if not name: name = f'winter statistics {sd}-{ed}' # Update name if not there
    # Make path if it is a html or txt file
    if   type == 'html': path = utils.path( config.dir_html_winterstats, f'{name}.html' )
    elif type ==  'txt': path = utils.path( config.dir_html_winterstats, f'{name}.txt'  )

    # Sort on hellmann
    winter = sort( winter, '+' )

    # Make output
    title, main, footer = '', '', ''

    # Head of txt of console
    if type in [ 'txt', 'cmd' ]:
        title += f'PLAATS{s:17} PROVINCIE         PERIODE{s:11} TG{s:5} '
        title += f'HELLMANN TX MIN  TG MIN  TN MIN  TX<0  TG<0  TN<0  TN<-5  '
        title += 'TX<-10 TX<-15 TX<-20\n'

    if type == 'html':
        title += '<table>\n<thead>\n<tr><th colspan="15">{name}</th></tr>\n'
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
        title += '<th title="Vorstdagen"> tn&lt;0 </th>\n'
        title += '<th title="Hellmanndagen"> tg&lt;0 </th>\n'
        title += '<th title="Dagen met matige vorst"> tn&lt;-5 </th>\n'
        title += '<th title="Dagen met strenge vorst"> tn&lt;-10 </th>\n'
        title += '<th title="Dagen met zeer strenge vorst"> tn&lt;-15 </th>\n'
        title += '<th title="Dagen met zeer strenge vorst"> tn&lt;-20 </th>\n'
        title += '</tr>\n</thead>\n'
        title += '<tbody>'

    # Calculate values
    for s in winter:
        tg_gem    = fix.ent( s.tg_gem, 'TG' )
        tx_min    = fix.ent( s.tx_min, 'TX' )
        tg_min    = fix.ent( s.tg_min, 'TG' )
        tn_min    = fix.ent( s.tn_min, 'TN' )
        hellmann  = fix.ent( s.tn_min, 'hellmann' )  # hellmann

        if type == 'html':
            period_txt = f'{utils.ymd_to_txt(s.date_start)} - {utils.ymd_to_txt(s.date_end)}'
            # TODO the extension html tables
            content += f'<tr>'
            content += f'<td> {s.station.place} </td>'
            content += f'<td> {s.station.province} </td>'
            content += f'<td title="{period_txt}"> {s.period} </td>'
            content += f'<td> {tg_gem} </td>'
            content += f'<td> {hellmann} </td>'
            content += f'<td> {tx_min} </td>'
            content += f'<td> {tg_min} </td>'
            content += f'<td> {tn_min} </td>'
            content += f'<td> {s.tx_lt_0} </td>'
            content += f'<td> {s.tn_lt_0} </td>'
            content += f'<td> {s.tg_lt_0} </td>'
            content += f'<td> {s.tn_lt__5} </td>'
            content += f'<td> {s.tn_lt__10} </td>'
            content += f'<td> {s.tn_lt__15} </td>'
            content += f'<td> {s.tn_lt__20} </td>'
            content += f'</tr>'

        elif type in ['txt','cmd']:
            content += f'{s.station.place:<23} {s.station.province:17} '
            content += f'{s.station.period:18} {tg_gem:7} {hellmann:^8} '
            content += f'{tx_min:<7} {tg_min:<7} {tn_min:<7} {s.tx_lt_0:^5} '
            content += f'{s.tg_lt_0:^5} {s.tn_lt_0:^5} {s.tn_lt__5:^6} '
            content += f'{s.tn_lt__10:^6} {s.tn_lt__15:^6} {s.tn_lt__20:^6} \n'

    # Close of content, footer
    if type in ['txt','cmd']:
        footer += station[0].dayvalues_notification
    elif type == 'html':
        footer += '</tbody>\n'
        footer += '<tfoot>\n'
        footer += '<tr>\n<td colspan="15">\n'
        footer += station[0].dayvalues_notification
        footer += '</td>\n</tr>\n</tfoot>\n</table>\n'

    # Write to file or console
    output = '{title}\n{main}\n{footer}'
    if type == 'cmd':
        log.console( output, True )
    elif type == 'html':
        page = html.Template()
        page.header = ''
        page.main   = output
        page.footer = ''
        page.file_path = path
        page.save()
    elif type == 'txt':
        io.save(path, output) # Schrijf naar bestand

    return path
