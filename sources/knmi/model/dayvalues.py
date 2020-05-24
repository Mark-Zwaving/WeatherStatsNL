# -*- coding: utf-8 -*-
'''Library contains functions for grabbing and searching dayvalues from a file'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.4"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, threading
import config
import model.utils as utils
import view.log as log
import knmi.model.daydata as daydata


def prepare( station, yyyymmdd, file_name, file_type ):
    day = day( station, yyyymmdd )
    if day:
        log.console(f'...Preparing dayvalues ({type}): {station.wmo} {station.place}...')
        # Prepare a name for a file
        if not file_name:
            file_name = f'{station.wmo}-{yyyymmdd}'

        if type == 'html':
            path = utils.path(config.dir_data_html_dayvalues, f'{file_name}.html')
        elif type == 'txt':
            path = utils.path(config.dir_data_txt_dayvalues, f'{file_name}.txt')

        content = ''
        if type == 'html':
            view_dayvalues.html()


        if type == 'txt' or type == 'cmd':
            content = 'TODO'

        if type == 'cmd':
            log.console(content, True)

        if type != 'cmd':
            io.write(path, content)  # Write content to file
    else:
        log.console('Error in dayvalues')

    return file_name
