# -*- coding: utf-8 -*-
'''Library contains classes and functions for calculating summerstatistics'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config as c, fn, fn_html as h, calc_stats as st, dates as d
import write as wr, ask, fn_read as r, knmi

class AllExtremes:
    '''Class saves en stores extremes statistics of a station in a given period'''
    def __init__(self, station, etm_l):
        self.station      =  station
        self.etm_l        =  etm_l
        self.date_start   =  etm_l[0].YYYYMMDD
        self.date_end     =  etm_l[-1].YYYYMMDD
        self.period       =  f'{self.date_start}-{self.date_end}'
        self.place        =  station.plaats
        self.province     =  station.provincie
        self.wmo          =  station.wmo

        self.tx_max       =  st.max_val(etm_l,'TX')
        self.tg_max       =  st.max_val(etm_l,'TG')
        self.tn_max       =  st.max_val(etm_l,'TN')

        self.tx_min       =  st.min_val(etm_l,'TX')
        self.tg_min       =  st.min_val(etm_l,'TG')
        self.tn_min       =  st.min_val(etm_l,'TN')

        self.sq_max       =  st.max_val(etm_l,'SQ')          # Som zonuren
        self.rh_max       =  st.max_val(etm_l,'RH')          # Som regen mm

def sort_allextremes(lijst, pm = '+'):
    sorted = []
    while lijst:
        max, key = c.min_value_geg, 0
        # Haal key minimum waarde uit lijst
        for i in range(len(lijst)):
            val = lijst[i].tx_max['max']
            if val > max:
                max = val; key = i
        sorted.append(lijst[key]) # Voeg waarde toe
        del lijst[key] # Verwijder max waarde uit lijst
    return sorted if pm == '+' else sorted.reverse()

def alg_allextremes(lijst_stations, date_start, date_end, name, type):
    '''Hoofdfunctie voor het berekenen van de extremes'''
    all_ext, periode, path, content = [], f'{date_start}-{date_end}', '', ''
    bronvermelding = lijst_stations[0].notification
    max_rows = c.html_popup_table_max_rows

    if not name: name = f'statistics-{periode}-{d.act_datetime_unique()}'
    title = f'Statistics {periode}'
    filename = ''

    if type == 'html':
        name = f'{name}.html'
        path = c.dir_html

    if type == 'txt':
        name = f'{name}.txt'
        path = c.dir_text

    for station in lijst_stations:
        l = fn.select_dates_from_list( r.knmi_etmgeg_data(station),
                                       date_start, date_end )
        if not l: # Geen data gevonden, naar de volgende
            continue
        else:
            print(f"Calculate all extremes for station: {station.wmo} {station.plaats}")
            # Vul Winterstats object met  waarden en voegtoe aan lijst
            all_ext.append( AllExtremes( station, l ))

    fn.lnprintln(f'...Preparing output ({type})...')

    all_ext = sort_allextremes(all_ext,'+') # Sorteer op tg

    # Maak content op basis van type uitvoer html of text
    # Maak titel
    if type in ['txt','cmd']:
        s = ' '
        content = f'PLAATS{s:15} PROVINCIE{s:7} PERIODE{s:11} TG      ' \
                  f'TX MAX  TG MAX  TN MAX  TX MIN  TG MIN  TN MIN  ' \
                  f'∑ZON       ∑REGEN  \n'

    if type == 'html':
        content  = f'''
        <table>
            <thead>
            <tr> <th colspan="11"> {title} </th> </tr>
            <tr>
                <th> plaats </th>
                <th> provincie </th>
                <th> periode </th>
                <th title="Warmste dag"> tx max </th>
                <th title="Hoogste gemiddelde"> tg max </th>
                <th title="Hoogste minimum"> tn max </th>
                <th title="Laagste maximum"> tx min </th>
                <th title="Laagste gemiddelde"> tg min </th>
                <th title="Laagste minimum"> tn min </th>
                <th title="Totaal aantal uren zon"> zon </th>
                <th title="Totaal aantal mm regen"> regen </th>
            </tr>
            </thead>
            <tbody>
        '''

    # Walkthrough all cities
    for g in all_ext:
        tx_max = '.' if not g.tx_max['max'] else fn.rm_s(fn.fix(g.tx_max['max'],'tx'))
        tg_max = '.' if not g.tg_max['max'] else fn.rm_s(fn.fix(g.tg_max['max'],'tg'))
        tn_max = '.' if not g.tn_max['max'] else fn.rm_s(fn.fix(g.tn_max['max'],'tn'))
        rh_max = '.' if not g.rh_max['max'] else fn.rm_s(fn.fix(g.rh_max['max'],'rh'))
        sq_max = '.' if not g.sq_max['max'] else fn.rm_s(fn.fix(g.sq_max['max'],'sq'))
        tx_min = '.' if not g.tx_min['min'] else fn.rm_s(fn.fix(g.tx_min['min'],'tx'))
        tg_min = '.' if not g.tg_min['min'] else fn.rm_s(fn.fix(g.tg_min['min'],'tg'))
        tn_min = '.' if not g.tn_min['min'] else fn.rm_s(fn.fix(g.tn_min['min'],'tn'))

        if type in ['txt','cmd']:
            content += f"{g.place:<21} {g.province:<16} {g.period:<18} "
            content += f"{tx_max:<7} {tg_max:<7} {tn_max:<7} {tx_min:<7} {tg_min:<7} {tn_min:<7} "
            content += f"{sq_max:<10} {rh_max:<11} \n"

        if type == 'html':
            date_txt = f"{d.Datum(g.date_start).tekst()} - {d.Datum(g.date_end).tekst()}"
            content += f'''
                <tr>
                    <td> {g.place} </td>
                    <td> {g.province} </td>
                    <td title="{date_txt}"> {g.period} </td>

                    <td> {tx_max}    {h.table_extremes(g.tx_max['lijst'][-1:], max_rows)} </td>
                    <td> {tg_max}    {h.table_extremes(g.tg_max['lijst'][-1:], max_rows)} </td>
                    <td> {tn_max}    {h.table_extremes(g.tn_max['lijst'][-1:], max_rows)} </td>
                    <td> {tx_min}    {h.table_extremes(g.tx_min['lijst'][-1:], max_rows)} </td>
                    <td> {tg_min}    {h.table_extremes(g.tg_min['lijst'][-1:], max_rows)} </td>
                    <td> {tn_min}    {h.table_extremes(g.tn_min['lijst'][-1:], max_rows)} </td>

                    <td> {sq_max} </td>
                    <td> {rh_max} </td>
                </tr>
                '''

    if type in ['txt','cmd']:
        content += bronvermelding

    if type == 'html':
        content += f'''
            </tbody>
            <tfoot> <tr> <td colspan="11"> {bronvermelding} </td> </tr> </tfoot>
        </table>'''

        css = r.get_string_css_from_file( 'default-table-statistics.css' ) # Get css from file
        content = h.pagina(title, css, content) # Make html page
        content = fn.clean_s(content) # Remove unnecessary whitespace

    if type == 'cmd':
        fn.lnprintln(c.line + c.ln + content + c.ln + c.line)

    if type in ['html','txt']:
        file_name = fn.mk_path(path, name) # Make file name
        wr.write_to_file(file_name, content) # Schrijf naar bestand

    return file_name
