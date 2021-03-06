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
import sources.model.winterstats as winstats
import sources.model.summerstats as sumstats
import sources.model.allstats as allstats
import sources.model.dayvalues as mdayval
import sources.model.current_weather as mcurweather
import sources.control.ask as cask
import sources.control.fio as fio
import sources.view.console as console
import sources.view.translate as tr
import sources.view.txt as vt
import sources.view.color as vcol
import sources.view.graphs as vg

# Menu choice 1
def process_knmi_dayvalues_all():
    '''Function downloads, unzipped  all knmi stations in the list'''
    console.header('START DOWNLOADING ALL DATA DAYVALUES KNMI STATIONS...', True)

    st = time.time_ns()
    for stat in stations.list:
        daydata.process_data( stat )
        console.log(' ', True)

    console.log(vt.process_time('Total processing time is ', st), True)

    console.footer('END DOWNLOADING ALL STATIONS KNMI DATA DAY VALUES', True)
    cask.ask_back_to_main_menu()

# Menu choice 2
def process_knmi_dayvalues_selected():
    '''Function asks for one or more wmo numbers to download their data'''
    console.header('START DOWNLOAD STATION(S) KNMI DATA DAY VALUES...', True )

    done, max = 0, (stations.list)
    while True:

        places = cask.ask_for_stations(
                                '\nSelect one or more stations ? ',
                                 stations.list
                                )
        if utils.is_quit(places):
            break

        st = time.time_ns()
        for stat in places:
            daydata.process_data( stat )
            console.log(' ', True)

        console.log(vt.process_time('Total processing time is ', st), True)

        again = cask.ask_again(f'Do you want to download more stations ?', True)
        if utils.is_quit(again):
            break

    console.footer('END DOWNLOAD STATION(S) KNMI DATA DAY VALUES...', True )

# Menu optie
def process_weather_knmi_global():
    '''Function downloads and print a global weather forecast from the website from the knmi'''
    console.header('START DOWNLOAD KNMI GLOBAL FORECAST...', True)

    ok, t = False, ''
    if utils.has_internet():
        sd   = utils.loc_date_now().strftime('%Y%m%d')
        url  = config.knmi_forecast_global_url
        file = utils.mk_path(config.dir_forecasts_txt, f'basisverwachting-{sd}.txt')
        ok = fio.download( url, file )
        if ok:
            ok, t = fio.read(file)
            if ok:
                t = '\n' + vt.clean_up( t )
                console.log(t, True)
            else:
                console.log('Not ok. Something went wrong along the way.')
    else:
        console.log('No internet connection...', True)

    console.footer('END DOWNLOAD KNMI GLOBAL FORECAST...', True)
    cask.ask_back_to_main_menu()

def process_weather_buienradar_global():
    '''Function downloads and print a global weather forecast from the website from the knmi'''
    console.header('START DOWNLOAD BUIENRADAR GLOBAL FORECAST...', True)

    ok = False
    if utils.has_internet():
        t, url = '', config.buienradar_json_data
        ok, t = mcurweather.buienradar_weather()
        if ok:
            t = '\n' + vt.clean_up( t )
            console.log(t, True)
        else:
            console.log('Not ok. Something went wrong along the way.')
    else:
        console.log('No internet connection...', True)

    console.footer('END DOWNLOAD BUIENRADAR GLOBAL FORECAST...', True)
    cask.ask_back_to_main_menu()

def process_weather_knmi_model():
    '''Function downloads and prints a discussion about the weather models from the website from the knmi'''
    console.header('START DOWNLOAD KNMI DISCUSSION WEATHER MODELS...', True)

    ok, t = False, ''
    if utils.has_internet():
        sd   = utils.loc_date_now().strftime('%Y%m%d')
        url  = config.knmi_forecast_model_url
        name = f'guidance_model-{sd}.txt'
        file = utils.mk_path(config.dir_forecasts_txt, name)
        ok = fio.download( url, file )
        if ok:
            ok, t = fio.read(file)
            if ok:
                t = '\n' + vt.clean_up( t )
                console.log(t, True)
            else:
                console.log('Not ok. Something went wrong along the way.')
    else:
        console.log('No internet connection...', True)

    console.footer('END DOWNLOAD KNMI DISCUSSION WEATHER MODELS...', True)
    cask.ask_back_to_main_menu()

def process_weather_knmi_current():
    '''Function downloads and print a actual weather values to the screen'''
    console.header('START DOWNLOAD CURRENT VALUES KNMI WEATHERSTATIONS...', True)

    ok, t = False, ''
    if utils.has_internet():
        ok, t = mcurweather.knmi_stations()
        if ok:
            t = '\n' + vt.clean_up( t )
            console.log(t, True)
        else:
            console.log('Not ok. Something went wrong along the way.')
    else:
        console.log('No internet connection...', True)

    console.footer('END DOWNLOAD CURRENT VALUES KNMI WEATHERSTATIONS...', True)
    cask.ask_back_to_main_menu()

def process_weather_buienradar_current():
    '''Function downloads and print a actual weather values to the screen'''
    console.header('START DOWNLOAD CURRENT VALUES BUIENRADAR WEATHERSTATIONS...', True)

    ok, t = False, ''
    if utils.has_internet():
        ok, t = mcurweather.buienradar_stations()
        if ok:
            t = '\n' + vt.clean_up( t )
            console.log(t, True)
        else:
            console.log('Not ok. Something went wrong along the way.')
    else:
        console.log('No internet connection...', True)

    console.footer('END DOWNLOAD CURRENT VALUES BUIENRADAR WEATHERSTATIONS...', True)
    cask.ask_back_to_main_menu()

def process_weather_knmi_guidance():
    '''Function downloads and prints a global a more in depth forecast from the website from the knmi'''
    console.header('START DOWNLOAD KNMI GUIDANCE...', True)

    ok, t = False, ''
    if utils.has_internet():
        sd   = utils.loc_date_now().strftime('%Y%m%d')
        url  = config.knmi_forecast_guidance_url
        name = f'guidance_meerdaagse-{sd}.txt'
        file = utils.mk_path(config.dir_forecasts_txt, name)
        ok = fio.download(url, file)
        if ok:
            ok, t = fio.read(file)
            if ok:
                t = '\n' + vt.clean_up( t )
                console.log(t, True)
            else:
                console.log('Not ok. Something went wrong along the way.')
    else:
        console.log('No internet connection...', True)

    console.footer('END DOWNLOAD KNMI GUIDANCE...', True)
    cask.ask_back_to_main_menu()

# Menu choice 3
def get_dayvalues_by_date():
    '''Funtion gets day values from data knmi '''
    while True:
        console.header('START: SEARCHING AND PREPARING DAY VALUES...', True)
        # Ask for station

        places = cask.ask_for_stations('\nSelect one or more weather stations ?')# QUESTION: # QUESTION:
        if not places: break
        elif utils.is_quit(places): break

        period = cask.ask_for_period( '\nSelect one date or period(s) for the dayvalues ? ' )
        if utils.is_quit(period): break

        type = cask.ask_for_file_type( '\nSelect output filetype ? ', config.default_output )
        if utils.is_quit(type): break

        download = cask.ask_for_yn( '\nDo you want to download the data first ?', 'no' )
        if utils.is_quit(download): break
        download = True if utils.is_yes(download) else False

        check = cask.ask_type_options( '\nDo you want to add only new files or rewrite it all ? ',
                                       ['add', 'rewrite'], 'add' )
        if utils.is_quit(check): break
        console.log('CHECK-1: ' + str(check) )
        check = True if check == 'add' else False
        console.log('CHECK-2: ' + str(check) )

        st = time.time_ns()
        path = mdayval.calculate( places, period, type, check, download )
        console.log(vt.process_time('Total processing time is ', st), True)

        fopen = cask.ask_to_open_with_app (
                    f'\nOpen the (last made) file (type={type}) with your default application ?'
                    )
        if fopen:
            webbrowser.open_new_tab(path)

        # Always ask for going back
        t = f'\nDo you want to select another period(s) and or station(s) ?'
        again = cask.ask_again(t)
        if utils.is_quit(again):
            break

    console.footer('END SEARCHING AND PREPARING DAY VALUES...', True)

# Menu choice 4
def search_for_days():
    '''Funtion searches files for days with specific values. ie > 30 degrees'''
    while True:
        console.header('START SEARCHING FOR SPECIFIC DAYS...', True)

        period = cask.ask_for_period( '\nFor which time periode do you want to search ? ' )
        if utils.is_quit(period): break

        places = cask.ask_for_stations('\nSelect one or more weather stations ?')
        if not places:
            cask.ask_back_to_main_menu()
            break
        elif utils.is_quit(places):
            break

        query = cask.ask_for_query('\nType in a query for selecting days ? ')
        if utils.is_quit(query):
            break

        type = cask.ask_for_file_type(
                    '\nSelect output filetype ? ', config.default_output
                    )
        if utils.is_quit(type):
            break

        fname = f'days-{utils.make_query_txt_only(query)}-{period}-{utils.now_for_file()}'
        fname = fname.replace('*','x').replace(' ','')
        fname = cask.ask_for_file_name(
                        '\nGive a name for the file ? <optional>', fname
                    )
        if utils.is_quit(fname):
            break

        st = time.time_ns()
        path = search4days.calculate(places, period, query, type, fname)
        console.log(vt.process_time('Total processing time is ', st), True)

        if type in [ 'text', 'html' ]:
            fopen = cask.ask_to_open_with_app(
                            f'\nOpen the file (type={type}) with your default application ?'
                        )
            if fopen:
                webbrowser.open_new_tab( path )

        # Always ask for going back
        again = cask.ask_again(f'Do you want to search for days again ?', True)
        if utils.is_quit(again):
            break

    console.footer('END SEARCH FOR DAYS...', True)

def graph_period():
    '''Funtion makes images for a period from the data of the knmi'''
    while True:
        console.header('START MAKING A IMAGE GRAPH...', True)

        period = cask.ask_for_period('What time periode ?')
        if utils.is_quit(period):
            break

        places = cask.ask_for_stations('\nSelect weather station(s) ?')
        if not places:
            cask.ask_back_to_main_menu()
            break
        elif utils.is_quit(places):
            break

        entities = cask.ask_for_entities('\nSelect weather entity(s) ?')
        if utils.is_quit(entities):
            break

        console.log('Fill in the parameters for the image', False)
        title  = cask.ask_for_txt('\nGive a title for the graph')
        ylabel = cask.ask_for_txt('\nGive a y-as label for the graph')

        default = cask.ask_for_yn(
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
            'plot_climate_per' : config.climate_period,
            'plot_image_type'  : config.plot_image_type,
            'plot_dpi'         : config.plot_dpi,
            'plot_min_max_ave_period' : config.plot_min_max_ave_period
        }

        if utils.is_no(default):
            # Update option list
            plot_width = cask.ask_for_int(
                                '\nGive the width (in pixels) for the graph.',
                                config.plot_width )
            if utils.is_quit(plot_width): break
            else: options['plot_width'] = plot_width

            plot_height = cask.ask_for_int(
                                '\nGive the height (in pixels) for the graph.',
                                config.plot_height )
            if utils.is_quit(plot_height): break
            else: options['plot_height'] = plot_height

            plot_graph_type = cask.ask_type_options(
                                    '\nWhich type of graph do you want to use ? ',
                                    ['line', 'bar'],
                                    config.plot_graph_type )
            if utils.is_quit(plot_graph_type): break
            else: options['plot_graph_type'] = plot_graph_type

            if config.plot_graph_type == 'line':
                # TODO MAKE OPTIONS FOR EACH ENTITIY LATER l_opt = []
                # option = { 'line-width': 1,
                #     	   'markersize': 2,
                #            'colors': vcol.hexas().toList()
                #
                #            }

                plot_line_width = cask.ask_for_int (
                                            '\nSet the width of the line (in pixels) ? ',
                                            config.plot_line_width ) # Width line
                if utils.is_quit(plot_line_width): break
                else: options['plot_line_width'] = plot_line_width

                plot_marker_size = cask.ask_for_int (
                                            '\nSet the marker size (in pixels) ? ',
                                            config.plot_marker_size ) # Dot sizes on day
                if utils.is_quit(plot_marker_size): break
                else: options['plot_marker_size'] = plot_marker_size

            plot_cummul_val = cask.ask_for_yn(
                                    '\nDo you want cummulative values for the graph ? ',
                                    config.plot_cummul_val )
            if utils.is_quit(plot_cummul_val): break
            else: options['plot_cummul_val'] = plot_cummul_val # Take first yess or no

            plot_marker_txt = cask.ask_for_yn(
                                        '\nValues next to the markers ? ',
                                        config.plot_marker_txt )
            if utils.is_quit(plot_marker_txt): break
            else: options['plot_marker_txt'] = plot_marker_txt # Take first yess or no


            plot_min_max_ave_period = cask.ask_for_yn(
                                        '\nCalculate min, max and average value in period too ? ',
                                        config.plot_min_max_ave_period )
            if utils.is_quit(plot_min_max_ave_period): break
            else: options['plot_min_max_ave_period'] = plot_min_max_ave_period # Take first yess or no

            plot_climate_ave = cask.ask_for_yn(
                                        '\nCalculate and plot the climate averages too ? ',
                                        config.plot_climate_ave )
            if utils.is_quit(plot_climate_ave): break
            else: options['plot_climate_ave'] = plot_climate_ave # Take first yess or no

            if utils.is_yes(options['plot_climate_ave']):
                sy, ey = config.climate_period.split('-')
                plot_climate_y_s = cask.ask_for_int (
                                    '\nGive a start year for the calculation of climate averages <yyyy> ? ',
                                    sy )
                if utils.is_quit(plot_climate_y_s): break
                plot_climate_y_e = cask.ask_for_int (
                                    '\nGive an end year for the calculation of climate average <yyyy> ? ',
                                    ey )
                if utils.is_quit(plot_climate_y_e): break
                options['plot_climate_per'] = f'{plot_climate_y_s}-{plot_climate_y_e}'

            plot_image_type = cask.ask_type_options(
                                    '\nWhat type of image ? ',
                                    ['png', 'jpg', 'ps', 'pdf', 'svg'],
                                    config.plot_image_type )
            if utils.is_quit(plot_image_type): break
            else: options['plot_image_type'] = plot_image_type

            plot_dpi = cask.ask_for_int( '\nGive the dpi ? ', config.plot_dpi )
            if utils.is_quit(plot_dpi): break
            else: options['plot_dpi'] = plot_dpi

        fname = f"graph-{period.replace('*', 'x')}-{utils.now_for_file()}"
        fname = cask.ask_for_file_name('\nGive a name for the file ? ', fname)
        if utils.is_quit(fname):
            break

        console.header( 'PREPARING IMAGES...', True )
        st = time.time_ns()
        path = vg.plot( places, entities, period, title, ylabel, fname, options )
        console.log(vt.process_time('Total processing time is ', st), True)

        fopen = cask.ask_to_open_with_app(
                f'\nOpen the file (type={options["plot_image_type"]}) with your default application ?'
                )
        if fopen: webbrowser.open_new_tab(path)

        # Always ask for going back
        again = cask.ask_again(f'\nDo you want to make more images ?')
        if utils.is_quit(again):
            break

    console.footer('END MAKING A IMAGE GRAPH...', True)

# Menu choice 5
def table_winterstats():
    '''Function makes calculations for winterstatistics'''
    while True:
        console.header('START CALCULATE WINTER STATISTICS...', True)
        # Ask for all in one
        ok, period, places, type, name = cask.ask_period_stations_type_name(
                                            'winter'
                                            )
        if not ok: break

        console.header(f'CALCULATING WINTER STATISTICS...', True)

        st = time.time_ns()
        path = winstats.calculate( places, period, name, type )
        console.log(vt.process_time('Total processing time is ', st), True)

        if type != 'cmd':
            fopen = cask.ask_to_open_with_app(
                        f'\nOpen the file (type={type}) with your default application ?'
                    )
            if fopen:
                webbrowser.open_new_tab(path)

        # Always ask for going back
        again = cask.ask_again(
                    f'\nDo you want to make another winterstatistics table ?'
                )
        if utils.is_quit(again):
            break

    console.footer(f'END CALCULATE WINTER STATISTICS...', True)

# Menu choice 6
def table_summerstats():
    '''Function makes calculations for winterstatistics'''
    while True:
        console.header('START CALCULATE SUMMER STATISTICS...', True)
        ok, period, places, type, name = cask.ask_period_stations_type_name(
                                            'summer'
                                            )
        if not ok: break

        console.header('CALCULATING SUMMER STATISTICS...', True)

        st = time.time_ns()
        path = sumstats.calculate( places, period, name, type )
        console.log(vt.process_time('Total processing time is ', st), True)

        if type != 'cmd':
            fopen = cask.ask_to_open_with_app(
                        f'\nOpen the file (type={type}) with your default application ?'
                    )
            if fopen:
                webbrowser.open_new_tab(path)

        # Always ask for going back
        again = cask.ask_again(
                    f'\nDo you want to make another summerstatistics table ?'
                )
        if utils.is_quit(again):
            break

    console.footer(f'END CALCULATE SUMMER STATISTICS...', True)

# Menu choice 7
def table_allstats():
    '''Function makes calculations for all statistics'''
    while True:
        console.header('START CALCULATE ALL STATISTICS...', True)
        # Ask for all in one
        ok, period, places, type, name = cask.ask_period_stations_type_name(
                                            'all'
                                            )
        if not ok: break

        console.header(f'CALCULATING ALL STATISTICS...', True)

        st = time.time_ns()
        path = allstats.calculate( places, period, name, type )
        console.log(vt.process_time('Total processing time is ', st), True)

        if type != 'cmd':
            fopen = cask.ask_to_open_with_app(
                        f'\nOpen the file (type={type}) with your default application ?'
                    )
            if fopen: webbrowser.open_new_tab(path)

        # Always ask for going back
        again = cask.ask_again(
                    f'\nDo you want to make another all statistics table ?'
                )
        if utils.is_quit(again):
            break

    console.footer(f'END CALCULATE ALL STATISTICS...', True)

# # Menu choice 7
# def table_heatwaves():
#     while True:
#         console.header('START CALCULATE HEATWAVES...', True)
#         ok, period, places, type, name = cask.ask_period_stations_type_name(True)
#
#         if not ok:
#             break
#         else:
#             console.header('CALCULATING HEATWAVES...', True)
#
#             st = time.time_ns()
#             # path = hs.alg_heatwaves(l, sd, ed, type, name)
#             vt.show_process_time(st)
#
#             if type != 'cmd':
#                 fopen = cask.ask_to_open_with_app(
#                             f'\nOpen the file (type={type}) with your default application ?'
#                             )
#                 if fopen:
#                     webbrowser.open_new_tab(path)
#
#             # Always ask for going back
#             again = cask.ask_again(
#                         f'Do you want to make another heatwaves table ?',
#                         True
#                     )
#             if utils.is_quit(again):
#                 break
#
#     console.footer(f'END CALCULATE HEATWAVES...', True)
#
# # Menu choice 7
# def table_coldwaves():
#     while True:
#         console.header('START CALCULATE COLDWAVES...', True)
#         ok, period, places, type, name = cask.ask_period_stations_type_name(True)
#
#         if not ok:
#             break
#         else:
#             console.header('CALCULATING COLDWAVES...', True)
#
#             st = time.time_ns()
#             # path = hs.alg_heatwaves(l, sd, ed, type, name)
#             vt.show_process_time(st)
#
#             if type != 'cmd':
#                 fopen = cask.ask_to_open_with_app(
#                             f'\nOpen the file (type={type}) with your default application ?'
#                             )
#                 if fopen:
#                     webbrowser.open_new_tab(path)
#
#             # Always ask for going back
#             again = cask.ask_again(
#                         f'Do you want to make another coldwaves table ?'
#                         )
#             if utils.is_quit(again):
#                 break
#
#     console.footer(f'END CALCULATE COLDWAVES...', True)
