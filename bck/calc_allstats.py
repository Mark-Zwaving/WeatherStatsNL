# -*- coding: utf-8 -*-
'''Library contains classes and functions for calculating summerstatistics'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.2"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config as c, fn, fn_html as h, calc_stats as st, dates as d
import write as wr, ask, fn_read as r, knmi

# Make constraints to show or to hide. Set constraint to True when adding constraints
# See Class SummerStats: below for the possible entities to put constraints on
def show ( stats ):
    hidden, show = False, True

    # To add 1 or more constraint(s). Set constraint to True
    constraint = False

    if constraint:
        show = False # Hidden en show are both False now

        # Code here your constraints
        # Example: hellman >= 20 and with at least one day with a TN lower -10
        if  stats.hellmann['value'] >= 200 and \
            stats.tn_lt__10['value'] > 0:
            show = True

        #End of coding constraints

    return show and not hidden # Both must be True

class AllStats:
    '''Class saves en stores summer statistics of a station in a given period'''
    def __init__(self, station, etm_l):
        self.station    = station
        self.etm_l      = etm_l
        self.date_start = etm_l[0].YYYYMMDD
        self.date_end   = etm_l[-1].YYYYMMDD
        self.period     = f'{self.date_start}-{self.date_end}'
        self.place      = station.plaats
        self.province   = station.provincie
        self.wmo        = station.wmo
        self.hellmann   = st.hellmann(etm_l)  # Dictionary { 'value', 'list_all_days' }
        self.heat_sum   = st.heat_sum(etm_l)  # Dictionary { 'value', 'list_all_days' }
        self.tg_gem     = st.mean(etm_l,'TG') # Dictionary { 'value', 'list_all_days' }
        self.tx_max     = st.max(etm_l,'TX')  # Dictionary { 'value', 'list_all_days' }
        self.tg_max     = st.max(etm_l,'TG')  # Dictionary { 'value', 'list_all_days' }
        self.tn_max     = st.max(etm_l,'TN')  # Dictionary { 'value', 'list_all_days' }
        self.tx_min     = st.min(etm_l,'TX')  # Dictionary { 'value', 'list_all_days' }
        self.tg_min     = st.min(etm_l,'TG')  # Dictionary { 'value', 'list_all_days' }
        self.tn_min     = st.min(etm_l,'TN')  # Dictionary { 'value', 'list_all_days' }
        self.tx_gte_20  = st.cnt(etm_l,'TX','≥',200)  # Warme dag  # Dictionary { 'value', 'list_all_days' }
        self.tx_gte_25  = st.cnt(etm_l,'TX','≥',250)  # Zomerse dag  # Dictionary { 'value', 'list_all_days' }
        self.tx_gte_30  = st.cnt(etm_l,'TX','≥',300)  # Tropische dag  # Dictionary { 'value', 'list_all_days' }
        self.tx_gte_35  = st.cnt(etm_l,'TX','≥',350)  # Tropische  # Dictionary { 'value', 'list_all_days' }
        self.tx_gte_40  = st.cnt(etm_l,'TX','≥',400)  # Tropische  # Dictionary { 'value', 'list_all_days' }
        self.tg_gte_18  = st.cnt(etm_l,'TG','≥',180)  # Warmte getal dag  # Dictionary { 'value', 'list_all_days' }
        self.tn_gte_20  = st.cnt(etm_l,'TN','≥',200)  # Tropen nacht  # Dictionary { 'value', 'list_all_days' }
        self.tx_lt_0    = st.cnt(etm_l,'TX','<',0)    # IJsdag  # Dictionary { 'value', 'list_all_days' }
        self.tg_lt_0    = st.cnt(etm_l,'TG','<',0)    # Dictionary { 'value', 'list_all_days' }
        self.tn_lt_0    = st.cnt(etm_l,'TN','<',0)    # Vorstdag  # Dictionary { 'value', 'list_all_days' }
        self.tn_lt__5   = st.cnt(etm_l,'TN','<',-50)  # Matige vorst  # Dictionary { 'value', 'list_all_days' }
        self.tn_lt__10  = st.cnt(etm_l,'TN','<',-100) # Strenge vorst  # Dictionary { 'value', 'list_all_days' }
        self.tn_lt__15  = st.cnt(etm_l,'TN','<',-150) # Zeer strenge vorst  # Dictionary { 'value', 'list_all_days' }
        self.tn_lt__20  = st.cnt(etm_l,'TN','<',-200) # Zeer strenge vorst  # Dictionary { 'value', 'list_all_days' }
        self.sq_gte_10  = st.cnt(etm_l,'SQ','≥',100)  # Zonuren > 10  # Dictionary { 'value', 'list_all_days' }
        self.sq_tot     = st.sum(etm_l,'SQ')          # Som zonuren  # Dictionary { 'value', 'list_all_days' }
        self.rh_gte_10  = st.cnt(etm_l,'RH','≥',100)  # Regen > 10mm  # Dictionary { 'value', 'list_all_days' }
        self.rh_tot     = st.sum(etm_l,'RH')          # Som regen mm  # Dictionary { 'value', 'list_all_days' }

def sort_allstats_num(lijst, pm = '+'):
    sorted = []
    while lijst:
        max, key = c.min_value_geg, 0
        # Haal key minimum waarde uit lijst
        for i in range(len(lijst)):
            val = lijst[i].tg_gem['value']
            if val > max:
                max = val; key = i
        sorted.append(lijst[key]) # Voeg waarde toe
        del lijst[key] # Verwijder max waarde uit lijst
    return sorted if pm == '+' else sorted.reverse()

def alg_allstats(lijst_stations, date_start, date_end, name, type):
    '''Hoofdfunctie voor het berekenen van de zomerstats'''
    all_geg, periode, path, content = [], f'{date_start}-{date_end}', '', ''
    bronvermelding = lijst_stations[0].notification
    max_rows = c.html_popup_table_max_rows

    # Filename
    if not name:
        name = f'All statistics {periode}'

    title = name
    file_name = ''

    if type == 'html':
        name = f'{name}.html'
        path = c.dir_html_allstats

    if type == 'txt':
        name = f'{name}.txt'
        path = c.dir_text_allstats

    for station in lijst_stations:
        l = fn.select_dates_from_list( r.knmi_etmgeg_data(station),
                                       date_start, date_end )
        if not l: # Geen data gevonden, naar de volgende
            continue
        else:
            print(f"Calculate all statistics for station: {station.wmo} {station.plaats}")
            # Vul Winterstats object met  waarden en voegtoe aan lijst
            all_geg.append( AllStats( station, l ))

    fn.lnprintln(f'...Preparing output ({type})...')

    all_geg = sort_allstats_num(all_geg,'+') # Sorteer op tg

    # Maak content op basis van type uitvoer html of text
    # Maak titel
    if type in ['txt','cmd']:
        s = ' '
        content = f'PLAATS{s:15} PROVINCIE{s:7} PERIODE{s:11} TG      ∑WARMTE HELLMANN' \
                  f'TX MAX  TG MAX  TN MAX  TX MIN  TG MIN  TN MIN  ' \
                  f'TX≥20 TX≥25 TX≥30 TX≥35 TX≥35 TG≥20 TG≥18 TN≥20 '\
                  f'ZON≥10 ∑ZON       REGEN≥10 ∑REGEN  \n'

    if type == 'html':
        colspan = 30
        content = f'''
        <table>
            <thead>
            <tr> <th colspan="{colspan}"> {title} </th> </tr>
            <tr>
                <th> plaats </th>
                <th> provincie </th>
                <th> periode </th>
                <th> tg </th>
                <th title="Warmte getal"> warmte </th>
                <th title="hellmann getal"> hellmann </th>
                <th title="Warmste dag"> tx max </th>
                <th title="Hoogste gemiddelde"> tg max </th>
                <th title="Hoogste minimum"> tn max </th>
                <th title="Laagste maximum"> tx min </th>
                <th title="Laagste gemiddelde"> tg min </th>
                <th title="Laagste minimum"> tn min </th>
                <th title="Aantal warme dagen"> tx&ge;20 </th>
                <th title="Aantal zomers dagen"> tx&ge;25 </th>
                <th title="Aantal tropische dagen"> tx&ge;30 </th>
                <th title="Aantal tropische dagen"> tx&ge;35 </th>
                <th title="Aantal tropische dagen"> tx&ge;40 </th>
                <th title="Aantal tropennachten"> tn&ge;20 </th>
                <th title="Warmte getal dagen"> tg&ge;18 </th>
                <th title="vorstdag"> TX&lt;0 </th>
                <th title="hellmandag"> TG&lt;0 </th>
                <th title="ijsdag"> TN&lt;0 </th>
                <th title="matige vorst"> TN&lt;-5 </th>
                <th title="strenge vorst"> TN&lt;-10 </th>
                <th title="zeer strenge vorst"> TN&lt;-15 </th>
                <th title="zeer strenge vorst"> TN&lt;-20 </th>
                <th title="Totaal aantal uren zon"> zon </th>
                <th title="Dagen met meer dan tien uur zon"> zon&ge;10hour</th>
                <th title="Totaal aantal mm regen"> regen </th>
                <th title="Dagen met meer dan tien mm regen"> regen&ge;10mm</th>
            </tr>
            </thead>
            <tbody>
        '''

    # Walkthrough all cities
    for g in all_geg:
        # Show see function start at page
        if show(g):
            heat     = g.heat_sum['value']
            heat_sum = '.' if not heat else fn.rm_s(fn.fix(heat, 'heat_ndx'))
            hellmann = g.hellmann['value']
            hellmann_sum = '.' if not hellmann else fn.rm_s(fn.fix(hellmann, 'hellmann'))  # hellmann
            tg_gem = '.' if not g.tg_gem['value'] else fn.rm_s(fn.fix(g.tg_gem['value'],'tg'))
            tx_max = '.' if not g.tx_max['value'] else fn.rm_s(fn.fix(g.tx_max['value'],'tx'))
            tg_max = '.' if not g.tg_max['value'] else fn.rm_s(fn.fix(g.tg_max['value'],'tg'))
            tn_max = '.' if not g.tn_max['value'] else fn.rm_s(fn.fix(g.tn_max['value'],'tn'))
            rh_tot = '.' if not g.rh_tot['value'] else fn.rm_s(fn.fix(g.rh_tot['value'],'rh'))
            sq_tot = '.' if not g.sq_tot['value'] else fn.rm_s(fn.fix(g.sq_tot['value'],'sq'))
            tx_min = '.' if not g.tx_min['value'] else fn.rm_s(fn.fix(g.tx_min['value'],'tx'))
            tg_min = '.' if not g.tg_min['value'] else fn.rm_s(fn.fix(g.tg_min['value'],'tg'))
            tn_min = '.' if not g.tn_min['value'] else fn.rm_s(fn.fix(g.tn_min['value'],'tn'))
            tx_gte_20 = str(g.tx_gte_20['value'])
            tx_gte_25 = str(g.tx_gte_25['value'])
            tx_gte_30 = str(g.tx_gte_30['value'])
            tx_gte_35 = str(g.tx_gte_35['value'])
            tx_gte_40 = str(g.tx_gte_40['value'])
            tg_gte_18 = str(g.tg_gte_18['value'])
            tn_gte_20 = str(g.tn_gte_20['value'])
            sq_gte_10 = str(g.sq_gte_10['value'])
            rh_gte_10 = str(g.rh_gte_10['value'])
            tx_lt_0   = str(g.tx_lt_0['value'])
            tg_lt_0   = str(g.tg_lt_0['value'])
            tn_lt_0   = str(g.tn_lt_0['value'])
            tn_lt__5  = str(g.tn_lt__5['value'])
            tn_lt__10 = str(g.tn_lt__10['value'])
            tn_lt__15 = str(g.tn_lt__15['value'])
            tn_lt__20 = str(g.tn_lt__20['value'])

            if type in ['txt','cmd']:
                content += f"{g.place:<21} {g.province:<16} {g.period:<18} "
                content += f"{tg_gem:<7} {heat_sum:<10} {hellmann_sum:^10} "
                content += f"{tx_max:<7} {tg_max:<7} {tn_max:<7} {tx_min:<7} {tg_min:<7} {tn_min:<7} "
                content += f"{tx_gte_20:^6} {tx_gte_25:^6} {tx_gte_30:^6} {tx_gte_35:^6} "
                content += f"{tg_gte_20:^6} {tg_gte_18:^6} {tn_gte_20:^6} "
                content += f"{tx_lt_0:^5} {tg_lt_0:^5} {tn_lt_0:^5} {tn_lt__5:^6} "
                content += f"{tn_lt__10:^6} {tn_lt__15:^6} {tn_lt__20:^6} "
                content += f"{sq_gte_10:^7} {sq_tot:<10} {rh_gte_10:^9} {rh_tot:<11} \n"

            if type == 'html':
                date_txt = f"{d.Datum(g.date_start).tekst()} - {d.Datum(g.date_end).tekst()}"
                html_heat_sum   = h.table_heat_ndx(g.heat_sum['list_all_days'], max_rows)
                html_hellmann   = h.table_hellmann(g.hellmann['list_all_days'], max_rows)
                html_tx_max     = h.table_extremes(g.tx_max['list_all_days'], max_rows)
                html_tg_max     = h.table_extremes(g.tg_max['list_all_days'], max_rows)
                html_tn_max     = h.table_extremes(g.tn_max['list_all_days'], max_rows)
                html_tx_min     = h.table_extremes(g.tx_min['list_all_days'], max_rows)
                html_tg_min     = h.table_extremes(g.tg_min['list_all_days'], max_rows)
                html_tn_min     = h.table_extremes(g.tn_min['list_all_days'], max_rows)
                html_tx_gte_20  = h.table_count(g.tx_gte_20['list_all_days'], max_rows)
                html_tx_gte_25  = h.table_count(g.tx_gte_25['list_all_days'], max_rows)
                html_tx_gte_30  = h.table_count(g.tx_gte_30['list_all_days'], max_rows)
                html_tx_gte_35  = h.table_count(g.tx_gte_35['list_all_days'], max_rows)
                html_tx_gte_40  = h.table_count(g.tx_gte_40['list_all_days'], max_rows)
                html_tn_gte_20  = h.table_count(g.tn_gte_20['list_all_days'], max_rows)
                html_tg_gte_18  = h.table_count(g.tg_gte_18['list_all_days'], max_rows)
                html_tx_lt_0    = h.table_count(g.tx_lt_0['list_all_days'], max_rows)
                html_tg_lt_0    = h.table_count(g.tg_lt_0['list_all_days'], max_rows)
                html_tn_lt_0    = h.table_count(g.tn_lt_0['list_all_days'], max_rows)
                html_tn_lt__5   = h.table_count(g.tn_lt__5['list_all_days'], max_rows)
                html_tn_lt__10  = h.table_count(g.tn_lt__10['list_all_days'], max_rows)
                html_tn_lt__15  = h.table_count(g.tn_lt__15['list_all_days'], max_rows)
                html_tn_lt__20  = h.table_count(g.tn_lt__20['list_all_days'], max_rows)
                html_sq_gte_10  = h.table_count(g.sq_gte_10['list_all_days'], max_rows)
                html_rh_gte_10  = h.table_count(g.rh_gte_10['list_all_days'], max_rows)

                content += f'''
                    <tr>
                        <td> {g.place} </td>
                        <td> {g.province} </td>
                        <td title="{date_txt}"> {g.period} </td>
                        <td> {tg_gem} </td>
                        <td> {heat_sum}  {html_heat_sum} </td>
                        <td> {hellmann_sum}  {html_hellmann} </td>

                        <td> {tx_max}    {html_tx_max} </td>
                        <td> {tg_max}    {html_tg_max} </td>
                        <td> {tn_max}    {html_tn_max} </td>
                        <td> {tx_min}    {html_tx_min} </td>
                        <td> {tg_min}    {html_tg_min} </td>
                        <td> {tn_min}    {html_tn_min} </td>

                        <td> {tx_gte_20} {html_tx_gte_20} </td>
                        <td> {tx_gte_25} {html_tx_gte_25} </td>
                        <td> {tx_gte_30} {html_tx_gte_30} </td>
                        <td> {tx_gte_35} {html_tx_gte_35} </td>
                        <td> {tx_gte_40} {html_tx_gte_40} </td>
                        <td> {tn_gte_20} {html_tn_gte_20} </td>
                        <td> {tg_gte_18} {html_tg_gte_18} </td>
                        <td> {tx_lt_0}   {html_tx_lt_0} </td>
                        <td> {tg_lt_0}   {html_tg_lt_0} </td>
                        <td> {tn_lt_0}   {html_tn_lt_0} </td>
                        <td> {tn_lt__5}  {html_tn_lt__5} </td>
                        <td> {tn_lt__10} {html_tn_lt__10} </td>
                        <td> {tn_lt__15} {html_tn_lt__15} </td>
                        <td> {tn_lt__20} {html_tn_lt__20} </td>

                        <td> {sq_tot} </td>
                        <td> {sq_gte_10} {html_sq_gte_10} </td>
                        <td> {rh_tot} </td>
                        <td> {rh_gte_10} {html_rh_gte_10} </td>
                    </tr>
                    '''
            # End show

    if type in ['txt','cmd']:
        content += bronvermelding

    if type == 'html':
        content += f'''
            </tbody>
            <tfoot> <tr> <td colspan="{colspan}"> {bronvermelding} </td> </tr> </tfoot>
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
