'''Library contains functions for asking questions and to deal with the input
given by a user'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.2.1'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import os, time, config, stations, webbrowser, numpy as np
import sources.model.utils as utils
import sources.model.search4days as search4days
import sources.model.daydata as daydata
import sources.model.winterstats as winterstats
import sources.model.summerstats as summerstats
import sources.model.allstats as allstats
import sources.model.dayvalues as model_dayvalues
import sources.model.current_weather as current_weather
import sources.control.ask as control_ask
import sources.control.fio as fio
import sources.view.log as log
import sources.view.translate as tr
import sources.view.txt as view_txt
import sources.view.dayvalues as view_dayvalues
import sources.view.html as view_html
import sources.view.color as vcolors
import sources.view.graphs as view_graph

# Menu choice 1
def process_knmi_dayvalues_all():
    '''Function downloads, unzipped  all knmi stations in the list'''
    log.header('START DOWNLOADING ALL DATA DAYVALUES KNMI STATIONS...', True)

    st = time.time_ns()
    for stat in stations.list:
        daydata.process_data( stat )
        log.console(' ', True)

    log.console(view_txt.process_time('Total processing time is ', st), True)

    log.footer('END DOWNLOADING ALL STATIONS KNMI DATA DAY VALUES', True)
    control_ask.ask_back_to_main_menu()

# Menu choice 2
def process_knmi_dayvalues_selected():
    '''Function asks for one or more wmo numbers to download their data'''
    log.header('START DOWNLOAD STATION(S) KNMI DATA DAY VALUES...', True )

    done, max = 0, (stations.list)
    while True:

        places = control_ask.ask_for_stations(
                                '\nSelect one or more stations ? ',
                                 stations.list
                                )
        if utils.is_quit(places):
            break

        log.console('\nStart processing data...\n', True)
        st = time.time_ns()
        for stat in places:
            daydata.process_data( stat )
            log.console(' ', True)

        log.console(view_txt.process_time('Total processing time is ', st), True)

        again = control_ask.ask_again(f'Do you want to download more stations ?', True)
        if utils.is_quit(again):
            break

    log.footer('END DOWNLOAD STATION(S) KNMI DATA DAY VALUES...', True )

# Menu optie
def process_weather_knmi_global():
    '''Function downloads and print a global weather forecast from the website from the knmi'''
    log.header('START DOWNLOAD KNMI GLOBAL FORECAST...', True)

    ok, t = False, ''
    if utils.has_internet():
        sd   = utils.loc_date_now().strftime('%Y%m%d')
        url  = config.knmi_forecast_global_url
        file = utils.mk_path(config.dir_txt_forecasts, f'basisverwachting-{sd}.txt')
        ok = fio.download( url, file )
        if ok:
            ok, t = fio.read(file)
            if ok:
                t = '\n' + view_txt.clean_up( t )
                log.console(t, True)
            else:
                log.console('Not ok. Something went wrong along the way.')
    else:
        log.console('No internet connection...', True)

    log.footer('END DOWNLOAD KNMI GLOBAL FORECAST...', True)
    control_ask.ask_back_to_main_menu()

def process_weather_buienradar_global():
    '''Function downloads and print a global weather forecast from the website from the knmi'''
    log.header('START DOWNLOAD BUIENRADAR GLOBAL FORECAST...', True)

    ok = False
    if utils.has_internet():
        t, url = '', config.buienradar_json_data
        ok, t = current_weather.buienradar_weather()
        if ok:
            t = '\n' + view_txt.clean_up( t )
            log.console(t, True)
        else:
            log.console('Not ok. Something went wrong along the way.')
    else:
        log.console('No internet connection...', True)

    log.footer('END DOWNLOAD BUIENRADAR GLOBAL FORECAST...', True)
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
        ok = fio.download( url, file )
        if ok:
            ok, t = fio.read(file)
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

def process_weather_buienradar_current():
    '''Function downloads and print a actual weather values to the screen'''
    log.header('START DOWNLOAD CURRENT VALUES BUIENRADAR WEATHERSTATIONS...', True)

    ok, t = False, ''
    if utils.has_internet():
        ok, t = current_weather.buienradar_stations()
        if ok:
            t = '\n' + view_txt.clean_up( t )
            log.console(t, True)
        else:
            log.console('Not ok. Something went wrong along the way.')
    else:
        log.console('No internet connection...', True)

    log.footer('END DOWNLOAD CURRENT VALUES BUIENRADAR WEATHERSTATIONS...', True)
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
        ok = fio.download(url, file)
        if ok:
            ok, t = fio.read(file)
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
        place = control_ask.ask_for_one_station('Select a weather station ? ')
        if not place:
            control_ask.ask_back_to_main_menu()
            break
        elif utils.is_quit(place):
            break

        ymd, data = control_ask.ask_for_date_with_check_data(
                                place, '\nSelect a date <yyyymmdd> ?'
                            )
        if utils.is_quit(ymd):
            break

        type = control_ask.ask_for_file_type(
                    '\nSelect output filetype ? ', config.default_output
                )
        if utils.is_quit(type):
            break

        # Ask for a file name
        if type != 'cmd':
            fname = f'dayvalues-{place.place.lower()}-{ymd}-{utils.now_for_file()}'
            fname = control_ask.ask_for_file_name (
                        f'\nGive a name for the {type} file ?', fname
                    )
            if utils.is_quit(fname):
                break

        st = time.time_ns()
        path = model_dayvalues.calculate(data, ymd, place, type, fname)
        log.console(view_txt.process_time('Total processing time is ', st), True)

        fopen = control_ask.ask_to_open_with_app(
                    f'\nOpen the file (type={type}) with your default application ?'
                )
        if fopen:
            webbrowser.open_new_tab(path)

        # Always ask for going back
        again = control_ask.ask_again(f'\nDo you want to select another station and date ?')
        if utils.is_quit(again):
            break

    log.footer('END SEARCHING AND PREPARING DAY VALUES...', True)

# Menu choice 4
def search_for_days():
    '''Funtion searches files for days with specific values. ie > 30 degrees'''
    while True:
        log.header('START SEARCHING FOR SPECIFIC DAYS...', True)

        period = control_ask.ask_for_period(
                    'For which time periode do you want to search ? '
                    )
        if utils.is_quit(period):
            break

        places = control_ask.ask_for_stations('\nSelect one or more weather stations ?')
        if not places:
            control_ask.ask_back_to_main_menu()
            break
        elif utils.is_quit(places):
            break

        query = control_ask.ask_for_query('\nType in a query for selecting days ? ')
        if utils.is_quit(query):
            break

        type = control_ask.ask_for_file_type(
                    '\nSelect output filetype ? ', config.default_output
                    )
        if utils.is_quit(type):
            break

        fname = f'days-{utils.make_query_txt_only(query)}-{period}-{utils.now_for_file()}'
        fname = fname.replace('*','x').replace(' ','')
        fname = control_ask.ask_for_file_name(
                        '\nGive a name for the file ? <optional>', fname
                    )
        if utils.is_quit(fname):
            break

        st = time.time_ns()
        path = search4days.calculate(places, period, query, type, fname)
        log.console(view_txt.process_time('Total processing time is ', st), True)

        if type in [ 'text', 'html' ]:
            fopen = control_ask.ask_to_open_with_app(
                            f'\nOpen the file (type={type}) with your default application ?'
                        )
            if fopen:
                webbrowser.open_new_tab( path )

        # Always ask for going back
        again = control_ask.ask_again(f'Do you want to search for days again ?', True)
        if utils.is_quit(again):
            break

    log.footer('END SEARCH FOR DAYS...', True)

def graph_period():
    '''Funtion makes images for a period from the data of the knmi'''
    while True:
        log.header('START MAKING A IMAGE GRAPH...', True)

        period = control_ask.ask_for_period('What time periode ?')
        if utils.is_quit(period):
            break

        places = control_ask.ask_for_stations('\nSelect weather station(s) ?')
        if not places:
            control_ask.ask_back_to_main_menu()
            break
        elif utils.is_quit(places):
            break

        entities = control_ask.ask_for_entities('\nSelect weather entity(s) ?')
        if utils.is_quit(entities):
            break

        log.console('Fill in the parameters for the image', False)
        title  = control_ask.ask_for_txt('\nGive a title for the graph')
        ylabel = control_ask.ask_for_txt('\nGive a y-as label for the graph')

        default = control_ask.ask_for_yn(
                    '\nDo you want to use default values ?\nSee file -> config.py...',
                    config.plot_default
                    )
        if utils.is_quit(default):
            break

        print(default)

        # Make option list
        options = {
            'plot_width'       : config.plot_width,
            'plot_height'      : config.plot_height,
            'plot_graph_type'  : config.plot_graph_type,
            'plot_line_width'  : config.plot_line_width,
            'plot_marker_size' : config.plot_marker_size,
            'plot_cummul_val'  : config.plot_cummul_val,
            'plot_marker_txt'  : config.plot_marker_txt,
            'plot_climate_ave' : config.plot_climate_ave,
            'plot_image_type'  : config.plot_image_type,
            'plot_dpi'         : config.plot_dpi
        }

        if utils.is_no(default):
            # Update option list
            plot_width = control_ask.ask_for_int(
                                '\nGive the width (in pixels) for the graph.',
                                config.plot_width )
            if utils.is_quit(plot_width): break
            else: options['plot_width'] = plot_width

            plot_height = control_ask.ask_for_int(
                                '\nGive the height (in pixels) for the graph.',
                                config.plot_height )
            if utils.is_quit(plot_height): break
            else: options['plot_height'] = plot_height

            plot_graph_type = control_ask.ask_type_options(
                                    '\nWhich type of graph do you want to use ? ',
                                    ['line', 'bar'],
                                    config.plot_graph_type )
            if utils.is_quit(plot_graph_type): break
            else: options['plot_graph_type'] = plot_graph_type

            if config.plot_graph_type == 'line':
                # TODO MAKE OPTIONS FOR EACH ENTITIY LATER l_opt = []
                # option = { 'line-width': 1,
                #     	   'markersize': 2,
                #            'colors': vcolors.hexas().toList()
                #
                #            }

                plot_line_width = control_ask.ask_for_int (
                                            '\nSet the width of the line (in pixels) ? ',
                                            config.plot_line_width ) # Width line
                if utils.is_quit(plot_line_width): break
                else: options['plot_line_width'] = plot_line_width

                plot_marker_size = control_ask.ask_for_int (
                                            '\nSet the marker size (in pixels) ? ',
                                            config.plot_marker_size ) # Dot sizes on day
                if utils.is_quit(plot_marker_size): break
                else: options['plot_marker_size'] = plot_marker_size

            plot_cummul_val = control_ask.ask_for_yn(
                                    '\nDo you want cummulative values for the graph ? ',
                                    config.plot_cummul_val )
            if utils.is_quit(plot_cummul_val): break
            else: options['plot_cummul_val'] = plot_cummul_val[0] # Take first yess or no

            plot_marker_txt = control_ask.ask_for_yn(
                                        '\nValues next to the markers ? ',
                                        config.plot_marker_txt )
            if utils.is_quit(plot_marker_txt): break
            else: options['plot_marker_txt'] = plot_marker_txt[0] # Take first yess or no

            plot_climate_ave = control_ask.ask_for_yn(
                                        '\nCalculate and add climate averages too ? ',
                                        config.plot_climate_ave )
            if utils.is_quit(plot_climate_ave): break
            else: options['plot_climate_ave'] = plot_climate_ave[0] # Take first yess or no

            plot_image_type = control_ask.ask_type_options(
                                    '\nWhat type of image ? ',
                                    ['png', 'jpg', 'ps', 'pdf', 'svg'],
                                    config.plot_image_type )
            if utils.is_quit(plot_image_type): break
            else: options['plot_image_type'] = plot_image_type

            plot_dpi = control_ask.ask_for_int( '\nGive the dpi ? ', config.plot_dpi )
            if utils.is_quit(plot_dpi): break
            else: options['plot_dpi'] = plot_dpi

        fname = f"graph-{period.replace('*', 'x')}-{utils.now_for_file()}"
        fname = control_ask.ask_for_file_name('\nGive a name for the file ? ', fname)
        if utils.is_quit(fname):
            break

        log.header( 'PREPARING IMAGES...', True )
        st = time.time_ns()
        path = view_graph.plot( places, entities, period, title, ylabel, fname, options )
        log.console(view_txt.process_time('Total processing time is ', st), True)

        fopen = control_ask.ask_to_open_with_app(
                    f'\nOpen the file (type={type}) with your default application ?'
                )
        if fopen: webbrowser.open_new_tab(path)

        # Always ask for going back
        again = control_ask.ask_again(f'\nDo you want to make more images ?')
        if utils.is_quit(again):
            break

    log.footer('END MAKING A IMAGE GRAPH...', True)

# Menu choice 5
def table_winterstats():
    '''Function makes calculations for winterstatistics'''
    while True:
        log.header('START CALCULATE WINTER STATISTICS...', True)
        # Ask for all in one
        ok, period, places, type, name = control_ask.ask_period_stations_type_name(
                                            'winter'
                                            )
        if not ok:
            control_ask.ask_back_to_main_menu()
            break

        log.header(f'CALCULATING WINTER STATISTICS...', True)

        st = time.time_ns()
        path = winterstats.calculate( places, period, name, type )
        log.console(view_txt.process_time('Total processing time is ', st), True)

        if type != 'cmd':
            fopen = control_ask.ask_to_open_with_app(
                        f'\nOpen the file (type={type}) with your default application ?'
                    )
            if fopen:
                webbrowser.open_new_tab(path)

        # Always ask for going back
        again = control_ask.ask_again(
                    f'\nDo you want to make another winterstatistics table ?'
                )
        if utils.is_quit(again):
            break

    log.footer(f'END CALCULATE WINTER STATISTICS...', True)

# Menu choice 6
def table_summerstats():
    '''Function makes calculations for winterstatistics'''
    while True:
        log.header('START CALCULATE SUMMER STATISTICS...', True)
        ok, period, places, type, name = control_ask.ask_period_stations_type_name(
                                            'summer'
                                            )
        if not ok:
            control_ask.ask_back_to_main_menu()
            break

        log.header('CALCULATING SUMMER STATISTICS...', True)

        st = time.time_ns()
        path = summerstats.calculate( places, period, name, type )
        log.console(view_txt.process_time('Total processing time is ', st), True)

        if type != 'cmd':
            fopen = control_ask.ask_to_open_with_app(
                        f'\nOpen the file (type={type}) with your default application ?'
                    )
            if fopen:
                webbrowser.open_new_tab(path)

        # Always ask for going back
        again = control_ask.ask_again(
                    f'\nDo you want to make another summerstatistics table ?'
                )
        if utils.is_quit(again):
            break

    log.footer(f'END CALCULATE SUMMER STATISTICS...', True)

# Menu choice 7
def table_allstats():
    '''Function makes calculations for all statistics'''
    while True:
        log.header('START CALCULATE ALL STATISTICS...', True)
        # Ask for all in one
        ok, period, places, type, name = control_ask.ask_period_stations_type_name(
                                            'all'
                                            )
        if not ok:
            control_ask.ask_back_to_main_menu()
            break

        log.header(f'CALCULATING ALL STATISTICS...', True)

        st = time.time_ns()
        path = allstats.calculate( places, period, name, type )
        log.console(view_txt.process_time('Total processing time is ', st), True)

        if type != 'cmd':
            fopen = control_ask.ask_to_open_with_app(
                        f'\nOpen the file (type={type}) with your default application ?'
                    )
            if fopen: webbrowser.open_new_tab(path)

        # Always ask for going back
        again = control_ask.ask_again(
                    f'\nDo you want to make another all statistics table ?'
                )
        if utils.is_quit(again):
            break

    log.footer(f'END CALCULATE ALL STATISTICS...', True)

# # Menu choice 7
# def table_heatwaves():
#     while True:
#         log.header('START CALCULATE HEATWAVES...', True)
#         ok, period, places, type, name = control_ask.ask_period_stations_type_name(True)
#
#         if not ok:
#             break
#         else:
#             log.header('CALCULATING HEATWAVES...', True)
#
#             st = time.time_ns()
#             # path = hs.alg_heatwaves(l, sd, ed, type, name)
#             view_txt.show_process_time(st)
#
#             if type != 'cmd':
#                 fopen = control_ask.ask_to_open_with_app(
#                             f'\nOpen the file (type={type}) with your default application ?'
#                             )
#                 if fopen:
#                     webbrowser.open_new_tab(path)
#
#             # Always ask for going back
#             again = control_ask.ask_again(
#                         f'Do you want to make another heatwaves table ?',
#                         True
#                     )
#             if utils.is_quit(again):
#                 break
#
#     log.footer(f'END CALCULATE HEATWAVES...', True)
#
# # Menu choice 7
# def table_coldwaves():
#     while True:
#         log.header('START CALCULATE COLDWAVES...', True)
#         ok, period, places, type, name = control_ask.ask_period_stations_type_name(True)
#
#         if not ok:
#             break
#         else:
#             log.header('CALCULATING COLDWAVES...', True)
#
#             st = time.time_ns()
#             # path = hs.alg_heatwaves(l, sd, ed, type, name)
#             view_txt.show_process_time(st)
#
#             if type != 'cmd':
#                 fopen = control_ask.ask_to_open_with_app(
#                             f'\nOpen the file (type={type}) with your default application ?'
#                             )
#                 if fopen:
#                     webbrowser.open_new_tab(path)
#
#             # Always ask for going back
#             again = control_ask.ask_again(
#                         f'Do you want to make another coldwaves table ?'
#                         )
#             if utils.is_quit(again):
#                 break
#
#     log.footer(f'END CALCULATE COLDWAVES...', True)
