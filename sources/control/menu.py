'''Library contains functions for asking questions and to deal with the input
given by a user'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1.6"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, time, config, webbrowser, subprocess
import numpy as np
import model.utils as utils
import model.convert as convert
import model.search4days as search4days
import model.daydata as daydata
import model.winterstats as winterstats
import model.summerstats as summerstats
import model.allstats as allstats
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
            name = control_ask.ask_for_file_name (
                        f'Give a name for the {type} file ?', default, True
                    )
            if utils.quit_menu(name):
                break
            name += f'.{type}'

        st = time.time_ns()
        log.header('SEARCHING FOR AND PREPARING DAY VALUES', True)
        log.console(f'Station: {stat.wmo} {stat.place}', True)
        log.console(f'Date: {utils.ymd_to_txt(ymd)}', True)

        day = data[np.where(data[:,daydata.YYYYMMDD] == int(ymd))][0]
        txt_date = utils.ymd_to_txt(ymd)
        footer = stat.dayvalues_notification

        # Make output
        if type == 'html':
            header  = f'<i class="text-info fas fa-home"></i> '
            header += f'{stat.wmo} - {stat.place} '
            header += f'{stat.province} - {txt_date} '

            page = view_html.Template()
            page.title  = f'{stat.place}-{ymd}'
            page.header = header
            page.main   = view_html.main_ent( day )
            page.footer = footer
            page.set_path( config.dir_html_dayvalues, name )

            if page.save():
                view_txt.show_process_time(st)
                fopen = control_ask.ask_to_open_with_app(
                            f'Open the file {name} in your browser ?', True
                        )
                if fopen:
                    webbrowser.open_new_tab( page.file_path ) # Opens in default browser

        elif type == 'txt':
            title = txt_date
            main  = view_dayvalues.txt_main( day )
            txt   = f'{title}\n{main}'
            path  = utils.mk_path( config.dir_txt_dayvalues, name )

            if io.save(path, txt):
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

        log.console( 'For which time periode do you want to search ? \n' )
        period = control_ask.ask_for_period( )
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

        fname = control_ask.ask_for_file_name(
                        'Give a name for the file ? <optional>',
                         f'days-{utils.make_query_txt_only(query)}-{period}-{utils.now_act_for_file()}',
                        True
                    )
        if utils.quit_menu(fname):
            break

        st = time.time_ns()
        # Search for the days the
        data = search4days.process( stations, period, query )

        if type =='html':
            fname = f'{fname}.html'
            path = utils.mk_path(config.dir_html_search_for_days, fname)

            # Proces data in html table
            html_main = view_html.table_search_for_days(data, period)

            # Write to html, screen, console
            html = view_html.Template()
            html.title  = f'Days {query}'
            html.header = f'Days: {query}'
            html.add_css_file( dir='./css/', name='table-statistics.css' )
            html.main   = html_main
            html.footer = ''
            html.set_path( config.dir_html_search_for_days, fname )
            html.save()

        elif type == 'text':
            # TODO:
            pass
        elif type == 'cmd':
            # TODO
            pass

        view_txt.show_process_time(st)

        if type in [ 'text', 'html' ]:
            fopen = control_ask.ask_to_open_with_app(
                            f'\nOpen the file ? \n{path}\n', True
                        )
            if fopen:
                webbrowser.open_new_tab( path )

        # Always ask for going back
        again = control_ask.ask_again(f'Do you want to search for days ?', True)
        if utils.quit_menu(again):
            break

    log.footer('END MAKING A IMAGE GRAPH...', True)

def graph_period():
    '''Funtion makes images for a period from the data of the knmi'''
    while True:
        log.header('START MAKING A IMAGE GRAPH...', True)

        log.console( 'What time periode ?\n' )
        period = control_ask.ask_for_period( )
        if utils.quit_menu(period):
            break

        stations = control_ask.ask_for_stations('Select a weather station ?', True)
        if utils.quit_menu(stations):
            break

        entities = control_ask.ask_for_entities('Select a weather entities ?', True)
        if utils.quit_menu(entities):
            break

        log.console('Fill in the parameters for the image', False)
        title  = control_ask.ask_txt('Give a title for the graph ? ', False)
        ylabel = control_ask.ask_txt('Give a y-as label for the graph ? ', False)

        more = control_ask.ask_for_yn(
                    'Do you want to use default values ?\nSee file -> config.py...',
                    False
                    )
        if utils.quit_menu(more):
            break

        if np.array_equal( more, config.answer_no ):
            config.plot_width = control_ask.ask_for_int(
                                    'Give the width (in pixels) for the graph.',
                                    1280,
                                    space=False
                                    )
            config.plot_height = control_ask.ask_for_int(
                                    'Give the height (in pixels) for the graph.',
                                    720,
                                    space=False
                                    )
            config.plot_graph_type = control_ask.ask_type_options(
                                        'Which type of graph do you want to use ? ',
                                        'graph', ['line', 'bar'],
                                        space=False
                                    )
            config.plot_cummul_val = control_ask.ask_for_yn(
                                        'Do you want cummulative values for the graph ? ',
                                        space=False
                                    )[0] # Take first yess or no
            config.plot_marker_txt = control_ask.ask_for_yn(
                                        'Values next to the markers ? ',
                                        space=False
                                    )[0] # Take first yess or no
            config.plot_image_type = control_ask.ask_type_options(
                                        'What type of image ? ', 'image',
                                        ['png', 'jpg', 'ps', 'pdf', 'svg'],
                                        space=False
                                    )
            config.plot_dpi = control_ask.ask_for_int(
                                'Give the dpi (default is 100) ? ', 100, space=False
                                )

            if config.plot_graph_type == 'line':
                # l_opt = []
                # option = { 'line-width': 1,
                #     	   'markersize': 2,
                #            'colors': vcolors.hexas().toList()
                #
                #            }

                config.plot_line_width = control_ask.ask_for_int(
                                            'Set the width of the line (in pixels) ? ',
                                            1, space=False
                                        ) # Width line
                config.plot_marker_size = control_ask.ask_for_int(
                                            'Set the marker size (in pixels) ? ',
                                            3, space=False
                                        ) # Dot sizes on day

        name = control_ask.ask_for_file_name( 'Give a name for the file ? <optional>',
                                              f'graph-{period.replace("*", "x")}-{utils.now_act_for_file()}',
                                              True
                                              )
        if utils.quit_menu(name):
            break

        st = time.time_ns()
        log.header( 'PREPARING IMAGES...', True )
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
