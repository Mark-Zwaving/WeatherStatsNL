# -*- coding: utf-8 -*-
'''Library contains functions for building html'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config, numpy as np
import sources.control.fio as fio
import sources.model.utils as utils
import sources.model.daydata as daydata
import sources.view.html as vhtml
import sources.view.log as log

def calculate(places, period, type, name=''):
    log.console(f'\nStart make dayvalues...\n', True)
    cnt_places = len(places)
    first = True

    for place in places:

        log.console(f'Station: {place.wmo} {place.place}', True)
        d1 = daydata.read_station_period(place, period)[1]
        dates = d1[:,daydata.YYYYMMDD]
        cnt_dates = len(dates)

        # Base directory
        if type == 'html':
            dir = config.dir_html_dayvalues
        elif type == 'txt':
            dir = config.dir_txt_dayvalues

        # Make paths
        w_dir = utils.mk_path(dir, place.wmo)

        # Make directory
        fio.mk_dir(w_dir)

        for yyyymmdd in dates:
            ymd = utils.f_to_s(yyyymmdd)
            log.console(f'Date: {utils.ymd_to_txt(ymd)}', True)

            # Get year, month and day
            y, m, d = ymd[:4], ymd[4:6], ymd[6:8]

            # Make paths
            y_dir = utils.mk_path(w_dir, y)
            m_dir = utils.mk_path(y_dir, m)

            # Make directories
            fio.mk_dir(y_dir)
            fio.mk_dir(m_dir)

            # Make file name
            if cnt_places > 1 or cnt_dates > 1:
                if first:
                    if name != '':
                        t  = '\nYour one default name for the file cannot be used. '
                        t += 'Because more than one date is given.\n'
                        t += 'Now a default name for the file (based on wmo and '
                        t += 'date) will be used.'
                        log.console(t, True)
                        input('Press a key to continue...\n')
                    first = False
                name = f'dayvalues-{place.wmo}-{y}-{m}-{d}' # Default
            fname = f'{name}.{type}'

            # Make path
            path = utils.mk_path(m_dir, fname)

            # Get correct day
            day = d1[np.where(dates == yyyymmdd)][0]

            path_to_root = './../../../../'

            # Make output
            if type == 'html':
                header  = f'<i class="text-info fas fa-home"></i> '
                header += f'{place.wmo} - {place.place} '
                header += f'{place.province} - {utils.ymd_to_txt(ymd)} '

                page = vhtml.Template()
                page.title  = f'{place.wmo} {place.place} {ymd}'
                page.header = header
                page.strip  = True
                page.main   = vhtml.main_ent( day )
                page.footer = vhtml.footer_data_notification(place)
                page.file_path = path
                page.path_to_root = path_to_root
                # Styling
                page.css_files = [ f'{path_to_root}/dayvalues/css/default.css',
                                   f'{path_to_root}/dayvalues/css/dayvalues.css' ]
                page.script_files = [ f'{path_to_root}/dayvalues/js/dayvalues.js',
                                      f'{path_to_root}/static/js/default.js']
                ok = page.save()

            if ok:
                log.console(f'Successfull made {path}', True)
            else:
                log.console(f'Failed to make {path}', True)
            log.console(' ', True)

            # elif type == 'txt':
            #     title = txt_date
            #     main  = view_dayvalues.txt_main( day )
            #     txt   = f'{title}\n{main}'
            #     path  = utils.mk_path( station.dayvalues_dir_txt, fname )

    return path
