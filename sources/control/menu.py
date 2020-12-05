'''Library contains functions for asking questions and to deal with the input
given by a user'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1.8"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, time, config, webbrowser
import numpy as np
import model.utils as utils
import model.search4days as search4days
import model.daydata as daydata
import model.winterstats as winterstats
import model.summerstats as summerstats
import model.allstats as allstats
import model.download as download
import model.dayvalues as model_dayvalues
import model.read as read
import model.current_weather as current_weather
import control.ask as control_ask
import control.io as io
import view.log as log
import view.translate as tr
import view.txt as view_txt
import view.dayvalues as view_dayvalues
import view.html as view_html
import view.color as vcolors
import view.graphs as view_graph

# Menu choice 1
def process_knmi_dayvalues_all():
    '''Function downloads, unzipped  all knmi stations in the list'''
    log.header('START DOWNLOADING ALL DATA DAYVALUES KNMI STATIONS...', True)

    st = time.time_ns()
    for stat in config.stations:
        daydata.process_data( stat )
    view_txt.show_process_time(st)

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
        for stat in stations:
            daydata.process_data( stat )
        view_txt.show_process_time(st)

        # Always ask for going back
        if stations.size != config.stations.size:
            again = control_ask.ask_again(f'Do you want to download more stations ?', True)
            if utils.quit_menu(again):
                break
        else:
            break

    log.footer('END DOWNLOAD STATION(s) KNMI DATA DAY VALUES...', True )

# Menu optie
def process_weather_knmi_global():
    '''Function downloads and print a global weather forecast from the website from the knmi'''
    log.header('START DOWNLOAD KNMI GLOBAL FORECAST...', True)

    ok, t = False, ''
    if utils.has_internet():
        sd   = utils.loc_date_now().strftime('%Y%m%d')
        url  = config.knmi_forecast_global_url
        file = utils.mk_path(config.dir_txt_forecasts, f'basisverwachting-{sd}.txt')
        ok = download.file( url, file )
        if ok:
            ok, t = read.file(file)
            if ok:
                t = '\n' + view_txt.clean_up( t )
                log.console(t, True)
            else:
                log.console('Not ok. Something went wrong along the way.')
    else:
        log.console('No internet connection...', True)

    log.footer('END DOWNLOAD KNMI GLOBAL FORECAST...', True)
    control_ask.ask_back_to_main_menu()

def process_weather_knmi_model():
    '''Function downloads and prints a discussion about the weather models from the website from the knmi'''
    log.header('START DOWNLOAD KNMI DISCUSSION WEATHER MODELS...', True)

    ok, t = False, ''
    if utils.has_internet():
        sd   = utils.loc_date_now().strftime('%Y%m%d')
        url  = config.knmi_forecast_model_url
        name = f'guidance_model-{sd}.txt'
        file = utils.mk_path(config.dir_txt_forecasts, name)
        ok = download.file( url, file )
        if ok:
            ok, t = read.file(file)
            if ok:
                t = '\n' + view_txt.clean_up( t )
                log.console(t, True)
            else:
                log.console('Not ok. Something went wrong along the way.')
    else:
        log.console('No internet connection...', True)

    log.footer('END DOWNLOAD KNMI DISCUSSION WEATHER MODELS...', True)
    control_ask.ask_back_to_main_menu()

def process_weather_knmi_current():
    '''Function downloads and print a actual weather values to the screen'''
    log.header('START DOWNLOAD CURRENT VALUES KNMI WEATHERSTATIONS...', True)

    ok, t = False, ''
    if utils.has_internet():
        ok, t = current_weather.knmi_stations()
        if ok:
            t = '\n' + view_txt.clean_up( t )
            log.console(t, True)
        else:
            log.console('Not ok. Something went wrong along the way.')
    else:
        log.console('No internet connection...', True)

    log.footer('END DOWNLOAD CURRENT VALUES KNMI WEATHERSTATIONS...', True)
    control_ask.ask_back_to_main_menu()


def process_weather_knmi_guidance():
    '''Function downloads and prints a global a more in depth forecast from the website from the knmi'''
    log.header('START DOWNLOAD KNMI GUIDANCE...', True)

    ok, t = False, ''
    if utils.has_internet():
        sd   = utils.loc_date_now().strftime('%Y%m%d')
        url  = config.knmi_forecast_guidance_url
        name = f'guidance_meerdaagse-{sd}.txt'
        file = utils.mk_path(config.dir_txt_forecasts, name)
        ok = download.file( url, file )
        if ok:
            ok, t = read.file(file)
            if ok:
                t = '\n' + view_txt.clean_up( t )
                log.console(t, True)
            else:
                log.console('Not ok. Something went wrong along the way.')
    else:
        log.console('No internet connection...', True)

    log.footer('END DOWNLOAD KNMI GUIDANCE...', True)
    control_ask.ask_back_to_main_menu()

# Menu choice 3
def get_dayvalues_by_date():
    '''Funtion gets day values from data knmi '''
    while True:
        log.header('START: SEARCHING AND PREPARING DAY VALUES...', True)
        # Ask for station
        stat = control_ask.ask_for_one_station('Select a weather station ? ', True)
        if utils.quit_menu(stat):
            break

        ymd, data = control_ask.ask_for_date_with_check_data(
                                stat, 'Select a date <yyyymmdd> ?', True
                            )
        if utils.quit_menu(ymd):
            break

        type = control_ask.ask_for_file_type( 'Select filetype ? ', 2, True )
        if utils.quit_menu(type):
            break

        # Ask for a file name
        if type != 'cmd':
            default = f'dayvalues-{stat.place.lower()}-{ymd}-{utils.now_act_for_file()}'
            fname = control_ask.ask_for_file_name (
                        f'Give a name for the {type} file ?', default, True
                    )
            if utils.quit_menu(fname):
                break

        st = time.time_ns()
        path = model_dayvalues.calculate(data, ymd, stat, type, fname)
        view_txt.show_process_time(st)

        fopen = control_ask.ask_to_open_with_app(
                    f'Open the file {path} in your browser ?', True
                )
        if fopen:
            webbrowser.open_new_tab(path)

        # Always ask for going back
        again = control_ask.ask_again(f'Do you want to select another station and date ?', True)
        if utils.quit_menu(again):
            break

    log.footer('END SEARCHING AND PREPARING DAY VALUES...', True)

# Menu choice 4
def search_for_days():
    '''Funtion searches files for days with specific values. ie > 30 degrees'''
    while True:
        log.header('START SEARCHING FOR SPECIFIC DAYS...', True)

        period = control_ask.ask_for_period(
                    'For which time periode do you want to search ? ', True
                    )
        if utils.quit_menu(period):
            break

        stations = control_ask.ask_for_stations('Select one or more weather stations ?', True)
        if utils.quit_menu(stations):
            break

        query = control_ask.ask_for_query('Type a query ? ', True)
        if utils.quit_menu(query):
            break

        type = control_ask.ask_for_file_type('Select filetype ? ')
        if utils.quit_menu(type):
            break

        default = f'days-{utils.make_query_txt_only(query)}-{period}-{utils.now_act_for_file()}'
        default = default.replace('*','x').replace(' ','')
        fname = control_ask.ask_for_file_name(
                        'Give a name for the file ? <optional>', default, True
                    )
        if utils.quit_menu(fname):
            break

        st = time.time_ns()
        path = search4days.calculate(stations, period, query, type, fname)
        view_txt.show_process_time(st)

        if type in [ 'text', 'html' ]:
            fopen = control_ask.ask_to_open_with_app(
                            f'\nOpen the file ? \n{path}\n', True
                        )
            if fopen:
                webbrowser.open_new_tab( path )

        # Always ask for going back
        again = control_ask.ask_again(f'Do you want to search for days again ?', True)
        if utils.quit_menu(again):
            break

    log.footer('END SEARCH FOR DAYS...', True)

def graph_period():
    '''Funtion makes images for a period from the data of the knmi'''
    while True:
        log.header('START MAKING A IMAGE GRAPH...', True)

        period = control_ask.ask_for_period('What time periode ?')
        if utils.quit_menu(period):
            break

        stations = control_ask.ask_for_stations('Select a weather station ?', True)
        if utils.quit_menu(stations):
            break

        entities = control_ask.ask_for_entities('Select a weather entities ?', True)
        if utils.quit_menu(entities):
            break

        log.console('Fill in the parameters for the image', False)
        title  = control_ask.ask_txt('Give a title for the graph', True)
        ylabel = control_ask.ask_txt('Give a y-as label for the graph', True)

        default_values = control_ask.ask_for_yn(
                    'Do you want to use default values ?\nSee file -> config.py...',
                    config.default_values,
                    True )
        if utils.quit_menu(default_values):
            break
        else:
            config.default_values = default_values[0]

        if config.default_values in config.answer_no:
            plot_width = control_ask.ask_for_int(
                                'Give the width (in pixels) for the graph.',
                                config.plot_width,
                                True )
            if utils.quit_menu(plot_width): break
            else: config.plot_width = plot_width

            plot_height = control_ask.ask_for_int(
                                'Give the height (in pixels) for the graph.',
                                config.plot_height,
                                True )
            if utils.quit_menu(plot_height): break
            else: config.plot_height = plot_height

            plot_graph_type = control_ask.ask_type_options(
                                    'Which type of graph do you want to use ? ',
                                    'graph', ['line', 'bar'],
                                    config.plot_graph_type,
                                    True )
            if utils.quit_menu(plot_graph_type): break
            else: config.plot_graph_type = plot_graph_type

            if config.plot_graph_type == 'line':
                # TODO MAKE OPTIONS FOR EACH ENTITIY LATER l_opt = []
                # option = { 'line-width': 1,
                #     	   'markersize': 2,
                #            'colors': vcolors.hexas().toList()
                #
                #            }

                plot_line_width = control_ask.ask_for_int (
                                            'Set the width of the line (in pixels) ? ',
                                            config.plot_line_width,
                                            True ) # Width line
                if utils.quit_menu(plot_line_width): break
                else: config.plot_line_width = plot_line_width

                plot_marker_size = control_ask.ask_for_int (
                                            'Set the marker size (in pixels) ? ',
                                            config.plot_marker_size,
                                            True ) # Dot sizes on day
                if utils.quit_menu(plot_marker_size): break
                else: config.plot_marker_size = plot_marker_size


            plot_cummul_val = control_ask.ask_for_yn(
                                    'Do you want cummulative values for the graph ? ',
                                    config.plot_cummul_val,
                                    True )
            if utils.quit_menu(plot_cummul_val): break
            else: config.plot_cummul_val = plot_cummul_val[0] # Take first yess or no

            plot_marker_txt = control_ask.ask_for_yn(
                                        'Values next to the markers ? ',
                                        config.plot_marker_txt,
                                        True )
            if utils.quit_menu(plot_marker_txt): break
            else: config.plot_marker_txt = plot_marker_txt[0] # Take first yess or no

            plot_climate_ave = control_ask.ask_for_yn(
                                        'Calculate and add climate averages too ? ',
                                        config.plot_climate_ave,
                                        True )
            if utils.quit_menu(plot_climate_ave): break
            else: config.plot_climate_ave = plot_climate_ave[0] # Take first yess or no

            plot_image_type = control_ask.ask_type_options(
                                    'What type of image ? ', 'image',
                                    ['png', 'jpg', 'ps', 'pdf', 'svg'],
                                    config.plot_image_type,
                                    True )
            if utils.quit_menu(plot_image_type): break
            else: config.plot_image_type = plot_image_type

            plot_dpi = control_ask.ask_for_int(
                                'Give the dpi ? ',
                                config.plot_dpi,
                                True )
            if utils.quit_menu(plot_dpi): break
            else: config.plot_dpi = plot_dpi

        default = f'graph-{period.replace("*", "x")}-{utils.now_act_for_file()}'
        name = control_ask.ask_for_file_name('Give a name for the file ? ', default, True)
        if utils.quit_menu(name):
            break

        st = time.time_ns()
        log.header( 'PREPARING IMAGES...', True )

        if config.plot_climate_ave in config.answer_yes:
            log.console('Calculating climate data might take a while...\n', True)

        path = utils.mk_path( config.dir_img_period, name + f'.{config.plot_image_type}' )
        view_graph.plot( stations, entities, period, title, ylabel, path )
        view_txt.show_process_time(st)

        fopen = control_ask.ask_to_open_with_app(
                    f'Open the image {name} in your browser ?', True
                )
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
        ok, period, stations, type, name = control_ask.ask_period_stations_type_name(
                                            'winterstats',
                                            True
                                            )

        if not ok:
            log.console('Something went wrong ...')
            break

        log.header(f'CALCULATING WINTER STATISTICS...', True)

        st = time.time_ns()
        path = winterstats.calculate( stations, period, name, type )
        view_txt.show_process_time(st)

        if type != 'cmd':
            fopen = control_ask.ask_to_open_with_app(
                        f'Open the {type} in your browser/application ?', True
                    )
            if fopen:
                webbrowser.open_new_tab(path)

        # Always ask for going back
        again = control_ask.ask_again(
                    f'Do you want to make another winterstatistics table ?', True
                )
        if utils.quit_menu(again):
            break

    log.footer(f'END CALCULATE WINTER STATISTICS...', True)

# Menu choice 6
def table_summerstats():
    '''Function makes calculations for winterstatistics'''
    while True:
        log.header('START CALCULATE SUMMER STATISTICS...', True)
        ok, period, stations, type, name = control_ask.ask_period_stations_type_name(
                                            'summerstats',
                                            True
                                            )
        if not ok:
            break
        else:
            log.header('CALCULATING SUMMER STATISTICS...', True)

            st = time.time_ns()
            path = summerstats.calculate( stations, period, name, type )
            view_txt.show_process_time(st)

            if type != 'cmd':
                fopen = control_ask.ask_to_open_with_app(
                            f'Open the {type} in your browser/application ?', True
                        )
                if fopen:
                    webbrowser.open_new_tab(path)

            # Always ask for going back
            again = control_ask.ask_again(
                        f'Do you want to make another summerstatistics table ?',
                        True
                    )
            if utils.quit_menu(again):
                break

    log.footer(f'END CALCULATE SUMMER STATISTICS...', True)

# Menu choice 7
def table_allstats():
    '''Function makes calculations for all statistics'''
    while True:
        log.header('START CALCULATE ALL STATISTICS...', True)
        # Ask for all in one
        ok, period, stations, type, name = control_ask.ask_period_stations_type_name(
                                            'allstats',
                                            True
                                            )

        if not ok:
            log.console('Something went wrong ...')
            break

        log.header(f'CALCULATING ALL STATISTICS...', True)

        st = time.time_ns()
        path = allstats.calculate( stations, period, name, type )
        view_txt.show_process_time(st)

        if type != 'cmd':
            fopen = control_ask.ask_to_open_with_app(
                        f'Open the {type} in your browser/application ?', True
                    )
            if fopen: webbrowser.open_new_tab(path)

        # Always ask for going back
        again = control_ask.ask_again(
                    f'Do you want to make another all statistics table ?', True
                )
        if utils.quit_menu(again):
            break

    log.footer(f'END CALCULATE ALL STATISTICS...', True)


# Menu choice 7
def table_heatwaves():
    while True:
        log.header('START CALCULATE HEATWAVES...', True)
        ok, period, stations, type, name = control_ask.ask_period_stations_type_name(True)

        if not ok:
            break
        else:
            log.header('CALCULATING HEATWAVES...', True)

            st = time.time_ns()
            # path = hs.alg_heatwaves(l, sd, ed, type, name)
            view_txt.show_process_time(st)

            if type != 'cmd':
                fopen = control_ask.ask_to_open_with_app(
                            f'Open the {type} in your browser/application ?',
                            True
                        )
                if fopen:
                    webbrowser.open_new_tab(path)

            # Always ask for going back
            again = control_ask.ask_again(
                        f'Do you want to make another heatwaves table ?',
                        True
                    )
            if utils.quit_menu(again):
                break

    log.footer(f'END CALCULATE HEATWAVES...', True)

# Menu choice 7
def table_coldwaves():
    while True:
        log.header('START CALCULATE COLDWAVES...', True)
        ok, period, stations, type, name = control_ask.ask_period_stations_type_name(True)

        if not ok:
            break
        else:
            log.header('CALCULATING COLDWAVES...', True)

            st = time.time_ns()
            # path = hs.alg_heatwaves(l, sd, ed, type, name)
            view_txt.show_process_time(st)

            if type != 'cmd':
                fopen = control_ask.ask_to_open_with_app(
                            f'Open the {type} in your browser/application ?',
                            True
                        )
                if fopen:
                    webbrowser.open_new_tab(path)

            # Always ask for going back
            again = control_ask.ask_again(
                        f'Do you want to make another coldwaves table ?',
                        True
                    )
            if utils.quit_menu(again):
                break

    log.footer(f'END CALCULATE COLDWAVES...', True)
