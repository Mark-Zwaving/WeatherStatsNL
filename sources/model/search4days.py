# -*- coding: utf-8 -*-
'''Functions for seaching days with charateristics'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.1.1'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import numpy as np, config
import model.stats as stats
import model.daydata as daydata
import model.utils as utils
import model.station as station
import view.log as log
import view.html as view_html
import view.dayvalues as dayvalues
import view.translate as tr
import view.icon as icon

def query_simple( data, query ):
    ent, op, val = query.split(' ')
    days = stats.terms_days(data, ent, op, val)

    return days

def query_parser( query ):
    l, queries = query.lower().split(' '), []
    mem, key, max = 0, 0, len(l)
    while key < max:
        el = l[key]
        if el in ['and', 'or']:
            q = '' # Create part query
            for i in range(mem,key):
                q += f' {l[i]} '
            queries.append( utils.clear(q) ) # Append query part
            queries.append( el ) # Append 'or', 'and'
            mem = key + 1 # Always start at the next key
        key += 1

    q = '' # Create last part query
    for i in range(mem,key):
        q += f' {l[i]} '
    queries.append( utils.clear(q) )

    return queries

def np_and( np1, np2 ):
    if np1.size == 0 and np2.size == 0:
        return np.array([])
    elif np1.size == 0 and np2.size > 0:
        return np.array([])
    elif np2.size == 0 and np1.size > 0:
        return np.array([])
    else:
        ymd, stn, l = daydata.YYYYMMDD, daydata.STN, []
        # Get only the (same) days in both lists for a station
        for n1 in list(np1):
            for n2 in list(np2):
                if n1[ymd] == n2[ymd] and n1[stn] == n2[stn]:
                    # Check first if element already in list
                    found = False
                    for el in l:
                        if set(el) == set(n1):
                            found = True
                    if not found:
                        l.append(n1)

        return np.array(l)

def np_or( np1, np2 ):
    if np1.size == 0 and np2.size == 0:
        return np.array([])
    elif np1.size == 0 and np2.size > 0:
        return np2
    elif np2.size == 0 and np1.size > 0:
        return np1
    else:
        ymd, stn, l = daydata.YYYYMMDD, daydata.STN, []
        npl = np.concatenate( (np1, np2) ) # Sum together
        # Add only unique days for station to the list
        # for el in np:
        #
        # for n1 in list(np1):
        #     for n2 in list(np2):
        #         if n1[ymd] == n2[ymd] and n1[stn] == n2[stn]:
        #             pass
        #         else:
        #             l.append(n1)

        return npl

def query_advanced( data, query ):
    # Make a query list
    queries = query_parser( query )
    # Make one list with the days based on the queries
    # The other list with the (and, or) operators
    days, oper = [], []
    for el in queries:
        if el not in ['and', 'or']:
            days.append(query_simple(data, el))
        else:
            oper.append(el)

    # Proces all the days with the and,or operators and add to sel
    ndx, key, max, sel = 0, 1, len(days), np.array([])
    while key < max:
        op, d1, d2 = oper[ndx], days[key-1], days[key] # Get the days from the query
        # Make new days and put in same list as a replacement
        if op == 'and':
            np_a = np_and( d1, d2 )
            if np_a.size != 0:
                sel = np_a if sel.size == 0 else np.concatenate( (sel, np_a) )
        elif op == 'or':
            # Or is +/- the same as a normal plus
            np_o = np_or( d1, d2 )
            if np_o.size != 0:
                sel = np_o if sel.size == 0 else np.concatenate( (sel, np_o) )

        days[key] = sel
        ndx += 1 # Next operator
        key += 1 # Next days in list

    # All selected (unique)  days
    return sel

def process( stations, period, query ):
    # Read all data stations in a given period
    data = daydata.read_stations_period( stations, period )

    # Get all the days to search for
    log.console(f'Executing query: {query}', True)
    if query.find('and') == -1 and query.find('or') == -1:
        return query_simple( data, query ) # Process only one simple query
    else:
        return query_advanced( data, query ) # Process query with and, or

def calculate(stations, period, query, type, fname):
    data = process( stations, period, query ) # All days for the terms given

    # Make path if it is a html or txt file
    path = ''
    fname = f'{fname}.{type}'
    if type == 'html':
        dir = config.dir_html_search_for_days
    elif type == 'txt':
        dir = config.dir_txt_search_for_days

    path = utils.mk_path(dir, fname)

    if type =='html':
        title = f'Days {query}'

        # Proces data in html table
        colspan = 29
        html  = f'''
        <table id="stats">
            <thead>
                <tr>
                    <th colspan="{colspan}">
                        {icon.weather_all()}
                        {title}
                        {icon.wave_square()}
                        {period}
                        {icon.cal_period()}
                    </th>
                </tr>
                <tr>
                    <th> place {icon.home(size='fa-sm')}</th>
                    <th> state {icon.flag(size='fa-sm')}</th>
                    <th> periode {icon.cal_period(size='fa-sm')}</th>
                    <th> day {icon.cal_day(size='fa-sm')}</th>
                    <th> TX {icon.temp_full(size='fa-sm')}</th>
                    <th> TG {icon.temp_half(size='fa-sm')}</th>
                    <th> TN {icon.temp_empty(size='fa-sm')}</th>
                    <th> T10N {icon.temp_empty(size='fa-sm')}</th>
                    <th> SQ {icon.sun(size='fa-sm')}</th>
                    <th> SP {icon.sun(size='fa-sm')}</th>
                    <th> RH {icon.shower_heavy(size='fa-sm')}</th>
                    <th> RHX {icon.shower_heavy(size='fa-sm')} </th>
                    <th> DR {icon.shower_heavy(size='fa-sm')}</th>
                    <th> PG {icon.compress_alt(size='fa-sm')}</th>
                    <th> PX {icon.compress_alt(size='fa-sm')}</th>
                    <th> PN {icon.compress_alt(size='fa-sm')}</th>
                    <th> UG {icon.drop_tint(size='fa-sm')}</th>
                    <th> UX {icon.drop_tint(size='fa-sm')}</th>
                    <th> UN {icon.drop_tint(size='fa-sm')}</th>
                    <th> NG {icon.cloud(size='fa-sm')}</th>
                    <th> DDVEC {icon.arrow_loc(size='fa-sm')}</th>
                    <th> FHVEC {icon.wind(size='fa-sm')}</th>
                    <th> FG {icon.wind(size='fa-sm')}</th>
                    <th> FHX {icon.wind(size='fa-sm')}</th>
                    <th> FHN {icon.wind(size='fa-sm')}</th>
                    <th> FXX {icon.wind(size='fa-sm')}</th>
                    <th> VVX {icon.eye(size='fa-sm')}</th>
                    <th> VVN {icon.eye(size='fa-sm')}</th>
                    <th> Q {icon.radiation(size='fa-sm')}</th>
                </tr>
            </thead>
            <tbody>
        '''

        if len(data) > 0:
            for day in data:
                stn, ymd, ddvec, fhvec, fg, fhx, fhxh, fhn, fhnh, fxx, fxxh, tg, \
                tn, tnh, tx, txh, t10n, t10nh, sq, sp, q, dr, rh, rhx, \
                rhxh, pg, px, pxh, pn, pnh, vvn, vvnh, vvx, vvxh, ng, ug, \
                ux, uxh, un, unh, ev24 = dayvalues.ents( day )

                place = station.from_wmo_to_name(stn)
                state = station.from_wmo_to_province(stn)
                date = f'{day[daydata.YYYYMMDD]:.0f}'
                html += f'''
                <tr>
                    <td> <span class="val">{place}</span> </td>
                    <td> <span class="val">{state}</span> </td>
                    <td> <span class="val">{period}</span> </td>
                    <td> <span class="val">{date}</span> </td>
                    <td> <span class="val">{tx}</span> <br> <small>{txh}</small> </td>
                    <td> <span class="val">{tg}</span> </td>
                    <td> <span class="val">{tn}</span> <br> <small>{tnh}</small> </td>
                    <td> <span class="val">{t10n}</span> <br> <small>{t10nh}</small> </td>
                    <td> <span class="val">{sq}</span> </td>
                    <td> <span class="val">{sp}</span> </td>
                    <td> <span class="val">{rh}</span> </td>
                    <td> <span class="val">{rhx}</span> <br> <small>{rhxh}</small> </td>
                    <td> <span class="val">{dr}</span> </td>
                    <td> <span class="val">{pg}</span> </td>
                    <td> <span class="val">{px}</span> <br> <small>{pxh}</small> </td>
                    <td> <span class="val">{pn}</span> <br> <small>{pnh}</small> </td>
                    <td> <span class="val">{ug}</span> </td>
                    <td> <span class="val">{ux}</span> <br> <small>{uxh}</small> </td>
                    <td> <span class="val">{un}</span> <br> <small>{unh}</small> </td>
                    <td> <span class="val">{ng}</span> </td>
                    <td> <span class="val">{ddvec}</span> </td>
                    <td> <span class="val">{fhvec}</span> </td>
                    <td> <span class="val">{fg}</span> </td>
                    <td> <span class="val">{fhx}</span> <br> <small>{fhxh}</small> </td>
                    <td> <span class="val">{fhn}</span> <br> <small>{fhnh}</small> </td>
                    <td> <span class="val">{fxx}</span> <br> <small>{fxxh}</small> </td>
                    <td> <span class="val">{vvx}</span> <br> <small>{vvxh}</small> </td>
                    <td> <span class="val">{vvn}</span> <br> <small>{vvnh}</small> </td>
                    <td> <span class="val">{q}</span> </td>
                </tr>
                '''
        else:
            html += f'''
                <tr>
                    <td colspan="{colspan}"> {tr.t("No days found")} </td>
                </tr>
                '''

        html += f'''
            </tbody>
            <tfoot>
                <tr>
                    <td colspan="{colspan}"> {config.knmi_dayvalues_notification} </td>
                </tr>
            </tfoot>
        </table>
        '''

        # Write to html, screen, console
        page           =  view_html.Template()
        page.title     =  title
        page.main      =  html
        page.strip     =  True
        page.set_path(dir, fname)
        # Styling
        page.add_css_file(dir='./../static/css/', name='table-statistics.css')
        page.add_css_file(dir='./../static/css/', name='default.css')
        page.add_css_file(dir='./css/', name='search4days.css')
        # Scripts
        page.add_script_file(dir='./js/', name='search4days.js')
        page.add_script_file(dir='./../static/js/', name='sort-col.js')
        page.add_script_file(dir='./../static/js/', name='default.js')

        page.save()

    elif type == 'text':
        # TODO:
        pass
    elif type == 'cmd':
        # TODO
        pass

    return path
#
