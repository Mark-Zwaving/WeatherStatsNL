'''Library contains functions for asking questions and to deal with the input
given by a user'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, time, config, html, webbrowser, subprocess
import knmi.model.daydata as daydata
import knmi.view.dayvalues as view_dayvalues
import model.utils as utils
import control.ask as control_ask
import control.io as io
import view.log as log
import view.translate as tr
import view.txt as view_txt

def menu_choices( choice ):
    if   choice ==  '1':  process_knmi_dayvalues_all()
    elif choice ==  '2':  process_knmi_dayvalues_selected()
    elif choice ==  '3':  get_dayvalues_by_date()
    elif choice ==  '4': menu.calc_winterstats()
    elif choice ==  '5': pass #menu.calc_coldwaves()
    elif choice ==  '6': menu.calc_zomerstats()
    elif choice ==  '7': menu.calc_heat_waves()
    elif choice ==  '8': menu.calc_allstats()
    elif choice ==  '9': menu.calc_allextremes()
    elif choice == '10': menu.make_images()
    else:
        log.console(f'Input {choice} unknown. Try again...', True)

# Menu choice 1
def process_knmi_dayvalues_all():
    '''Function downloads, unzipped  all knmi stations in the list'''
    log.header('START DOWNLOADING ALL DATA DAYVALUES KNMI STATIONS...', True)
    st = time.time_ns()
    for station in config.stations:
        daydata.process_data( station )
    et = time.time_ns()
    log.footer(view_txt.process_time_ext('Total processing time', et-st), True)
    log.footer('END DOWNLOADING ALL STATIONS KNMI DATA DAY VALUES', True)
    control_ask.ask("Press a 'key' to go back to the main menu")

# Menu choice 2
def process_knmi_dayvalues_selected():
    '''Function asks for one or more wmo numbers to download their data'''
    log.header('START DOWNLOAD STATION KNMI DATA DAY VALUES...', True )
    l = control_ask.ask_for_stations('Select one or more stations ? ')
    if l != config.answer_quit:
        log.header('...DOWNLOADING STARTED...', True )
        st = time.time_ns()
        for station in l:
            daydata.process_data( station )
        et = time.time_ns()
        log.footer(view_txt.process_time_ext('Total processing time', et-st), True)
    log.footer('END DOWNLOAD STATION KNMI DATA DAY VALUES...', True )
    control_ask.ask("Press a 'key' to go back to the main menu")

#Menu choice 3 get day
def get_dayvalues_by_date():
    '''Funtion gets day values from data knmi '''
    log.header('START: SEARCHING AND PREPARING DAY VALUES...', True)
    yyyymmdd = control_ask.ask_for_date('Give in the date <yyyymmdd> you look for ?')
    if yyyymmdd != config.answer_quit:
        stations = control_ask.ask_for_stations('Select a weather station ? ')
        if stations != []:
            type = control_ask.ask_for_file_type('Select filetype ? ')
            if type != config.answer_quit:
                for station in stations:
                    ok, file_name = True, False
                    if type != 'cmd':
                        file_name = control_ask.ask_for_file_name(f'Give a name for the {type} file ? <optional> ')
                        if file_name == config.answer_quit:
                            ok = False

                    if not file_name:
                        now = utils.now_act_for_file()
                        file_name = f'dayvalues-{now}.{type}'

                    if ok:
                        log.header('SEARCHING FOR AND PREPARING DAY VALUES', True)

                        st = time.time_ns()
                        log.console(f'Station: {station.wmo} {station.place}', True)
                        log.console(f'Date: {utils.ymd_to_txt(yyyymmdd)} <{yyyymmdd}>', True)
                        ok_data, day = daydata.day(station, yyyymmdd)

                        if ok_data:
                            txt_date = utils.ymd_to_txt(yyyymmdd)
                            header = f'{station.wmo} - {station.place} {station.province} - {txt_date}'
                            footer = station.data_notification

                            if type == 'html':
                                page = html.Template()
                                page.title  = f'{station.place}-{yyyymmdd}'
                                page.header = header
                                page.main   = view_dayvalues.html_main( day )
                                page.footer = footer
                                page.file_name = file_name

                                et = False
                                if page.save():
                                    et = time.time_ns()
                                    fopen = control_ask.ask_to_open_with_app("Open the file in your browser ?")
                                    if fopen:
                                        webbrowser.open_new_tab( page.file_name ) # Opens in default browser

                                if not et:
                                    et = time.time_ns()

                            if type == 'txt':
                                title = txt_date
                                main  = view_dayvalues.txt_main( day )
                                txt   = f'{title}\n{main}'
                                dir   = config.dir_data_txt_dayvalues
                                path  = os.path.abspath(os.path.join(dir, file_name))

                                if io.save(path, txt):
                                    et = time.time_ns()
                                    fopen = control_ask.ask_to_open_with_app("Open the file in your <default app or browser ?")

                                    if fopen:
                                        print(path)
                                        input()
                                        webbrowser.open_new_tab(path)
                        else:
                            log.console( 'Error reading data!', station.place, yyyymmdd )
                        log.footer(view_txt.process_time_ext('Total processing time', et-st), True)

    log.footer('END SEARCHING AND PREPARING DAY VALUES...', True)
    control_ask.ask("Press a 'key' to go back to the main menu\n")

# Menu choice
def calc_winterstats():
    '''Functie regelt berekeningen voor de winterstats'''
    fn.lnprintln(f'{c.line}{c.ln}START CALCULATE WINTER STATISTICS')
    dates = control_ask.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = control_ask.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = control_ask.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = control_ask.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln(f'...CALCULATING WINTER STATISTICS...')
                    start_ns = time.time_ns()
                    file_name = ws.alg_winterstats(l, dates['start'], dates['einde'], name, type)
                    end_ns = time.time_ns()
                    w.write_process_time_ns( 'Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = control_ask.ask_open_url("Open the file in your (default) browser ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END CALCULATE WINTER STATISTICS...{c.ln}{c.line}')

    control_ask.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice
def calc_zomerstats():
    fn.lnprintln(f'{c.line}{c.ln}START CALCULATE SUMMER STATISTICS...')
    dates = control_ask.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = control_ask.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = control_ask.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = control_ask.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln(f'...CALCULATING SUMMERSTATS...')
                    start_ns = time.time_ns()
                    file_name = zs.alg_zomerstats(l, dates['start'], dates['einde'], name, type)
                    end_ns = time.time_ns()
                    w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = control_ask.ask_open_url("Open the file with your (default) browser ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END CALCULATE SUMMER STATISTICS...{c.ln}{c.line}')

    control_ask.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice
def calc_heat_waves():
    fn.lnprintln(f'{c.line}{c.ln}START CALCULATE HEATWAVES...')
    dates = control_ask.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = control_ask.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = control_ask.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = control_ask.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln(f'...CALCULATING HEATWAVES...')
                    start_ns = time.time_ns()
                    file_name = hs.alg_heatwaves(l, dates['start'], dates['einde'], type, name)
                    end_ns = time.time_ns()
                    w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = control_ask.ask_open_url("Open the file with your (default) browser ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END CALCULATE HEATWAVES...{c.ln}{c.line}')

    control_ask.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice
def calc_allstats():
    fn.lnprintln(f'{c.line}{c.ln}START CALCULATE ALL STATISTICS...')
    dates = control_ask.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = control_ask.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = control_ask.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = control_ask.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln(f'...CALCULATING ALL STATISTICS...')
                    start_ns = time.time_ns()
                    file_name = alls.alg_allstats(l, dates['start'], dates['einde'], name, type)
                    end_ns = time.time_ns()
                    w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = control_ask.ask_open_url("Open the file with your (default) browser ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END CALCULATE ALL STATISTICS...{c.ln}{c.line}')

    control_ask.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice
def calc_allextremes():
    fn.lnprintln(f'{c.line}{c.ln}START CALCULATE ALL EXTREMES...')
    dates = control_ask.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = control_ask.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = control_ask.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = control_ask.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln(f'...CALCULATING ALL EXTREMES...')
                    start_ns = time.time_ns()
                    file_name = ae.alg_allextremes(l, dates['start'], dates['einde'], name, type)
                    end_ns = time.time_ns()
                    w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = control_ask.ask_open_url("Open the file with your (default) browser ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END CALCULATE ALL EXTREMES...{c.ln}{c.line}')

    control_ask.ask(f"Press a 'key' to go back to the main menu{c.ln}")


def make_images():
    fn.lnprintln(f'{c.line}{c.ln}START MAKE IMAGE(S)...')
    dates = control_ask.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        oke = True
        l = control_ask.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            name = control_ask.ask_file_naam('Set a name for the output file ? <optional> ')
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

            oke = control_ask.ask_open_url("Open the image with your (default) browser ?")
            if oke:
                webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END MAKE IMAGE(S)...{c.ln}{c.line}')

    control_ask.ask(f"Press a 'key' to go back to the main menu{c.ln}")


#Menu choice 3 get_dagwaarden
def get_dayvalues():
    '''Funtion gets day values from data knmi '''
    fn.lnprintln(f'{c.line}{c.ln}START: SEARCHING AND PREPARING DAY VALUES...')
    yyyymmdd = control_ask.ask_date('Give the date <yyyymmdd> you look for ? ')
    if yyyymmdd != c.stop:
        station = control_ask.ask_station('Select a weather station ? ')
        if station != c.stop:
            type = control_ask.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = control_ask.ask_file_naam('Set a name for the output file ? <optional> ')
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
                        oke = control_ask.ask_open_url("Open the file with your (default) app ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END SEARCHING AND PREPARING DAY VALUES...{c.ln}{c.line}')

    control_ask.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice
def calc_winterstats():
    '''Functie regelt berekeningen voor de winterstats'''
    fn.lnprintln(f'{c.line}{c.ln}START CALCULATE WINTER STATISTICS')
    dates = control_ask.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = control_ask.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = control_ask.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = control_ask.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln(f'...CALCULATING WINTER STATISTICS...')
                    start_ns = time.time_ns()
                    file_name = ws.alg_winterstats(l, dates['start'], dates['einde'], name, type)
                    end_ns = time.time_ns()
                    w.write_process_time_ns( 'Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = control_ask.ask_open_url("Open the file in your (default) browser ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END CALCULATE WINTER STATISTICS...{c.ln}{c.line}')

    control_ask.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice
def calc_zomerstats():
    fn.lnprintln(f'{c.line}{c.ln}START CALCULATE SUMMER STATISTICS...')
    dates = control_ask.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = control_ask.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = control_ask.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = control_ask.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln(f'...CALCULATING SUMMERSTATS...')
                    start_ns = time.time_ns()
                    file_name = zs.alg_zomerstats(l, dates['start'], dates['einde'], name, type)
                    end_ns = time.time_ns()
                    w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = control_ask.ask_open_url("Open the file with your (default) browser ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END CALCULATE SUMMER STATISTICS...{c.ln}{c.line}')

    control_ask.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice
def calc_heat_waves():
    fn.lnprintln(f'{c.line}{c.ln}START CALCULATE HEATWAVES...')
    dates = control_ask.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = control_ask.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = control_ask.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = control_ask.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln(f'...CALCULATING HEATWAVES...')
                    start_ns = time.time_ns()
                    file_name = hs.alg_heatwaves(l, dates['start'], dates['einde'], type, name)
                    end_ns = time.time_ns()
                    w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = control_ask.ask_open_url("Open the file with your (default) browser ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END CALCULATE HEATWAVES...{c.ln}{c.line}')

    control_ask.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice
def calc_allstats():
    fn.lnprintln(f'{c.line}{c.ln}START CALCULATE ALL STATISTICS...')
    dates = control_ask.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = control_ask.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = control_ask.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = control_ask.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln(f'...CALCULATING ALL STATISTICS...')
                    start_ns = time.time_ns()
                    file_name = alls.alg_allstats(l, dates['start'], dates['einde'], name, type)
                    end_ns = time.time_ns()
                    w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = control_ask.ask_open_url("Open the file with your (default) browser ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END CALCULATE ALL STATISTICS...{c.ln}{c.line}')

    control_ask.ask(f"Press a 'key' to go back to the main menu{c.ln}")

# Menu choice
def calc_allextremes():
    fn.lnprintln(f'{c.line}{c.ln}START CALCULATE ALL EXTREMES...')
    dates = control_ask.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        l = control_ask.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            type = control_ask.ask_file_type('Select filetype ? ')
            if type != c.stop:
                oke, name = True, False
                if type != 'cmd':
                    name = control_ask.ask_file_naam('Set a name for the output file ? <optional> ')
                    if name == c.stop:
                        oke = False
                if oke:
                    fn.lnprintln(f'...CALCULATING ALL EXTREMES...')
                    start_ns = time.time_ns()
                    file_name = ae.alg_allextremes(l, dates['start'], dates['einde'], name, type)
                    end_ns = time.time_ns()
                    w.write_process_time_ns('Total calculation time: ', (end_ns-start_ns) )

                    if type != 'cmd':
                        oke = control_ask.ask_open_url("Open the file with your (default) browser ?")
                        if oke:
                            webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END CALCULATE ALL EXTREMES...{c.ln}{c.line}')

    control_ask.ask(f"Press a 'key' to go back to the main menu{c.ln}")


def make_images():
    fn.lnprintln(f'{c.line}{c.ln}START MAKE IMAGE(S)...')
    dates = control_ask.ask_start_and_end_date() # Ask start and end date
    if dates != c.stop:
        oke = True
        l = control_ask.ask_stations('Select one or more stations ? ' )
        if l != c.stop:
            name = control_ask.ask_file_naam('Set a name for the output file ? <optional> ')
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

            oke = control_ask.ask_open_url("Open the image with your (default) browser ?")
            if oke:
                webbrowser.open_new(file_name) # Opens in default browser

    fn.lnprintln(f'END MAKE IMAGE(S)...{c.ln}{c.line}')

    control_ask.ask(f"Press a 'key' to go back to the main menu{c.ln}")
