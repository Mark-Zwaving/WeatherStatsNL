# -*- coding: utf-8 -*-
'''Library contains functions for building html'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.2'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config
import numpy as np
import model.utils as utils
import model.daydata as daydata
import view.html as view_html
import view.log as log

def calculate(data, ymd, station, type, fname):
    log.console(f'Station: {station.wmo} {station.place}', True)
    log.console(f'Date: {utils.ymd_to_txt(ymd)}', True)

    day = data[np.where(data[:,daydata.YYYYMMDD] == int(ymd))][0]
    txt_date = utils.ymd_to_txt(ymd)
    footer = station.dayvalues_notification.lower()

    # Make path if it is a html or txt file
    path  = ''
    fname = f'{fname}.{type}'
    if type == 'html':
        dir = config.dir_html_dayvalues
    elif type == 'txt':
        dir = config.dir_txt_dayvalues
    path = utils.mk_path(dir, fname)

    # Make output
    if type == 'html':
        header  = f'<i class="text-info fas fa-home"></i> '
        header += f'{station.wmo} - {station.place} '
        header += f'{station.province} - {txt_date} '

        page = view_html.Template()
        page.title  = f'{station.place}-{ymd}'
        page.header = header
        page.strip  = True
        page.main   = view_html.main_ent( day )
        page.footer = footer
        page.set_path( dir, fname )
        # Styling
        page.add_css_file(dir='./../static/css/', name='default.css')
        page.add_css_file(dir='./css/', name='dayvalues.css')
        # Scripts
        page.add_script_file(dir='./js/', name='dayvalues.js')
        page.add_script_file(dir='./../static/js/', name='default.js')
        page.save()

    elif type == 'txt':
        title = txt_date
        main  = view_dayvalues.txt_main( day )
        txt   = f'{title}\n{main}'
        path  = utils.mk_path( config.dir_txt_dayvalues, name )

    return path
