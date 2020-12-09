'''Library contains functions for asking questions and to deal with the input
given by a user'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.2.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import sys, re, config, stations
import numpy as np
import sources.model.utils as utils
import sources.model.daydata as daydata
import sources.model.validate as validate
import sources.view.log as log
import sources.view.txt as vt
import sources.view.translate as tr

# Check and sanitize input
def clear( s ):
    s = re.sub( '\n|\r|\t', '', s ).replace('  ', ' ').strip()
    return s if s else False

def ask_back_to_main_menu(space=False):
    if space: log.console(' ')
    input("Press a 'key' to go back to the main menu... ")
    if space: log.console(' ')

def ask(txt='?', space=False):
    t = clear(txt)
    if t:
        t = tr.txt( txt )
    else:
        t = ' ... ? '

    if space: log.console(' ')
    res = input(t)
    if space: log.console(' ')

    return res

def ask_for_txt(txt='?', default=False, space=False):
    t = f'{txt}\n'
    if default != False:
        t += vt.enter_default(default) + '\n'
    t += vt.enter_back_to_main() + '\n'
    t += ' ? '

    if space: log.console(' ')
    answ = ask(t, space)
    if space: log.console(' ')

    return answ

def ask_for_int(txt, default=False, space=False):
    if space: log.console(' ')
    while True:
        answ = ask_for_txt(txt, default=default, space=space)

        if utils.is_empthy( answ ):
            return default
        elif utils.is_quit(answ):
            return config.answer_quit[0] # Return first el for quit
        else:
            answ = re.sub( '\D', '', answ ) # Remove non-digits
            try:
                answ_i = int(answ)
            except ValueError:
                log.console('Give an real integer  ... ', True)
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
        if utils.is_quit(answ):
            log.footer('Application stopped...', True )
            sys.exit()

def ask_again(txt, space=False):
    t  = f'{txt} Press a key...'
    answ = ask_for_txt( t, default=False, space=space )

    if utils.is_quit(answ):
        return config.answer_quit[0] # Return first el for quit

    return answ

def ask_to_open_with_app( txt, space=False ):
    t  = f'{txt}\n'
    t += "Press 'y' to open the file, or press any other key to skip opening the file... "
    answ = answ = ask_for_txt( t, default=False, space=space )

    if utils.is_yes(answ):
        return True
    else:
        return False

def ask_for_entities( txt, space=False):
    l = []
    txt  = f'{txt}\n'
    txt += vt.dayvalues_entities(sep=',')
    txt += "See file: './data/text/dayvalues/dayvalues.txt' for the meaning of the entities\n"
    txt += 'To add one weather entity, type in the enitity name. e.g. TX\n'
    txt += 'To add one more stations, give entity name separated by a comma. e.g TX, TG, TN'
    while True:
        ask_txt = txt
        if len(l) > 0:
            ask_txt += "\nPress 'n' to move to the next !"

        answ = answ = ask_for_txt( ask_txt, default=False, space=space )

        if utils.is_empthy(answ):
            log.console('Please type in something ...', True)
            continue # Again
        elif utils.is_quit(answ):
            return config.answer_quit[0] # Return first el for quit
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
            else:
                log.console(f"Unknown option {ent} given. Fill in one or more entities separated by an ',' ", True)

        if len(l) > 0:
            cnt, kol, t = 1, 10, 'All weather entities who are added are: '
            for ent in l:
                t += ent + ', '
                if cnt % kol == 0:
                    t += '\n'
            t = t[0:-2] # Remove space and comma
            log.console( t, True )

    return l

def ask_for_one_station( txt, l=False, space=False):
    result = False
    if l == False:
        l = utils.only_existing_stations_in_map() # Update l

    if len(l) != 0:
        t  = f'{txt}\n'
        t += vt.knmi_stations(l, 3, 25)
        t += 'To add a station, give a wmo-number or a city name'
        while True:
            answ = ask_for_txt( t, default=False, space=space )

            if utils.is_empthy(answ):
                log.console('Please type in something ...', True)
                continue
            elif utils.is_quit(answ):
                return config.answer_quit[0] # Return first el for quit
            elif stations.name_in_list(answ, l) or stations.wmo_in_list(answ, l):
               result = stations.find_by_wmo_or_name(answ, l)
               log.console(f'{result.wmo}: {result.place} {result.province} selected', True)
               break
            else:
                ask( f'Station: {answ} unknown !\nPress a key to try again...', True )
    else:
        t = 'No weatherdata found in data map. Download weatherdata first.'
        log.console(t, True)

    return result

def ask_for_stations( txt, l=False, space=False):
    result = list()
    if l == False:
        l = utils.only_existing_stations_in_map() # Update l

    if len(l) != 0:
        t  = f'{txt}\n'
        t += vt.knmi_stations( l, 3, 25 )
        t += 'To add one station, give a wmo-number or a city name\n'
        t += 'To add more stations, give a wmo-number or a city name separated by a comma\n'
        t += "Press '*' to add all available weather stations"

        while True:
            ask_txt = t
            if len(result) > 0:
                ask_txt += "\nPress 'n' to move to the next !"

            answ = ask_for_txt( ask_txt, default=False, space=space )
            log.console(' ', True)

            if utils.is_empthy(answ):
                log.console('Please type in something ...', True)
                continue
            elif utils.is_quit(answ):
                return config.answer_quit[0] # Return first el for quit
            elif answ == '*':
                result =  l
            elif answ == 'n' and len(result) > 0:
                return result
            else:
                ll = list() # Make a list with stations
                if answ.find(',') != -1:
                    ll = [clear(e) for e in answ.split(',')] # Clean input
                else:
                    if stations.name_in_list(answ, l):
                        ll.append(answ)
                    elif stations.wmo_in_list(answ, l):
                        ll.append(answ)
                    else:
                        log.console(f'Station: {answ} is unknown !')

                # Add all added stations
                for s in ll:
                    st = stations.find_by_wmo_or_name(s, l)
                    if st != False:
                        all = f'{st.wmo} {st.place} {st.province}'
                        if stations.check_if_station_already_in_list( st, result ) != True:
                            result.append(st)
                            log.console(f'Station: {all} added...')
                        else:
                            log.console(f'Station: {all} already added...')
                    else:
                        log.console(f'Station: {answ} not found...')

            if len(result) == len(l):
                log.console('\nAll available weatherstations added...', True)
                break
            elif len(result) > 0:
                log.console('\nAll weatherstation(s) who are added are: ', True)

                for s in result:
                    log.console(f'{s.wmo}: {s.place} {s.province}', True)
            else:
                continue
    else:
        t = 'No weatherdata found in data map. Download weatherdata first.'
        log.console(t, True)
        return False

    return l

def ask_for_date( txt, space=False):
    while True:
        answ = ask_for_txt( txt, default=False, space=space )

        if utils.is_empthy(answ):
            log.console('Please type in something ...', True)
            continue
        elif utils.is_quit(answ):
            return config.answer_quit[0] # Return first el for quit
        elif validate.yyyymmdd(answ):
            return answ
        else:
            log.console(f'Error in date: {answ}\n', True)

def ask_for_period( txt='', space=False ):
    info = False
    while True:
        t= f'{txt} \n'
        t += 'Period           start  -  end    \n'
        t += 'Default format  yyyymmdd-yyyymmdd \n'
        t += 'For example:    20200510-20200520 \n'
        if config.help_info or info:
            t += 'Formats with a wild card *  \n'
            t += '  --- still in development --- \n'
            t += '  ********            selects all the available data (=8x*)\n'
            t += '  ****                selects (current) year     (=4x*)\n'
            t += '  **                  selects (current) month    (=2x*)\n'
            t += '  yyyy****            selects the whole year yyyy\n'
            t += '  yyyymm**            selects the month mm in the year yyyy\n'
            t += '  ****mm**            selects a month mm for every year \n'
            t += '  ****mmdd            selects a monthday mmdd for every year \n'
            t += '  yyyy****-yyyy****   selects a full year from yyyy untill yyyy \n'
            t += '  yyyymmdd-yyyy*mmdd  selects a day mmdd in a year from start day to endyear\n'
            t += '  yyyymmdd-yyyy*mmdd* selects a certain period from mmdd=mmdd* in a year from yyyy to yyyy\n'
            t += 'Examples wildcard * \n'
            t += '  2015****            selects the year 2015 \n'
            t += '  201101**-202001**   selects all januarys from 2011 unto 2020 \n'
            t += '  ****07**            selects all julys from avalaible data \n'
            t += '  ****1225            selects all 25 decembers from avalaible data'
        else:
            t+= "Type 'i' for more info..."

        answ = ask_for_txt( t, default=False, space=space )

        if utils.is_empthy(answ):
            log.console('Please type in something ...', True)
        elif utils.is_quit(answ):
            return config.answer_quit[0] # Return first el for quit
        elif answ == 'i':
            info = True
        else:
            if daydata.check_periode( answ ):
                return answ.replace(' ', '')
            else:
                err  = f'Period of format {answ} is unknown... Press a key... '
                ask(err)

def ask_for_date_with_check_data( stat, txt, space=False ):
    log.console(f'Loading data {stat.place} ...')
    ok, data = daydata.read( stat )
    if not ok:
        input(f'Error reading data! {stat.place}')
        return config.answer_quit[0], np.array([])

    sd = int( data[ 0, daydata.YYYYMMDD])
    ed = int( data[-1, daydata.YYYYMMDD])

    t = f'{txt}\n'
    t += f'Available range data for - {stat.place} - is from {sd} untill {ed}'
    while True:
        answ = ask_for_date(t, space)

        if utils.is_quit(answ):
            return config.answer_quit[0] # Return first el for quit, np.array([])
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


def ask_for_yn( txt, default, space=False ):
    ok = False
    t  = f'{txt}\n'
    t += '\t1) Yes\n'
    t += '\t2) No'

    while True:
        answ = ask_for_txt( t, default=default, space=space )

        if utils.is_empthy(answ): # 'ie. y, n, no, yes 1, 2'
            answ = str(default)

        answ = answ.lower()

        if utils.is_quit(answ):
            return config.answer_quit[0] # Return first el for quit
        elif utils.is_yes(answ):
            return config.answer_yes[0]
        elif utils.is_no(answ):
            return config.answer_no[0]
        else:
            try:
                answi = int(answ)
            except ValueError: # Input was not a number
                pass
            else: # Input is a number
                if answi == 1:
                    return config.answer_yes[0]
                elif answi == 2:
                    return config.answer_no[0]

        log.console(f'Unknown option: {answ} ?\nTry again.', True)

def ask_type_options(txt, l, default=config.default_output, space=False):
    t = f'{txt}\n'
    i, max = 1, len(l)
    while True:
        t += f'\t{i}) {l[i-1]}'
        if i < max:
            i, t = i + 1, t + '\n'
        else:
            break

    while True:
        answ = ask_for_txt( t, default=default, space=space )

        if utils.is_empthy(answ):
            i = 0
            while i < max:
                if l[i] == default:
                    return default
                elif str(i) == str(default):
                    return l[i]
                i += 1

        if utils.is_quit(answ):
            return config.answer_quit[0] # Return first el for quit
        else:
            try:
                answi = int(answ)
            except ValueError: # Input is not a number
                if answ in l:
                    return answ
            else: # Input is a number
                i = 0
                while i < max:
                    if i + 1 == answi:
                        return l[i]
                    i += 1

                log.console(f'Unknown option: {answ} ?\nTry again.', True)

def ask_for_file_type(txt, default=config.default_output, space=False):
    l = ['txt TODO', 'html', 'cmd TODO']
    return ask_type_options(txt, l, default, space)

def ask_for_graph_type(txt, default=1, space=False):
    l = ['line', 'bar']
    return ask_type_options(txt, 'graph', l, default, space)

def ask_for_file_name(txt, default='x-x-x-x', space=False):
    answ = ask_for_txt( txt, default, space )

    if utils.is_empthy(answ):
        return str(default)
    elif utils.is_quit(answ):
        return config.answer_quit[0] # Return first el for quit

    return answ

def ask_for_color(txt, default='', space=False):
    pass

def ask_period_stations_type_name( name, space=False ):
    # Ask start and end date
    ok, period, places, type, name = False, '', list(), '', name

    # Ask for period
    t = f'Give the period for the calculation of {name} statistics'
    period = ask_for_period( t, space )
    if utils.is_quit(period):
        return ok, period, places, type, name

    # Ask for one or more stations
    places = ask_for_stations(
                    '\nSelect one (or more) weather station(s) ?', space
                )
    if not places:
        return ok, period, places, type, name
    elif utils.is_quit(places):
        return ok, period, places, type, name

    # Ask for a file type
    type = ask_for_file_type('\nSelect output filetype ? ', config.default_output, space )
    if utils.is_quit(type):
        return ok, period, places, type, name

    ok = True
    # Ask for a name
    if type != 'cmd':
        fname = f'{name}-{period.replace("*","x")}-{utils.now_for_file()}'
        fname = ask_for_file_name(
                '\nSet a name for the output file ? <optional> ', fname, space
            )
        if utils.is_quit(fname):
            ok = False # Oke quit

    return ok, period, places, type, fname

def ask_for_query( txt, space=False ):
    info = False
    while True:
        t = f'{txt}\n'
        t += 'For example: TX > 35\n'
        if config.help_info or info:
            t += 'Possible properties are\n'
            t += "' gt', '> '         = greater than             ie TG >  20  Warm nights\n"
            t += "' ge', '>=', ' ≥'   = greater than and equal   ie TX >= 30  Tropical days\n"
            t += "' lt', '< '         = less than                ie TN <   0  Frosty days\n"
            t += "' le', '<=', ' ≤'   = less than equal          ie TX <=  0  Icy days\n"
            t += "' eq', '=='         = equal                    ie DDVEC == 90  A day with a wind from the east\n"
            t += "' ne', '!=', '<>'   = not equal                ie RH !=  0  A day with rain\n"
            t += "' or', '||'  'or '  ie SQ > 10  or TX >= 25    Sunny and warm days\n"
            t += "'and', '&&'  'and'  ie RH > 10 and TX <  0     Most propably a day with snow\n"
            t += '\nPossible entities are\n'
            t += "'DDVEC' = Vector mean wind direction (degrees)    'FHVEC' = Vector mean windspeed (m/s)\n"
            t += "'FG'    = Daily mean windspeed (in 0.1 m/s)       'FHX'   = Maximum hourly mean windspeed (m/s)\n"
            t += "'FHN'   = Minimum hourly mean windspeed (m/s)     'FXX'   = Maximum wind gust (m/s)\n"
            t += "'TG'    = Daily mean temperature in (°C)          'TN'    = Minimum temperature (°C)\n"
            t += "'TX'    = Maximum temperature (°C)                'T10N'  = Minimum temperature at 10 cm (°C)\n"
            t += "'SQ'    = Sunshine duration (hour)                'SP'    = % of maximum sunshine duration\n"
            t += "'Q'     = Global radiation (J/cm2)                'DR'    = Precipitation duration (hour)\n"
            t += "'RH'    = Daily precipitation amount (mm)         'RHX'   = Maximum hourly precipitation (mm)\n"
            t += "'PG'    = Daily mean sea level pressure (hPa)     'PX'    = Maximum hourly sea level pressure (hPa)\n"
            t += "'PN'    = Minimum hourly sea level pressure (hPa) 'EV24'  = Potential evapotranspiration (mm)\n"
            t += "'VVN'   = Minimum visibility 0: <100m, 1:100-200m, 2:200-300m,..., 49:4900-5000m, 50:5-6 km, \n"
            t += '          56:6-7km, 57:7-8km,..., 79:29-30km, 80:30-35km, 81:35-40km,..., 89: >70km)\n'
            t += "'VVX'   = Maximum visibility 0: <100 m, 1:100-200 m, 2:200-300 m,..., 49:4900-5000 m, 50:5-6 km, \n"
            t += '          56:6-7km, 57:7-8km,..., 79:29-30km, 80:30-35km, 81:35-40km,..., 89: >70km)\n'
            t += "'NG'    = Mean daily cloud cover (octants)         'UG'    = Daily mean relative atmospheric humidity (%)\n"
            t += "'UX'    = Maximum atmospheric humidity (%)         'UN'    = Minimum relative atmospheric humidity (%)"
        else:
            t += "Type 'i' for more info..."

        answ = ask_for_txt( t, default=False, space=space )
        # TODO MAKE ADVANCED CHECKS

        if utils.is_empthy(answ):
            log.console('Please type in something ...', True)
        elif answ == 'i':
            info = True
        elif utils.is_quit(answ):
            return config.answer_quit[0] # Return first el for quit
        # TODO
        # elif validate.query(answ): # TODO
        #     return answ
        else:
            return utils.make_query_txt_only( answ )

    return answ  # No checking for now
