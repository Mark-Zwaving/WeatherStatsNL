# -*- coding: utf-8 -*-
'''Library contains classes and functions to calculate winterstatistics'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9.3"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import write as wr, fn, calc_stats as st, config as cfg, fn_html as h
import dates as dat, fn_read as r

class AlgemeneWinterStats:
    '''Class stores and saves winter statistics of a station in a given period'''
    def __init__(self, station, etm_l ):
        self.station    =  station
        self.etm_l      =  etm_l
        self.wmo        =  station.wmo
        self.place      =  station.plaats
        self.province   =  station.provincie
        self.date_start =  etm_l[0].YYYYMMDD
        self.date_end   =  etm_l[-1].YYYYMMDD
        self.period     =  f'{self.date_start}-{self.date_end}'
        self.tg_gem     =  st.gem_val(etm_l,'TG')
        self.hellmann   =  st.hellmann_getal(etm_l)
        self.tx_min     =  st.min_val(etm_l,'TX')
        self.tg_min     =  st.min_val(etm_l,'TG')
        self.tn_min     =  st.min_val(etm_l,'TN')
        self.tx_lt_0    =  st.cnt_day(etm_l,'TX','<',0)     # Ijsdagen
        self.tg_lt_0    =  st.cnt_day(etm_l,'TG','<',0)     # Hellmanndagen
        self.tn_lt_0    =  st.cnt_day(etm_l,'TN','<',0)     # Lichte vorst
        self.tn_lt__5   =  st.cnt_day(etm_l,'TN','<',-50)   # Matige vorst
        self.tn_lt__10  =  st.cnt_day(etm_l,'TN','<',-100)  # Strenge vort
        self.tn_lt__15  =  st.cnt_day(etm_l,'TN','<',-150)  # Zeer strenge vorst
        self.tn_lt__20  =  st.cnt_day(etm_l,'TN','<',-200)

def sort_winterstats_num(lijst, pm = '+'):
    sorted = []
    while lijst:
        max, key = cfg.min_value_geg, 0
        # Haal key minimum waarde uit lijst
        for i in range(len(lijst)):
            val = lijst[i].hellmann['getal']

            if val > max:
                max = val; key = i

        sorted.append(lijst[key]) # Voeg waarde toe
        del lijst[key] # Verwijder min waarde uit lijst

    return sorted if pm == '+' else sorted.reverse()

def alg_winterstats(lijst_stations, datum_start, datum_eind, name, type):
    '''Hoofdfunctie voor het berekenen van de winterstatistieken'''
    bronvermelding = cfg.lijst_stations[0].bronvermelding
    winter_geg, periode, path, content = [], f'{datum_start}-{datum_eind}', '', ''
    max_rows = cfg.html_popup_table_max_rows

    # Name
    if not name: name = f'winter statistics {periode}'

    title = name
    file_name = ''

    if type == 'html':
        name = f'{name}.html'
        path = cfg.lijst_stations[0].dir_html

    if type == 'txt':
        name = f'{name}.txt'
        path = cfg.lijst_stations[0].dir_text

    for station in lijst_stations:
        l = fn. select_dates_from_list(r.knmi_etmgeg_data(station),
                                       datum_start, datum_eind)
        if not l: # Geen data gevonden, naar de volgende
            continue
        else:
            print(f"Calculate winter statistics for station: {station.wmo} {station.plaats}")
            # Vul Winterstats object met berekende waarden toe aan lijst met gegevens
            winter_geg.append( AlgemeneWinterStats( station, l ) )

    fn.lnprintln(f'...Preparing output ({type})...')

    winter_geg = sort_winterstats_num(winter_geg,'+') # Sorteer, alleen op hellmann

    # Head of tables
    if type in ['txt','cmd']:
        s, path = ' ', lijst_stations[0].dir_text
        content  = f'PLAATS{s:17} PROVINCIE         PERIODE{s:11} TG{s:5} HELLMANN TX MIN  ' \
                   f'TG MIN  TN MIN  TX<0  TG<0  TN<0  TN<-5  TX<-10 ' \
                   f'TX<-15 TX<-20\n'

    if type == 'html':
        content = f'''
            <table>
                <thead>
                <tr> <th colspan="15"> {title} </th> </tr>
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
                    <th title="Vorstdagen"> tn&lt;0 </th>
                    <th title="Hellmanndagen"> tg&lt;0 </th>
                    <th title="Dagen met matige vorst"> tn&lt;-5 </th>
                    <th title="Dagen met strenge vorst"> tn&lt;-10 </th>
                    <th title="Dagen met zeer strenge vorst"> tn&lt;-15 </th>
                    <th title="Dagen met zeer strenge vorst"> tn&lt;-20 </th>
                </tr>
                </thead>
                <tbody>'''

    # Calculate values
    for g in winter_geg:
        tg_gem    = fn.rm_s(fn.fix(g.tg_gem['gem'],'tg'))
        tx_min    = fn.rm_s(fn.fix(g.tx_min['min'],'tx'))
        tg_min    = fn.rm_s(fn.fix(g.tg_min['min'],'tg'))
        tn_min    = fn.rm_s(fn.fix(g.tn_min['min'],'tn'))
        tx_lt_0   = str(g.tx_lt_0['tel'])    # Ijsdagen
        tn_lt_0   = str(g.tn_lt_0['tel'])    # Lichte vorst
        tg_lt_0   = str(g.tg_lt_0['tel'])    # Hellmanndagen
        tn_lt__10 = str(g.tn_lt__10['tel'])  # Strenge vort
        tn_lt__5  = str(g.tn_lt__5['tel'])   # Matige vorst
        tn_lt__15 = str(g.tn_lt__15['tel'])  # Zeer strenge vorst
        tn_lt__20 = str(g.tn_lt__20['tel'])
        hellmann  = fn.rm_s(fn.fix(g.hellmann['getal'], 'hellmann'))  # hellmann

        if type == 'html':
            dat_txt = f'{dat.Datum(g.date_start).tekst()} - {dat.Datum(g.date_end).tekst()}'
            content += f'''
                <tr>
                    <td> {g.place} </td>
                    <td> {g.province} </td>
                    <td title="{dat_txt}"> {g.period} </td>
                    <td> {tg_gem} </td>
                    <td> {hellmann}  {h.table_hellmann(g.hellmann['lijst'], max_rows)} </td>
                    <td> {tx_min}    {h.table_extremes(g.tx_min['lijst'][-1:], max_rows)} </td>
                    <td> {tg_min}    {h.table_extremes(g.tg_min['lijst'][-1:], max_rows)} </td>
                    <td> {tn_min}    {h.table_extremes(g.tn_min['lijst'][-1:], max_rows)} </td>
                    <td> {tx_lt_0}   {h.table_count(g.tx_lt_0['lijst'], max_rows)} </td>
                    <td> {tg_lt_0}   {h.table_count(g.tg_lt_0['lijst'], max_rows)} </td>
                    <td> {tn_lt_0}   {h.table_count(g.tn_lt_0['lijst'], max_rows)} </td>
                    <td> {tn_lt__5}  {h.table_count(g.tn_lt__5['lijst'], max_rows)} </td>
                    <td> {tn_lt__10} {h.table_count(g.tn_lt__10['lijst'], max_rows)} </td>
                    <td> {tn_lt__15} {h.table_count(g.tn_lt__15['lijst'], max_rows)} </td>
                    <td> {tn_lt__20} {h.table_count(g.tn_lt__20['lijst'], max_rows)} </td>
                </tr> '''

        if type in ['txt','cmd']:
            content += f"{g.place:<23} {g.province:17} {g.period:18} {tg_gem:7} "
            content += f"{hellmann:^8} {tx_min:<7} {tg_min:<7} {tn_min:<7} "
            content += f"{tx_lt_0:^5} {tg_lt_0:^5} {tn_lt_0:^5} {tn_lt__5:^6} "
            content += f"{tn_lt__10:^6} {tn_lt__15:^6} {tn_lt__20:^6} \n"

    # Close of content
    if type in ['txt','cmd']:
        content += bronvermelding

    if type == 'html':
        content += f'''
            </tbody>
            <tfoot> <tr> <td colspan="15"> {bronvermelding} </td> </tr> </tfoot>
        </table> '''

        css = r.get_string_css_from_file( 'default-table-statistics.css' ) # Get css from file
        content = h.pagina(title, css, content) # Make html page
        content = fn.clean_s(content) # Remove unnecessary whitespace

    if type == 'cmd':
        fn.lnprintln(cfg.line + cfg.ln + content + cfg.ln + cfg.line)

    if type in ['txt','html']:
        file_name = fn.mk_path(path, name) # Make file name
        wr.write_to_file(file_name, content) # Schrijf naar bestand

    return file_name
