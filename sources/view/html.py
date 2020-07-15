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
import control.io as io
import view.log as log
import view.icon as icon
import view.translate as tr
import view.txt as view_txt
import view.dayvalues as dayvalues
import view.fix as fix
import model.utils as utils
import model.station as station
import model.daydata as daydata

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

        self.template  = utils.mk_path( config.dir_html_templates, 'template.html' )
        self.base_dir  = os.path.dirname(os.path.abspath(__file__))
        self.file_dir  = self.base_dir
        self.file_path = utils.mk_path( self.file_dir, self.file_name )

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

        ok, self.html = io.read( self.template )
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

        return ok

    def save(self):
        ok = False

        try:
            ok = self.create( )
            html = self.html
            if config.strip_html_output:
                html = re.sub('\n|\r|\t', '', html)
                html = re.sub('\s+', ' ', html)
            ok = io.write( self.file_path, html )
        except Exception as e:  # ERROR ?????
            log.console( f'Error: {e}' )
        else:
            log.console( f'Creating file: {self.file_path} succesful' )
            ok = True

        return ok

    def delete(self):
        io.delete(self.file_path)


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
    if tx    !=  no:  tx    =  f'{icon.tx} {tx}'
    if tg    !=  no:  tg    =  f'{icon.tg} {tg}'
    if tn    !=  no:  tn    =  f'{icon.tn} {tn}'
    if t10n  !=  no:  t10n  =  f'{icon.t10n} {t10n}'
    if ddvec !=  no:  ddvec =  f'{icon.arro} {ddvec}'
    if fhvec !=  no:  fhvec =  f'{icon.wind} {fhvec}'
    if fg    !=  no:  fg    =  f'{icon.wind} {fg}'
    if fhx   !=  no:  fhx   =  f'{icon.wind} {fhx}'
    if fhn   !=  no:  fhn   =  f'{icon.wind} {fhn}'
    if fxx   !=  no:  fxx   =  f'{icon.wind} {fxx}'
    if vvn   !=  no:  vvn   =  f'{icon.bino} {vvn}'
    if vvx   !=  no:  vvx   =  f'{icon.bino} {vvx}'
    if sq    !=  no:  sq    =  f'{icon.sun} {sq}'
    if sp    !=  no:  sp    =  f'{icon.sun} {sp}'
    if  q    !=  no:  q     =  f'{icon.radi} {q}'
    if rh    !=  no:  rh    =  f'{icon.umbr} {rh}'
    if dr    !=  no:  dr    =  f'{icon.umbr} {dr}'
    if rhx   !=  no:  rhx   =  f'{icon.umbr} {rhx}'
    if ux    !=  no:  ux    =  f'{icon.drop} {ux}'
    if un    !=  no:  un    =  f'{icon.drop} {un}'
    if ug    !=  no:  ug    =  f'{icon.drop} {ug}'
    if ng    !=  no:  ng    =  f'{icon.clou} {ng}'
    if pg    !=  no:  pg    =  f'{icon.pres} {pg}'
    if pn    !=  no:  pn    =  f'{icon.pres} {pn}'
    if px    !=  no:  px    =  f'{icon.pres} {px}'
    if ev24  !=  no:  ev24  =  f'{icon.swea} {ev24}'

    main  = ''
    main += div_ent( view_txt.ent_to_title('TX'), tx, txh )
    main += div_ent( view_txt.ent_to_title('TG'), tg, False )
    main += div_ent( view_txt.ent_to_title('TN'), tn, tnh )
    main += div_ent( view_txt.ent_to_title('T10N'), t10n, t10nh )
    main += div_ent( view_txt.ent_to_title('DDVEC'), ddvec, False )
    main += div_ent( view_txt.ent_to_title('FG'), fg, False )
    main += div_ent( view_txt.ent_to_title('RH'), rh, False )
    main += div_ent( view_txt.ent_to_title('SQ'), sq, False )
    main += div_ent( view_txt.ent_to_title('PG'), pg, False )
    main += div_ent( view_txt.ent_to_title('UG'), ug, False )
    main += div_ent( view_txt.ent_to_title('FXX'), fxx, fxxh )
    main += div_ent( view_txt.ent_to_title('FHVEC'), fhvec, False )
    main += div_ent( view_txt.ent_to_title('FHX'), fhx, fhxh )
    main += div_ent( view_txt.ent_to_title('FHN'), fhn, fhnh )
    main += div_ent( view_txt.ent_to_title('SP'), sp, False )
    main += div_ent( view_txt.ent_to_title('Q'), q, False )
    main += div_ent( view_txt.ent_to_title('DR'), dr, False )
    main += div_ent( view_txt.ent_to_title('RHX'), rhx, rhxh )
    main += div_ent( view_txt.ent_to_title('PX'), px, pxh )
    main += div_ent( view_txt.ent_to_title('PN'), pn, pnh )
    main += div_ent( view_txt.ent_to_title('VVN'), vvn, vvnh )
    main += div_ent( view_txt.ent_to_title('VVX'), vvx, vvxh )
    main += div_ent( view_txt.ent_to_title('NG'), ng, False )
    main += div_ent( view_txt.ent_to_title('UX'), ux, uxh )
    main += div_ent( view_txt.ent_to_title('UN'), un, unh )
    main += div_ent( view_txt.ent_to_title('EV24'), ev24, False )

    return main

def table_count(days, ent, t_ent, max):
    html = ''
    if np.size(days, axis=0) > 0:
        if max != 0:
            tel   = 1
            cnt   = np.size(days, axis=0)
            ndx   = daydata.ndx_ent( ent )
            t_ndx = -1 if t_ent == '' else daydata.ndx_ent( t_ent )
            tme   = '' if t_ndx == -1 else '<th>time</th>'
            max   = cnt if max == -1 else max  #  -1 for all!
            max   = cnt if max > cnt else max  #  check bereik
            html += f'''
                    <table class="popup">
                        <thead>
                            <tr>
                                <th>date</th>
                                <th>value</th>
                                {tme}
                                <th>cnt</th>
                            </tr>
                        </thead>
                        <tbody>
                    '''

            total = np.size(days, axis=0)
            for day in days[::-1]:
                ymd  = int(day[daydata.YYYYMMDD])
                symd = utils.ymd_to_txt( ymd )
                val  = fix.ent( day[ndx], ent )
                tme  = '' if t_ndx == -1 else '<td>'+fix.ent(day[t_ndx],t_ent)+'</td>'
                html += f'''
                            <tr>
                                <td title="{symd}">{ymd}</td>
                                <td>{val}</td>
                                {tme}
                                <td>{total}</td>
                            </tr>
                        '''
                total -= 1

            html += '''
                        </tbody>
                    </table>
                    '''

    return html

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

def table_hellmann ( l, max ):
    html = ''
    if l:
        if max is not 0:
            l.reverse()
            cnt = len(l)
            max = cnt if max == -1 else max # -1 for all!
            end = cnt if max > cnt else max # check bereik
            html += '<table class="popup">'
            html += '<thead><tr><th>datum</th><th>getal</th><th>totaal</th><th>aantal</th></tr></thead>'
            html += '<tbody>'

            for e in l[:end]:
                sdt = d.Datum(e.datum).tekst()
                get = fn.rm_s(fn.fix(e.getal, 'hellmann'))
                som = fn.rm_s(fn.fix(e.som, 'hellmann'))
                html += f'<tr><td title="{sdt}">{e.datum}</td><td>{som}</td>'
                html += f'<td>{get}</td><td>{e.aantal}</td></tr>'

            html += '</tbody>'
            html += '</table>'

    return html

def table_heat_ndx( l, max ):
    html = ''
    if l:
        if max is not 0:
            l.reverse()
            cnt = len(l)
            max = cnt if max == -1 else max # -1 for all!
            end = cnt if max > cnt else max # check bereik
            html += '<table class="popup">'
            html += '<thead><tr><th>datum</th><th>tg</th><th>getal</th>'
            html += '<th>totaal</th><th>aantal</th></tr></thead>'
            html += '<tbody>'

            for e in l[:end]:
                sdt = d.Datum(e.datum).tekst()
                tg  = fn.rm_s(fn.fix(e.tg, 'tg'))
                get = fn.rm_s(fn.fix(e.getal, 'heat_ndx'))
                som = fn.rm_s(fn.fix(e.totaal, 'heat_ndx'))
                html += f'<tr><td title="{sdt}">{e.datum}</td><td>{tg}</td>'
                html += f'<td>{get}</td><td>{som}</td><td>{e.aantal}</td></tr>'

            html += '</tbody>'
            html += '</table>'

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

def table_search_for_days(data, symd, eymd):
    colcnt = 26
    html  = '<table>'
    html += '<thead>'
    html += '<tr>'
    html += f'<th> station </th>'
    html += f'<th> periode </th>'
    html += f'<th> day </th>'
    html += f'<th> TX </th>'
    html += f'<th> TG </th>'
    html += f'<th> TN </th>'
    html += f'<th> T10N </th>'
    html += f'<th> SQ </th>'
    html += f'<th> RH </th>'
    html += f'<th> UG </th>'
    html += f'<th> NG </th>'
    html += f'<th> DDVEC </th>'
    html += f'<th> FHVEC </th>'
    html += f'<th> FG </th>'
    html += f'<th> FHX </th>'
    html += f'<th> FHN </th>'
    html += f'<th> FXX </th>'
    html += f'<th> SP </th>'
    html += f'<th> Q </th>'
    html += f'<th> DR </th>'
    html += f'<th> RHX  </th>'
    html += f'<th> PG </th>'
    html += f'<th> PX </th>'
    html += f'<th> PN </th>'
    html += f'<th> VVN </th>'
    html += f'<th> VVX </th>'
    html += '</tr>'
    html += '</thead>'
    html += '<tbody>'
    if len(data) > 0:
        for day in data:
            stn, ymd, ddvec, fhvec, fg, fhx, fhxh, fhn, fhnh, fxx, fxxh, tg, \
            tn, tnh, tx, txh, t10n, t10nh, sq, sp, q, dr, rh, rhx, \
            rhxh, pg, px, pxh, pn, pnh, vvn, vvnh, vvx, vvxh, ng, ug, \
            ux, uxh, un, unh, ev24 = dayvalues.ents( day )

            # Make correct id
            id = ''
            name = station.from_wmo_to_name(stn)
            prov = station.from_wmo_to_province(stn)
            if name != stn: id += f' {name} ' # Add name if  given
            if prov != stn: id += f' {prov} ' # Add prov if given
            if id == '':    id  = f' {stn} '  # No name or prov use wmo
            date = int(day[daydata.YYYYMMDD])

            html += '<tr>'
            html += f'<td> {id} </td>'
            html += f'<td> {symd}-{eymd} </td>'
            html += f'<td> {date} </td>'
            html += f'<td> {tx} {txh} </td>'
            html += f'<td> {tg} </td>'
            html += f'<td> {tn} {tnh} </td>'
            html += f'<td> {t10n} {t10nh} </td>'
            html += f'<td> {sq} </td>'
            html += f'<td> {rh} </td>'
            html += f'<td> {ug} </td>'
            html += f'<td> {ng} </td>'
            html += f'<td> {ddvec} </td>'
            html += f'<td> {fhvec} </td>'
            html += f'<td> {fg} </td>'
            html += f'<td> {fhx} {fhxh} </td>'
            html += f'<td> {fhn} {fhnh} </td>'
            html += f'<td> {fxx} {fxxh} </td>'
            html += f'<td> {sp} </td>'
            html += f'<td> {q} </td>'
            html += f'<td> {dr} </td>'
            html += f'<td> {rhx} {rhxh} </td>'
            html += f'<td> {pg} </td>'
            html += f'<td> {px} {pxh} </td>'
            html += f'<td> {pn} {pnh} </td>'
            html += f'<td> {vvn} {vvnh} </td>'
            html += f'<td> {vvx} {vvxh} </td>'
            html += '</tr>'
    else:
        html += f'<tr> <td colspan="{colcnt}"> {tr.t("No days found")} </td> </tr>'

    html += '</tbody>'
    html += '<tfoot>'
    html += f'<tr> <td colspan="{colcnt}"> {config.knmi_dayvalues_notification} </td> </tr>'
    html += '</tfoot>'
    html += '</table>'

    return html

#
