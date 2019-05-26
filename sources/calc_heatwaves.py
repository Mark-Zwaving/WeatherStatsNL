# -*- coding: utf-8 -*-
'''Library contains classes and functions to calculate heatwave statistics'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import ask, config as cfg, fn, calc_stats as st, calc_sommerstats as zs
import write as wr, fn_html as h, dates as d

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

def gen_calc_heat_waves(lijst_station, start_datum, eind_datum, type, name):
    '''Main function calculating heatwaves'''
    heatwave_list, periode, path, content = [], f'{start_datum}-{eind_datum}', '', ''
    bronvermelding = cfg.lijst_stations[0].bronvermelding

    # Name
    if not name:
        name = f'heatwaves {periode}'

    title = name

    if type == 'html':
        name = f'{name}.html'
        path = cfg.lijst_stations[0].dir_html
    elif type == 'txt':
        name = f'{name}.txt'
        path = cfg.lijst_stations[0].dir_text

    file_name = fn.mk_path(path, name) # Make file name

    # Vul heat list met hittegolven
    for station in lijst_station:
        l = fn.select_dates_from_list( fn.knmi_etmgeg_data(station),
                                       start_datum, eind_datum )
        if not l:
            continue
        else:
            # Fill Heatwave object with values if there and add to list
            heat_list = list_heatwaves_station(station, l)
            if heat_list:
                for heat in heat_list:
                    heatwave_list.append(heat)

    # Check eerst of er überhaupt hittegolven zijn
    if heatwave_list:
        heatwave_list = sort_heatstats(heatwave_list, '+') # Sort on warmtegetal

        # Maak content op basis van type uitvoer html of text
        if type == 'txt':
            print(f"Maken {type}-betand met de hittegolven")

            # Maak titel
            content  = f"PLAATS{' ':24} PERIODE{' ':10} ∑WARMTE ∑DAG TG{' ':4} " \
                      f"TX MAX TX≥30 TX≥35 ZON GEM   "
            # content += f"DATUMS & TEMPS "
            content += cfg.ln
            # Doorloop alle hittegolven
            for heatwave in heatwave_list:
                plaats    = f'{heatwave.station.plaats}, ' \
                            f'{heatwave.station.provincie}'
                periode   = f'{heatwave.etmgeg_list[0].YYYYMMDD}-' \
                            f'{heatwave.etmgeg_list[-1].YYYYMMDD}'
                tg_ave    = f"{st.gem_val(heatwave.etmgeg_list,'TG')['gem']:.1f}°C"
                sq_sum    = f"{st.som_val(heatwave.etmgeg_list,'SQ')['som']:.1f}uur"
                tx_max    = f"{st.max_val(heatwave.etmgeg_list,'TX')['max']:.1f}°C"
                tx_gte_30 = f"{st.cnt_day(heatwave.etmgeg_list,'TX','>=',300)['tel']}"
                tx_gte_35 = f"{st.cnt_day(heatwave.etmgeg_list,'TX','>=',350)['tel']}"

                txt_datum_temps = ''
                # Make txt dates with T values
                for etmgeg in heatwave.etmgeg_list:
                    txt_datum_temps += f'{etmgeg.YYYYMMDD[-4:]}|' \
                                       f'TX:{int(etmgeg.TX)/10:0.1f}°C '
                                       # f'TG:{int(etmgeg.TG)/10:0.1f}°C|' \
                                       # f'TN:{int(etmgeg.TN)/10:0.1f}°C '

                content += f"{plaats:<30} {periode:<17} {heatwave.tot_heat_sum:^7.1f} " \
                           f"{heatwave.day_count:^4} {tg_ave:^6} {tx_max:^6} {tx_gte_30:^5} " \
                           f"{tx_gte_35:^5} {sq_sum:<9} "
                # content += txt_datum_temps
                content += cfg.ln

            content += bronvermelding

        # TODO TODO TODO
        elif type == 'html':
            content  = f'''
            <table>
                <thead>
                <tr> <th colspan="9"> {title} </th> </tr>
                <tr>
                    <th> plaats </th>
                    <th title="Periode hittegolf"> periode </th>
                    <th title="Aantal dagen"> ∑dagen </th>
                    <th title="Warmte getal: totaal en gemiddelde"> ∑warmte </th>
                    <th title="Warmste dag"> tx max </th>
                    <th title="Gemiddelde temperatuur"> tg </th>
                    <th title="Aantal tropische dagen"> tx&ge;30 </th>
                    <th title="Aantal tropische dagen"> tx&ge;35 </th>
                    <th title="Aantal zonuren"> ∑zon </th>4
                </tr>
                </thead>
                <tbody>
            '''
            for heatwave in heatwave_list:
                plaats    = f'{heatwave.station.plaats}, ' \
                            f'{heatwave.station.provincie}'
                periode   = f'{heatwave.etmgeg_list[0].YYYYMMDD}-' \
                            f'{heatwave.etmgeg_list[-1].YYYYMMDD}'
                tg_ave    = f"{st.gem_val(heatwave.etmgeg_list,'TG')['gem']:.1f}°C"
                sq_sum    = f"{st.som_val(heatwave.etmgeg_list,'SQ')['som']:.1f}uur"
                tx_max    = f"{st.max_val(heatwave.etmgeg_list,'TX')['max']:.1f}°C"
                tx_gte_30 = f"{st.cnt_day(heatwave.etmgeg_list,'TX','>=',300)['tel']}"
                tx_gte_35 = f"{st.cnt_day(heatwave.etmgeg_list,'TX','>=',350)['tel']}"

                per = periode.split('-')
                datum_txt = f"{d.Datum(per[0]).tekst()} - {d.Datum(per[1]).tekst()}"
                content += f'''
                    <tr>
                        <td> {plaats} </td> <td title="{datum_txt}"> {periode} </td> <td> {tg_ave} </td>
                        <td> {heatwave.tot_heat_sum} </td> <td> {tx_max} </td> <td> {tg_ave} </td>
                        <td> {tx_gte_30} </td> <td> {tx_gte_35} </td> <td> {sq_sum} </td>
                    </tr>
                    '''

            content += f'''
                </tbody>
                <tfoot>
                    <tr> <td colspan="9"> {bronvermelding} </td> </tr>
                </tfoot>
            </table> '''

            content = h.pagina(title, h.style_winterstats_table(), content)

    else: # No heatwaves found
        content = f'Voor {lijst_station[0].plaats} in {periode} zijn geen hittegolven gevonden...'
        if type =='txt':
            pass
        elif type == 'html':
            content = h.pagina('Geen hittegolven', '', '<p>' + content + '</p>')

    if type == 'txt':
        print(cfg.line + cfg.ln + content + cfg.ln + cfg.line)

    wr.write_to_file(file_name, content) # Schrijf naar bestand
