import config as c, write as w, fn, check, ask as a
#--------------------------------------------------------------------------------
def ask(s):
    s = fn.san(input(s))
    print(' ')
    return s
#--------------------------------------------------------------------------------
def ask_stations( txt ):
    l = []
    while True:
        print(txt)
        w.write_stations(c.lijst_stations, 4, 25)
        print(c.tab + 'Voor één station: geef het wmonummer of een plaatsnaam '
                      'van een weerstation')
        print(c.tab + 'Voor meerdere stations: geef het wmonummer of plaatsnaam '
                      'gescheiden door een komma')
        print(c.tab + "Toets een '*' voor het toevoegen van alle stations" )
        if len(l) > 0: print(c.tab + "KIES 'd' om door te gaan !")
        print(c.ln + "Druk op 'q' om terug te keren naar het hoofdmenu")
        s_ask = ask(' ? ')

        if not s_ask: # Waarschijnlijk op de enter geramd zonder invoer...
            continue # Nog een een keer dan maar
        elif s_ask == c.stop:
            return c.stop
        elif s_ask == '*':
            l = c.lijst_stations
        elif s_ask == 'd' and len(l) > 0:
            return l
        else:
            lt = []
            if s_ask.find(',') != -1:
                lt = s_ask.split(',')
            else:
                lt.append(s_ask)
            for s_in in lt:
                station = fn.search_station(s_in.strip())
                if station != False:
                    s_info = station.wmo+' ' +station.plaats
                    if not fn.is_station_in_list(station, l):
                        l.append(station)
                        print(f"Station: '{s_info}' toegevoegd...")
                    else:
                        print(f"Station: '{s_info}' was al toegevoegd...")
                else:
                    print(f"Station: '{s_in}' niet gevonden...")

        if len(l) == len(c.lijst_stations):
            print('Alle beschikbare stations zijn toegevoegd...')
            break
        elif len(l) > 0:
            print(c.ln + 'Alle station(s) die zijn toegevoegd zijn:')
            w.write_stations(l, 8)

    return l
#--------------------------------------------------------------------------------
def ask_date( txt ):
    while True:
        print("Druk op 'q' om terug te keren naar het hoofdmenu")
        print(txt)
        s_in = ask(' ? ')
        if s_in == c.stop:
            return c.stop
        elif check.check_date(s_in):
            return s_in
        else:
            print(f"Fout in datum: '{s_in}'. Probeer opnieuw...")
#--------------------------------------------------------------------------------
def ask_start_and_end_date():
    start = ask_date("Geef startdatum [yyyymmdd] ? ")
    if start == c.stop: return c.stop
    einde = ask_date("Geef einddatum [yyyymmdd] ?")
    if einde == c.stop: return c.stop

    if int(start) > int(einde): # Keer om
        mem = start; start = einde; einde = mem

    return { 'start': start, 'einde': einde }
#--------------------------------------------------------------------------------
def ask_file_type(txt):
    s_in = False
    while True:
        print(txt)
        print(c.tab + "Druk op 'q' om terug te keren naar het hoofdmenu")
        print(c.tab + "Kies: 'txt' voor een tekstbestand of "
              "'html' voor een htmlbestand ?")
        s_in = ask(' ? ')
        if s_in == c.stop:
            return c.stop
        elif s_in == 'txt' or s_in == 'html':
            break

    return s_in
#--------------------------------------------------------------------------------
def ask_file_naam(txt):
    s_in = False
    print(txt)
    print(c.tab + "Druk op 'q' om terug te keren naar het hoofdmenu")
    print(c.tab + "Druk op <enter> om geen naam op te geven")
    s_in = ask(' ? ')
    return s_in
#--------------------------------------------------------------------------------
def ask_enter_menu():
    print(' ')
    input('Druk <enter> om terug te keren naar het hoofdmenu')
    print(' ')
