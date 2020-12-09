# -*- coding: utf-8 -*-
'''Library contains functions for building html'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.3'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config, numpy as np
import sources.model.utils as utils
import sources.model.daydata as daydata
import sources.view.html as view_html
import sources.view.log as log

def calculate(data, ymd, station, type, fname):
    log.console(f'Station: {station.wmo} {station.place}', True)
    log.console(f'Date: {utils.ymd_to_txt(ymd)}', True)

    sel = np.where(data[:,daydata.YYYYMMDD] == float(ymd))
    day = data[sel][0]

    # Make path if it is a html or txt file
    dir, path  = '', ''
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
        header += f'{station.province} - {utils.ymd_to_txt(ymd)} '

        page = view_html.Template()
        page.title  = f'{station.place}-{ymd}'
        page.header = header
        page.strip  = True
        page.main   = view_html.main_ent( day )
        page.footer = view_html.footer_data_notification(station)
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
        path  = utils.mk_path( station.dayvalues_dir_txt, fname )

    return path
