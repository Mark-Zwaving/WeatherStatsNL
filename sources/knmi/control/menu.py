'''Library contains functions for asking questions and to deal with the input
given by a user'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.9"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, time, config, webbrowser, subprocess
import model.utils as utils
import model.convert as convert
import knmi.model.daydata as daydata
import knmi.model.winterstats as winterstats
import knmi.view.dayvalues as view_dayvalues
import control.ask as control_ask
import control.io as io
import view.log as log
import view.translate as tr
import view.txt as view_txt
import view.html as view_html
import view.graphs as graph
import numpy as np

def menu_choices( choice ):
    if   choice ==  '1':  process_knmi_dayvalues_all()
    elif choice ==  '2':  process_knmi_dayvalues_selected()
    elif choice ==  '3':  get_dayvalues_by_date()
    elif choice ==  '4':  graph_period()
    elif choice ==  '5':  table_winterstats()
    elif choice ==  'x':  table_zomerstats()
    elif choice ==  'x':  table_heat_waves()
    elif choice ==  'x':  table_allstats()
    elif choice ==  'x':  table_allextremes()
    else:
        log.console(f'Input {choice} unknown. Try again...', True)

# Menu choice 1
def process_knmi_dayvalues_all():
    '''Function downloads, unzipped  all knmi stations in the list'''
    log.header('START DOWNLOADING ALL DATA DAYVALUES KNMI STATIONS...', True)
    st = time.time_ns()
    for station in config.stations:
        daydata.process_data( station )
    log.console(view_txt.menu_process_time(st), True)
    log.footer('END DOWNLOADING ALL STATIONS KNMI DATA DAY VALUES', True)
    control_ask.ask_back_to_main_menu()

# Menu choice 2
def process_knmi_dayvalues_selected():
    '''Function asks for one or more wmo numbers to download their data'''
    while True:
        log.header('START DOWNLOAD STATION KNMI DATA DAY VALUES...', True )
        l = control_ask.ask_for_stations('Select one or more stations ? ')
        if l != config.answer_quit:
            break
        else:
            log.header('...DOWNLOADING STARTED...', True )
            st = time.time_ns()
            for station in l:
                daydata.process_data( station )
            log.console(view_txt.menu_process_time(st), True)

        # Always ask for going back
        again = control_ask.ask_again(f'Do you want to download more stations ?', True)
        if again == config.answer_quit:
            break

    log.footer('END DOWNLOAD STATION(s) KNMI DATA DAY VALUES...', True )

# Menu choice 3
def get_dayvalues_by_date():
    '''Funtion gets day values from data knmi '''
    while True:
        log.header('START: SEARCHING AND PREPARING DAY VALUES...', True)
        # Ask for station
        station = control_ask.ask_for_one_station('Select a weather station ? ', True)
        if station == config.answer_quit:
            break
        else:
            log.console(f'Loading data {station.place} ...')
            ok, data = daydata.read( station )
            if ok:
                txt = '\nSelect a date <yyyymmdd> ?\n'
                yyyymmdd = control_ask.ask_for_date_with_check_data(station, data, txt, True)
                if yyyymmdd == config.answer_quit:
                    break
                else:
                    type = control_ask.ask_for_file_type('Select filetype ? ')
                    if type == config.answer_quit:
                        break
                    else:
                        ok, name = True, False
                        if type != 'cmd': # Ask for a file name
                            name = control_ask.ask_for_file_name(f'Give a name for the {type} file ? <optional> ', True)
                            if not name:
                                print(name)
                                now  = utils.now_act_for_file()
                                name = f'dayvalues-{yyyymmdd}-{now}.{type}'
                                print(name)
                            elif name == config.answer_quit:
                                break

                        if ok:
                            st = time.time_ns()
                            log.header('SEARCHING FOR AND PREPARING DAY VALUES', True)
                            log.console(f'Station: {station.wmo} {station.place}', True)
                            log.console(f'Date: {utils.ymd_to_txt(yyyymmdd)}', True)

                            day = data[np.where(data[:,daydata.YYYYMMDD] == int(yyyymmdd))][0]

                            if ok:
                                txt_date = utils.ymd_to_txt(yyyymmdd)
                                footer = station.dayvalues_notification

                                if type == 'html':
                                    header  = f'<i class="text-info fas fa-home"></i> '
                                    header += f'{station.wmo} - {station.place} '
                                    header += f'{station.province} - {txt_date} '

                                    page = view_html.Template()
                                    page.title  = f'{station.place}-{yyyymmdd}'
                                    page.header = header
                                    page.main   = view_html.main_ent( day )
                                    page.footer = footer
                                    page.file_name = name

                                    et = False
                                    if page.save(): # Error
                                        et = time.time_ns()
                                        fopen = control_ask.ask_to_open_with_app(f'Open the file {name} in your browser ?', True)
                                        if fopen:
                                            webbrowser.open_new_tab( page.file_path ) # Opens in default browser
                                    else:
                                        et = time.time_ns()

                                elif type == 'txt':
                                    title = txt_date
                                    main  = view_dayvalues.txt_main( day )
                                    txt   = f'{title}\n{main}'
                                    path  = utils.path( config.dir_txt_dayvalues, name )

                                    if io.save(path, txt):
                                        et = time.time_ns()
                                        fopen = control_ask.ask_to_open_with_app(f'Open the file {path} in your browser ?', True)
                                        if fopen:
                                            webbrowser.open_new_tab(path)
                                    else:
                                        et = time.time_ns()

                                elif type == 'image':
                                    title = txt_date
                                    main  = view_dayvalues.txt_main( day )
                                    txt   = f'{title}\n{main}'
                                    path  = utils.path( config.dir_txt_dayvalues, name )

                                    if io.save(path, txt):
                                        et = time.time_ns()
                                        fopen = control_ask.ask_to_open_with_app(f'Open the file {path} in your browser ?', True)
                                        if fopen:
                                            webbrowser.open_new_tab(path)
                                    else:
                                        et = time.time_ns()

                                log.console(view_txt.menu_process_time(st), True)
                            else:
                                log.console( 'Error reading data!', station.place, yyyymmdd )

        # Always ask for going back
        again = control_ask.ask_again(f'Do you want to select another station and date ?', True)
        if again == config.answer_quit:
            break

    log.footer('END SEARCHING AND PREPARING DAY VALUES...', True)

# Menu choice 4
def graph_period():
    '''Funtion makes images for a period from the data of the knmi'''
    while True:
        log.header('START MAKING A IMAGE GRAPH...', True)
        log.console( 'What time periode ?\n' )
        s_ymd, e_ymd = control_ask.ask_for_start_and_end_date( )
        if s_ymd != config.answer_quit and e_ymd != config.answer_quit:
            stations = control_ask.ask_for_stations('Select a weather station ?', True)
            if stations != config.answer_quit:
                entities = control_ask.ask_for_entities('Select a weather entities ?', True)
                if entities != config.answer_quit:

                    # TODO: make options for other type graphs
                    # type = control_ask.ask_for_graph_type('Select graph type ? ')

                    name = control_ask.ask_for_file_name( f'Give a name for the .png file ? <optional>', True)
                    if name != config.answer_quit:
                        log.console('Fill in the parameters for the image', True)
                        title  = control_ask.ask_txt('Give a title for the graph ? ', space=False)
                        ylabel = control_ask.ask_txt('Give a y-as label for the graph ? ', space=False)
                        # width  = control_ask.ask_txt('Give the width (in pixels) for the graph ? ', space=False)
                        # height = control_ask.ask_txt('Give the height (in pixels) for the graph ? ', space=False)

                        width  = 1280
                        height =  720
                        size   = ( convert.pixel_to_inch(width), convert.pixel_to_inch(height) )

                        st = time.time_ns()
                        log.header( 'PREPARING IMAGES...', True )

                        if not name:
                            name = graph.name( s_ymd, e_ymd, stations, entities )
                        path = utils.path( config.dir_img_period, name )
                        graph.plot( stations, entities, s_ymd, e_ymd, title, ylabel, size, path )

                        log.console(view_txt.menu_process_time(st), True)

                        fopen = control_ask.ask_to_open_with_app( f'Open the image {name} in your browser ?', True)
                        if fopen:
                            webbrowser.open_new_tab(path)

        # Always ask for going back
        again = control_ask.ask_again(f'Do you want to make more images ?', True)
        if again == config.answer_quit:
            break
    log.footer('END MAKING A IMAGE GRAPH...', True)


# Menu choice 5
def table_winterstats():
    '''Function makes calculations for winterstatistics'''
    while True:
        log.header('START CALCULATE WINTER STATISTICS...', True)
        # Ask for all in one
        ok, sd, ed, stations, type, name = control_ask.ask_period_stations_type_name(True)

        if not ok:
            break
        else:
            log.header(f'CALCULATING WINTER STATISTICS...', True)

            st = time.time_ns()
            path = winterstats.calculation( stations, sd, ed, name, type )
            log.console(view_txt.menu_process_time(st), True)

            if type != 'cmd':
                fopen = control_ask.ask_to_open_with_app(f'Open the {type} in your browser/application ?', True)
                if fopen:
                    webbrowser.open_new_tab(path)

            # Always ask for going back
            again = control_ask.ask_again(f'Do you want to make another winterstatistics table ?', True)
            if again == config.answer_quit:
                break

    log.footer(f'END CALCULATE WINTER STATISTICS...', True)

# Menu choice 6
def table_zomerstats():
    '''Function makes calculations for winterstatistics'''
    while True:
        log.header('START CALCULATE SUMMER STATISTICS...', True)
        ok, sd, ed, stations, type, name = control_ask.ask_period_stations_type_name(True)
        if not ok:
            break
        else:
            log.header('CALCULATING WINTER STATISTICS...', True)

            st = time.time_ns()
            path = summerstats.calculation( stations, sd, ed, name, type )
            log.console(view_txt.menu_process_time(st), True)

            if type != 'cmd':
                fopen = control_ask.ask_to_open_with_app(f'Open the {type} in your browser/application ?', True)
                if fopen:
                    webbrowser.open_new_tab(path)

            # Always ask for going back
            again = control_ask.ask_again(f'Do you want to make another summerstatistics table ?', True)
            if again == config.answer_quit:
                break

    log.footer(f'END CALCULATE SUMMER STATISTICS...', True)

# Menu choice 7
def table_heatwaves():
    while True:
        log.header('START CALCULATE HEATWAVES...', True)
        ok, sd, ed, stations, type, name = control_ask.ask_period_stations_type_name(True)

        if not ok:
            break
        else:
            log.header('CALCULATING HEATWAVES...', True)

            st = time.time_ns()
            # path = hs.alg_heatwaves(l, sd, ed, type, name)
            log.console(view_txt.menu_process_time(st), True)

            if type != 'cmd':
                fopen = control_ask.ask_to_open_with_app(f'Open the {type} in your browser/application ?', True)
                if fopen:
                    webbrowser.open_new_tab(path)

            # Always ask for going back
            again = control_ask.ask_again(f'Do you want to make another heatwaves table ?', True)
            if again == config.answer_quit:
                break

    log.footer(f'END CALCULATE HEATWAVES...', True)

# Menu choice 8
def table_allstats():
    while True:
        log.header('START CALCULATE STATISTICS...', True)
        ok, sd, ed, stations, type, name = control_ask.ask_period_stations_type_name(True)
        if not ok:
            break
        else:
            log.header('CALCULATING STATISTICS...', True)

            st = time.time_ns()
            # path = alls.alg_allstats(stations, sd, ed, name, type)
            log.console(view_txt.menu_process_time(st), True)

            if type != 'cmd':
                fopen = control_ask.ask_to_open_with_app(f'Open the {type} in your browser/application ?', True)
                if fopen:
                    webbrowser.open_new_tab(path)


            # Always ask for going back
            again = control_ask.ask_again(f'Do you want to make another summerstatistics table ?', True)
            if again == config.answer_quit:
                break

    log.footer(f'END CALCULATE STATISTICS...', True)

# Menu choice 9
def calc_allextremes():
    while True:
        log.header('START CALCULATE EXTREMES...', True)
        ok, sd, ed, stations, type, name = control_ask.ask_period_stations_type_name(True)
        if not ok:
            break
        else:
            log.header('CALCULATING EXTREMES...', True)

            st = time.time_ns()
            # path = ae.alg_allextremes(l, sd, ed, name, type)
            log.console(view_txt.menu_process_time(st), True)

            if type != 'cmd':
                fopen = control_ask.ask_to_open_with_app(f'Open the {type} in your browser/application ?', True)
                if fopen:
                    webbrowser.open_new_tab(path)

            # Always ask for going back
            again = control_ask.ask_again(f'Do you want to make another statistics table for extremes ?', True)
            if again == config.answer_quit:
                break

    log.footer(f'END CALCULATE EXTREMES...', True)
