'''Library contains functions for asking questions and to deal with the input
given by a user'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "1.0"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import sys, re
import config
import knmi.model.daydata as daydata
import knmi.model.fn as fn
import view.log as log
import view.txt as view_txt
import view.translate as tr

# Check and sanitize input
def clear( s ):
    s = re.sub( '\n|\r|\t', '', s ).strip().replace('  ', ' ').lower()
    return s if s else False

def ask(txt='?'):
    txt = tr.txt( txt )
    res = clear(input(txt))
    return res

def pause(s='Paused'):
    ask(s)

def stop():
    ans = ask("Exit program? Press 'q' or 'Q' to exit...")
    if ans in config.answer_quit:
        log.footer('Application stopped...', True )
        sys.exit()

def ask_to_open_with_app(txt):
    log.console(txt, True)
    log.console("Press 'Y' or 'y' to open the file", True)
    log.console('Or press - any other key - to skip opening the file', True)

    return True if ask(" ? ") in config.answer_yes else False

def ask_for_stations( txt ):
    l = []
    while True:
        log.console(txt, True)
        log.console(view_txt.knmi_stations(config.stations, 3, 25), True)
        log.console('To add one station, give a wmo-number or a city name of a weatherstation', True)
        log.console('To more more stations, give a wmo-number or a city name separated by a comma', True)
        log.console("Press '*' to add all available weather stations", True)
        if len(l) > 0: log.console("Press 'n' to move to the next !", True)
        log.console("Press 'q' or 'Q' to go back to the main menu", True)

        log.console(' ')
        ans = ask(' ? ')
        log.console(' ')

        if not ans: # Waarschijnlijk op de enter geramd zonder invoer...
            continue # Nog een een keer dan maar

        if ans in config.answer_quit:
            return config.answer_quit
        elif ans == '*':
            l = config.stations
        elif ans == 'n' and len(l) > 0:
            return l
        else:
            lt = [] # Make a list with stations
            if ans.find(',') != -1:
                lt = ans.split(',')
            else:
                station = fn.find_knmi_station(ans)
                if station != False:
                    lt.append(ans)
                else:
                    log.console(f'Station: {ans} unknown !', True)

            lt = [clear(e) for e in lt] # Clean input

            # Add all added stations
            for st in lt:
                station = fn.find_knmi_station(st)
                if station != False:
                    wmo = f'{station.wmo} {station.place} {station.province} '
                    if not fn.is_station_in_list(station, l):
                        l.append(station)
                        log.console(f"Station: {wmo} added...", True)
                    else:
                        log.console(f"Station: {wmo} already added...", True)
                else:
                    log.console(f"Station: {answ} not found...", True)

        if len(l) == len(config.stations):
            log.console('All available weatherstations added...', True)
            break
        elif len(l) > 0:
            log.console('All weatherstation(s) who were added are:', True)
            for station in l:
                log.console(f'{station.wmo}: {station.place} {station.province}', True)
            log.console(' ')

    return l

def ask_for_date( txt ):
    while True:
        log.console(txt, True)
        log.console("Press 'q' or 'Q' to go back to the main menu", True)
        ans = ask(' ? ')
        if ans == config.answer_quit:
            return config.answer_quit
        elif v.check_date(ans):
            return ans
        else:
            log.console(f'Error in date: {s_in}', True)
            ask('Press a key to try again...')

def ask_for_start_and_end_date():
    start = ask_date('Give start date <format:yyyymmdd> ? ')
    if start in config.answer_quit:
        return config.answer_quit

    einde = ask_date('Give end date <format:yyyymmdd> ? ')
    if einde in config.answer_quit:
        return config.answer_quit

    if int(start) > int(einde):
        mem = start; start = einde; einde = mem

    return { 'start': start, 'einde': einde }

def ask_for_file_type(txt):
    types = ['txt', 'html', 'cmd']
    while True:
        log.console(txt, True)
        log.console(" - 'txt' for a text file", True)
        log.console(" - 'html' for a html file", True)
        log.console(" - 'cmd' for commandline only", True)
        log.console("Press 'q' or 'Q' to go back to the main menu")

        ans = ask(' ? ')
        if ans == config.answer_quit: return config.answer_quit
        elif ans in types: return ans
        else:
            log.console(f'Unknown option: {ans}', True)
            ask('Press a key to try again...')

def ask_for_file_naam(txt):
    log.console(txt, True)
    log.console('Press <enter> for no given name.\nDefault name will be used')

    return ask(' ? ', True)

def ask_enter_menu():
    log.console("Press a 'key' to go back to the main menu ...", True)
    input()
