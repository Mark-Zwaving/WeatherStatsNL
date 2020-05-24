# -*- coding: utf-8 -*-
'''Library contains classes and functions to calculate heatwave statistics'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9.4"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import ask, config as cfg, fn, calc_stats as st, calc_sommerstats as zs
import write as wr, fn_html as h, dates as d, fn_read as r, ask as a
import numpy as np, plot
from matplotlib import pyplot as plt

# Make constraints to show or to hide. Set constraint to True when adding constraints
# See Class HeatwaveStats: below for the possible entities to put constraints on
def show ( heatwave ):
    hidden, show = False, True
    # To add 1 or more constraint(s). Set constraint to True
    constraint = False

    if constraint:
        show = False # Hidden en show are both False now

        # Code here your constraints

        if  heatwave.day_count >= 6 and \
            heatwave.tx_gte_30['value'] >= 6:
            show = True

        #End of coding constraints

    return show and not hidden # Both must be True


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
        self.heat_sum     =  st.heat_sum(etm_l) # Dictionary { 'value', 'list_all_days' }
        self.heat_sum_tot =  self.heat_sum['value']
        self.day_count    =  len(etm_l)
        self.tn_ave       =  st.mean(etm_l,'TN') # Dictionary { 'value', 'list_all_days' }
        self.tg_ave       =  st.mean(etm_l,'TG') # Dictionary { 'value', 'list_all_days' }
        self.tx_ave       =  st.mean(etm_l,'TX') # Dictionary { 'value', 'list_all_days' }
        self.sq_sum       =  st.sum(etm_l,'SQ') # Dictionary { 'value', 'list_all_days' }
        self.tx_max       =  st.max(etm_l,'TX') # Dictionary { 'value', 'list_all_days' }
        self.tg_max       =  st.max(etm_l,'TG') # Dictionary { 'value', 'list_all_days' }
        self.tn_max       =  st.max(etm_l,'TN') # Dictionary { 'value', 'list_all_days' }
        self.tx_gte_30    =  st.cnt(etm_l,'TX','>=',300) # Dictionary { 'value', 'list_all_days' }
        self.tx_gte_35    =  st.cnt(etm_l,'TX','>=',350) # Dictionary { 'value', 'list_all_days' }
        self.tx_gte_40    =  st.cnt(etm_l,'TX','>=',400) # Dictionary { 'value', 'list_all_days' }

def sort_heatwave_list(heatwaves, pm = '+'):
    sorted = []
    while heatwaves: # Check alle hittegolven
        days_max = 0
        heat_max = cfg.min_value_geg
        key = 0

        # Doorloop de hele lijst en haal de key van maximum waarde uit de lijst
        for ndx in range(len(heatwaves)):
            days_act = heatwaves[ndx].day_count
            heat_act = heatwaves[ndx].heat_sum_tot

            if days_act > days_max:
                days_max = days_act
                heat_max = heat_act
                key = ndx
            elif days_act == days_max:
                if heat_act > heat_max:
                    heat_max = heat_act
                    days_max = days_act
                    key = ndx

        sorted.append(heatwaves[key]) # Voeg maximum waarde toe
        del heatwaves[key] # Verwijder max waarde uit lijst

    return sorted

def alg_heatwaves(lijst_station, ymd_s, ymd_e, type, name):
    '''Main function calculating heatwaves'''
    heatwave_lists, heatwaves, periode, path, content = [] ,[], f'{ymd_s}-{ymd_e}', '', ''
    bronvermelding = cfg.lijst_stations[0].notification
    max_rows = cfg.html_popup_table_max_rows

    # Name
    if not name: name = f'heatwaves-{periode}-{d.act_datetime_unique()}'
    title = f'Heatwaves {periode}'
    filename = ''

    if type == 'html':
        name = f'{name}.html'
        path = cfg.dir_html_heatwaves
    if type == 'txt':
        name = f'{name}.txt'
        path = cfg.dir_text_heatwaves

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

        # Make images
        graphs  = []
        legends = [] # Legenda
        for heatwave in heatwave_lists:
            legends.append(heatwave.place)
            print(f"...Make image for {heatwave.place}...")
            x_label = ''
            y_label = heatwave.place
            x_data_ymd = fn.get_list_X_from_list_EtmGeg(heatwave.etm_l, 'YYYYMMDD')
            y_data_tx  = fn.get_list_X_from_list_EtmGeg(heatwave.etm_l, 'TX')
            y_data_tx  = [int(x)/10 for x in y_data_tx] # Divide by 10
            graphs.append(plot.Plot(y_data_tx, x_data_ymd, y_label))

        plot.graph( graphs,
                    f'Heatwaves\nperiod {periode}',
                    'DATES\n(yyyymmdd)',
                    'TX  \n°C  ',
                    cfg.dir_images_heatwaves,
                    f'{name}.png',
                    [24.0,42.0],
                    False
                    )

        content = ''
        # Make start/header of content
        if type == 'html':
            colspan = 15
            content = f'''
            <table>
                <thead>
                <tr> <th colspan="{colspan}"> {title} </th> </tr>
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
                    <th title="Aantal 35 plus dagen"> tx&ge;35 </th>
                    <th title="Aantal 40 plus dagen"> tx&ge;40</th>
                    <th title="Aantal zonuren"> ∑zon </th>
                </tr>
                </thead>
                <tbody>
            '''

        if type in ['txt','cmd']:
            content  = f"PLAATS{' ':24} PERIODE{' ':10} ∑WARMTE ∑DAG  TX MAX    TN MAX   " \
                        "TX GEM   TG       TN GEM TX≥30  TX≥35  TX≥40 ZON TOT\n"
            # content += f"DATUMS & TEMPS "
            #content += cfg.ln

        for heatwave in heatwave_lists:
            # Show or not
            if show(heatwave):
                heat_ndx   =  fn.rm_s(fn.fix(heatwave.heat_sum_tot,'heat_ndx'))
                tn_ave     =  fn.rm_s(fn.fix(heatwave.tn_ave['value'],'tg'))
                tg_ave     =  fn.rm_s(fn.fix(heatwave.tg_ave['value'],'tg'))
                tx_ave     =  fn.rm_s(fn.fix(heatwave.tx_ave['value'],'tx'))
                tx_max     =  fn.rm_s(fn.fix(heatwave.tx_max['value'],'tx'))
                tg_max     =  fn.rm_s(fn.fix(heatwave.tg_max['value'],'tg'))
                tn_max     =  fn.rm_s(fn.fix(heatwave.tn_max['value'],'tn'))
                sq_sum     =  fn.rm_s(fn.fix(heatwave.sq_sum['value'],'sq'))
                tx_gte_30  =  str(heatwave.tx_gte_30['value'])
                tx_gte_35  =  str(heatwave.tx_gte_35['value'])
                tx_gte_40  =  str(heatwave.tx_gte_40['value'])

                if type == 'html':
                    date_txt = f"{d.Datum(heatwave.date_start).tekst()} - {d.Datum(heatwave.date_end).tekst()}"
                    content += f'''
                        <tr>
                            <td> {heatwave.place} </td>
                            <td> {heatwave.province} </td>
                            <td title="{date_txt}"> {heatwave.period} </td>
                            <td> {heatwave.day_count} {h.table_list_heatwave_days(heatwave.etm_l, max_rows)} </td>
                            <td> {heat_ndx} </td>
                            <td> {tx_max} {h.table_extremes(heatwave.tx_max['list_all_days'][-1:], max_rows)} </td>
                            <td> {tg_max} {h.table_extremes(heatwave.tg_max['list_all_days'][-1:], max_rows)} </td>
                            <td> {tn_max} {h.table_extremes(heatwave.tn_max['list_all_days'][-1:], max_rows)} </td>
                            <td> {tx_ave} </td>
                            <td> {tg_ave} </td>
                            <td> {tn_ave} </td>
                            <td> {tx_gte_30} {h.table_count(heatwave.tx_gte_30['list_all_days'], max_rows)} </td>
                            <td> {tx_gte_35} {h.table_count(heatwave.tx_gte_35['list_all_days'], max_rows)} </td>
                            <td> {tx_gte_40} {h.table_count(heatwave.tx_gte_40['list_all_days'], max_rows)} </td>
                            <td> {sq_sum} </td>
                        </tr> '''

                if type in ['txt','cmd']:
                    txt_datum_temps = ''
                    for etm in heatwave.etm_l:
                        txt_datum_temps += f"{etm.YYYYMMDD[4:]}|TX:{fn.fix(etm.TX,'tx')}"

                    content += f"{heatwave.place:<30} {heatwave.period:<17} {heat_ndx:^7} {heatwave.day_count:^4} "
                    content += f"{tx_max:^8}  {tn_max:^8} {tn_max:^8} {tx_ave:^8} {tg_ave:^8} "
                    content += f"{tn_ave:^8} {tx_gte_30:^5} {tx_gte_35:^5} {tx_gte_40:^5} {sq_sum:<9}\n"
                    # content += txt_datum_temps
                    #content += cfg.ln

            # End show

        # Close of content
        if type == 'html':
            content += f'''
                </tbody>
                <tfoot> <tr> <td colspan="{colspan}"> {bronvermelding} </td> </tr> </tfoot>
            </table> '''

            css = r.get_string_css_from_file( 'default-table-statistics.css' ) # Get css from file
            content = h.pagina(title, css, content) # Make html page
            content = fn.clean_s(content) # Remove unnecessary whitespace

        if type in ['txt','cmd']:
            content += bronvermelding

    else: # No heatwaves found
        content = f'Voor de opgegeven periode: {periode} zijn geen hittegolven gevonden...'
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
