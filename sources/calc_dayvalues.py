# -*- coding: utf-8 -*-
'''Library contains functions for grabbing and searching dayvalues from a file'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.4"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, threading, config as c, knmi, write as w, fn, fn_html as h, dates as d
import fn_read as r

def prepare_day_values( station, yyyymmdd, name, type ):
    day = r.get_knmi_etmgeg_by_station_and_date( station, yyyymmdd )
    file_name = ''
    if day:
        # Prepare a default name
        if not name: name = f'{station.wmo}-{yyyymmdd}'

        if type == 'html':
            name = f'{name}.html'
            path = station.dir_html

        if type == 'txt':
            name = f'{name}.txt'
            path = station.dir_text

        content = ''
        if type == 'html':
            header = f'''
            <header>
                <h3>
                    {station.wmo} - {station.plaats} {station.provincie} -
                    {d.Datum(day.YYYYMMDD).tekst()}
                </h3>
            </header>
            '''

            footer = f'<footer> {station.bronvermelding} </footer>'

            title = f'{station.plaats}-{yyyymmdd}'
            css     = r.get_string_css_from_file( 'default-dayvalues.css' ) # Get css from file
            content = header + h.div_entities(day) + footer
            content = h.pagina(title, css, content) # Make html page
            content = fn.clean_s(content) # Remove unnecessary whitespace

        if type == 'txt' or type == 'cmd':
            content = 'TODO'

        if type == 'cmd':
            fn.println(content)

        if type != 'cmd':
            file_name = fn.mk_path( path, name )
            w.write_to_file(file_name, content) # Write to

    else:
        if c.log:
            fn.println('Error in dayvalues')

    return file_name
