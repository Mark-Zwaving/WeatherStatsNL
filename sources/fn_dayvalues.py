import os, threading, urllib, urllib.request, urllib.error, zipfile
import config as c, knmi, write as w, fn, fn_html
import datetime, time, math, locale, datum

def get_list_day_values_by_station( station ):
    l, name = [], station.file_etmgeg_txt
    try:
        with open(name, 'r') as f:
            l = f.readlines()
    except IOError as e:
        if c.log:
            s = f"Read data from file: '{name}' failed"
            s += "{c.ln}{e.reason}{c.ln}{e.strerror}"
            print(s)
    else:
        if c.log:
            print(f"Read data from file: '{name}' done!")

        l = l[station.skip_lines:] # Only real data in list

    return l

def get_string_day_values_by_station_and_date( station, yyyymmdd ):
    '''Function: gets the weatherdata from a station at a given date'''
    result, oke, lock_read = '', False, threading.Lock()
    with lock_read:
        wmo_name, f_name = f'{station.wmo} {station.plaats}', station.file_etmgeg_txt
        l = get_list_day_values_by_station(station)
        if l:
            for day in l:
                if day[6:14] == yyyymmdd:
                    result = day
                    if c.log:
                        print(f"Read data station: {wmo_name} from date: {yyyymmdd} succes!")
                    break
        else:
            if c.log:
                print(f"Read data station: {wmo_name} failed")
                print(f"Filename:'{f_name}'")

    return result

def prepare_day_values( l_stations, yyyymmdd, name, type ):
    station = l_stations[0]
    dayvalues = get_string_day_values_by_station_and_date( station, yyyymmdd )

    print(f'>>>>>> {dayvalues}')

    # Prepare name
    if not name:
        name = f'{station.wmo}-{yyyymmdd}'

    if type == 'html':
        name = f'{name}.html'
        path = station.dir_html
    elif type == 'txt':
        name = f'{name}.txt'
        path = station.dir_text

    file_name = fn.mk_path(path, name)

    content = ''
    if dayvalues is not '':
        d = knmi.Etmgeg(dayvalues)

        if type == 'html':
            title = f'{station.plaats}-{yyyymmdd}'
            css  = '''
            <style>
                #container {
                    grid-template-columns: repeat(3, 1fr);
                    grid-gap: 10px;
                    grid-auto-rows: minmax(100px, auto);
                }
            </style>
            '''

            header = f'''
            <header>
                <h3> {station.wmo} - {station.plaats} - {station.provincie} </h3>
                <h4> {datum.Datum(d.YYYYMMDD).tekst()} </h4>
            </header>
            '''

            data = '<div id="container">'
            if d.DDVEC is not d.empthy: data += f'<div id="ddvec"> {fn.fix(d.DDVEC,"DDVEC")} </div>'
            if d.FHVEC is not d.empthy: data += f'<div id="fhvec"> {fn.fix(d.FHVEC,"FHVEC")} </div>'
            if d.FG    is not d.empthy: data += f'<div id="fg"> {fn.fix(d.FG,"FG")} </div>'
            if d.FHX   is not d.empthy: data += f'<div id="fhx"> {fn.fix(d.FHX,"FHX")} </div>'
            if d.FHXH  is not d.empthy: data += f'<div id="fhxh"> {fn.fix(d.FHXH,"FHXH")} </div>'
            if d.FHN   is not d.empthy: data += f'<div id="fhn"> {fn.fix(d.FHN,"FHN")} </div>'
            if d.FHNH  is not d.empthy: data += f'<div id="fhnh"> {fn.fix(d.FHNH,"FHNH")} </div>'
            if d.FXX   is not d.empthy: data += f'<div id="fxx"> {fn.fix(d.FXX,"FXX")} </div>'
            if d.FXXH  is not d.empthy: data += f'<div id="fxxh"> {fn.fix(d.FXXH,"FXXH")} </div>'
            if d.TG    is not d.empthy: data += f'<div id="tg"> {fn.fix(d.TG,"TG")} </div>'
            if d.TN    is not d.empthy: data += f'<div id="tn"> {fn.fix(d.TN,"TN")} </div>'
            if d.TNH   is not d.empthy: data += f'<div id="tnh"> {fn.fix(d.TNH,"TNH")} </div>'
            if d.TX    is not d.empthy: data += f'<div id="tx"> {fn.fix(d.TX,"TX")} </div>'
            if d.TXH   is not d.empthy: data += f'<div id="txh"> {fn.fix(d.TXH,"TXH")} </div>'
            if d.T10N  is not d.empthy: data += f'<div id="t10n"> {fn.fix(d.T10N,"T10N")} </div>'
            if d.T10NH is not d.empthy: data += f'<div id="t10nh"> {fn.fix(d.T10NH,"T10NH")} </div>'
            if d.SQ    is not d.empthy: data += f'<div id="sq"> {fn.fix(d.SQ,"SQ")} </div>'
            if d.SP    is not d.empthy: data += f'<div id="sp"> {fn.fix(d.SP,"SP")} </div>'
            if d.Q     is not d.empthy: data += f'<div id="q"> {fn.fix(d.Q,"Q")} </div>'
            if d.DR    is not d.empthy: data += f'<div id="dr"> {fn.fix(d.DR,"DR")} </div>'
            if d.RH    is not d.empthy: data += f'<div id="rh"> {fn.fix(d.RH,"RH")} </div>'
            if d.RHX   is not d.empthy: data += f'<div id="rhx"> {fn.fix(d.RHX,"RHX")} </div>'
            if d.RHXH  is not d.empthy: data += f'<div id="rhxh"> {fn.fix(d.RHXH,"RHXH")} </div>'
            if d.PG    is not d.empthy: data += f'<div id="pg"> {fn.fix(d.PG,"PG")} </div>'
            if d.PX    is not d.empthy: data += f'<div id="px"> {fn.fix(d.PX,"PX")} </div>'
            if d.PXH   is not d.empthy: data += f'<div id="pxh"> {fn.fix(d.PXH,"PXH")} </div>'
            if d.PN    is not d.empthy: data += f'<div id="pn"> {fn.fix(d.PN,"PXH")} </div>'
            if d.PNH   is not d.empthy: data += f'<div id="pnh"> {fn.fix(d.PNH,"PNH")} </div>'
            if d.VVN   is not d.empthy: data += f'<div id="vvn"> {fn.fix(d.VVN,"VVN")} </div>'
            if d.VVNH  is not d.empthy: data += f'<div id="vvnh"> {fn.fix(d.VVNH,"VVNH")} </div>'
            if d.VVX   is not d.empthy: data += f'<div id="vvx"> {fn.fix(d.VVX,"VVX")} </div>'
            if d.VVXH  is not d.empthy: data += f'<div id="vvxh"> {fn.fix(d.VVXH,"VVXH")} </div>'
            if d.NG    is not d.empthy: data += f'<div id="ng"> {fn.fix(d.NG,"NG")} </div>'
            if d.UG    is not d.empthy: data += f'<div id="ug"> {fn.fix(d.UG,"UG")} </div>'
            if d.UX    is not d.empthy: data += f'<div id="ux"> {fn.fix(d.UX,"UX")} </div>'
            if d.UXH   is not d.empthy: data += f'<div id="uxh"> {fn.fix(d.UXH,"UXH")} </div>'
            if d.UN    is not d.empthy: data += f'<div id="un"> {fn.fix(d.UN,"UN")} </div>'
            if d.UNH   is not d.empthy: data += f'<div id="unh"> {fn.fix(d.UNH,"UNH")} </div>'
            if d.EV24  is not d.empthy: data += f'<div id="ev24"> {fn.fix(d.EV24,"EV24")} </div>'

            data += '</div>'
            footer = f'''
                <footer>
                    {station.bronvermelding}
                </footer>
            '''

            data = header + data + footer
            content = fn_html.pagina(title, css, data)

        if type == 'txt':
            content = 'TODO'

    if type == 'txt':
        print(cfg.line + cfg.ln + content + cfg.ln + cfg.line)

    w.write_to_file(file_name, content) # Write to file
