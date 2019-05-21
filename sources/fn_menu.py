import time, fn, config as c, download as d, write as w, ask as a
import zomerstats as zs, winterstats as ws, hittestats as hs

# Menu choice 1
def download_etmgeg_all_stations():
    '''Functie downloadt (en unzipt) alle knmi stations in de lijst'''
    print(c.line + c.ln + 'DOWNLOADEN DAGGEGEVENS...')
    start_ns = time.time_ns()
    for station in c.lijst_stations:
        d.download_and_unzip_etmgeg_station ( station )
    w.write_process_time_ns('Totale rekentijd is: ', start_ns)
    print(c.ln + 'EINDE DOWNLOADEN VAN DAGGEGEVENS...' + c.ln + c.line)
    a.ask_enter_menu()

# Menu choice 2
def download_etmgeg_station():
    '''Functie vraagt eerst om één of meerdere stations en downloadt ze daarna '''
    print(c.line + c.ln + 'DOWNLOAD DAGGEGEVENS...')
    l = a.ask_stations('Voer één of meerdere stations in om te downloaden' )
    if l != c.stop:
        start_ns = time.time_ns()
        print(c.ln + c.line + c.ln + 'DOWNLOAD GESTART...' + c.ln)
        for station in l:
            print(f"Downloading station: {station.wmo} {station.plaats}")
            d.download_and_unzip_etmgeg_station ( station )
    w.write_process_time_ns('Totale rekentijd is: ', start_ns)
    print(c.ln + 'EINDE DOWNLOAD DAGGEGEVENS...' + c.ln + c.line)
    a.ask_enter_menu()

# Menu choice
def calc_winterstats():
    '''Functie regelt berekeningen voor de winterstats'''
    print(c.line + c.ln + 'BEREKENEN WINTERSTATISTIEKEN...' + c.ln)
    # Vraag start en eind datum
    dates = a.ask_start_and_end_date()
    if dates != c.stop:
        # Vraag stationlijst
        l = a.ask_stations('Voeg één of meerdere stations toe voor de berekeningen van de winterstatitieken')
        if l != c.stop:
            # Vraag uitvoer bestandstype
            print(c.ln + c.line + c.ln + 'SELECTEER BESTANDSTYPE' + c.ln)
            type = a.ask_file_type('Kies het bestandstype voor het opslaan van de winterstatistieken')
            print('EINDE SELECTEER BESTANDSTYPE' + c.ln + c.line + c.ln)
            if type != c.stop:
                # Bereken winterstats
                start_ns, start_d, einde_d = time.time_ns(), dates['start'], dates['einde']
                ws.alg_winterstats(l, start_d, einde_d, type)
                w.write_process_time_ns('Totale rekentijd is: ', start_ns)


    print('EINDE BEREKENEN WINTERSTATISTIEKEN...' + c.ln + c.line)
    a.ask_enter_menu()

# Menu choice
def calc_zomerstats():
    print(c.line + c.ln + 'BEREKEN ZOMERSTATISTIEKEN...')
    # Vraag start en eind datum
    dates = a.ask_start_and_end_date()
    if dates != c.stop:
        # Vraag stationlijst
        l = a.ask_stations('Voeg één of meerdere stations toe voor de berekening van de zomerstatistieken')
        if l != c.stop:
            # Vraag uitvoer bestandstype
            print(c.ln + c.line + c.ln + 'SELECTEER BESTANDSTYPE' + c.ln)
            type = a.ask_file_type('Kies het bestandstype voor het opslaan van de zomerstatistieken')
            print('EINDE SELECTEER BESTANDSTYPE' + c.ln + c.line + c.ln)
            if type != c.stop:
                # Bereken zomerstats
                start_ns, start_d, einde_d = time.time_ns(), dates['start'], dates['einde']
                zs.alg_zomerstats(l, start_d, einde_d, type)
                w.write_process_time_ns('Totale rekentijd is: ', start_ns)
    print('EINDE BEREKENEN ZOMERSTATISTIEKEN...' + c.ln + c.line)
    a.ask_enter_menu()

# Menu choice
def calc_heat_waves():
    print(c.line + c.ln + 'BEREKEN HITTEGOLVEN...')
    # Vraag start en eind datum
    dates = a.ask_start_and_end_date()
    if dates != c.stop:
        # Vraag stationlijst
        l = a.ask_stations('Voeg één of meerdere stations toe voor de berekening van de hittegolven')
        if l != c.stop:
            # Vraag uitvoer bestandstype
            print(c.ln + c.line + c.ln + 'SELECTEER BESTANDSTYPE' + c.ln)
            type = a.ask_file_type('Kies het bestandstype voor het opslaan van de hittegolven')
            print('EINDE SELECTEER BESTANDSTYPE' + c.ln + c.line + c.ln)
            if type != c.stop:
                # Geef bestandsnaam
                print(c.ln + c.line + c.ln + 'GEEF BESTANDSNAAM' + c.ln)
                name = a.ask_file_naam('Geef een naam voor het bestand <optioneel>')
                print('EINDE GEEF BESTANDSNAAM' + c.ln + c.line + c.ln)
                if name != c.stop:
                    # Bereken hittegolven
                    start_ns, start_d, einde_d = time.time_ns(), dates['start'], dates['einde']
                    hs.gen_calc_heat_waves(l, start_d, einde_d, type, name)
                    w.write_process_time_ns('Totale rekentijd is: ', start_ns)
    print('EINDE BEREKENEN HITTEGOLVEN...' + c.ln + c.line)
    a.ask_enter_menu()
