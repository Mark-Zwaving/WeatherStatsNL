'''Library contains functions for asking questions and to deal with the input
given by a user'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1.3"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import sys, re, config
import knmi.model.daydata as daydata
import knmi.model.station as knmi_station
import view.log as log
import view.txt as view_txt
import view.translate as tr
import model.validate as validate

# Check and sanitize input
def clear( s ):
    s = re.sub( '\n|\r|\t', '', s ).strip().replace('  ', ' ').lower()
    return s if s else False

def ask(txt='?', space=True):
    if space: log.console(' ')
    res = clear( input( tr.txt( txt ) ) )
    if space: log.console(' ')

    return res

def ask_txt(txt='?', space=True):
    if space: log.console(' ')
    answ = input( tr.txt( txt ) ).strip()
    if space: log.console(' ')

    return answ

def pause(s='Paused'):
    ask(s, True)

def stop():
    answ = ask("Exit program? Press 'q' or 'Q' to exit...", True)

    if answ:
        if ans in config.answer_quit:
            log.footer('Application stopped...', True )
            sys.exit()

def ask_again(txt, space=True):
    log.console(txt, True)
    log.console("Press a key ... Or press 'q' or 'Q' to quit", True)

    answ = ask(' ? ', space)

    if answ in config.answer_quit:
        return config.answer_quit

    return answ

def ask_to_open_with_app(txt, space=True):
    log.console(txt, True)
    log.console("Press 'Y' or 'y' to open the file", True)
    log.console('Or press - any other key - to skip opening the file', True)

    answ = ask(' ? ', space)

    if answ:
        if answ in config.answer_yes:
            return True
    return False

def ask_for_entities( txt, space=True):
    l = []
    while True:
        log.console(txt, True)
        log.console(view_txt.dayvalues_entities(sep=','), True)
        log.console('To add one weather entity, type in the enitity name. e.g. TX', True)
        log.console('To one more stations, give entity name separated by a comma. e.g TX, TG, TN', True)
        log.console('See - ./data/text/dayvalues/dayvalues.txt - for the meaning of the entities', True)
        if len(l) > 0: log.console("Press 'n' to move to the next !", True)
        log.console("Press 'q' or 'Q' to go back to the main menu", True)

        answ = ask(' ? ', space)

        if not answ: # Oke whatever
            log.console('Please type in something ...', True)
            continue # Again

        if answ in config.answer_quit:
            return config.answer_quit
        elif answ == 'n' and len(l) > 0:
            return l
        elif answ.find(',') != -1:
            lt = [clear(e) for e in answ.split(',')] # Clean input
            for e in lt:
                ok, ent = daydata.is_ent( e )
                if ok:
                    l.append(e)
        else:
            ok, ent = daydata.is_ent( answ )
            if ok:
                l.append(ent)

        if len(l) > 0:
            log.console('All weather entities who are added are:', True)
            cnt, kol, txt = 1, 10, ''
            for ent in l:
                txt += ent + ', '
                if cnt % kol == 0:
                    txt += '\n'

            log.console(f'{txt}', True)
            log.console(' ')
    return l

def ask_for_one_station( txt, space=True):
    while True:
        log.console(txt, True)
        log.console(view_txt.knmi_stations(config.stations, 3, 25), True)
        log.console('To add a station, give a wmo-number or a city name of a weatherstation', True)
        log.console("Press 'q' or 'Q' to go back to the main menu", True)

        answ = ask(' ? ', space)

        if answ in config.answer_quit:
            return config.answer_quit
        elif knmi_station.name_in_list(answ) or knmi_station.wmo_in_list(answ):
           station = knmi_station.find_by_wmo_or_name(answ)
           log.console(f'{station.wmo}: {station.place} {station.province} selected', True)
           return station
        else:
            log.console(f'Station: {answ} unknown !', True)
            ask('Press a key to try again...')

def ask_for_stations( txt, space=True):
    l = []
    while True:
        log.console(txt, True)
        log.console(view_txt.knmi_stations(config.stations, 3, 25), True)
        log.console('To add one station, give a wmo-number or a city name of a weatherstation', True)
        log.console('To add more stations, give a wmo-number or a city name separated by a comma', True)
        log.console("Press '*' to add all available weather stations", True)
        if len(l) > 0: log.console("Press 'n' to move to the next !", True)
        log.console("Press 'q' or 'Q' to go back to the main menu", True)

        answ = ask(' ? ', space)

        if not answ: # Waarschijnlijk op de enter geramd zonder invoer...
            log.console('Please type in something ...', True)
            continue # Nog een keer dan maar

        if answ in config.answer_quit:
            return config.answer_quit
        elif answ == '*':
            l = config.stations
        elif answ == 'n' and len(l) > 0:
            return l
        else:
            lt = [] # Make a list with stations
            if answ.find(',') != -1:
                lt = [clear(e) for e in answ.split(',')] # Clean input
            else:
                if knmi_station.name_in_list(answ):
                    lt.append(answ)
                elif knmi_station.wmo_in_list(answ):
                    lt.append(answ)
                else:
                    log.console(f'Station: {answ} unknown !', True)

            # Add all added stations
            for st in lt:
                station = knmi_station.find_by_wmo_or_name(st)
                if station != False:
                    all = f'{station.wmo} {station.place} {station.province}'
                    if knmi_station.check_if_station_already_in_list( station, l ) != True:
                        l.append(station)
                        log.console(f"Station: {all} added...", True)
                    else:
                        log.console(f"Station: {all} already added...", True)
                else:
                    log.console(f"Station: {answ} not found...", True)

        print(' ')
        if len(l) == len(config.stations):
            log.console('All available weatherstations added...', True)
            break
        elif len(l) > 0:
            log.console('All weatherstation(s) who were added are:', True)
            for station in l:
                log.console(f'{station.wmo}: {station.place} {station.province}', True)
        else:
            continue
        print(' ')

    return l

def ask_for_date( txt, space=True):
    while True:
        log.console(txt, True)
        log.console("Press 'q' or 'Q' to go back to the main menu", True)
        answ = ask(' ? ', space)
        if answ in config.answer_quit:
            return config.answer_quit
        elif validate.yyyymmdd(answ):
            return answ
        else:
            log.console(f'Error in date: {answ}', True)
            ask('Press a key to try again...')

def ask_for_start_and_end_date(space=True):
    sd = ask_for_date('Give a START date <format:yyyymmdd> ? ', space)
    if sd == config.answer_quit:
        return config.answer_quit, sd

    ed = ask_for_date('Give a END date <format:yyyymmdd> ? ', space)
    if ed == config.answer_quit:
        return ed, config.answer_quit

    if int(sd) > int(ed):
        mem = sd; sd = ed; ed = mem

    return sd, ed

def ask_for_date_with_check_data( station, data, txt, space=True ):
    sd, ed = data[ 0, daydata.YYYYMMDD], data[-1, daydata.YYYYMMDD]
    txt += f'Available range data for {station.place} is from {sd} untill {ed}'
    while True:
        answ = ask_for_date(txt, space)
        if answ == config.answer_quit:
            return config.answer_quit
        else:
            ymd = int(answ)
            if ymd < sd or ymd > ed:
                log.console(f'Date {ymd} is out of range for {station.place}')
            else:
                return answ

def ask_type_options(txt, type, l, space=True):
    while True:
        log.console(txt, True)
        for n, el in enumerate(l):
            log.console(f'\t{n+1}) {el}: {type}', True)
        log.console("Press 'q' or 'Q' to go back to the main menu")

        answ = ask(' ? ', space)

        if answ:
            if answ in [str(el) for el in range(len(l))]:
                return l[int(answ)-1]
            elif answ in l:
                return answ
            elif answ in config.answer_quit:
                return config.answer_quit

        log.console(f'Unknown option: {answ} ? ', True)

        ask('Press a key to try again ... ', space)

def ask_for_file_type(txt, space=True):
    l = ['txt', 'html', 'cmd']
    return ask_type_options(txt, 'file', l, space)

def ask_for_graph_type(txt, space=True):
    l = ['line', 'bar']
    return ask_type_options(txt, 'graph', l, space)

def ask_for_file_name(txt, space=True):
    log.console(txt, True)
    log.console('Press <enter> for no given name. Default name will be used', True)

    return ask(' ? ', space)

def ask_back_to_main_menu(space=True):
    log.console("Press a 'key' to go back to the main menu...", space)
    input()

def ask_period_stations_type_name(space=True):
    # Ask start and end date
    ok, sd, ed, stations, type, name = False, '', '', [], '', ''
    sd, ed = control_ask.ask_for_start_and_end_date()
    if sd != config.answer_quit and ed != config.answer_quit:
        # Ask for one or more stations
        stations = ask_for_stations('Select one (or more) weather station(s) ?', space)
        if stations != config.answer_quit:
            # Ask for a file type
            type = control_ask.ask_for_file_type('Select filetype ? ', space)
            if type != config.answer_quit:
                # Ask for a name
                ok = True
                if type != 'cmd':
                    name = control_ask.ask_for_file_name('Set a name for the output file ? <optional> ', space)
                    if name != config.answer_quit:
                        ok = False # Oke quit

    return ok, sd, ed, station, type, name
