# -*- coding: utf-8 -*-
'''Library contains classes and functions to calculate winterstatistics'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import write as wr, fn, calc_stats as st, config as cfg, fn_html as h
import dates as dat, fn_read as r

class Hellmann:
    '''Deze klasse bewaart gegevens hellman dagen'''
    def __init__(self, datum, getal, som, aantal):
        self.datum  = datum
        self.getal  = getal
        self.som    = som
        self.aantal = aantal

def hellmann_getal(lijst_geg):
    som, aantal, l = 0, 0, []
    for geg in lijst_geg:
        if geg.TG != geg.empthy:
            iTG = int(geg.TG)
            if iTG < 0:
                datum = geg.YYYYMMDD
                getal = abs(iTG)
                som += getal
                aantal += 1 # Verwerk nieuw getal
                if cfg.log:
                    print(f"HLM|datum:{datum}sgetal:{getal}|som:{som}|aantal:{aantal}")
                l.append(Hellmann(datum, getal, som, aantal))

    return {'getal':som, 'lijst':l}

class AlgemeneWinterStats:
    '''Deze klasse bewaart algemene gegevens winterstatistieken van een station
       in een bepaalde periode'''
    def __init__(self, wmo, plaats, provincie, periode, tx_min, tg_min, tn_min, tg_gem, hellmann,
                       tx_lt_0, tg_lt_0, tn_lt_0, tn_lt__5, tn_lt__10, tn_lt__15, tn_lt__20 ):
        self.wmo       =  wmo
        self.plaats    =  plaats
        self.provincie =  provincie
        self.periode   =  periode
        self.tg_gem    =  tg_gem
        self.hellmann  =  hellmann
        self.tx_min    =  tx_min
        self.tg_min    =  tg_min
        self.tn_min    =  tn_min
        self.tx_lt_0   =  tx_lt_0    # Ijsdagen
        self.tg_lt_0   =  tg_lt_0    # Hellmanndagen
        self.tn_lt_0   =  tn_lt_0    # Lichte vorst
        self.tn_lt__5  =  tn_lt__5   # Matige vorst
        self.tn_lt__10 =  tn_lt__10  # Strenge vort
        self.tn_lt__15 =  tn_lt__15  # Zeer strenge vorst
        self.tn_lt__20 =  tn_lt__20

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
            winter_geg.append (
                AlgemeneWinterStats (
                    station.wmo,
                    station.plaats,
                    station.provincie,
                    l[0].YYYYMMDD + '-' + l[-1].YYYYMMDD,   # Periode
                    st.min_val(l,'TX'),
                    st.min_val(l,'TG'),
                    st.min_val(l,'TN'),
                    st.gem_val(l,'TG'),
                    hellmann_getal(l),
                    st.cnt_day(l,'TX','<',0),    # Ijsdagen
                    st.cnt_day(l,'TG','<',0),    # Hellmanndagen
                    st.cnt_day(l,'TN','<',0),    # Vorstdagen
                    st.cnt_day(l,'TN','<',-50),  # Matige vorst
                    st.cnt_day(l,'TN','<',-100), # Strenge vorst
                    st.cnt_day(l,'TN','<',-150), # Zeer strenge vorst
                    st.cnt_day(l,'TN','<',-200),
                )
            )

    print(f"{cfg.ln}...Preparing output...{cfg.ln}")

    winter_geg = sort_winterstats_num(winter_geg,'+') # Sorteer, alleen op hellmann

    # Head of tables
    if type == 'txt' or type == 'cmd':
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
        tg_gem = '.' if not g.tg_gem['gem'] else fn.rm_s(fn.fix(g.tg_gem['gem'],'tg'))
        tx_min = '.' if not g.tx_min['min'] else fn.rm_s(fn.fix(g.tx_min['min'],'tx'))
        tg_min = '.' if not g.tg_min['min'] else fn.rm_s(fn.fix(g.tg_min['min'],'tg'))
        tn_min = '.' if not g.tn_min['min'] else fn.rm_s(fn.fix(g.tn_min['min'],'tn'))
        tx_lt_0   = str(g.tx_lt_0['tel'])    # Ijsdagen
        tn_lt_0   = str(g.tn_lt_0['tel'])    # Lichte vorst
        tg_lt_0   = str(g.tg_lt_0['tel'])    # Hellmanndagen
        tn_lt__10 = str(g.tn_lt__10['tel'])  # Strenge vort
        tn_lt__5  = str(g.tn_lt__5['tel'])   # Matige vorst
        tn_lt__15 = str(g.tn_lt__15['tel'])  # Zeer strenge vorst
        tn_lt__20 = str(g.tn_lt__20['tel'])
        hellmann  = fn.rm_s(fn.fix(g.hellmann['getal'], 'hellmann'))  # hellmann

        if type == 'html':
            html_tx_min    = tx_min + h.table_extremes(g.tx_min['lijst'], -1)
            html_tg_min    = tg_min + h.table_extremes(g.tg_min['lijst'], -1)
            html_tn_min    = tn_min + h.table_extremes(g.tn_min['lijst'], -1)
            html_tx_lt_0   = tx_lt_0 + h.table_count(g.tx_lt_0['lijst'], -1)
            html_tg_lt_0   = tg_lt_0 + h.table_count(g.tg_lt_0['lijst'],  -1)
            html_tn_lt_0   = tn_lt_0 + h.table_count(g.tn_lt_0['lijst'],  -1)
            html_tn_lt__5  = tn_lt__5 + h.table_count(g.tn_lt__5['lijst'], -1)
            html_tn_lt__10 = tn_lt__10 + h.table_count(g.tn_lt__10['lijst'], -1)
            html_tn_lt__15 = tn_lt__15 + h.table_count(g.tn_lt__15['lijst'], -1)
            html_tn_lt__20 = tn_lt__20 + h.table_count(g.tn_lt__20['lijst'], -1)
            html_hellmann  = hellmann + h.table_hellmann(g.hellmann['lijst'], -1)

            d_l = g.periode.split('-')
            dat_txt = f'{dat.Datum(d_l[0]).tekst()} - {dat.Datum(d_l[1]).tekst()}'

            content += f'''
                <tr>
                    <td> {g.plaats} </td> <td> {g.provincie} </td>
                    <td title="{dat_txt}"> {g.periode} </td> <td> {tg_gem} </td>
                    <td> {html_hellmann} </td> <td> {html_tx_min} </td> <td> {html_tg_min} </td>
                    <td> {html_tn_min} </td> <td> {html_tx_lt_0} </td> <td> {html_tg_lt_0} </td>
                    <td> {html_tn_lt_0} </td> <td> {html_tn_lt__5} </td> <td> {html_tn_lt__10} </td>
                    <td> {html_tn_lt__15} </td> <td> {html_tn_lt__20} </td>
                </tr> '''

        if type == 'txt' or type == 'cmd':
            content += f"{g.plaats:<23} {g.provincie:17} {g.periode:18} {tg_gem:7} "
            content += f"{hellmann:^8} {tx_min:<7} {tg_min:<7} {tn_min:<7} "
            content += f"{tx_lt_0:^5} {tg_lt_0:^5} {tn_lt_0:^5} {tn_lt__5:^6} "
            content += f"{tn_lt__10:^6} {tn_lt__15:^6} {tn_lt__20:^6} \n"

    # Close of content
    if type == 'txt' or type == 'cmd':
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
        print(cfg.line + cfg.ln + content + cfg.ln + cfg.line)

    if type == 'txt' or type == 'html':
        file_name = fn.mk_path(path, name) # Make file name
        wr.write_to_file(file_name, content) # Schrijf naar bestand

    return file_name
