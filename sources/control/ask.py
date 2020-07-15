'''Library contains functions for asking questions and to deal with the input
given by a user'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1.7"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import sys, re, config
import numpy as np
import model.utils as utils
import model.daydata as daydata
import model.station as station
import model.validate as validate
import view.log as log
import view.txt as view_txt
import view.translate as tr

# Check and sanitize input
def clear( s ):
    s = re.sub( '\n|\r|\t', '', s ).strip().replace('  ', ' ').lower()
    return s if s else False

def enter_default(default):
    return f'Press <enter> for default (={default})\n'

def back_to_main():
    return "Press 'q' to go back to the main menu\n"

def ask_back_to_main_menu(space=True):
    if space: log.console(' ')
    input("Press a 'key' to go back to the main menu")
    if space: log.console(' ')

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

def ask_for_int(txt, default, space=True):
    if space: log.console(' ')
    while True:
        txt = f'{txt}\n{enter_default(default)}'
        answ = re.sub( '\D', '', input(txt).strip() ) # Remove non-digits
        if utils.is_empthy( answ ):
            return default
        else:
            try:
                answ_i = int(answ)
            except ValueError:
                print('Give a real integer  ... ')
                continue
            else:
                break
    if space: log.console(' ')

    return answ_i

def pause(s='Paused'):
    ask(s, True)

def stop():
    answ = ask("Exit program? \nPress 'q' to exit...", True)

    if answ:
        if ans in config.answer_quit:
            log.footer('Application stopped...', True )
            sys.exit()

def ask_again(txt, default, space=True):
    txt  = f'{txt} Press a key...\n'
    txt += back_to_main()
    txt += ' ? '

    answ = ask(txt, space)

    if utils.is_empthy( answ ):
        return default
    elif answ in config.answer_quit:
        return config.answer_quit
    else:
        return answ

def ask_to_open_with_app( txt, space=True ):
    txt  = f'{txt}\n'
    txt += "Press 'y' to open the file, or press any other key to skip opening the file\n"
    txt += ' ? '

    answ = ask(txt, space)

    return True if answ in config.answer_yes else False

def ask_for_entities( txt, space=True):
    l = []
    txt  = f'{txt}\n'
    txt += view_txt.dayvalues_entities(sep=',')
    txt += 'To add one weather entity, type in the enitity name. e.g. TX\n'
    txt += 'To one more stations, give entity name separated by a comma. e.g TX, TG, TN\n'
    txt += 'See - ./data/text/dayvalues/dayvalues.txt - for the meaning of the entities\n'
    txt += back_to_main()

    while True:
        ask_txt = txt
        if len(l) > 0:
            ask_txt += "Press 'n' to move to the next !\n"
        ask_txt += '\n ? '

        answ = ask(ask_txt, space)

        if utils.is_empthy(answ):
            log.console('Please type in something ...', True)
            continue # Again
        elif answ in config.answer_quit:
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
            cnt, kol, txt = 1, 10, 'All weather entities who are added are:\n'
            for ent in l:
                txt += ent + ', '
                if cnt % kol == 0:
                    txt += '\n'
            log.console( txt, True )

    return l

def ask_for_one_station( txt, space=True):
    txt  = f'{txt}\n'
    txt += view_txt.knmi_stations(config.stations, 3, 25)
    txt += 'To add a station, give a wmo-number or a city name of a weatherstation\n'
    txt += back_to_main()
    txt += ' ? '

    while True:
        answ = ask(txt, space)

        if utils.is_empthy(answ):
            log.console('Please type in something ...', True)
            continue
        elif answ in config.answer_quit:
            return config.answer_quit
        elif station.name_in_list(answ) or station.wmo_in_list(answ):
           st = station.find_by_wmo_or_name(answ)
           log.console(f'{st.wmo}: {st.place} {st.province} selected', True)
           return st
            ask( f'Station: {answ} unknown !\nPress a key to try again...', True )
        else:

def ask_for_stations( txt, space=True):
    l = []
    txt  = f'{txt}\n'
    txt += view_txt.knmi_stations( config.stations, 3, 25 )
    txt += 'To add one station, give a wmo-number or a city name of a weatherstation\n'
    txt += 'To add more stations, give a wmo-number or a city name separated by a comma\n'
    txt += "Press '*' to add all available weather stations\n"
    txt += back_to_main()

    while True:
        ask_txt = txt
        if len(l) > 0:
            ask_txt = "Press 'n' to move to the next ! \n ? "

        answ = ask(ask_txt, space)

        if utils.is_empthy(answ):
            log.console('Please type in something ...', True)
            continue
        elif answ in config.answer_quit:
            return config.answer_quit
        elif answ == '*':
            l = config.stations
        elif answ == 'n' and len(l) > 0:
            return np.array(l)
        else:
            lt = [] # Make a list with stations
            if answ.find(',') != -1:
                lt = [clear(e) for e in answ.split(',')] # Clean input
            else:
                if station.name_in_list(answ):
                    lt.append(answ)
                elif station.wmo_in_list(answ):
                    lt.append(answ)
                else:
                    log.console(f'Station: {answ} is unknown !', True)

            # Add all added stations
            for s in lt:
                st = station.find_by_wmo_or_name(s)
                if st != False:
                    all = f'{st.wmo} {st.place} {st.province}'
                    if station.check_if_station_already_in_list( st, l ) != True:
                        l.append(st)
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
            for st in l:
                log.console(f'{st.wmo}: {st.place} {st.province}', True)
        else:
            continue
        print(' ')

    return np.array(l)

def ask_for_date( txt, space=True):
    while True:
        answ = ask(f'{txt}\n{back_to_main()} ? ', space)

        if utils.is_empthy(answ):
            log.console('Please type in something ...', True)
            continue
        elif answ in config.answer_quit:
            return config.answer_quit
        elif validate.yyyymmdd(answ):
            return answ
        else:
            log.console(f'Error in date: {answ}\n', True)

def ask_for_period( space=True ):
    txt  = 'Give period: \n'
    txt += 'Period           start  -  end    \n'
    txt += 'Default format  yyyymmdd-yyyymmdd \n'
    txt += 'For example: 20200510-20200520'
    txt += 'Other formats with wild card * \n'
    txt += '  yyyy****           selects the whole year \n'
    txt += '  ****mm**           selects a month fo every year \n'
    txt += '  ****mmdd           selects a day for every year \n'
    txt += 'Examples wildcard * \n'
    txt += '  2015****           selects the year 2015 \n'
    txt += '  201101**-202001**  selects all januarys from 2011 unto 2020 \n'
    txt += '  ****07**           selects all julys from avalaible data \n'
    txt += '  ****1225           selects all 25 decembers from avalaible data \n'
    txt += back_to_main()
    txt += 'Type in period\n ? '

    while True:
        answ = ask( txt, space )

        if utils.is_empthy(answ):
            log.console('Please type in something ...', True)
            continue
        elif utils.quit_menu(answ):
            return config.answer_quit
        else:
            return answ.replace(' ', '')

def ask_for_date_with_check_data( stat, txt, space=True ):
    log.console(f'Loading data {stat.place} ...')
    ok, data = daydata.read( stat )
    if not ok:
        input(f'Error reading data! {stat.place}')
        return config.answer_quit, np.array([])

    sd = int( data[ 0, daydata.YYYYMMDD])
    ed = int( data[-1, daydata.YYYYMMDD])

    txt = f'{txt}\n'
    txt += f'Available range data for - {stat.place} - is from {sd} untill {ed}'
    while True:
        answ = ask_for_date(txt, space)

        if utils.quit_menu(answ):
            return config.answer_quit, np.array([])
        else:
            try:
                ymd = int(answ)
            except Exception as e:
                pass
            else:
                if ymd < sd or ymd > ed:
                    log.console(f'Date {ymd} is out of range for {stat.place}')
                else:
                    return answ, data

def ask_for_yn( txt, space=True ):
    l = ['yes', 'no']
    txt  = f'{txt}\n'
    txt += '\t1) Yes\n\t2) No\n'
    txt += back_to_main()
    txt += ' ? '
    while True:
        answ = ask( txt, space )

        if utils.is_empthy(answ):
            log.console("Please type in 'Yes' or 'No' ...", True)
            continue
        elif answ in config.answer_quit: return config.answer_quit
        elif answ in config.answer_yes:  return config.answer_yes
        elif answ in config.answer_no:   return config.answer_no
        else:
            try:
                answi = int(answ)
            except ValueError: # Input was not a number
                pass
            else: # Input is a number
                if answi in [1,2]:
                    if answi == 1:
                        return config.answer_yes
                    elif answi == 2:
                        return config.answer_no

        log.console(f'Unknown option: {answ} ?\nTry again.', True)

def ask_type_options(txt, type, l, default=1, space=True):
    txt = f'{txt}\n'
    for n, el in enumerate(l):
        txt += f'\t{n+1}) {el} {type}\n'
    txt += enter_default(default)
    txt += back_to_main()
    txt += ' ? '
    while True:
        answ = ask(txt, space)

        if utils.is_empthy(answ):
            answ = str(default)

        if answ in config.answer_quit:
            return config.answer_quit
        else:
            try:
                answi = int(answ)
            except ValueError: # Input is not a number
                if answ in l:
                    return answ
            else: # Input is a number
                answi -= 1
                if answi in range(len(l)):
                    return l[answi]
                else:
                    log.console(f'Unknown option: {answ} ?\nTry again.', True)

def ask_for_file_type(txt, default=2, space=True):
    l = ['txt TODO', 'html', 'cmd TODO']
    return ask_type_options(txt, '', l, default, space)

def ask_for_graph_type(txt, space=True):
    l = ['line', 'bar']
    return ask_type_options(txt, 'graph', l, default, space)

def ask_for_file_name(txt, default='x', space=True):
    txt  = f'{txt}\n'
    txt += enter_default(default)
    txt += back_to_main()
    txt += ' ? '

    answ = ask( txt, space)

    if utils.is_empthy(answ):
        return default
    elif answ in config.answer_quit:
        return config.answer_quit

    return answ

def ask_for_color(txt, default='', space=True):
    pass

def ask_period_stations_type_name( name, space=True ):
    # Ask start and end date
    ok, period, stations, type, name = False, '', [], '', ''
    period = ask_for_period( space )
    if not utils.quit_menu(period):
        # Ask for one or more stations
        stations = ask_for_stations(
                        'Select one (or more) weather station(s) ?',
                        space
                    )
        if not utils.quit_menu(stations) :
            # Ask for a file type
            type = ask_for_file_type(
                        'Select filetype ? ',
                        space
                        )
            if not utils.quit_menu(type):
                ok = True
                if type != 'cmd': # Ask for a name

                    name = ask_for_file_name(
                            'Set a name for the output file ? <optional> ',
                            f'{name}-{period.replace("*","x")}-{utils.now_act_for_file()}',
                            space
                    )
                    if utils.quit_menu(name):
                        ok = False # Oke quit

    return ok, period, stations, type, name

def ask_for_query( txt, space=True ):
    info = False
    i  = 'Possible properties are\n'
    i += "' gt', '> '         'greater than'             'ie TG >  20  Warm nights'\n"
    i += "' ge', '>=', ' ≥'   'greater than and equal'   'ie TX >= 30  Tropical days'\n"
    i += "' lt', '< '         'less than'                'ie TN <   0  Frosty days'\n"
    i += "' le', '<=', ' ≤'   'less than equal'          'ie TX <=  0  Icy days'\n"
    i += "' eq', '=='         'equal'                    'ie DDVEC == 90  A day with a wind from the east'\n"
    i += "' ne', '!=', '<>'   'not equal'                'ie RH !=  0  A day with rain'\n"
    i += "' or', '||'  'or '  'ie SQ > 15  or TX >= 25    Sunny and warm days'\n"
    i += "'and', '&&'  'and'  'ie RH > 10 and TX <  0     Propably a day with snow'\n"
    i += '\nPossible entities are\n'
    i += "'DDVEC' = 'Vector mean wind direction (degrees)'    'FHVEC' = 'Vector mean windspeed (m/s)'\n"
    i += "'FG'    = 'Daily mean windspeed (in 0.1 m/s)'       'FHX'   = 'Maximum hourly mean windspeed (m/s)'\n"
    i += "'FHN'   = 'Minimum hourly mean windspeed (m/s)'     'FXX'   = 'Maximum wind gust (m/s)'\n"
    i += "'TG'    = 'Daily mean temperature in (°C)'          'TN'    = 'Minimum temperature (°C)'\n"
    i += "'TX'    = 'Maximum temperature (°C)                 'T10N'  = 'Minimum temperature at 10 cm (°C)'\n"
    i += "'SQ'    = 'Sunshine duration (hour)                 'SP'    = '% of maximum sunshine duration'\n"
    i += "'Q'     = 'Global radiation (J/cm2)                 'DR'    = 'Precipitation duration (hour)'\n"
    i += "'RH'    = 'Daily precipitation amount (mm)          'RHX'   = 'Maximum hourly precipitation (mm)'\n"
    i += "'PG'    = 'Daily mean sea level pressure (hPa)      'PX'    = 'Maximum hourly sea level pressure (hPa)'\n"
    i += "'PN'    = 'Minimum hourly sea level pressure (hPa)' 'EV24'  = 'Potential evapotranspiration (mm)'\n"
    i += "'VVN'   = 'Minimum visibility 0: <100m, 1:100-200m, 2:200-300m,..., 49:4900-5000m, 50:5-6 km, \'\n"
    i += ' 56:6-7km, 57:7-8km,..., 79:29-30km, 80:30-35km, 81:35-40km,..., 89: >70km)\n'
    i += "'VVX'   = 'Maximum visibility 0: <100 m, 1:100-200 m, 2:200-300 m,..., 49:4900-5000 m, 50:5-6 km, '\n"
    i += ' 56:6-7km, 57:7-8km,..., 79:29-30km, 80:30-35km, 81:35-40km,..., 89: >70km)\n'
    i += "'NG'    = 'Mean daily cloud cover (octants)         'UG'    = 'Daily mean relative atmospheric humidity (%)'\n"
    i += "'UX'    = 'Maximum atmospheric humidity (%)         'UN'    = 'Minimum relative atmospheric humidity (%)'\n"

    txt = f'{txt}\n'
    txt += 'For example: TX > 35\n'
    if not info:
        txt += f"Type 'i' for more info.\n"
    txt += back_to_main()
    txt += '\n ? '

    while True:
        if info:
            print(i)

        answ = ask(txt, True) # TODO MAKE ADVANCED CHECKS

        info = True if answ == 'i' else False
        if utils.is_empthy(answ):
            log.console('Please type in something ...', True)
            continue
        elif info:
            continue
        elif answ in config.answer_quit:
            return config.answer_quit
        # TODO
        # elif validate.query(answ): # TODO
        #     return answ
        else:
            return utils.make_query_txt_only( answ )

    return answ  # No checking for now
