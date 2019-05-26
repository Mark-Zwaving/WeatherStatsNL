# -*- coding: utf-8 -*-
'''Library contains functions for grabbing and searching dayvalues from a file'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, threading, config as c, knmi, write as w, fn, fn_html, dates as d

def get_list_day_values_by_station( station ):
    l, name = [], station.file_etmgeg_txt
    try:
        with open(name, 'r') as f:
            l = f.readlines()
    except IOError as e:
        if c.log:
            print (f'''
Read data from file: '{name}' failed"
{c.ln}{e.reason}{c.ln}{e.strerror}
            ''')
    else:
        if c.log:
            print(f"Read data from file: '{name}' succesful")

        l = l[station.skip_lines:] # Only real data in list

    return l

def get_string_day_values_by_station_and_date( station, yyyymmdd ):
    '''Function: gets the weatherdata from a station at a given date'''
    result, oke, lock_read = '', False, threading.Lock()
    with lock_read:
        wmo_name, f_name = f'{station.wmo} {station.plaats}', station.file_etmgeg_txt
        l = get_list_day_values_by_station(station)
        if l:
            for day in l:
                if day[6:14] == yyyymmdd:
                    result = day
                    if c.log:
                        print(f"Read data station: {wmo_name} from date: {yyyymmdd} succes!")
                    break
        else:
            if c.log:
                print(f"Read data station: {wmo_name} failed")
                print(f"Filename:'{f_name}'")

    return result

def prepare_day_values( l_stations, yyyymmdd, name, type ):
    station = l_stations[0]
    dayvalues = get_string_day_values_by_station_and_date( station, yyyymmdd )

    # Prepare a default name
    if not name:
        name = f'{station.wmo}-{yyyymmdd}'

    if type == 'html':
        name = f'{name}.html'
        path = station.dir_html
    elif type == 'txt':
        name = f'{name}.txt'
        path = station.dir_text

    file_name = fn.mk_path(path, name)

    content = ''
    if dayvalues is not '':
        day = knmi.Etmgeg(dayvalues)

        if type == 'html':
            title = f'{station.plaats}-{yyyymmdd}'
            css  = fn_html.css_day_values ()

            header = f'''
            <header>
                <h3>
                    {station.wmo} - {station.plaats} {station.provincie} -
                    {d.Datum(day.YYYYMMDD).tekst()}
                </h3>
            </header>
            '''

            footer = f'''
                <footer>
                    {station.bronvermelding}
                </footer>
            '''

            data = fn_html.div_entities( day )
            html = header + data + footer
            content = fn_html.pagina(title, css, html)

        if type == 'txt':
            content = 'TODO'

        if type == 'cmd':
            content = 'TODO'

    if type == 'txt':
        print(f'{cfg.line}{cfg.ln}{content}{cfg.ln}{cfg.line}')

    w.write_to_file(file_name, content) # Write to file
