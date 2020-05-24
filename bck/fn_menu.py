<<<<<<< Updated upstream:sources/fn_menu.py
# -*- coding: utf-8 -*-
'''Library contains functions to handle with menu options'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import time, fn, config as c, fn_download as d, write as w, ask as a
import calc_sommerstats as zs, calc_winterstats as ws, calc_heatwaves as hs
import calc_dayvalues as day, dates as dat, webbrowser

# Menu choice 1
def download_etmgeg_all_stations():
    '''Functie downloadt (en unzipt) alle knmi stations in de lijst'''
    fn.lnprintln(f'{c.line}{c.ln}START DOWNLOADING ALL STATIONS KNMI DATA DAY VALUES...')
    start_ns = time.time_ns()
    for station in c.lijst_stations:
        d.download_and_unzip_etmgeg_station ( station )
    end_ns = time.time_ns()
    w.write_process_time_ns( 'Total calculation time: ', (end_ns-start_ns) )

    fn.lnprintln(f'END DOWNLOADING ALL STATIONS KNMI DATA DAY VALUES...{c.ln}{c.line}')

    a.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice 2
def download_etmgeg_station():
    '''Functie vraagt eerst om één of meerdere stations en downloadt ze daarna '''
    fn.lnprintln(f'{c.line}{c.ln}START DOWNLOAD STATION KNMI DATA DAY VALUES...')
    l = a.ask_stations('Select one or more stations ? ' )
    if l != c.stop:
        fn.lnprintln(f'...DOWNLOADING STARTED...')
        start_ns = time.time_ns()
        for station in l: d.download_and_unzip_etmgeg_station ( station )
        end_ns = time.time_ns()
        w.write_process_time_ns( 'Total calculation time: ', (end_ns-start_ns) )
    fn.lnprintln(f'END DOWNLOAD STATION KNMI DATA DAY VALUES...{c.ln}{c.line}')

    a.ask(f"Press a 'key' to go back to the main menu{c.ln}")

#Menu choice 3 get_dagwaarden
def get_dayvalues():
    '''Funtion gets day values from data knmi '''
    fn.lnprintln(f'{c.line}{c.ln}START: SEARCHING AND PREPARING DAY VALUES...')
    yyyymmdd = a.ask_date('Give the date <yyyymmdd> you look for ? ')
    if yyyymmdd != c.stop:
        station = a.ask_station('Select a weather station ? ')
        if station != c.stop:
            type = a.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = a.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln('...SEARCHING FOR AND PREPARING DAY VALUES...')
                    print(f'Station: {station.wmo} {station.plaats}')
                    fn.println(f'DATE: {dat.Datum(yyyymmdd).tekst()}')
                    start_ns = time.time_ns()
                    file_name = day.prepare_day_values( station, yyyymmdd, name, type )
                    end_ns = time.time_ns()
                    w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = a.ask_open_url("Open the file with your (default) app ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END SEARCHING AND PREPARING DAY VALUES...{c.ln}{c.line}')

    a.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice
def calc_winterstats():
    '''Functie regelt berekeningen voor de winterstats'''
    fn.lnprintln(f'{c.line}{c.ln}START CALCULATE WINTER STATISTICS')
    dates = a.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = a.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = a.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = a.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln(f'...CALCULATING WINTER STATISTICS...')
                    start_ns = time.time_ns()
                    file_name = ws.alg_winterstats(l, dates['start'], dates['einde'], name, type)
                    end_ns = time.time_ns()
                    w.write_process_time_ns( 'Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = a.ask_open_url("Open the file in your (default) browser ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END CALCULATE WINTER STATISTICS...{c.ln}{c.line}')

    a.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice
def calc_zomerstats():
    fn.lnprintln(f'{c.line}{c.ln}START CALCULATE SUMMER STATISTICS...')
    dates = a.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = a.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = a.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = a.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln(f'...CALCULATING SUMMERSTATS...')
                    start_ns = time.time_ns()
                    file_name = zs.alg_zomerstats(l, dates['start'], dates['einde'], name, type)
                    end_ns = time.time_ns()
                    w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = a.ask_open_url("Open the file with your (default) browser ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END CALCULATE SUMMER STATISTICS...{c.ln}{c.line}')

    a.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice
def calc_heat_waves():
    fn.lnprintln(f'{c.line}{c.ln}START CALCULATE HEATWAVES...')
    dates = a.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = a.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = a.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = a.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln(f'...CALCULATING HEATWAVES...')
                    start_ns = time.time_ns()
                    file_name = hs.alg_heatwaves(l, dates['start'], dates['einde'], type, name)
                    end_ns = time.time_ns()
                    w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = a.ask_open_url("Open the file with your (default) browser ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END CALCULATE HEATWAVES...{c.ln}{c.line}')

    a.ask(f"Press a 'key' to go back to the main menu{c.ln}")
=======
# -*- coding: utf-8 -*-
'''Library contains functions to handle with menu options'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import time, fn, config as c, fn_download as d, write as w, ask as a
import calc_sommerstats as zs, calc_winterstats as ws, calc_heatwaves as hs
import calc_allstats as alls, calc_extremes as ae
import calc_dayvalues as day, dates as dat, webbrowser
import make_image as mi

# Menu choice 1
def download_etmgeg_all_stations():
    '''Functie downloadt (en unzipt) alle knmi stations in de lijst'''
    fn.lnprintln(f'{c.line}{c.ln}START DOWNLOADING ALL STATIONS KNMI DATA DAY VALUES...')
    start_ns = time.time_ns()
    for station in c.lijst_stations:
        d.download_and_unzip_etmgeg_station ( station )
    end_ns = time.time_ns()
    w.write_process_time_ns( 'Total calculation time: ', (end_ns-start_ns) )

    fn.lnprintln(f'END DOWNLOADING ALL STATIONS KNMI DATA DAY VALUES...{c.ln}{c.line}')

    a.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice 2
def download_etmgeg_station():
    '''Functie vraagt eerst om één of meerdere stations en downloadt ze daarna '''
    fn.lnprintln(f'{c.line}{c.ln}START DOWNLOAD STATION KNMI DATA DAY VALUES...')
    l = a.ask_stations('Select one or more stations ? ' )
    if l != c.stop:
        fn.lnprintln(f'...DOWNLOADING STARTED...')
        start_ns = time.time_ns()
        for station in l: d.download_and_unzip_etmgeg_station ( station )
        end_ns = time.time_ns()
        w.write_process_time_ns( 'Total calculation time: ', (end_ns-start_ns) )
    fn.lnprintln(f'END DOWNLOAD STATION KNMI DATA DAY VALUES...{c.ln}{c.line}')

    a.ask(f"Press a 'key' to go back to the main menu{c.ln}")

#Menu choice 3 get_dagwaarden
def get_dayvalues():
    '''Funtion gets day values from data knmi '''
    fn.lnprintln(f'{c.line}{c.ln}START: SEARCHING AND PREPARING DAY VALUES...')
    yyyymmdd = a.ask_date('Give the date <yyyymmdd> you look for ? ')
    if yyyymmdd != c.stop:
        station = a.ask_station('Select a weather station ? ')
        if station != c.stop:
            type = a.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = a.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln('...SEARCHING FOR AND PREPARING DAY VALUES...')
                    print(f'Station: {station.wmo} {station.plaats}')
                    fn.println(f'DATE: {dat.Datum(yyyymmdd).tekst()}')
                    start_ns = time.time_ns()
                    file_name = day.prepare_day_values( station, yyyymmdd, name, type )
                    end_ns = time.time_ns()
                    w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = a.ask_open_url("Open the file with your (default) app ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END SEARCHING AND PREPARING DAY VALUES...{c.ln}{c.line}')

    a.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice
def calc_winterstats():
    '''Functie regelt berekeningen voor de winterstats'''
    fn.lnprintln(f'{c.line}{c.ln}START CALCULATE WINTER STATISTICS')
    dates = a.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = a.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = a.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = a.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln(f'...CALCULATING WINTER STATISTICS...')
                    start_ns = time.time_ns()
                    file_name = ws.alg_winterstats(l, dates['start'], dates['einde'], name, type)
                    end_ns = time.time_ns()
                    w.write_process_time_ns( 'Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = a.ask_open_url("Open the file in your (default) browser ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END CALCULATE WINTER STATISTICS...{c.ln}{c.line}')

    a.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice
def calc_zomerstats():
    fn.lnprintln(f'{c.line}{c.ln}START CALCULATE SUMMER STATISTICS...')
    dates = a.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = a.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = a.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = a.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln(f'...CALCULATING SUMMERSTATS...')
                    start_ns = time.time_ns()
                    file_name = zs.alg_zomerstats(l, dates['start'], dates['einde'], name, type)
                    end_ns = time.time_ns()
                    w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = a.ask_open_url("Open the file with your (default) browser ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END CALCULATE SUMMER STATISTICS...{c.ln}{c.line}')

    a.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice
def calc_heat_waves():
    fn.lnprintln(f'{c.line}{c.ln}START CALCULATE HEATWAVES...')
    dates = a.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = a.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = a.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = a.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln(f'...CALCULATING HEATWAVES...')
                    start_ns = time.time_ns()
                    file_name = hs.alg_heatwaves(l, dates['start'], dates['einde'], type, name)
                    end_ns = time.time_ns()
                    w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = a.ask_open_url("Open the file with your (default) browser ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END CALCULATE HEATWAVES...{c.ln}{c.line}')

    a.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice
def calc_allstats():
    fn.lnprintln(f'{c.line}{c.ln}START CALCULATE ALL STATISTICS...')
    dates = a.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = a.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = a.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = a.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln(f'...CALCULATING ALL STATISTICS...')
                    start_ns = time.time_ns()
                    file_name = alls.alg_allstats(l, dates['start'], dates['einde'], name, type)
                    end_ns = time.time_ns()
                    w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = a.ask_open_url("Open the file with your (default) browser ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END CALCULATE ALL STATISTICS...{c.ln}{c.line}')

    a.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice
def calc_allextremes():
    fn.lnprintln(f'{c.line}{c.ln}START CALCULATE ALL EXTREMES...')
    dates = a.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = a.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = a.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = a.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln(f'...CALCULATING ALL EXTREMES...')
                    start_ns = time.time_ns()
                    file_name = ae.alg_allextremes(l, dates['start'], dates['einde'], name, type)
                    end_ns = time.time_ns()
                    w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = a.ask_open_url("Open the file with your (default) browser ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END CALCULATE ALL EXTREMES...{c.ln}{c.line}')

    a.ask(f"Press a 'key' to go back to the main menu{c.ln}")


def make_images():
    fn.lnprintln(f'{c.line}{c.ln}START MAKE IMAGE(S)...')
    dates = a.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        oke = True
        l = a.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            name = a.ask_file_naam('Set a name for the output file ? <optional> ')
            if name == c.stop:
                oke = False
            # Eventueel hier select options ?
            # !) image TEMP:
            # 2) image all
            # 3) et cetera
        if oke:
            fn.lnprintln(f'...MAKE IMAGES...')
            start_ns = time.time_ns()
            file_name = mi.make_image_temps_in_period(
                           l,
                           dates['start'], dates['einde'],
                           name)
            end_ns = time.time_ns()
            w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )

            oke = a.ask_open_url("Open the image with your (default) browser ?")
            if oke:
                webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END MAKE IMAGE(S)...{c.ln}{c.line}')

    a.ask(f"Press a 'key' to go back to the main menu{c.ln}")
>>>>>>> Stashed changes:sources/bck/fn_menu.py
