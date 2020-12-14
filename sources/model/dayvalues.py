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
import sources.view.console as console
import stations
from pathlib import Path

def calculate(places, period, type, check=False, download=False):
    console.log(f'\nStart make dayvalues...\n', True)
    cnt_places = len(places)

    for place in places:
        console.log(f'Station: {place.wmo} {place.place}', True)

        if download:
            daydata.process_data( stations.from_wmo_to_station(place.wmo) )
            console.log(' ')

        d1 = daydata.read_station_period(place, period)[1]
        dates = d1[:,daydata.YYYYMMDD]
        cnt_dates = len(dates)

        # Base directory
        dir = utils.mk_path(config.dir_dayvalues, type)

        # Make paths
        w_dir = utils.mk_path(dir, place.wmo)

        for yyyymmdd in dates:
            ymd = utils.f_to_s(yyyymmdd)

            # Get year, month and day
            y, m, d = ymd[:4], ymd[4:6], ymd[6:8]

            # Make paths
            y_dir = utils.mk_path(w_dir, y)
            m_dir = utils.mk_path(y_dir, m)

            # Make path
            path = utils.mk_path(m_dir, f'dayvalues-{place.wmo}-{y}-{m}-{d}.{type}')

            # if fio.path = Path(fname)  # Python 3.4
            if check:
                if Path(path).exists():  # Check if there is a file
                    console.log(f'Path for file {path} found and skipped...', True)
                    continue

            console.log(f'A file for station {place.place} for the date {ymd} will be made...', True)

            # Check and make directories
            ok = fio.mk_dir(m_dir)
            if not ok:
                ok = fio.mk_dir(y_dir)
                if not ok:
                    fio.mk_dir(w_dir)

            # Get correct day
            day = d1[np.where(dates == yyyymmdd)][0]

            path_to_root = './../../../../../'

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
                page.template = utils.mk_path( config.dir_templates_html, 'dayvalues.html' )
                # Styling
                page.css_files = [ f'{path_to_root}dayvalues/css/default.css',
                                   f'{path_to_root}dayvalues/css/dayvalues.css' ]
                page.script_files = [
                                      f'{path_to_root}dayvalues/js/default.js',
                                      f'{path_to_root}static/js/default.js']
                ok = page.save()

            if ok:
                console.log(f'Successfull made {path}', True)
            else:
                console.log(f'Failed to make {path}', True)
            console.log(' ', True)

            # elif type == 'txt':
            #     title = txt_date
            #     main  = view_dayvalues.txt_main( day )
            #     txt   = f'{title}\n{main}'
            #     path  = utils.mk_path( station.dayvalues_dir_txt, fname )

    return path
