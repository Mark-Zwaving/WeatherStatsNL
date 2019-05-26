# -*- coding: utf-8 -*-
'''Library contains classes and functions for calculating summerstatistics'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config as cfg, fn, fn_html as h, calc_stats as st, dates as d
import write as wr, ask

class Warmte_getal:
    '''Deze klasse bewaart gegevens warmte getal dagen'''
    def __init__(self, datum, tg, getal, totaal, aantal):
        self.datum  = datum
        self.tg     = tg / 10
        self.getal  = getal / 10
        self.totaal = totaal / 10
        self.aantal = aantal

def warmte_getal(lijst_geg):
    som, tel, l = 0, 0, []
    for geg in lijst_geg:
        if geg.TG != geg.empthy:
            iTG = int(geg.TG)
            if iTG >= 180:
                getal = iTG - 180
                datum, som, tel = geg.YYYYMMDD, som+getal, tel+1
                if cfg.log:
                    print(f"WRM|{datum}|iTG:{iTG}|som:{som}|"
                          f"getal:{getal}|tel:{tel}")
                l.append( Warmte_getal(datum, iTG, getal, som, tel) )

    return {'getal':som/10, 'lijst':l}

class Zomer_Stats:
    '''Deze klasse bewaart algemene gegevens winterstatistieken
       van een station in een bepaalde periode'''
    def __init__(self, wmo, plaats, provincie, periode, tg_gem, tx_max, tg_max,
                       tn_max, warmte_getal, tx_gte_20, tx_gte_25, tx_gte_30,
                       tx_gte_35, tg_gte_18, tg_gte_20, tn_gte_20, sq_gte_10,
                       sq_tot, rh_gte_10, rh_tot ):
        self.wmo       =  wmo
        self.plaats    =  plaats
        self.provincie =  provincie
        self.periode   =  periode
        self.tg_gem    =  tg_gem
        self.tx_max    =  tx_max
        self.tg_max    =  tg_max
        self.tn_max    =  tn_max
        self.warmte_getal = warmte_getal
        self.tx_gte_20  = tx_gte_20  # Warme dagen
        self.tx_gte_25  = tx_gte_25  # Zomerse dag
        self.tx_gte_30  = tx_gte_30  # Tropisch
        self.tx_gte_35  = tx_gte_35  # Tropisch
        self.tg_gte_18  = tg_gte_18  # Warmte getal dag
        self.tg_gte_20  = tg_gte_20  # Erg warme dag
        self.tn_gte_20  = tn_gte_20  # Tropennacht
        self.sq_gte_10  = sq_gte_10  # Dagen met meer dan tien uur zon
        self.sq_tot     = sq_tot     # Totaal aantal uren zon
        self.rh_gte_10  = rh_gte_10  # Regendagen met meer dan tien milimeter
        self.rh_tot     = rh_tot     # Totaal aantal mm

def sort_zomerstats_num(lijst, pm = '+'):
    sorted = []
    if not lijst and cfg.log:
        print("ZOSO|Lijst is leeg !")
    while lijst:
        max, key = cfg.min_value_geg, 0
        # Haal key minimum waarde uit lijst
        for i in range(len(lijst)):
            val = lijst[i].tg_gem['gem']
            if cfg.log:
                print(f'ZOSO|val:{val}|type(val):{type(val)}|max:{max}|'
                      f'type(max):{type(max)}')
            if val > max:
                max = val; key = i
        sorted.append(lijst[key]) # Voeg waarde toe
        del lijst[key] # Verwijder max waarde uit lijst
    return sorted if pm == '+' else sorted.reverse()

def alg_zomerstats(lijst_stations, datum_start, datum_eind, name, type):
    '''Hoofdfunctie voor het berekenen van de zomerstats'''
    zomer_geg, periode, path, content = [], f'{datum_start}-{datum_eind}', '', ''
    bronvermelding = cfg.lijst_stations[0].bronvermelding

    # Filename
    if not name:
        name = f'{datum_start}-{datum_eind}-sommerstats'

    title = name

    if type == 'html':
        name = f'{name}.html'
        path = cfg.lijst_stations[0].dir_html
    elif type == 'txt':
        name = f'{name}.txt'
        path = cfg.lijst_stations[0].dir_text

    file_name = fn.mk_path(path, name) # Make file name

    if cfg.log: print(f'start:{datum_start}|eind:{datum_eind}|type:{type}')

    for station in lijst_stations:
        l = fn.select_dates_from_list( fn.knmi_etmgeg_data(station),
                                       datum_start, datum_eind )
        if not l: # Geen data gevonden, naar de volgende
            continue
        else:
            # Vul Winterstats object met  waarden en voegtoe aan lijst
            zomer_geg.append (
                Zomer_Stats (
                    station.wmo,
                    station.plaats,
                    station.provincie,
                    l[0].YYYYMMDD + '-' + l[-1].YYYYMMDD,   # Periode
                    st.gem_val(l,'TG'),
                    st.max_val(l,'TX'),
                    st.max_val(l,'TG'),
                    st.max_val(l,'TN'),
                    warmte_getal(l),
                    st.counter(l,'TX','>=',200),  # Warme dag
                    st.counter(l,'TX','>=',250),  # Zomerse dag
                    st.counter(l,'TX','>=',300),  # Tropische dag
                    st.counter(l,'TX','>=',350),  # Tropische
                    st.counter(l,'TG','>=',180),  # Warmte getal dag
                    st.counter(l,'TG','>=',200),  # Warme gemiddelde
                    st.counter(l,'TN','>=',200),  # Tropen nacht
                    st.counter(l,'SQ','>=',100),  # Zonuren > 10
                    st.som_val(l,'SQ'),           # Som zonuren
                    st.counter(l,'RH','>=',100),  # Regen > 10mm
                    st.som_val(l,'RH')            # Som regen mm
                )
            )

    zomer_geg = sort_zomerstats_num(zomer_geg,'+') # Sorteer op tg

    print(f''''

Calculate sommerstats for {type}-file
Name: '{file_name}'

    ''')

    # Maak content op basis van type uitvoer html of text
    if type == 'txt':
        s = ' '
        # Maak titel
        content = f'PLAATS{s:15} PROVINCIE{s:7} PERIODE{s:11} TG      ∑WARMTE ' \
                  f'TX MAX  TG MAX  TN MAX  TX>=20 TX>=25 TX>=30 TX>=35 TG>=18 TG>=20 ' \
                  f'TN>=20 ZON>=10 ∑ZON      REGEN>=10 ∑REGEN     ' + cfg.ln

        for g in zomer_geg:
            tg_gem = '.' if not g.tg_gem['gem'] else f"{g.tg_gem['gem']:0.1f}°C"
            tx_max = '.' if not g.tx_max['max'] else f"{g.tx_max['max']:0.1f}°C"
            tg_max = '.' if not g.tg_max['max'] else f"{g.tg_max['max']:0.1f}°C"
            tn_max = '.' if not g.tn_max['max'] else f"{g.tn_max['max']:0.1f}°C"
            sq_tot = '.' if not g.sq_tot['som'] else f"{g.sq_tot['som']:0.1f}(u)"
            rh_tot = '.' if not g.rh_tot['som'] else f"{g.rh_tot['som']:0.1f}(mm)"

            content += f"{g.plaats:<21} {g.provincie:<16} {g.periode:<18} " \
                       f"{tg_gem:<7} {g.warmte_getal['getal']:<7.1f} {tx_max:<7} " \
                       f"{tg_max:<7} {tn_max:<7} {g.tx_gte_20['tel']:^6} " \
                       f"{g.tx_gte_25['tel']:^6} {g.tx_gte_30['tel']:^6} " \
                       f"{g.tx_gte_35['tel']:^6} {g.tg_gte_18['tel']:^6} " \
                       f"{g.tg_gte_20['tel']:^6} {g.tn_gte_20['tel']:^6} " \
                       f"{g.sq_gte_10['tel']:^7} {sq_tot:<9} " \
                       f"{g.rh_gte_10['tel']:^9} {rh_tot:<11} " + cfg.ln

        content += bronvermelding

    elif type == 'html':
        content  = f'''
        <table>
            <thead>
            <tr> <th colspan="19"> {title} </th> </tr>
            <tr>
                <th> plaats </th>
                <th> provincie </th>
                <th> periode </th>
                <th> tg </th>
                <th title="Warmte getal"> ∑warmte </th>
                <th title="Warmste dag"> tx max </th>
                <th title="Hoogste gemiddelde"> tg max </th>
                <th title="Hoogste minimum"> tn max </th>
                <th title="Aantal warme dagen"> tx&ge;20 </th>
                <th title="Aantal zomers dagen"> tx&ge;25 </th>
                <th title="Aantal tropische dagen"> tx&ge;30 </th>
                <th title="Aantal tropische dagen"> tx&ge;35 </th>
                <th title="Warmte getal dagen"> tg&ge;18 </th>
                <th title="Dagen met ene hoog gemiddelde"> tg&ge;20 </th>
                <th title="Aantal tropennachten"> tn&ge;20 </th>
                <th title="Totaal aantal uren zon"> ∑zon </th>
                <th title="Dagen met meer dan tien uur zon"> zon&ge;10<sub>uur</sub> </th>
                <th title="Totaal aantal mm regen"> ∑regen </th>
                <th title="Dagen met meer dan tien mm regen"> regen&ge;10<sub>mm</sub> </th>
            </tr>
            </thead>
            <tbody>
        '''
        for g in zomer_geg:
            tg_gem = '.' if not g.tg_gem['gem'] else f"{g.tg_gem['gem']:0.1f}°C"

            html_warmte_getal = f"{g.warmte_getal['getal']:0.1f}"
            if cfg.log:
                ask.ask(f'ZALG|{g.wmo}|{g.plaats}|{g.provincie}{html_warmte_getal}')

            if g.warmte_getal['getal'] is not 0:
                warm = g.warmte_getal['lijst']
                html_warmte_getal += h.table_warmte_getal(warm, len(warm))

            html_tx_max = wr.write_html_extremes( g.tx_max['lijst'], g.tx_max['max'],
                                                 len(g.tx_max['lijst']), '°C')
            html_tg_max = wr.write_html_extremes( g.tg_max['lijst'], g.tg_max['max'],
                                                 len(g.tg_max['lijst']), '°C')
            html_tn_max = wr.write_html_extremes( g.tn_max['lijst'], g.tn_max['max'],
                                                 len(g.tn_max['lijst']), '°C')
            html_tg_gte_20 = wr.write_html_count( g.tg_gte_20['lijst'],
                                                 g.tg_gte_20['tel'],
                                                 len(g.tg_gte_20['lijst']),
                                                 '°C')
            html_tx_gte_20 = wr.write_html_count( g.tx_gte_20['lijst'],
                                                 g.tx_gte_20['tel'],
                                                 len(g.tx_gte_20['lijst']),
                                                 '°C')
            html_tx_gte_25 = wr.write_html_count( g.tx_gte_25['lijst'],
                                                 g.tx_gte_25['tel'],
                                                 len(g.tx_gte_25['lijst']),
                                                 '°C')
            html_tx_gte_30 = wr.write_html_count( g.tx_gte_30['lijst'],
                                                 g.tx_gte_30['tel'],
                                                 len(g.tx_gte_30['lijst']),
                                                 '°C' )
            html_tx_gte_35 = wr.write_html_count( g.tx_gte_35['lijst'],
                                                 g.tx_gte_35['tel'],
                                                 len(g.tx_gte_35['lijst']),
                                                 '°C' )
            html_tg_gte_18 = wr.write_html_count( g.tg_gte_18['lijst'],
                                                 g.tg_gte_18['tel'],
                                                 len(g.tg_gte_18['lijst']),
                                                 '°C' )
            html_tn_gte_20 = wr.write_html_count( g.tn_gte_20['lijst'],
                                                 g.tn_gte_20['tel'],
                                                 len(g.tn_gte_20['lijst']),
                                                 '°C' )
            html_sq_gte_10 = wr.write_html_count( g.sq_gte_10['lijst'],
                                                 g.sq_gte_10['tel'],
                                                 len(g.sq_gte_10['lijst']),
                                                 'uur' )
            html_rh_gte_10 = wr.write_html_count( g.rh_gte_10['lijst'],
                                                  g.rh_gte_10['tel'],
                                                  len(g.rh_gte_10['lijst']),
                                                 'mm' )

            html_sq_tot = '.' if not g.sq_tot['som'] \
                              else f"{g.sq_tot['som']:0.1f}<sub>uur</sub>"
            html_rh_tot = '.' if not g.rh_tot['som'] \
                              else f"{g.rh_tot['som']:0.1f}<sub>mm</sub>"

            per = g.periode.split('-')
            datum_txt = f"{d.Datum(per[0]).tekst()} - {d.Datum(per[1]).tekst()}"
            content += f'''
                <tr>
                    <td> {g.plaats} </td> <td> {g.provincie} </td>
                    <td title="{datum_txt}"> {g.periode} </td> <td> {tg_gem} </td>
                    <td> {html_warmte_getal} </td> <td> {html_tx_max}°C </td> <td> {html_tg_max}°C </td>
                    <td> {html_tn_max}°C </td> <td> {html_tx_gte_20} </td> <td> {html_tx_gte_25} </td>
                    <td> {html_tx_gte_30} </td> <td> {html_tx_gte_35} </td> <td> {html_tg_gte_18} </td>
                    <td> {html_tg_gte_20} </td> <td> {html_tn_gte_20} </td> <td> {html_sq_tot} </td>
                    <td> {html_sq_gte_10} </td> <td> {html_rh_tot} </td> <td> {html_rh_gte_10} </td>
                </tr>
                '''

        content += f'''
            </tbody>
            <tfoot>
                <tr> <td colspan="19"> {bronvermelding} </td> </tr>
            </tfoot>
        </table> '''

        content = h.pagina(title, h.style_winterstats_table(), content)

    if type == 'txt':
        print(cfg.line + cfg.ln + content + cfg.ln + cfg.line)

    wr.write_to_file(file_name, content) # Schrijf naar bestand
