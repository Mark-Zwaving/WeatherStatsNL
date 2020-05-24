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

# Make constraints to show or to hide. Set constraint to True when adding constraints
# See Class SummerStats: below for the possible entities to put constraints on
def show ( winterstats ):
    hidden, show = False, True

    # To add 1 or more constraint(s). Set constraint to True
    constraint = False

    if constraint:
        show = False # Hidden en show are both False now

        # Code here your constraints
        # Example: hellman >= 20 and with at least one day with a TN lower -10
        if  winterstats.hellmann['value'] >= 200 and \
            winterstats.tn_lt__10['value'] > 0:
            show = True

        #End of coding constraints

    return show and not hidden # Both must be True


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
        self.tg_gem     =  st.mean(etm_l,'TG')  # Dictionary { 'value', 'list_all_days' }
        self.hellmann   =  st.hellmann(etm_l) # Dictionary { 'value', 'list_all_days' }
        self.tx_min     =  st.min(etm_l,'TX')  # Dictionary { 'value', 'list_all_days' }
        self.tg_min     =  st.min(etm_l,'TG')  # Dictionary { 'value', 'list_all_days' }
        self.tn_min     =  st.min(etm_l,'TN')  # Dictionary { 'value', 'list_all_days' }
        self.tx_lt_0    =  st.cnt(etm_l,'TX','<',0)     # Ijsdagen  # Dictionary { 'value', 'list_all_days' }
        self.tg_lt_0    =  st.cnt(etm_l,'TG','<',0)     # Hellmanndagen  # Dictionary { 'value', 'list_all_days' }
        self.tn_lt_0    =  st.cnt(etm_l,'TN','<',0)     # Lichte vorst  # Dictionary { 'value', 'list_all_days' }
        self.tn_lt__5   =  st.cnt(etm_l,'TN','<',-50)   # Matige vorst  # Dictionary { 'value', 'list_all_days' }
        self.tn_lt__10  =  st.cnt(etm_l,'TN','<',-100)  # Strenge vorst  # Dictionary { 'value', 'list_all_days' }
        self.tn_lt__15  =  st.cnt(etm_l,'TN','<',-150)  # Zeer strenge vorst  # Dictionary { 'value', 'list_all_days' }
        self.tn_lt__20  =  st.cnt(etm_l,'TN','<',-200)

def sort_winterstats_num(lijst, pm = '+'):
    sorted = []
    while lijst:
        max, key = cfg.min_value_geg, 0
        # Haal key minimum waarde uit lijst
        for i in range(len(lijst)):
            val = lijst[i].hellmann['value']

            if val > max:
                max = val; key = i

        sorted.append(lijst[key]) # Voeg waarde toe
        del lijst[key] # Verwijder min waarde uit lijst

    return sorted if pm == '+' else sorted.reverse()

def alg_winterstats(lijst_stations, datum_start, datum_eind, name, type):
    '''Hoofdfunctie voor het berekenen van de winterstatistieken'''
    bronvermelding = cfg.lijst_stations[0].notification
    winter_geg, periode, path, content = [], f'{datum_start}-{datum_eind}', '', ''
    max_rows = cfg.html_popup_table_max_rows

    # Name
    if not name: name = f'winterstatistics-{periode}-{d.act_datetime_unique()}'
    title = f'Winterstatistics {periode}'
    filename = ''

    if type == 'html':
        name = f'{name}.html'
        path = cfg.dir_html_winterstats

    if type == 'txt':
        name = f'{name}.txt'
        path = cfg.dir_text_winterstats

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
        if show(g):
            tg_gem    = fn.rm_s(fn.fix(g.tg_gem['value'],'tg'))
            tx_min    = fn.rm_s(fn.fix(g.tx_min['value'],'tx'))
            tg_min    = fn.rm_s(fn.fix(g.tg_min['value'],'tg'))
            tn_min    = fn.rm_s(fn.fix(g.tn_min['value'],'tn'))
            tx_lt_0   = str(g.tx_lt_0['value'])    # Ijsdagen
            tn_lt_0   = str(g.tn_lt_0['value'])    # Lichte vorst
            tg_lt_0   = str(g.tg_lt_0['value'])    # Hellmanndagen
            tn_lt__10 = str(g.tn_lt__10['value'])  # Strenge vort
            tn_lt__5  = str(g.tn_lt__5['value'])   # Matige vorst
            tn_lt__15 = str(g.tn_lt__15['value'])  # Zeer strenge vorst
            tn_lt__20 = str(g.tn_lt__20['value'])
            hellmann  = fn.rm_s(fn.fix(g.hellmann['value'], 'hellmann'))  # hellmann
            html_hellmann = h.table_hellmann(g.hellmann['list_all_days'], max_rows)
            html_tx_min = h.table_extremes(g.tx_min['list_all_days'], max_rows)
            html_tg_min = h.table_extremes(g.tg_min['list_all_days'], max_rows)
            html_tn_min = h.table_extremes(g.tn_min['list_all_days'], max_rows)
            html_tx_lt_0 = h.table_count(g.tx_lt_0['list_all_days'], max_rows)
            html_tg_lt_0 = h.table_count(g.tg_lt_0['list_all_days'], max_rows)
            html_tn_lt_0 = h.table_count(g.tn_lt_0['list_all_days'], max_rows)
            html_tn_lt__5 = h.table_count(g.tn_lt__5['list_all_days'], max_rows)
            html_tn_lt__10 = h.table_count(g.tn_lt__10['list_all_days'], max_rows)
            html_tn_lt__15 = h.table_count(g.tn_lt__15['list_all_days'], max_rows)
            html_tn_lt__20 = h.table_count(g.tn_lt__20['list_all_days'], max_rows)

            if type == 'html':
                dat_txt = f'{dat.Datum(g.date_start).tekst()} - {dat.Datum(g.date_end).tekst()}'
                content += f'''
                    <tr>
                        <td> {g.place} </td>
                        <td> {g.province} </td>
                        <td title="{dat_txt}"> {g.period} </td>
                        <td> {tg_gem} </td>
                        <td> {hellmann}  {html_hellmann} </td>
                        <td> {tx_min}    {html_tx_min} </td>
                        <td> {tg_min}    {html_tg_min} </td>
                        <td> {tn_min}    {html_tn_min} </td>
                        <td> {tx_lt_0}   {html_tx_lt_0} </td>
                        <td> {tg_lt_0}   {html_tg_lt_0} </td>
                        <td> {tn_lt_0}   {html_tn_lt_0} </td>
                        <td> {tn_lt__5}  {html_tn_lt__5} </td>
                        <td> {tn_lt__10} {html_tn_lt__10} </td>
                        <td> {tn_lt__15} {html_tn_lt__15} </td>
                        <td> {tn_lt__20} {html_tn_lt__20} </td>
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
