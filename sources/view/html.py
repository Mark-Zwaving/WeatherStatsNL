# -*- coding: utf-8 -*-
'''Library contains functions for building html'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.9.4'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import os, re, config, datetime
import numpy as np
import sources.control.fio as fio
import sources.view.console as console
import sources.view.icon as icon
import sources.view.translate as tr
import sources.view.txt as vt
import sources.view.dayvalues as dayvalues
import sources.view.fix as fix
import sources.model.utils as utils
import sources.model.daydata as daydata

class Template():
    ''' Class to make a html page based on the template - template.html'''
    charset      = 'UTF-8'
    author       = 'WeatherstatsNL'
    viewport     = 'width=device-width, initial-scale=1.0, shrink-to-fit=no'
    script_files = []
    script_code  = ''
    css_files    = []
    css_code     = ''
    strip        = False

    def __init__(self, title='WeatherstatsNL - template',
                       header='', main='',  footer='' ):
        self.title  = title
        self.header = header
        self.main   = main
        self.footer = footer

        title = self.title.strip().replace(' ', '')
        dt    = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
        self.file_name = f'{title}-{dt}.html'

        self.template  = utils.mk_path( config.dir_templates_html, 'template.html' )
        self.base_dir  = os.path.dirname(os.path.abspath(__file__))
        self.file_dir  = self.base_dir
        self.file_path = utils.mk_path( self.file_dir, self.file_name )
        self.path_to_root = './'
        self.html_strip_output = config.html_strip_output

    def set_path(self, dir, name):
        self.file_path = utils.mk_path( dir, name )

    def add_css_file(self, dir='./../static/css/', name='ccs.css'):
        self.css_files.append(f'{dir}{name}')

    def add_script_file(self, dir='./../static/js/', name='js.js'):
        self.script_files.append(f'{dir}{name}')

    def create(self):
        css = ''
        for css_file in self.css_files:
            css += f'<link rel="stylesheet" type="text/css" href="{css_file}">\n'
        js = ''
        for js_file in self.script_files:
            js += f'<script src="{js_file}"> </script>\n'

        ok, self.html = fio.read( self.template )
        if ok:
            self.html = self.html.replace('{{%now%}}', str( datetime.datetime.now() ))
            self.html = self.html.replace('{{%title%}}', self.title)
            self.html = self.html.replace('{{%charset%}}', self.charset)
            self.html = self.html.replace('{{%author%}}', self.author)
            self.html = self.html.replace('{{%viewport%}}', self.viewport)
            self.html = self.html.replace('{{%css_files%}}', css)
            self.html = self.html.replace('{{%css_code%}}', self.css_code)
            self.html = self.html.replace('{{%header%}}', self.header)
            self.html = self.html.replace('{{%main%}}', self.main)
            self.html = self.html.replace('{{%footer%}}', self.footer)
            self.html = self.html.replace('{{%script_files%}}', js)
            self.html = self.html.replace('{{%script_code%}}', self.script_code)
            self.html = self.html.replace('{{%path_to_root%}}', self.path_to_root)

        return ok

    def save(self):
        ok = self.create()
        if ok:
            html = self.html
            if self.html_strip_output:
                html = re.sub('\n|\r|\t', '', html)
                html = re.sub('\s+', ' ', html)
            ok = fio.write( self.file_path, html )

        return ok

    def delete(self):
        fio.delete(self.file_path)

def footer_data_notification(station):
    t  = f'{station.data_notification}'.lower()
    t += f'<br>{utils.now_created_notification()}'
    return t

def div_ent( title=False, val=False, time=False ):
    val  =  val if  val != False else ''
    time = time if time != False else ''
    return f'''
            <div class="card col-11 col-xs-11 col-sm-11 col-md-6 col-lg-4 col-xl-3 mx-auto border-0">
                <div class="card-body">
                    <h6 class="card-title text-capitalize day_title">
                        {title}
                    </h4>
                    <div class="card-text day_data">
                        {val}
                        <br>
                        <small class="text-muted">{time}</small>
                    </div>
                </div>
            </div>
            '''.format( title, val, time )

def main_ent( day ):
    no = config.no_data_given
    stn, ymd, ddvec, fhvec, fg, fhx, fhxh, fhn, fhnh, fxx, fxxh, tg, tn,\
    tnh, tx, txh, t10n, t10nh, sq, sp, q, dr, rh, rhx, rhxh, pg, px, pxh,\
    pn, pnh, vvn, vvnh, vvx, vvxh, ng, ug, ux, uxh, un, unh, ev24 = dayvalues.ents(day)

    # Add icons
    if tx    !=  no:  tx    =  f'{icon.temp_full(color="text-danger")} {tx}'
    if tg    !=  no:  tg    =  f'{icon.temp_half(color="text-success")} {tg}'
    if tn    !=  no:  tn    =  f'{icon.temp_empty(color="text-primary")} {tn}'
    if t10n  !=  no:  t10n  =  f'{icon.temp_empty(color="text-warning")} {t10n}'
    if ddvec !=  no:  ddvec =  f'{icon.wind_dir(color="text-info")} {ddvec}'
    if fhvec !=  no:  fhvec =  f'{icon.wind(color="text-success")} {fhvec}'
    if fg    !=  no:  fg    =  f'{icon.wind(color="text-success")} {fg}'
    if fhx   !=  no:  fhx   =  f'{icon.wind(color="text-success")} {fhx}'
    if fhn   !=  no:  fhn   =  f'{icon.wind(color="text-success")} {fhn}'
    if fxx   !=  no:  fxx   =  f'{icon.wind(color="text-success")} {fxx}'
    if vvn   !=  no:  vvn   =  f'{icon.eye(color="text-info")} {vvn}'
    if vvx   !=  no:  vvx   =  f'{icon.eye(color="text-info")} {vvx}'
    if sq    !=  no:  sq    =  f'{icon.sun(color="text-warning")} {sq}'
    if sp    !=  no:  sp    =  f'{icon.sun(color="text-warning")} {sp}'
    if  q    !=  no:  q     =  f'{icon.radiation(color="text-danger")} {q}'
    if rh    !=  no:  rh    =  f'{icon.shower_heavy(color="text-primary")} {rh}'
    if dr    !=  no:  dr    =  f'{icon.shower_heavy(color="text-primary")} {dr}'
    if rhx   !=  no:  rhx   =  f'{icon.shower_heavy(color="text-primary")} {rhx}'
    if ux    !=  no:  ux    =  f'{icon.drop_tint(color="text-primary")} {ux}'
    if un    !=  no:  un    =  f'{icon.drop_tint(color="text-primary")} {un}'
    if ug    !=  no:  ug    =  f'{icon.drop_tint(color="text-primary")} {ug}'
    if ng    !=  no:  ng    =  f'{icon.cloud(color="text-secondary")} {ng}'
    if pg    !=  no:  pg    =  f'{icon.compress_alt(color="text-warning")} {pg}'
    if pn    !=  no:  pn    =  f'{icon.compress_alt(color="text-warning")} {pn}'
    if px    !=  no:  px    =  f'{icon.compress_alt(color="text-warning")} {px}'
    if ev24  !=  no:  ev24  =  f'{icon.sweat(color="text-warning")} {ev24}'

    main  = ''
    main += div_ent( vt.ent_to_title('TX'), tx, txh )
    main += div_ent( vt.ent_to_title('TG'), tg, False )
    main += div_ent( vt.ent_to_title('TN'), tn, tnh )
    main += div_ent( vt.ent_to_title('T10N'), t10n, t10nh )
    main += div_ent( vt.ent_to_title('DDVEC'), ddvec, False )
    main += div_ent( vt.ent_to_title('FG'), fg, False )
    main += div_ent( vt.ent_to_title('RH'), rh, False )
    main += div_ent( vt.ent_to_title('SQ'), sq, False )
    main += div_ent( vt.ent_to_title('PG'), pg, False )
    main += div_ent( vt.ent_to_title('UG'), ug, False )
    main += div_ent( vt.ent_to_title('FXX'), fxx, fxxh )
    main += div_ent( vt.ent_to_title('FHVEC'), fhvec, False )
    main += div_ent( vt.ent_to_title('FHX'), fhx, fhxh )
    main += div_ent( vt.ent_to_title('FHN'), fhn, fhnh )
    main += div_ent( vt.ent_to_title('SP'), sp, False )
    main += div_ent( vt.ent_to_title('Q'), q, False )
    main += div_ent( vt.ent_to_title('DR'), dr, False )
    main += div_ent( vt.ent_to_title('RHX'), rhx, rhxh )
    main += div_ent( vt.ent_to_title('PX'), px, pxh )
    main += div_ent( vt.ent_to_title('PN'), pn, pnh )
    main += div_ent( vt.ent_to_title('VVN'), vvn, vvnh )
    main += div_ent( vt.ent_to_title('VVX'), vvx, vvxh )
    main += div_ent( vt.ent_to_title('NG'), ng, False )
    main += div_ent( vt.ent_to_title('UX'), ux, uxh )
    main += div_ent( vt.ent_to_title('UN'), un, unh )
    main += div_ent( vt.ent_to_title('EV24'), ev24, False )

    return main

def table_days(days, entity, time_ent=''):
    html = ''
    total = np.size(days, axis=0)
    if total > 0:
        # Time th cell yess or no
        b_time_cell  = True if time_ent != '' else False
        th_time_cell = '<th>time</th>' if b_time_cell else ''
        time_ndx = daydata.ndx_ent(time_ent) if b_time_cell else -1
        val_ndx  = daydata.ndx_ent(entity) # Index of value

        # HTML table header
        html += f'''
                <table class="popup">
                    <thead>
                        <tr>
                            <th>pos</th>
                            <th>date</th>
                            <th>val</th>
                            {th_time_cell}
                        </tr>
                    </thead>
                    <tbody>
                '''

        pos, max = 1, config.html_popup_table_val_10
        if max == -1:
            max = total

        for day in days:
            ymd  = int(day[daydata.YYYYMMDD]) # Get data int format
            symd = utils.ymd_to_txt( ymd ) # Get date string format
            val = fix.ent( day[val_ndx], entity )  # Get value with right output

            # Get a time value or not
            time_val = f'<td>{fix.ent(day[time_ndx], time_ent)}</td>' if b_time_cell else ''

            html += f'''
                        <tr>
                            <td>{pos}</td>
                            <td title="{symd}">{ymd}</td>
                            <td>{val}</td>
                            {time_val}
                        </tr>
                    '''
            if pos == max:
                break
            else:
                pos += 1

        html += '''
                </tbody>
            </table>
                '''
    return html

def table_days_count(days, entity, time_ent=''):
    html = ''
    total = np.size(days, axis=0)
    if total > 0:
        # Time th cell yess or no
        b_time_cell  = True if time_ent != '' else False
        th_time_cell = '<th>time</th>' if b_time_cell else ''
        time_ndx = daydata.ndx_ent( time_ent ) if b_time_cell else -1
        val_ndx  = daydata.ndx_ent( entity )  # Index of value

        html += f'''
                <table class="popup">
                    <thead>
                        <tr>
                            <th>date</th>
                            <th>val</th>
                            {th_time_cell}
                            <th>cnt</th>
                        </tr>
                    </thead>
                    <tbody>
                '''

        pos, max = 1, config.html_popup_table_cnt_rows
        if max == -1:
            max = total

        days = np.flip(days, axis=0) # Reverse the matrix. Last day first
        for day in days:
            ymd  = int(day[daydata.YYYYMMDD])
            symd = utils.ymd_to_txt( ymd )
            val  = fix.ent( day[val_ndx], entity )
            tme  = f'<td>{fix.ent(day[time_ndx],time_ent)}</td>' if b_time_cell else ''
            html += f'''
                        <tr>
                            <td title="{symd}">{ymd}</td>
                            <td>{val}</td>
                            {tme}
                            <td>{total}</td>
                        </tr>
                    '''
            if pos == max:
                break
            else:
                total, pos = total - 1, pos + 1

        html += '''
                    </tbody>
                </table>
                '''

    return html


def table_day_sum(days, entity=''):
    html = ''
    total = np.size(days, axis=0)
    if total > 0:
        # HTML table header
        html += f'''
                <table class="popup">
                    <thead>
                        <tr>
                            <th>date</th>
                            <th>val</th>
                            <th>sum</th>
                            <th>cnt</th>
                        </tr>
                    </thead>
                    <tbody>
                '''

        # Prepare values
        l, sum, cnt = list(), 0.0, 1
        ndx_ent  = daydata.ndx_ent(entity) # Index of value
        for day in days:
            ymd  = int(day[daydata.YYYYMMDD]) # Get data int format
            symd = utils.ymd_to_txt(ymd) # Get date string format
            raw  = day[ndx_ent]
            sum += raw
            l.append( f'''
                        <tr>
                            <td title="{symd}">{ymd}</td>
                            <td>{fix.ent(raw,  entity)}</td>
                            <td>{fix.rounding(sum,  entity)}</td>
                            <td>{cnt}</td>
                        </tr>
                    ''' )
            cnt += 1

        l.reverse() # Reverse list
        # Put to html until max
        cnt, max = 1, config.html_popup_table_val_10
        if max == -1: max = total
        for el in l:
            html += el
            if cnt == max:
                break
            else:
                cnt += 1

        html += '''
                </tbody>
            </table>
                '''

def table_extremes(l, max):
    html = ''
    if l:
        if max is not 0:
            l.reverse() # Most extreme is last. Make first
            cnt = len(l)
            max = cnt if max == -1 else max # -1 for all!
            end = cnt if max > cnt else max # check bereik
            html += '<table class="popup">'
            html += '<thead><tr><th>datum</th><th>value</th><th>time</th><tr></thead>'
            html += '<tbody>'

            for e in l[:end]:
                sdt  = d.Datum( e.datum ).tekst()
                val = fn.rm_s( fn.fix( e.extreem, e.ent) )
                t_ent = knmi.ent_to_t_ent( e.ent )
                tme = fn.rm_s(fn.fix(e.tijd, t_ent)) if t_ent is not False else '.'
                html += f'<tr><td title="{sdt}">{e.datum}</td><td>{val}</td><td>{tme}</td></tr>'

            html += '</tbody>'
            html += '</table>'

    return html

def table_frost_sum( days, entity='TN' ):
    html = ''
    total = np.size(days, axis=0)
    if total > 0:
        # HTML table header
        html += f'''
                <table class="popup">
                    <thead>
                        <tr>
                            <th>date</th>
                            <th>tx</th>
                            <th>txh</th>
                            <th>tn</th>
                            <th>tnh</th>
                            <th>val</th>
                            <th>sum</th>
                            <th>cnt</th>
                        </tr>
                    </thead>
                    <tbody>
                '''

        # Prepare values
        l, tot, cnt = list(), 0.0, 1
        for day in days:
            ymd  = int(day[daydata.YYYYMMDD]) # Get data int format
            symd = utils.ymd_to_txt( ymd ) # Get date string format
            tx   = day[daydata.TX]
            txh  = day[daydata.TXH]
            tn   = day[daydata.TN]
            tnh  = day[daydata.TNH]

            # Calculate frost sum
            dsum = 0.0
            if tx < 0: dsum += abs(tx)
            if tn < 0: dsum += abs(tn)
            tot += dsum

            l.append( f'''
                        <tr>
                            <td title="{symd}">{ymd}</td>
                            <td>{fix.ent(tx,  entity)}</td>
                            <td>{fix.ent(txh, 'TXH')}</td>
                            <td>{fix.ent(tn,  entity)}</td>
                            <td>{fix.ent(tnh, 'TNH')}</td>
                            <td>{fix.rounding(dsum, entity)}</td>
                            <td>{fix.rounding(tot,  entity)}</td>
                            <td>{cnt}</td>
                        </tr>
                    ''' )
            cnt += 1

        l.reverse() # Reverse list
        # Put to html until max
        cnt, max = 1, config.html_popup_table_val_10
        if max == -1: max = total
        for el in l:
            html += el
            if cnt == max:
                break
            else:
                cnt += 1

        html += '''
                </tbody>
            </table>
                '''
    return html

def table_hellmann(days, entity='TG'):
    html = ''
    total = np.size(days, axis=0)
    if total > 0:
        # HTML table header
        html += f'''
                <table class="popup">
                    <thead>
                        <tr>
                            <th>date</th>
                            <th>tg</th>
                            <th>val</th>
                            <th>sum</th>
                            <th>cnt</th>
                        </tr>
                    </thead>
                    <tbody>
                '''

        # Prepare values
        l, sum, cnt = list(), 0.0, 1
        ndx_ent  = daydata.ndx_ent(entity) # Index of value
        for day in days:
            ymd  = int(day[daydata.YYYYMMDD]) # Get data int format
            symd = utils.ymd_to_txt( ymd ) # Get date string format
            raw  = day[daydata.TG]
            hman = abs(raw)
            sum += hman
            l.append( f'''
                        <tr>
                            <td title="{symd}">{ymd}</td>
                            <td>{fix.ent(raw,  entity)}</td>
                            <td>{fix.rounding(hman, entity)}</td>
                            <td>{fix.rounding(sum,  entity)}</td>
                            <td>{cnt}</td>
                        </tr>
                    ''' )
            cnt += 1

        l.reverse() # Reverse list
        # Put to html until max
        cnt, max = 1, config.html_popup_table_val_10
        if max == -1: max = total
        for el in l:
            html += el
            if cnt == max:
                break
            else:
                cnt += 1

        html += '''
                </tbody>
            </table>
                '''
    return html

def table_heat_ndx(days, entity='TG'):
    html = ''
    total = np.size(days, axis=0)
    if total > 0:
        # HTML table header
        html += f'''
                <table class="popup">
                    <thead>
                        <tr>
                            <th>date</th>
                            <th>tg</th>
                            <th>heat</th>
                            <th>sum</th>
                            <th>cnt</th>
                        </tr>
                    </thead>
                    <tbody>
                '''

        # Prepare values
        l, sum, cnt = list(), 0.0, 1
        for day in days:
            ymd  = int( day[daydata.YYYYMMDD] ) # Get data int format
            symd = utils.ymd_to_txt( ymd ) # Get date string format
            raw  = day[daydata.TG]
            heat = raw - 180.0
            sum += heat
            l.append( f'''
                        <tr>
                            <td title="{symd}">{ymd}</td>
                            <td>{fix.ent(raw,  entity)}</td>
                            <td>{fix.rounding(heat, entity)}</td>
                            <td>{fix.rounding(sum,  entity)}</td>
                            <td>{cnt}</td>
                        </tr>
                    ''' )
            cnt += 1

        l.reverse() # Reverse list
        # Put to html until max
        cnt, max = 1, config.html_popup_table_val_10
        if max == -1: max = total
        for el in l:
            html += el
            if cnt == max:
                break
            else:
                cnt += 1

        html += '''
                </tbody>
            </table>
                '''
    return html


def table_list_heatwave_days( l, max ):
    html = ''
    if l:
        if max is not 0:
            l.reverse()
            cnt = len(l)
            max = cnt if max == -1 else max # -1 for all!
            end = cnt if max > cnt else max # check bereik
            warm_sum = stat.heat_sum(l)['value'] # Total heat ndx
            html += '''<table class="popup">
                       <thead>
                       <tr><th>datum</th><th>∑dag</th><th>∑warmte</th>
                           <th>warmte</th><th>tx</th><th>tg</th><th>tn</th></tr>
                       </thead>
                       '''

            for e in l[:end]:
                sdt = d.Datum(e.YYYYMMDD).tekst()
                tx  = fn.rm_s(fn.fix(e.TX, 'tx'))
                tn  = fn.rm_s(fn.fix(e.TN, 'tn'))
                tg  = fn.rm_s(fn.fix(e.TG, 'tg'))

                tot_warm = fn.rm_s(fn.fix(warm_sum,'heat_ndx'))
                act_warm = stat.get_heat_ndx_of_etm_geg(e)
                g_warm = fn.rm_s(fn.fix(act_warm,'heat_ndx'))

                html += f'''<tr>
                            <td title="{sdt}">{e.YYYYMMDD}</td><td>{cnt}</td>
                            <td>{tot_warm}</td><td>{g_warm}</td><td>{tx}</td>
                            <td>{tg}</td><td>{tn}</td>
                            </tr>
                        '''

                # Minus act day heatndx for the total heatndx of the day before
                warm_sum -= act_warm
                cnt -= 1

            html += '</tbody>'
            html += '</table>'

    return html
