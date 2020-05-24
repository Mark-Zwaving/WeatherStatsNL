'''Library contains functions for asking questions and to deal with the input
given by a user'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import sys, config as c, write as w, fn, validate as v, ask as a

def ask(s):
    s = fn.san(input(s))
    return s

def pause( s ):
    input(s)

def stop():
    y = ['Q', 'q']
    s = f"Exit program ? Press 'q' or 'Q' to exit..."
    if ask(s) in y:
        sys.exit('Programm stopped...')

def ask_open_url(txt):
    print(txt)
    print(f"Press 'Y' or 'y' to open the file ")
    print("Or press 'any other key' to skip opening the file")

    yn = ask(" ? ")
    return True if yn in ['Y','y'] else False

def ask_station(txt):
    while True:
        fn.println(txt)
        w.write_stations(c.lijst_stations, 3, 25)
        print('Give a wmo-number or a city name of a weatherstation ?')
        fn.println("Press 'q' to go back to the main menu")

        s_ask = ask(' ? ')
        if s_ask == c.stop:
            return c.stop
        else:
            station = fn.search_station(s_ask)
            if station != False:
                return station
            else:
                fn.println(f'Station: {s_ask} unknown !')
                ask("Press a key to try again...")

def ask_stations( txt ):
    l = []
    while True:
        fn.println(txt)
        w.write_stations(c.lijst_stations, 3, 25)
        text = '''
For one station: give a wmo-number or a city name of a weatherstation
For more stations: give a wmo-number or a city name separated by a comma
Press '*' to add all available weather stations
        '''
        if len(l) > 0: text += f"{c.ln}Press 'd' to move to the next !"

        text += f"{c.ln}Press 'q' to go back to main menu"
        fn.println(text)
        s_ask = ask(' ? ')

        if not s_ask: # Waarschijnlijk op de enter geramd zonder invoer...
            continue # Nog een een keer dan maar
        elif s_ask == c.stop:
            return c.stop
        elif s_ask == '*':
            l = c.lijst_stations
        elif s_ask == 'd' and len(l) > 0:
            return l
        else:
            lt = []
            info = ''
            if s_ask.find(',') != -1:
                lt = s_ask.split(',')
            else:
                station = fn.search_station(s_ask.strip())
                if station != False:
                    lt.append(s_ask.strip())
                else:
                    info += f'Station: {s_ask} unknown !'

            for s_in in lt:
                station = fn.search_station(s_in.strip())
                info = ''
                if station != False:
                    wmo = f'{station.wmo} {station.plaats} {station.provincie} '
                    if not fn.is_station_in_list(station, l):
                        l.append(station)
                        info += f"Station: '{wmo}' added..."
                    else:
                        info += f"Station: '{wmo}' already added..."
                else:
                    info += f"Station: '{s_in}' not found..."

            print(info)

        if len(l) == len(c.lijst_stations):
            print('All available weatherstations added...')
            break
        elif len(l) > 0:
            print(f'{c.ln}All weatherstation(s) who were added are:')
            for station in l:
                print(f'{station.wmo}: {station.plaats} {station.provincie}')
            print(' ')

    return l

def ask_date( txt ):
    while True:
        print(txt)
        print(f"Press 'q' to go back to the main menu")
        s_in = ask(' ? ')
        if s_in == c.stop:
            return c.stop
        elif v.check_date(s_in):
            return s_in
        else:
            print(f'Error in date: {s_in}')
            ask('Press a key to try again...')

def ask_start_and_end_date():
    start = ask_date("Give start date <format:yyyymmdd> ? ")
    if start == c.stop:
        return c.stop
    einde = ask_date("Give end date <format:yyyymmdd> ?")
    if einde == c.stop:
        return c.stop

    if int(start) > int(einde): # Keer om
        mem = start; start = einde; einde = mem

    return { 'start': start, 'einde': einde }

def ask_file_type(txt):
    types = ['txt', 'html', 'cmd']
    while True:
        fn.println(f'''
{txt}
Type:
 - 'txt' for a text file
 - 'html' for a html file
 - 'cmd' for commandline only
Press 'q' to go back to the main menu''')

        s_in = ask(' ? ')
        if s_in == c.stop:
            return c.stop
        elif s_in in types:
            return s_in
        else:
            print(f'Unknown option: {s_in}')
            ask('Press a key to try again...')

def ask_file_naam(txt):
    s_in = False
    fn.println(f'''
{txt}
Press '<enter>' for no name. Default name will be used
Press 'q' to go back to main menu''')
    s_in = ask(' ? ')
    return s_in

def ask_enter_menu():
    input(f"{c.ln}Press a 'key' to go back to the main menu ...{c.ln}")