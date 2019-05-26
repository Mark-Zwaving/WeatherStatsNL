# -*- coding: utf-8 -*-
'''Library contains functions to handle with menu options'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import time, fn, config as c, fn_download as d, write as w, ask as a
import calc_sommerstats as zs, calc_winterstats as ws, calc_heatwaves as hs
import calc_dayvalues as day

# Menu choice 1
def download_etmgeg_all_stations():
    '''Functie downloadt (en unzipt) alle knmi stations in de lijst'''
    print(f'{c.line}{c.ln}START DOWNLOADING ALL STATIONS KNMI DATA DAY VALUES...{c.ln}')
    start_ns = time.time_ns()
    for station in c.lijst_stations:
        d.download_and_unzip_etmgeg_station ( station )
    end_ns = time.time_ns()
    w.write_process_time_ns( 'Total calculation time: ', (end_ns-start_ns) )
    print(f'{c.ln}END DOWNLOADING ALL STATIONS KNMI DATA DAY VALUES...{c.ln}{c.line}')
    a.ask_enter_menu()

# Menu choice 2
def download_etmgeg_station():
    '''Functie vraagt eerst om één of meerdere stations en downloadt ze daarna '''
    print(f'{c.line}{c.ln}START DOWNLOAD STATION KNMI DATA DAY VALUES...{c.ln}')
    l = a.ask_stations('Select one or more stations ? ' )
    if l != c.stop:
        start_ns = time.time_ns()
        print(f'{c.ln}{c.line}{c.ln}DOWNLOAD STARTED...{c.ln}')
        for station in l:
            d.download_and_unzip_etmgeg_station ( station )
        end_ns = time.time_ns()
        w.write_process_time_ns( 'Total calculation time: ', (end_ns-start_ns) )
    print(f'{c.ln}END DOWNLOAD STATION KNMI DATA DAY VALUES...{c.ln}{c.line}')
    a.ask_enter_menu()

#Menu choice 3 get_dagwaarden
def get_dayvalues():
    '''Funtion gets day values from data knmi '''
    print(f'{c.line}{c.ln}START: SEARCHING AND PREPARING DAY VALUES...{c.ln}')
    yyyymmdd = a.ask_date('Give the date <yyyymmdd> you look for ? ')
    if yyyymmdd != c.stop:
        l = a.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = a.ask_file_type('Select filetype ? ')
            if type != c.stop:
                name = a.ask_file_naam('Set a name for the output file ? <optional> ')
                if name != c.stop:
                    # Bereken hittegolven
                    start_ns = time.time_ns()
                    day.prepare_day_values( l, yyyymmdd, name, type )
                    end_ns = time.time_ns()
                    # dayvalues
                    w.write_process_time_ns( 'Total calculation time: ', (end_ns-start_ns) )
    print(f'{c.ln}END SEARCHING AND PREPARING DAY VALUES...{c.ln}{c.line}')
    a.ask_enter_menu()

# Menu choice
def calc_winterstats():
    '''Functie regelt berekeningen voor de winterstats'''
    print(f'{c.line}{c.ln}START CALCULATE WINTER STATISTICS{c.ln}')
    dates = a.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = a.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = a.ask_file_type('Select filetype ? ')
            if type != c.stop:
                name = a.ask_file_naam('Set a name for the output file ? <optional> ')
                if name != c.stop:
                    # Bereken winterstats
                    start_ns = time.time_ns()
                    ws.alg_winterstats(l, dates['start'], dates['einde'], name, type)
                    end_ns = time.time_ns()
                    w.write_process_time_ns( 'Total calculation time: ', (end_ns-start_ns) )
    print(f'{c.ln}END CALCULATE WINTER STATISTICS...{c.ln}{c.line}')
    a.ask_enter_menu()

# Menu choice
def calc_zomerstats():
    print(f'{c.line}{c.ln}START CALCULATE SOMMER STATISTICS...{c.ln}')
    dates = a.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = a.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = a.ask_file_type('Select filetype ? ')
            if type != c.stop:
                name = a.ask_file_naam('Set a name for the output file ? <optional> ')
                if name != c.stop:
                    # Calculate sommer statistics
                    start_ns = time.time_ns()
                    zs.alg_zomerstats(l, dates['start'], dates['einde'], name, type)
                    end_ns = time.time_ns()
                    w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )
    print(f'{c.ln}END CALCULATE SOMMER STATISTICS...{c.ln}{c.line}')
    a.ask_enter_menu()

# Menu choice
def calc_heat_waves():
    print(f'{c.line}{c.ln}START CALCULATE HEATWAVES...{c.ln}')
    dates = a.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = a.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = a.ask_file_type('Select filetype ? ')
            if type != c.stop:
                name = a.ask_file_naam('Set a name for the output file ? <optional> ')
                if name != c.stop:
                    # Calculate heatwaves
                    start_ns = time.time_ns()
                    hs.gen_calc_heat_waves(l, dates['start'], dates['einde'], type, name)
                    end_ns = time.time_ns()
                    w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )
    print(f'{c.ln}END CALCULATE HEATWAVES...{c.ln}{c.line}')
    a.ask_enter_menu()
