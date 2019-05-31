# -*- coding: utf-8 -*-
'''Library contains classes and functions to calculate heatwave statistics'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import ask, config as cfg, fn, calc_stats as st, calc_sommerstats as zs
import write as wr, fn_html as h, dates as d, fn_read as r, ask as a

def sort_heatwave_list(heatwaves, pm = '+'):
    if cfg.debug:
        a.pause(f'''
        sort_heatwave_list(heatwaves, pm = '+'):
        ''')
    sorted = []
    while heatwaves: # Check alle hittegolven
        days_max = 0
        heat_max = cfg.min_value_geg
        key = 0

        # Doorloop de hele lijst en haal de key van maximum waarde uit de lijst
        for ndx in range(len(heatwaves)):
            days_act = heatwaves[ndx].day_count
            heat_act = heatwaves[ndx].tot_heat_sum
            if cfg.debug:
                a.pause(f'''
                days_act: {days_act}
                heat_act: {heat_act}
                ''')

            if days_act > days_max:
                days_max = days_act
                heat_act = heat_max
                key = ndx
            # else:
            #     if days_act == days_max:
            #         if heat_act >= heat_max:
            #             heat_act = heat_max
            #             days_max = days_act
            #             key = ndx
            #     elif days_act < days_max:
            #         if heat_act >= heat_max:
            #             heat_act = heat_max
            #             days_max = days_act
            #             key = ndx

        if cfg.debug:
            a.pause(f'''
            key = {key}
            days_act: {heatwaves[key].day_count}
            heat_act: {heatwaves[key].tot_heat_sum}
            ''')

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
            heatwave_lists.append(st.get_list_heatwaves(station, l))

    if cfg.debug:
        a.pause(f'Count heatwaves: {len(heatwave_lists)}')
        for lists in heatwave_lists: # contains lists with heatwave
            for heat in lists: # get the Heatwaves
                a.pause(f'''
    Station: {heat.station.plaats}
    Heatsum: {heat.tot_heat_sum}
    Day count: {heat.day_count}
                ''')
                a.stop()

    heatwaves = []
    for heatwavelists in heatwave_lists:
        for heatwave in heatwavelists:
            heatwaves.append(heatwave)

    # Check eerst of er überhaupt hittegolven zijn
    if heatwaves:
        heatwaves = sort_heatwave_list(heatwaves, '+') # Sort on warmtegetal and count

        fn.lnprintln(f"...Preparing output ({type})...")

        content = ''
        # Make start/header of content
        if type == 'html':
            content  = f'''
            <table>
                <thead>
                <tr> <th colspan="13"> {title} </th> </tr>
                <tr>
                    <th> plaats </th>
                    <th> provincie </th>
                    <th title="Periode hittegolf"> periode </th>
                    <th title="Aantal dagen"> ∑dagen </th>
                    <th title="Warmte getal: totaal en gemiddelde"> ∑warmte </th>
                    <th title="Warmste dag"> tx max </th>
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

        if type =='txt' or type == 'cmd':
            content  = f"PLAATS{' ':24} PERIODE{' ':10} ∑WARMTE ∑DAG  TX MAX    TN MAX   " \
                        "TX GEM   TG       TN GEM TX≥30  TX≥35 ZON TOT\n"
            # content += f"DATUMS & TEMPS "
            #content += cfg.ln

        for heatwave in heatwaves:

            etm_l = heatwave.etmgeg_list
            ymds = etm_l[0].YYYYMMDD
            ymde = etm_l[-1].YYYYMMDD
            plaats    = f'{heatwave.station.plaats}'
            province  = f' {heatwave.station.provincie}'
            periode   = f'{ymds}-{ymde}'
            tn_ave    = fn.rm_s(fn.fix(st.gem_val(etm_l,'TN')['gem'], 'tn'))
            tg_ave    = fn.rm_s(fn.fix(st.gem_val(etm_l,'TG')['gem'], 'tg'))
            tx_ave    = fn.rm_s(fn.fix(st.gem_val(etm_l,'TX')['gem'], 'tx'))
            sq_sum    = fn.rm_s(fn.fix(st.som_val(etm_l,'SQ')['som'], 'sq'))

            tx_max    = st.max_val(etm_l,'TX')
            tn_max    = st.max_val(etm_l,'TN')
            tx_max_val = fn.rm_s(fn.fix(tx_max['max'],'tx'))
            tn_max_val = fn.rm_s(fn.fix(tn_max['max'],'tn'))

            tx_gte_30 = st.cnt_day(etm_l,'TX','>=',300)
            tx_gte_35 = st.cnt_day(etm_l,'TX','>=',350)
            cnt_tx_gte_30 = str(tx_gte_30['tel'])
            cnt_tx_gte_35 = str(tx_gte_35['tel'])

            datum_txt = f"{d.Datum(ymds).tekst()} - {d.Datum(ymde).tekst()}"
            heat_ndx  = fn.rm_s(fn.fix(heatwave.tot_heat_sum, 'heat_ndx'))

            if type == 'html':
                html_days = f'{heatwave.day_count}{h.table_list_heatwave_days(heatwave.etmgeg_list, -1)}'
                html_tx_gte_30 = cnt_tx_gte_30 + h.table_count(tx_gte_30['lijst'], -1)
                html_tx_gte_35 = cnt_tx_gte_35 + h.table_count(tx_gte_35['lijst'], -1)
                html_tx_max = tx_max_val + h.table_extremes(tx_max['lijst'][-1:], -1)
                html_tn_max = tn_max_val + h.table_extremes(tn_max['lijst'][-1:], -1)

                content += f'''
                    <tr>
                        <td> {plaats} </td> <td> {province} </td>
                        <td title="{datum_txt}"> {periode} </td>
                        <td> {html_days} </td> <td> {heat_ndx} </td>
                        <td> {html_tx_max} </td> <td> {html_tn_max} </td>
                        <td> {tx_ave} </td> <td> {tg_ave} </td>
                        <td> {tn_ave} </td> <td> {html_tx_gte_30} </td>
                        <td> {html_tx_gte_35} </td> <td> {sq_sum} </td>
                    </tr>
                '''

            if type =='txt' or type == 'cmd':
                txt_datum_temps = ''
                for etm in etm_l:
                    txt_datum_temps += f"{etm.YYYYMMDD[-4:]}|TX:{fn.fix(etm.TX,'tx')}"

                content += f"{plaats:<30} {periode:<17} {heat_ndx:^7} {heatwave.day_count:^4} "
                content += f"{tx_max_val:^8}  {tn_max_val:^8} {tx_ave:^8} {tg_ave:^8} {tn_ave:^8} "
                content += f"{cnt_tx_gte_30:^5} {cnt_tx_gte_35:^5} {sq_sum:<9}\n"
                # content += txt_datum_temps
                #content += cfg.ln

        # Close of content
        if type =='html':
            content += f'''
                </tbody>
                <tfoot> <tr> <td colspan="13"> {bronvermelding} </td> </tr> </tfoot>
            </table> '''

            css = r.get_string_css_from_file( 'default-table-statistics.css' ) # Get css from file
            content = h.pagina(title, css, content) # Make html page
            content = fn.clean_s(content) # Remove unnecessary whitespace

        if type =='txt' or type == 'cmd':
            content += bronvermelding

    else: # No heatwaves found
        content = f'Voor {periode} zijn geen hittegolven gevonden...'
        if type =='txt':
            pass
        if type == 'html':
            content = h.pagina('Geen hittegolven', '', '<p>{content}</p>')

    if type != 'cmd':
        file_name = fn.mk_path(path, name) # Make file name
        wr.write_to_file(file_name, content) # Schrijf naar bestand
        return file_name

    if type == 'cmd':
        print(content)
