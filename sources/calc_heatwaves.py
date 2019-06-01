# -*- coding: utf-8 -*-
'''Library contains classes and functions to calculate heatwave statistics'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9.2"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import ask, config as cfg, fn, calc_stats as st, calc_sommerstats as zs
import write as wr, fn_html as h, dates as d, fn_read as r, ask as a

class HeatwaveStats:
    '''Class stores en calculates statistics in heatwaves'''
    def __init__(self, station, etm_l ):
        self.station      =  station
        self.etm_l        =  etm_l
        self.wmo          =  station.wmo
        self.place        =  station.plaats
        self.province     =  station.provincie
        self.date_start   =  etm_l[0].YYYYMMDD
        self.date_end     =  etm_l[-1].YYYYMMDD
        self.period       =  f'{self.date_start}-{self.date_end}'
        self.tot_heat_sum =  st.warmte_getal(etm_l)['getal']
        self.day_count    =  len(etm_l)
        self.tn_ave       =  st.gem_val(etm_l,'TN')
        self.tg_ave       =  st.gem_val(etm_l,'TG')
        self.tx_ave       =  st.gem_val(etm_l,'TX')
        self.sq_sum       =  st.som_val(etm_l,'SQ')
        self.tx_max       =  st.max_val(etm_l,'TX')
        self.tg_max       =  st.max_val(etm_l,'TG')
        self.tn_max       =  st.max_val(etm_l,'TN')
        self.tx_gte_30    =  st.cnt_day(etm_l,'TX','>=',300)
        self.tx_gte_35    =  st.cnt_day(etm_l,'TX','>=',350)

def sort_heatwave_list(heatwaves, pm = '+'):
    sorted = []
    while heatwaves: # Check alle hittegolven
        days_max = 0
        heat_max = cfg.min_value_geg
        key = 0

        # Doorloop de hele lijst en haal de key van maximum waarde uit de lijst
        for ndx in range(len(heatwaves)):
            days_act = heatwaves[ndx].day_count
            heat_act = heatwaves[ndx].tot_heat_sum

            if days_act > days_max:
                days_max = days_act
                heat_act = heat_max
                key = ndx
            elif days_act == days_max:
                if heat_act >= heat_max:
                    heat_act = heat_max
                    days_max = days_act
                    key = ndx

        sorted.append(heatwaves[key]) # Voeg maximum waarde toe
        del heatwaves[key] # Verwijder max waarde uit lijst

    return sorted

def alg_heatwaves(lijst_station, ymd_s, ymd_e, type, name):
    '''Main function calculating heatwaves'''
    heatwave_lists, heatwaves, periode, path, content = [] ,[], f'{ymd_s}-{ymd_e}', '', ''
    bronvermelding = cfg.lijst_stations[0].bronvermelding

    # Name
    if not name: name = f'heatwaves {periode}'

    title = name
    file_name = ''

    if type == 'html':
        name = f'{name}.html'
        path = cfg.lijst_stations[0].dir_html
    if type == 'txt':
        name = f'{name}.txt'
        path = cfg.lijst_stations[0].dir_text

    # Vul heat list met hittegolven
    for station in lijst_station:
        l = fn.select_dates_from_list(r.knmi_etmgeg_data(station), ymd_s, ymd_e)
        if not l:
            continue
        else:
            print(f"Calculate heatwave statistics for station: {station.wmo} {station.plaats}")
            # Check for heatwaves
            heat_etmgeg_lists = st.get_list_etmgeg_heatwaves( l )
            if heat_etmgeg_lists:
                for heatwaves in heat_etmgeg_lists:
                    heatwave_lists.append( HeatwaveStats(station, heatwaves) )

    # Check eerst of er überhaupt hittegolven zijn
    if heatwave_lists:
        heatwave_lists = sort_heatwave_list(heatwave_lists, '+') # Sort on warmtegetal and count

        fn.lnprintln(f"...Preparing output ({type})...")

        content = ''
        # Make start/header of content
        if type == 'html':
            content  = f'''
            <table>
                <thead>
                <tr> <th colspan="14"> {title} </th> </tr>
                <tr>
                    <th> plaats </th>
                    <th> provincie </th>
                    <th title="Periode hittegolf"> periode </th>
                    <th title="Aantal dagen"> ∑dagen </th>
                    <th title="Warmte getal: totaal en gemiddelde"> ∑warmte </th>
                    <th title="Warmste dag"> tx max </th>
                    <th title="Warmste gem dag"> tg max </th>
                    <th title="Warmste nacht"> tn max </th>
                    <th title="Gemiddelde maximum temperatuur"> tx ave </th>
                    <th title="Gemiddelde temperatuur"> tg </th>
                    <th title="Gemiddelde minimum temperatuur"> tn ave </th>
                    <th title="Aantal tropische dagen"> tx&ge;30 </th>
                    <th title="Aantal tropische dagen"> tx&ge;35 </th>
                    <th title="Aantal zonuren"> ∑zon </th>
                </tr>
                </thead>
                <tbody>
            '''

        if type in ['txt','cmd']:
            content  = f"PLAATS{' ':24} PERIODE{' ':10} ∑WARMTE ∑DAG  TX MAX    TN MAX   " \
                        "TX GEM   TG       TN GEM TX≥30  TX≥35 ZON TOT\n"
            # content += f"DATUMS & TEMPS "
            #content += cfg.ln

        for heatwave in heatwave_lists:
            heat_ndx   =  '.' if not heatwave.tot_heat_sum  else fn.rm_s(fn.fix(heatwave.tot_heat_sum, 'heat_ndx'))
            tn_ave     =  '.' if not heatwave.tn_ave['gem'] else fn.rm_s(fn.fix(heatwave.tn_ave['gem'],'tg'))
            tg_ave     =  '.' if not heatwave.tg_ave['gem'] else fn.rm_s(fn.fix(heatwave.tg_ave['gem'],'tg'))
            tx_ave     =  '.' if not heatwave.tx_ave['gem'] else fn.rm_s(fn.fix(heatwave.tx_ave['gem'],'tx'))
            tx_max     =  '.' if not heatwave.tx_max['max'] else fn.rm_s(fn.fix(heatwave.tx_max['max'],'tx'))
            tg_max     =  '.' if not heatwave.tg_max['max'] else fn.rm_s(fn.fix(heatwave.tg_max['max'],'tg'))
            tn_max     =  '.' if not heatwave.tn_max['max'] else fn.rm_s(fn.fix(heatwave.tn_max['max'],'tn'))
            sq_sum     =  '.' if not heatwave.sq_sum['som'] else fn.rm_s(fn.fix(heatwave.sq_sum['som'],'sq'))
            tx_gte_30  =  str(heatwave.tx_gte_30['tel'])
            tx_gte_35  =  str(heatwave.tx_gte_35['tel'])

            if type == 'html':
                date_txt = f"{d.Datum(heatwave.date_start).tekst()} - {d.Datum(heatwave.date_end).tekst()}"
                content += f'''
                    <tr>
                        <td> {heatwave.place} </td>
                        <td> {heatwave.province} </td>
                        <td title="{date_txt}"> {heatwave.period} </td>
                        <td> {heatwave.day_count} {h.table_list_heatwave_days(heatwave.etm_l, -1)} </td>
                        <td> {heat_ndx} </td>
                        <td> {tx_max} {h.table_extremes(heatwave.tx_max['lijst'][-1:], -1)} </td>
                        <td> {tg_max} {h.table_extremes(heatwave.tg_max['lijst'][-1:], -1)} </td>
                        <td> {tn_max} {h.table_extremes(heatwave.tn_max['lijst'][-1:], -1)} </td>
                        <td> {tx_ave} </td>
                        <td> {tg_ave} </td>
                        <td> {tn_ave} </td>
                        <td> {tx_gte_30} {h.table_count(heatwave.tx_gte_30['lijst'], -1)} </td>
                        <td> {tx_gte_35} {h.table_count(heatwave.tx_gte_35['lijst'], -1)} </td>
                        <td> {sq_sum} </td>
                    </tr> '''

            if type in ['txt','cmd']:
                txt_datum_temps = ''
                for etm in heatwave.etm_l:
                    txt_datum_temps += f"{etm.YYYYMMDD[4:]}|TX:{fn.fix(etm.TX,'tx')}"

                content += f"{heatwave.place:<30} {heatwave.period:<17} {heat_ndx:^7} {heatwave.day_count:^4} "
                content += f"{tx_max:^8}  {tn_max:^8} {tn_max:^8} {tx_ave:^8} {tg_ave:^8} "
                content += f"{tn_ave:^8} {tx_gte_30:^5} {tx_gte_35:^5} {sq_sum:<9}\n"
                # content += txt_datum_temps
                #content += cfg.ln

        # Close of content
        if type == 'html':
            content += f'''
                </tbody>
                <tfoot> <tr> <td colspan="14"> {bronvermelding} </td> </tr> </tfoot>
            </table> '''

            css = r.get_string_css_from_file( 'default-table-statistics.css' ) # Get css from file
            content = h.pagina(title, css, content) # Make html page
            content = fn.clean_s(content) # Remove unnecessary whitespace

        if type in ['txt','cmd']:
            content += bronvermelding

    else: # No heatwaves found
        content = f'Voor de opgegeven {periode} zijn geen hittegolven gevonden...'
        if type =='txt':
            pass
        if type == 'html':
            content = h.pagina('Geen hittegolven', '', f'<p>{content}</p>')

    if type in ['html','txt']:
        file_name = fn.mk_path(path, name) # Make file name
        wr.write_to_file(file_name, content) # Schrijf naar bestand
        return file_name

    if type == 'cmd':
        print(content)
