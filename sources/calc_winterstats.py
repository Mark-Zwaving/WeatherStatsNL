# -*- coding: utf-8 -*-
'''Library contains classes and functions to calculate winterstatistics'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import write as wr, fn, calc_stats as st, config as cfg, fn_html as h
import dates as dat

class Hellmann:
    '''Deze klasse bewaart gegevens hellman dagen'''
    def __init__(self, datum, getal, som, aantal):
        self.datum  = datum
        self.getal  = getal / 10
        self.som    = som / 10
        self.aantal = aantal

def hellmann_getal(lijst_geg):
    som, aantal, l = 0, 0, []
    for geg in lijst_geg:
        if geg.TG != geg.empthy:
            iTG = int(geg.TG)
            if iTG < 0:
                datum = geg.YYYYMMDD; getal = abs(iTG); som += getal; aantal += 1 # Verwerk nieuw getal
                if cfg.log:
                    print(f"HLM|datum:{datum}sgetal:{getal}|som:{som}|aantal:{aantal}")
                l.append(Hellmann(datum, getal, som, aantal))

    return {'getal':som/10, 'lijst':l}

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
    if not name:
        name = f'winterstats {periode}'

    title = name

    if type == 'html':
        name = f'{name}.html'
        path = cfg.lijst_stations[0].dir_html
    elif type == 'txt':
        name = f'{name}.txt'
        path = cfg.lijst_stations[0].dir_text

    file_name = fn.mk_path(path, name) # Make file name

    for station in lijst_stations:
        l = fn. select_dates_from_list(fn.knmi_etmgeg_data(station),
                                       datum_start, datum_eind)
        if not l: # Geen data gevonden, naar de volgende
            continue
        else:
            print(f"Calculate winterstats for station: {station.wmo} {station.plaats}")
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
                    st.counter(l,'TX','<',0),    # Ijsdagen
                    st.counter(l,'TG','<',0),    # Hellmanndagen
                    st.counter(l,'TN','<',0),    # Vorstdagen
                    st.counter(l,'TN','<',-50),  # Matige vorst
                    st.counter(l,'TN','<',-100), # Strenge vorst
                    st.counter(l,'TN','<',-150), # Zeer strenge vorst
                    st.counter(l,'TN','<',-200),
                )
            )

    winter_geg = sort_winterstats_num(winter_geg,'+') # Sorteer, alleen op hellmann

    print(f''''

Calculate winterstats for {type}-file
Name: '{file_name}'

    ''')

    if type == 'txt':
        s, path = ' ', lijst_stations[0].dir_text
        content  = f'PLAATS{s:17} PROVINCIE         PERIODE{s:11} TG{s:5} HELLMANN TX MIN  ' \
                   f'TG MIN  TN MIN  TX<0  TG<0  TN<0  TN<-5  TX<-10 ' \
                   f'TX<-15 TX<-20' + cfg.ln

        for g in winter_geg:
            tg_gem = '.' if not g.tg_gem['gem'] else f"{g.tg_gem['gem']:0.1f}°C"
            tx_min = '.' if not g.tx_min['min'] else f"{g.tx_min['min']:0.1f}°C"
            tg_min = '.' if not g.tg_min['min'] else f"{g.tg_min['min']:0.1f}°C"
            tn_min = '.' if not g.tn_min['min'] else f"{g.tn_min['min']:0.1f}°C"

            content += f"{g.plaats:<23} {g.provincie:17} {g.periode:18} {tg_gem:7} " \
                       f"{g.hellmann['getal']:^8.1f} {tx_min:<7} {tg_min:<7} {tn_min:<7} " \
                       f"{g.tx_lt_0['tel']:^5} {g.tg_lt_0['tel']:^5} {g.tn_lt_0['tel']:^5} " \
                       f"{g.tn_lt__5['tel']:^6} {g.tn_lt__10['tel']:^6} {g.tn_lt__15['tel']:^6} " \
                       f"{g.tn_lt__20['tel']:^6}" + cfg.ln

        content += bronvermelding

    elif type == 'html':
        table  = f'''
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
                <tbody>
        '''

        for g in winter_geg:
            tg_gem = '.' if not g.tg_gem['gem'] else f"{g.tg_gem['gem']:0.1f}°C"

            html_hellmann = f"{g.hellmann['getal']:0.1f}"

            if cfg.log:
                print(f'ALG|{g.gmo}|{g.plaats}|{g.provincie}|hellmann:{html_hellmann}')

            if g.hellmann['getal'] is not 0:
                hlm = g.hellmann['lijst']
                html_hellmann += h.table_hellmann(hlm, len(hlm))

            html_tx_min = wr.write_html_extremes( g.tx_min['lijst'], g.tx_min['min'],
                                                 len(g.tx_min['lijst']), '°C')
            html_tg_min = wr.write_html_extremes( g.tg_min['lijst'], g.tg_min['min'],
                                                 len(g.tg_min['lijst']), '°C')
            html_tn_min = wr.write_html_extremes( g.tn_min['lijst'], g.tn_min['min'],
                                                 len(g.tn_min['lijst']), '°C')
            html_tx_lt_0 = wr.write_html_count( g.tx_lt_0['lijst'], g.tx_lt_0['tel'],
                                               len(g.tx_lt_0['lijst']), '°C')
            html_tg_lt_0 = wr.write_html_count( g.tg_lt_0['lijst'], g.tg_lt_0['tel'],
                                               len(g.tg_lt_0['lijst']), '°C')
            html_tn_lt_0 = wr.write_html_count( g.tn_lt_0['lijst'], g.tn_lt_0['tel'],
                                               len(g.tn_lt_0['lijst']), '°C')
            html_tn_lt__5 = wr.write_html_count( g.tn_lt__5['lijst'], g.tn_lt__5['tel'],
                                               len(g.tn_lt__5['lijst']), '°C')
            html_tn_lt__10 = wr.write_html_count( g.tn_lt__10['lijst'], g.tn_lt__10['tel'],
                                                 len(g.tn_lt__10['lijst']), '°C')
            html_tn_lt__15 = wr.write_html_count( g.tn_lt__15['lijst'], g.tn_lt__15['tel'],
                                                 len(g.tn_lt__15['lijst']), '°C')
            html_tn_lt__20 = wr.write_html_count( g.tn_lt__20['lijst'], g.tn_lt__20['tel'],
                                                 len(g.tn_lt__20['lijst']), '°C')

            d_l = g.periode.split('-')
            dat_txt = f'{dat.Datum(d_l[0]).tekst()} - {dat.Datum(d_l[1]).tekst()}'
            table += f'''
                <tr>
                    <td> {g.plaats} </td> <td> {g.provincie} </td>
                    <td title="{dat_txt}"> {g.periode} </td> <td> {tg_gem} </td>
                    <td> {html_hellmann} </td> <td> {html_tx_min} </td> <td> {html_tg_min} </td>
                    <td> {html_tn_min} </td> <td> {html_tx_lt_0} </td> <td> {html_tg_lt_0} </td>
                    <td> {html_tn_lt_0} </td> <td> {html_tn_lt__5} </td> <td> {html_tn_lt__10} </td>
                    <td> {html_tn_lt__15} </td> <td> {html_tn_lt__20} </td>
                </tr>
                '''

        table += f'''
            </tbody>
            <tfoot>
                <tr> <td colspan="15"> {bronvermelding} </td> </tr>
            </tfoot>
        </table> '''

        content = h.pagina(title, h.style_winterstats_table(), table)

    if type == 'txt': print(cfg.line + cfg.ln + content + cfg.ln + cfg.line)

    wr.write_to_file(file_name, content) # Schrijf naar bestand
