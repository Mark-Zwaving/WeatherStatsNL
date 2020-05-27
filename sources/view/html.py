# -*- coding: utf-8 -*-
'''Library contains functions for building html'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, config, datetime
import control.io as io
import view.log as log
import view.icon as icon
import view.translate as tr
import view.txt as view_txt
import knmi.view.fix as fix
import knmi.model.daydata as daydata

class Template():
    ''' Class to make a html page based on the template - template.html'''
    charset     = 'UTF-8'
    author      = 'WeatherstatsNL'
    viewport    = 'width=device-width, initial-scale=1.0, shrink-to-fit=no'
    script_file = './js/js.js'
    css_file    = './css/css.css'

    def __init__(self, title='WeatherstatsNL - template',
                       header='Your Title',
                       main='Your Content',
                       footer='Your Footer'
                       ):
        self.title  = title
        self.header = header
        self.main   = main
        self.footer = footer

        title = self.title.strip().replace(' ', '')
        dt    = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
        self.file_name = f'{title}_{dt}.html'

        self.template  = os.path.abspath(os.path.join(config.dir_html_templates, 'template.html'))
        self.base_dir  = os.path.dirname(os.path.abspath(__file__))
        self.file_dir  = config.dir_html_dayvalues
        self.file_path = os.path.abspath(os.path.join(self.file_dir, self.file_name))

    def save(self, dir_map=False, file_name=False):
        ok = False
        if file_name:
            self.file_name = file_name
        if dir_map:
            self.file_dir = dir_map

        self.file_path = os.path.abspath(os.path.join(self.file_dir, self.file_name))

        try:
            self.html, ok = io.read(self.template)
            if ok:
                self.html = self.html.format( str(datetime.datetime.now()),
                                self.title, self.charset, self.author,
                                self.viewport, self.css_file, self.script_file,
                                self.header, self.main, self.footer
                                )
                io.write( self.file_path, self.html )
        except Exception as e:
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
    stn, ymd, ddvec, fhvec, fg, fhx, fhxh, fhn, fhnh, fxx, fxxh, tg, tn,\
    tnh, tx, txh, t10n, t10nh, sq, sp, q, dr, rh, rhx, rhxh, pg, px, pxh,\
    pn, pnh, vvn, vvnh, vvx, vvxh, ng, ug, ux, uxh, un, unh, ev24 = ents(day)

    # Add icons
    if tx: tx = f'{icon.tx} {tx}'
    if tg: tg = f'{icon.tg} {tg}'
    if tn: tn = f'{icon.tn} {tn}'
    if t10n:  t10n = f'{icon.t10n} {t10n}'
    if ddvec: ddvec = f'{icon.arro} {ddvec}'
    if fhvec: fhvec = f'{icon.wind} {fhvec}'
    if fg:  fg  = f'{icon.wind} {fg}'
    if fhx: fhx = f'{icon.wind} {fhx}'
    if fhn: fhn = f'{icon.wind} {fhn}'
    if fxx: fxx = f'{icon.wind} {fxx}'
    if vvn: vvn = f'{icon.bino} {vvn}'
    if vvx: vvx = f'{icon.bino} {vvx}'
    if sq: sq = f'{icon.sun} {sq}'
    if sp: sp = f'{icon.sun} {sp}'
    if  q: q  = f'{icon.radi} {q}'
    if rh: rh = f'{icon.umbr} {rh}'
    if dr: dr = f'{icon.umbr} {dr}'
    if rhx: rhx = f'{icon.umbr} {rhx}'
    if ux: ux = f'{icon.drop} {ux}'
    if un: un = f'{icon.drop} {un}'
    if ug: ug = f'{icon.drop} {ug}'
    if ng: ng = f'{icon.clou} {ng}'
    if pg: pg = f'{icon.pres} {pg}'
    if pn: pn = f'{icon.pres} {pn}'
    if px: px = f'{icon.pres} {px}'
    if ev24: ev24 = f'{icon.swea} {ev24}'

    main  = ''
    main += div_ent( view_txt.ent_to_titel('TX'), tx, txh ) if tx else ''
    main += div_ent( view_txt.ent_to_titel('TG'), tg, False ) if tg else ''
    main += div_ent( view_txt.ent_to_titel('TN'), tn, tnh ) if tn else ''
    main += div_ent( view_txt.ent_to_titel('T10N'), t10n, t10nh ) if t10n else ''
    main += div_ent( view_txt.ent_to_titel('DDVEC'), ddvec, False ) if ddvec else ''
    main += div_ent( view_txt.ent_to_titel('FG'), fg, False ) if fg else ''
    main += div_ent( view_txt.ent_to_titel('RH'), rh, False ) if rh else ''
    main += div_ent( view_txt.ent_to_titel('SQ'), sq, False ) if sq else ''
    main += div_ent( view_txt.ent_to_titel('PG'), pg, False ) if pg else ''
    main += div_ent( view_txt.ent_to_titel('UG'), ug, False ) if ug else ''

    main += div_ent( view_txt.ent_to_titel('FXX'), fxx, fxxh ) if fxx else ''
    main += div_ent( view_txt.ent_to_titel('FHVEC'), fhvec, False ) if fhvec else ''
    main += div_ent( view_txt.ent_to_titel('FHX'), fhx, fhxh ) if fhx else ''
    main += div_ent( view_txt.ent_to_titel('FHN'), fhn, fhnh ) if fhn else ''
    main += div_ent( view_txt.ent_to_titel('SP'), sp, False ) if sp else ''
    main += div_ent( view_txt.ent_to_titel('Q'), q, False ) if q else ''
    main += div_ent( view_txt.ent_to_titel('DR'), dr, False ) if dr else ''
    main += div_ent( view_txt.ent_to_titel('RHX'), rhx, rhxh ) if rhx else ''
    main += div_ent( view_txt.ent_to_titel('PX'), px, pxh ) if px else ''
    main += div_ent( view_txt.ent_to_titel('PN'), pn, pnh ) if pn else ''

    main += div_ent( view_txt.ent_to_titel('VVN'), vvn, vvnh ) if vvn else ''
    main += div_ent( view_txt.ent_to_titel('VVX'), vvx, vvxh ) if vvx else ''
    main += div_ent( view_txt.ent_to_titel('NG'), ng, False ) if ng else ''
    main += div_ent( view_txt.ent_to_titel('UX'), ux, uxh ) if ux else ''
    main += div_ent( view_txt.ent_to_titel('UN'), un, unh ) if un else ''
    main += div_ent( view_txt.ent_to_titel('EV24'), ev24, False ) if ev24 else ''

    return main

def table_count(l, max):
    html = ''
    if l:
        if max is not 0:
            l.reverse() # Last count is last. Make first
            cnt = len(l)
            max = cnt if max == -1 else max # -1 for all!
            end = cnt if max > cnt else max # check bereik
            html += '<table class="popup">'
            html += '<thead><tr><th>datum</th><th>waarde</th><th>tijd</th>'
            html += '<th>eis</th><th>aantal</th></tr></thead>'
            html += '<tbody>'

            for e in l[:end]:
                sdt = d.Datum(e.datum).tekst()
                val = fn.rm_s( fn.fix( e.waarde, e.ent ) )
                t_ent = knmi.ent_to_t_ent( e.ent )
                eis = fn.div_10(e.eis)
                tme = fn.rm_s(fn.fix(e.tijd, t_ent)) if t_ent is not False else '.'
                html += f'<tr><td title="{sdt}">{e.datum}</td><td>{val}</td>'\
                        f'<td>{tme}</td><td>{e.oper}{eis}</td><td>{e.tel}</td></tr>'

            html += '</tbody>'
            html += '</table>'

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
