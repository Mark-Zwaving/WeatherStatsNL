# -*- coding: utf-8 -*-
'''Library contains classes and functions for calculating summerstatistics'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9.2"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config as cfg, fn, fn_html as h, calc_stats as st, dates as d
import write as wr, ask, fn_read as r, knmi

class SummerStats:
    '''Class saves en stores summer statistics of a station in a given period'''
    def __init__(self, station, etm_l):
        self.station      =  station
        self.etm_l        =  etm_l
        self.date_start   =  etm_l[0].YYYYMMDD
        self.date_end     =  etm_l[-1].YYYYMMDD
        self.period       =  f'{self.date_start}-{self.date_end}'
        self.place        =  station.plaats
        self.province     =  station.provincie
        self.wmo          =  station.wmo
        self.tg_gem       =  st.gem_val(etm_l,'TG')
        self.tx_max       =  st.max_val(etm_l,'TX')
        self.tg_max       =  st.max_val(etm_l,'TG')
        self.tn_max       =  st.max_val(etm_l,'TN')
        self.warmte_getal =  st.warmte_getal(etm_l)
        self.tx_gte_20    =  st.cnt_day(etm_l,'TX','>=',200)  # Warme dag
        self.tx_gte_25    =  st.cnt_day(etm_l,'TX','>=',250)  # Zomerse dag
        self.tx_gte_30    =  st.cnt_day(etm_l,'TX','>=',300)  # Tropische dag
        self.tx_gte_35    =  st.cnt_day(etm_l,'TX','>=',350)  # Tropische
        self.tg_gte_18    =  st.cnt_day(etm_l,'TG','>=',180)  # Warmte getal dag
        self.tg_gte_20    =  st.cnt_day(etm_l,'TG','>=',200)  # Warme gemiddelde
        self.tn_gte_20    =  st.cnt_day(etm_l,'TN','>=',200)  # Tropen nacht
        self.sq_gte_10    =  st.cnt_day(etm_l,'SQ','>=',100)  # Zonuren > 10
        self.sq_tot       =  st.som_val(etm_l,'SQ')           # Som zonuren
        self.rh_gte_10    =  st.cnt_day(etm_l,'RH','>=',100)  # Regen > 10mm
        self.rh_tot       =  st.som_val(etm_l,'RH')           # Som regen mm

def sort_zomerstats_num(lijst, pm = '+'):
    sorted = []
    while lijst:
        max, key = cfg.min_value_geg, 0
        # Haal key minimum waarde uit lijst
        for i in range(len(lijst)):
            val = lijst[i].tg_gem['gem']
            if val > max:
                max = val; key = i
        sorted.append(lijst[key]) # Voeg waarde toe
        del lijst[key] # Verwijder max waarde uit lijst
    return sorted if pm == '+' else sorted.reverse()

def alg_zomerstats(lijst_stations, datum_start, datum_eind, name, type):
    '''Hoofdfunctie voor het berekenen van de zomerstats'''
    zomer_geg, periode, path, content = [], f'{datum_start}-{datum_eind}', '', ''
    bronvermelding = cfg.lijst_stations[0].bronvermelding

    # Filename
    if not name: name = f'summer statistics {periode}'

    title = name
    file_name = ''

    if type == 'html':
        name = f'{name}.html'
        path = cfg.lijst_stations[0].dir_html

    if type == 'txt':
        name = f'{name}.txt'
        path = cfg.lijst_stations[0].dir_text

    for station in lijst_stations:
        l = fn.select_dates_from_list( r.knmi_etmgeg_data(station),
                                       datum_start, datum_eind )
        if not l: # Geen data gevonden, naar de volgende
            continue
        else:
            print(f"Calculate summer statistics for station: {station.wmo} {station.plaats}")
            # Vul Winterstats object met  waarden en voegtoe aan lijst
            zomer_geg.append( SummerStats( station, l ))

    fn.lnprintln(f'...Preparing output ({type})...')

    zomer_geg = sort_zomerstats_num(zomer_geg,'+') # Sorteer op tg

    # Maak content op basis van type uitvoer html of text
    # Maak titel
    if type in ['txt','cmd']:
        s = ' '
        content = f'PLAATS{s:15} PROVINCIE{s:7} PERIODE{s:11} TG      ∑WARMTE ' \
                  f'TX MAX  TG MAX  TN MAX  ∑TX≥20 ∑TX≥25 ∑TX≥30 ∑TX≥35 ' \
                  f'∑TG≥18 ∑TG≥20 ∑TN≥20 ∑ZON≥10 ∑ZON       ∑REGEN≥10 ∑REGEN  \n'

    if type == 'html':
        content  = f'''
        <table>
            <thead>
            <tr> <th colspan="19"> {title} </th> </tr>
            <tr>
                <th> plaats </th>
                <th> provincie </th>
                <th> periode </th>
                <th> tg </th>
                <th title="Warmte getal"> ∑warmte </th>
                <th title="Warmste dag"> tx max </th>
                <th title="Hoogste gemiddelde"> tg max </th>
                <th title="Hoogste minimum"> tn max </th>
                <th title="Aantal warme dagen"> ∑tx&ge;20 </th>
                <th title="Aantal zomers dagen"> ∑tx&ge;25 </th>
                <th title="Aantal tropische dagen"> ∑tx&ge;30 </th>
                <th title="Aantal tropische dagen"> ∑tx&ge;35 </th>
                <th title="Warmte getal dagen"> tg&ge;18 </th>
                <th title="Dagen met een hoog gemiddelde"> tg&ge;20 </th>
                <th title="Aantal tropennachten"> ∑tn&ge;20 </th>
                <th title="Totaal aantal uren zon"> ∑zon </th>
                <th title="Dagen met meer dan tien uur zon"> ∑zon&ge;10hour</th>
                <th title="Totaal aantal mm regen"> ∑regen </th>
                <th title="Dagen met meer dan tien mm regen"> ∑regen&ge;10mm</th>
            </tr>
            </thead>
            <tbody>
        '''

    # Walkthrough all cities
    for g in zomer_geg:
        warm = g.warmte_getal['getal']
        heat_ndx = '.' if not warm else fn.rm_s(fn.fix(warm, 'heat_ndx'))
        tg_gem = '.' if not g.tg_gem['gem'] else fn.rm_s(fn.fix(g.tg_gem['gem'],'tg'))
        tx_max = '.' if not g.tx_max['max'] else fn.rm_s(fn.fix(g.tx_max['max'],'tx'))
        tg_max = '.' if not g.tg_max['max'] else fn.rm_s(fn.fix(g.tg_max['max'],'tg'))
        tn_max = '.' if not g.tn_max['max'] else fn.rm_s(fn.fix(g.tn_max['max'],'tn'))
        rh_tot = '.' if not g.rh_tot['som'] else fn.rm_s(fn.fix(g.rh_tot['som'],'rh'))
        sq_tot = '.' if not g.sq_tot['som'] else fn.rm_s(fn.fix(g.sq_tot['som'],'sq'))
        tx_gte_20 = str(g.tx_gte_20['tel'])
        tx_gte_25 = str(g.tx_gte_25['tel'])
        tx_gte_35 = str(g.tx_gte_35['tel'])
        tx_gte_30 = str(g.tx_gte_30['tel'])
        tg_gte_18 = str(g.tg_gte_18['tel'])
        tn_gte_20 = str(g.tn_gte_20['tel'])
        tg_gte_20 = str(g.tg_gte_20['tel'])
        sq_gte_10 = str(g.sq_gte_10['tel'])
        rh_gte_10 = str(g.rh_gte_10['tel'])

        if type in ['txt','cmd']:
            content += f"{g.place:<21} {g.province:<16} {g.period:<18} " \
                       f"{tg_gem:<7} {heat_ndx:<7} {tx_max:<7} {tg_max:<7} " \
                       f"{tn_max:<7} {tx_gte_20:^6} {tx_gte_25:^6} {tx_gte_30:^6} " \
                       f"{tx_gte_35:^6} {tg_gte_18:^6} {tg_gte_20:^6} {tn_gte_20:^6} " \
                       f"{sq_gte_10:^7} {sq_tot:<10} {rh_gte_10:^9} {rh_tot:<11} \n"

        if type == 'html':
            date_txt = f"{d.Datum(g.date_start).tekst()} - {d.Datum(g.date_end).tekst()}"
            content += f'''
                <tr>
                    <td> {g.place} </td>
                    <td> {g.province} </td>
                    <td title="{date_txt}"> {g.period} </td>
                    <td> {tg_gem} </td>
                    <td> {heat_ndx}  {h.table_heat_ndx(g.warmte_getal['lijst'], -1)} </td>
                    <td> {tx_max}    {h.table_extremes(g.tx_max['lijst'][-1:], -1)} </td>
                    <td> {tg_max}    {h.table_extremes(g.tg_max['lijst'][-1:], -1)} </td>
                    <td> {tn_max}    {h.table_extremes(g.tn_max['lijst'][-1:], -1)} </td>
                    <td> {tg_gte_20} {h.table_count(g.tg_gte_20['lijst'], -1)} </td>
                    <td> {tx_gte_20} {h.table_count(g.tx_gte_20['lijst'], -1)} </td>
                    <td> {tx_gte_25} {h.table_count(g.tx_gte_25['lijst'], -1)} </td>
                    <td> {tx_gte_30} {h.table_count(g.tx_gte_30['lijst'], -1)} </td>
                    <td> {tx_gte_35} {h.table_count(g.tx_gte_35['lijst'], -1)} </td>
                    <td> {tg_gte_18} {h.table_count(g.tg_gte_18['lijst'], -1)} </td>
                    <td> {tn_gte_20} {h.table_count(g.tn_gte_20['lijst'], -1)} </td>
                    <td> {sq_tot} </td>
                    <td> {sq_gte_10} {h.table_count(g.sq_gte_10['lijst'], -1)} </td>
                    <td> {rh_tot} </td>
                    <td> {rh_gte_10} {h.table_count(g.rh_gte_10['lijst'], -1)} </td>
                </tr>
                '''

    if type in ['txt','cmd']:
        content += bronvermelding

    if type == 'html':
        content += f'''
            </tbody>
            <tfoot> <tr> <td colspan="19"> {bronvermelding} </td> </tr> </tfoot>
        </table>'''

        css = r.get_string_css_from_file( 'default-table-statistics.css' ) # Get css from file
        content = h.pagina(title, css, content) # Make html page
        content = fn.clean_s(content) # Remove unnecessary whitespace

    if type == 'cmd':
        fn.lnprintln(cfg.line + cfg.ln + content + cfg.ln + cfg.line)

    if type in ['html','txt']:
        file_name = fn.mk_path(path, name) # Make file name
        wr.write_to_file(file_name, content) # Schrijf naar bestand

    return file_name
