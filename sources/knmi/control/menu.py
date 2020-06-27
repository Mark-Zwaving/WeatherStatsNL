'''Library contains functions for asking questions and to deal with the input
given by a user'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1.0"
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
import view.graphs as view_graph
import numpy as np

# Menu choice 1
def process_knmi_dayvalues_all():
    '''Function downloads, unzipped  all knmi stations in the list'''
    log.header('START DOWNLOADING ALL DATA DAYVALUES KNMI STATIONS...', True)
    st = time.time_ns()
    for station in config.stations:
        daydata.process_data( station )
    log.console(view_txt.menu_process_time(st) + '\n', True)
    log.footer('END DOWNLOADING ALL STATIONS KNMI DATA DAY VALUES', True)
    control_ask.ask_back_to_main_menu()

# Menu choice 2
def process_knmi_dayvalues_selected():
    '''Function asks for one or more wmo numbers to download their data'''
    while True:
        log.header('START DOWNLOAD STATION KNMI DATA DAY VALUES...', True )

        stations = control_ask.ask_for_stations('Select one or more stations ? ')
        if utils.quit_menu(stations):
            break

        log.header('...DOWNLOADING STARTED...', True )
        st = time.time_ns()
        for station in stations:
            daydata.process_data( station )
        log.console(view_txt.menu_process_time(st) + '\n', True)

        # Always ask for going back
        if stations.size != config.stations.size:
            again = control_ask.ask_again(f'Do you want to download more stations ?', True)
            if utils.quit_menu(again):
                break
        else:
            break

    log.footer('END DOWNLOAD STATION(s) KNMI DATA DAY VALUES...', True )

# Menu choice 3
def get_dayvalues_by_date():
    '''Funtion gets day values from data knmi '''
    while True:
        log.header('START: SEARCHING AND PREPARING DAY VALUES...', True)
        # Ask for station
        station = control_ask.ask_for_one_station('Select a weather station ? ', True)
        if utils.quit_menu(station):
            break

        log.console(f'Loading data {station.place} ...')
        ok, data = daydata.read( station )
        if not ok:
            log.console( 'Error reading data!', station.place, yyyymmdd )
            break

        txt = '\nSelect a date <yyyymmdd> ?\n'
        yyyymmdd = control_ask.ask_for_date_with_check_data(station, data, txt, True)
        if utils.quit_menu(yyyymmdd):
            break

        type = control_ask.ask_for_file_type('Select filetype ? ')
        if utils.quit_menu(type):
            break

        # Ask for a file name
        name = False
        if type != 'cmd':
            name = control_ask.ask_for_file_name( f'Give a name for the {type} file ? <optional> ',
                                                  f'dayvalues-{yyyymmdd}',
                                                  True )
            if utils.quit_menu(name):
                break
            name += f'.{type}'

        st = time.time_ns()
        log.header('SEARCHING FOR AND PREPARING DAY VALUES', True)
        log.console(f'Station: {station.wmo} {station.place}', True)
        log.console(f'Date: {utils.ymd_to_txt(yyyymmdd)}', True)

        day = data[np.where(data[:,daydata.YYYYMMDD] == int(yyyymmdd))][0]
        txt_date = utils.ymd_to_txt(yyyymmdd)
        footer = station.dayvalues_notification

        # Make output
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

        log.console(view_txt.menu_process_time(st) + '\n', True)

        # Always ask for going back
        again = control_ask.ask_again(f'Do you want to select another station and date ?', True)
        if utils.quit_menu(again):
            break

    log.footer('END SEARCHING AND PREPARING DAY VALUES...', True)

def select_days():
    pass

# Menu choice 4
def graph_period():
    '''Funtion makes images for a period from the data of the knmi'''
    while True:
        log.header('START MAKING A IMAGE GRAPH...', True)

        log.console( 'What time periode ?\n' )
        s_ymd, e_ymd = control_ask.ask_for_start_and_end_date( )
        if utils.quit_menu(s_ymd) or utils.quit_menu(e_ymd):
            break

        stations = control_ask.ask_for_stations('Select a weather station ?', True)
        if utils.quit_menu(stations):
            break

        entities = control_ask.ask_for_entities('Select a weather entities ?', True)
        if utils.quit_menu(entities):
            break

        graph = control_ask.ask_for_graph_type('Which type of graph do you want to use ?', space=True)
        if utils.quit_menu(graph):
            break

        name = control_ask.ask_for_file_name( 'Give a name for the image file ? <optional>',
                                              f'period-{s_ymd}-{e_ymd}',
                                              True )
        if utils.quit_menu(name):
            break

        log.console('Fill in the parameters for the image', True)
        title  = control_ask.ask_txt('Give a title for the graph ? ')
        ylabel = control_ask.ask_txt('Give a y-as label for the graph ? ')

        more = control_ask.ask_for_yn('Use default values ?\nSee file -> config.py...')
        if utils.quit_menu(more):
            break

        if np.array_equal( more, config.answer_no ):
            config.plot_width  = control_ask.ask_for_int('Give the width (in pixels) for the graph ? ', space=False)
            config.plot_height = control_ask.ask_for_int('Give the height (in pixels) for the graph ? ', space=False)
            answ_yn = control_ask.ask_for_yn('Values next to the markers ? ', space=False )
            config.plot_marker_txt = 'y' if np.array_equal(answ_yn,config.answer_yes) else 'n'
            config.plot_image_type = control_ask.ask_type_options(
                                'What type of image ? ', 'image',
                                ['png', 'jpg', 'ps', 'pdf', 'svg'],
                                space=False )
            config.plot_dpi = control_ask.ask_for_int('Give the dpi ? ', space=False)
            config.plot_graph_type = control_ask.ask_type_options(
                                         'What type of graph ? ', 'graph',
                                         ['line', 'bar'],
                                         space=False )

        st = time.time_ns()
        log.header( 'PREPARING IMAGES...', True )
        path = utils.path( config.dir_img_period, name + f'.{config.plot_image_type}' )
        view_graph.plot( stations, entities, s_ymd, e_ymd, title, ylabel, path )

        log.console(view_txt.menu_process_time(st) + '\n', True)

        fopen = control_ask.ask_to_open_with_app( f'Open the image {name} in your browser ?', True)
        if fopen:
            webbrowser.open_new_tab(path)

        # Always ask for going back
        again = control_ask.ask_again(f'Do you want to make more images ?', True)
        if utils.quit_menu(again):
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
            log.console('Something went wrong ...')
            break

        log.header(f'CALCULATING WINTER STATISTICS...', True)

        st = time.time_ns()
        path = winterstats.calculate( stations, sd, ed, name, type )
        log.console(view_txt.menu_process_time(st) + '\n', True)

        if type != 'cmd':
            fopen = control_ask.ask_to_open_with_app(f'Open the {type} in your browser/application ?', True)
            if fopen:
                webbrowser.open_new_tab(path)

        # Always ask for going back
        again = control_ask.ask_again(f'Do you want to make another winterstatistics table ?', True)
        if utils.quit_menu(again):
            break

    log.footer(f'END CALCULATE WINTER STATISTICS...', True)

# Menu choice 6
def table_summerstats():
    '''Function makes calculations for winterstatistics'''
    while True:
        log.header('START CALCULATE SUMMER STATISTICS...', True)
        ok, sd, ed, stations, type, name = control_ask.ask_period_stations_type_name(True)
        if not ok:
            break
        else:
            log.header('CALCULATING WINTER STATISTICS...', True)

            st = time.time_ns()
            path = summerstats.calculate( stations, sd, ed, name, type )
            log.console(view_txt.menu_process_time(st) + '\n', True)

            if type != 'cmd':
                fopen = control_ask.ask_to_open_with_app(f'Open the {type} in your browser/application ?', True)
                if fopen:
                    webbrowser.open_new_tab(path)

            # Always ask for going back
            again = control_ask.ask_again(f'Do you want to make another summerstatistics table ?', True)
            if utils.quit_menu(again):
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
            log.console(view_txt.menu_process_time(st) + '\n', True)

            if type != 'cmd':
                fopen = control_ask.ask_to_open_with_app(f'Open the {type} in your browser/application ?', True)
                if fopen:
                    webbrowser.open_new_tab(path)

            # Always ask for going back
            again = control_ask.ask_again(f'Do you want to make another heatwaves table ?', True)
            if utils.quit_menu(again):
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
            log.console(view_txt.menu_process_time(st) + '\n', True)

            if type != 'cmd':
                fopen = control_ask.ask_to_open_with_app(f'Open the {type} in your browser/application ?', True)
                if fopen:
                    webbrowser.open_new_tab(path)


            # Always ask for going back
            again = control_ask.ask_again(f'Do you want to make another summerstatistics table ?', True)
            if utils.quit_menu(again):
                break

    log.footer(f'END CALCULATE STATISTICS...', True)

# Menu choice 9
def table_allextremes():
    while True:
        log.header('START CALCULATE EXTREMES...', True)
        ok, sd, ed, stations, type, name = control_ask.ask_period_stations_type_name(True)
        if not ok:
            break
        else:
            log.header('CALCULATING EXTREMES...', True)

            st = time.time_ns()
            # path = ae.alg_allextremes(l, sd, ed, name, type)
            log.console(view_txt.menu_process_time(st) + '\n', True)

            if type != 'cmd':
                fopen = control_ask.ask_to_open_with_app(f'Open the {type} in your browser/application ?', True)
                if fopen:
                    webbrowser.open_new_tab(path)

            # Always ask for going back
            again = control_ask.ask_again(f'Do you want to make another statistics table for extremes ?', True)
            if utils.quit_menu(again):
                break

    log.footer(f'END CALCULATE EXTREMES...', True)
