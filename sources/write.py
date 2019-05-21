import config as c, math, time, fn_html as h
#--------------------------------------------------------------------------------
def write_to_file(file_name, content):
    '''Functie schrijft gegevens naar een bestand'''
    oke = False
    try:
        with open(file_name, 'w', encoding='utf-8') as file_out:
            file_out.write(content)
    except IOError as e:
        if c.log:
            print(f"Schrijven gegevens naar bestand '{file_name}' is mislukt."
                  f"{c.ln}{e.strerror}{c.ln}{e.errno}")
    else:
        print(f"Schrijven van gegevens naar bestand '{file_name}' is gelukt!")
        oke = True

    return oke
#--------------------------------------------------------------------------------
def write_zero_less_ten ( d ):
    '''Functie voegt een leading zero toe, mits nodig'''
    return '0' + str(d) if d < 10 else str(d)

def write_spaces_till( s, end ):
    '''Functie vult een string aan met spaties tot een bepaalde aantal'''
    return s + ' ' * (end-len(s))

def write_stations(lijst, kol = 4, kol_width = ','):
    '''Functie schrijft een lijst met beschikbare stations naar het scherm'''
    content, cnt = '', len(lijst)
    for i in range(cnt):
        station = lijst[i]
        if kol_width != ',':
            content += f"{station.wmo + ' ' + station.plaats:{kol_width}}"
            if (i+1) == cnt:
                content += c.ln
            elif (i+1) % kol == 0:
                content += c.ln
        else:
            content += f"{station.wmo} {station.plaats}"
            if (i+1) == cnt:
                content += c.ln
            elif (i+1) % kol == 0:
                content += ', ' + c.ln
            else:
                content += ', '

    print(content)
#--------------------------------------------------------------------------------
def write_process_time_ns(txt_in, start_ns):
    '''Functie berekent de rekentijd in nanoseconden! vanaf een starttijd'''
    dag_sec, uur_sec, min_sec = 86400, 3600, 60
    delta_ns  = time.time_ns() - start_ns
    delta_sec = delta_ns / 1000000000

    if c.log: print(f'Nano seconds: {delta_ns}')

    rest, seco = math.modf( delta_sec )
    rest, mill = math.modf( rest * 1000 )
    rest, micr = math.modf( rest * 1000 )
    mill, micr, nano = int(mill), int(micr), int(rest * 1000)

    # Calculate from seconds
    dag, rest_sec = int(seco // dag_sec), seco % dag_sec
    uur, rest_sec = int(rest_sec // uur_sec), rest_sec % uur_sec
    min, sec = int(rest_sec // min_sec), int(rest_sec % min_sec)

    # Maak uitvoer. Geef een lege string bij 0. Anders kijk voor enkelvoud of meervoudige tekst
    dag_txt = f"{dag} {'dagen'    if dag > 1 else 'dag'} "
    uur_txt = f"{uur} {'uren'     if uur > 1 else 'uur'} "
    min_txt = f"{min} {'minuten'  if min > 1 else 'minuut'} "
    sec_txt = f"{sec} {'seconden' if sec > 1 else 'seconde'} "
    mil_txt = f"{mill} {'milliseconden' if mill > 1 else 'milliseconde'} "
    mic_txt = f"{micr} {'microseconden' if micr > 1 else 'microseconde'} "
    nan_txt = f"{nano} {'nanoseconden'  if nano > 1 else 'nanoseconde'} "

    txt = ''
    if dag  > 0: txt += dag_txt
    if uur  > 0: txt += uur_txt
    if min  > 0: txt += min_txt
    if sec  > 0: txt += sec_txt
    if mill > 0: txt += mil_txt
    if micr > 0: txt += mic_txt
    if nano > 0: txt += nan_txt

    print(f'{txt_in}{txt}')

#--------------------------------------------------------------------------------
def write_process_time_s( txt_start, start_ns ):
    print(f"{txt_start}{(time.time_ns() - start_ns) / 1000000000:.4f} seconden")
#--------------------------------------------------------------------------------
def write_html_count(l, tel, n, ad):
    html = str(tel)
    # Add table html if count != 0
    if tel is not 0:
        html += h.table_count(l, n, ad)
    return html
#--------------------------------------------------------------------------------
def write_html_extremes(l, tel, n, ad):
    html = str(tel)
    # Add table html if count != 0
    if tel is not 0:
        html += h.table_extremes(l, n, ad)
    return html
