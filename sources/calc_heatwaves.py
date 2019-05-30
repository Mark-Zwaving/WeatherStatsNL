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
import write as wr, fn_html as h, dates as d, fn_read as r

class Heatwave:
    def __init__(self, station, etmgeg_list):
        self.station      = station
        self.etmgeg_list  = etmgeg_list
        self.tot_heat_sum = zs.warmte_getal(self.etmgeg_list)['getal']
        self.day_count    = len(self.etmgeg_list)

def sort_heatstats(lijst, pm = '+'):
    sorted = []
    while lijst:
        max, key = cfg.min_value_geg, 0

        # Haal key maximum waarde uit lijst
        for i in range(len(lijst)):
            val = lijst[i].tot_heat_sum
            if val > max:
                max = val; key = i

        sorted.append(lijst[key]) # Voeg maximum waarde toe
        del lijst[key] # Verwijder min waarde uit lijst

    return sorted if pm == '+' else sorted.reverse()

def list_heatwaves_station( station, etmgeg_list ):
    heatwave_list, mem_etmgeg_list = [], []
    day_count, day_heat_num = 0, 5
    day_30_1, day_30_2, day_30_3, heat = False, False, False, False

    for etmgeg in etmgeg_list:
        if etmgeg.TX != etmgeg.empthy:
            iTX = int(etmgeg.TX)
            # Check only 25+
            if iTX >= 250:
                day_count += 1 # Count 25+
                mem_etmgeg_list.append(etmgeg) # Save 25+
                if not heat: # No heatwave yet, check for it
                    # Check for 3 times 30+
                    if iTX >= 300:
                        if   not day_30_1: day_30_1 = True # First 30 true
                        elif not day_30_2: day_30_2 = True # Second 30 true
                        elif not day_30_3: day_30_3 = True # third 30 true

                        if day_30_3 and day_count >= day_heat_num:
                            heat = True # Heatwave !

                if cfg.log:
                    print( f"PLAATS:{station.plaats}|DATUM:{etmgeg.YYYYMMDD}|"
                           f"iTX(25+):{iTX}|TEL:{day_count}|HEAT:{heat}" )
            else:
                if heat == True: # Heatwave
                    # Add closed heatwave to list
                    heat_day = Heatwave( station, mem_etmgeg_list )
                    heatwave_list.append( heat_day )
                    if cfg.log:
                        heat_day = heatwave_list[-1] # last added
                        out  = 'Hittegolf afgelopen: Heatwave toegevoegd !' + cfg.ln
                        out += f'Station:{heat_day.station.plaats}' + cfg.ln
                        out += f'Start datum:{heat_day.etmgeg_list[0].YYYYMMDD}' + cfg.ln
                        out += f'Eind datum:{heat_day.etmgeg_list[-1].YYYYMMDD}' + cfg.ln
                        out += f'Tot_heat_sum:{heat_day.tot_heat_sum}' + cfg.ln
                        out += f'Day_count:{heat_day.day_count}' + cfg.ln
                        ask.ask(out)

                # Reset heatwave values
                day_count, day_30_1, day_30_2, day_30_3, heat = 0, False, False, False, False
                mem_etmgeg_list = []

        else: # Data cannot be checked.
            if heat: # Oke stop heatwave, add to list and reset values
                heat_day = Heatwave( station, mem_etmgeg_list )
                heatwave_list.append( heat_day )
                if cfg.log:
                    heat_day = heatwave_list[-1] # Last added
                    out  = 'Fout in data: heatwave geeindigd en toegevoegd' + cfg.ln
                    out += f'Station:{heat_day.station.plaats}' + cfg.ln
                    out += f'Start datum:{heat_day.etmgeg_list[0].YYYYMMDD}' + cfg.ln
                    out += f'Eind datum:{heat_day.etmgeg_list[-1].YYYYMMDD}' + cfg.ln
                    out += f'Tot_heat_sum:{heat_day.tot_heat_sum}' + cfg.ln
                    out += f'Day_count:{heat_day.day_count}' + cfg.ln
                    ask.ask(out)

            # Reset heatwave values
            day_count, day_30_1, day_30_2, day_30_3, heat = 0, False, False, False, False
            mem_etmgeg_list = []

    if heat: #Voeg hittegolf toe en is nog niet ten einde
        heat_day = Heatwave( station, mem_etmgeg_list )
        heatwave_list.append ( heat_day )
        if cfg.log:
            heat_day = heatwave_list[-1]
            out  = 'Hittegolf not niet geëindigd: Heatwave toegevoegd !' + cfg.ln
            out += f'Station:{heat_day.station.plaats}' + cfg.ln
            out += f'Start datum:{heat_day.etmgeg_list[0].YYYYMMDD}' + cfg.ln
            out += f'Eind datum:{heat_day.etmgeg_list[-1].YYYYMMDD}' + cfg.ln
            out += f'Tot_heat_sum:{heat_day.tot_heat_sum}' + cfg.ln
            out += f'Day_count:{heat_day.day_count}' + cfg.ln
            ask.ask(out)

    if cfg.log:
        ask.ask(f'Aantal gevonden hittegolven: {len(heatwave_list)}')
        print("Doorloop gevonden hittegolven")
        for heat_day in heatwave_list:
            out  = f'Start datum:{heat_day.etmgeg_list[0].YYYYMMDD}' + cfg.ln
            out += f'Eind datum:{heat_day.etmgeg_list[-1].YYYYMMDD}' + cfg.ln
            out += f'Station:{heat_day.station.plaats}' + cfg.ln
            out += f'Tot_heat_sum:{heat_day.tot_heat_sum}' + cfg.ln
            out += f'Day_count:{heat_day.day_count}'+ cfg.ln
            ask.ask(out)

    return heatwave_list

def gen_calc_heat_waves(lijst_station, ymd_s, ymd_e, type, name):
    '''Main function calculating heatwaves'''
    heatwave_list, periode, path, content = [], f'{ymd_s}-{ymd_e}', '', ''
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
            # Fill Heatwave object with values if there and add to list
            heat_list = list_heatwaves_station(station, l)
            if heat_list:
                for heat in heat_list:
                    heatwave_list.append(heat)

    # Check eerst of er überhaupt hittegolven zijn
    if heatwave_list:
        heatwave_list = sort_heatstats(heatwave_list, '+') # Sort on warmtegetal

        print(f"{cfg.ln}...Preparing output ({type})...{cfg.ln}")

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

        # Calculate heatwaves and fill content
        for heatwave in heatwave_list:
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
                heatwave.etmgeg_list
                html_days = str(heatwave.day_count) + h.table_list_heatwave_days( heatwave.etmgeg_list, -1 )
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
