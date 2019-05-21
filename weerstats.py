# -*- coding: utf-8 -*-
""" Berekent weerstatistieken van Nederlands KNMI stations
    @Uitvoer:    $ python weerstats.py (3.7)
    @Author:     Mark Zwaving
    @license:    Creative Commons Attribution 4.0 International Public License
"""
#--------------------------------------------------------------------------------
# import libraries
import config as c, fn_menu as menu, ask as a, testing

# Hoofdprogramma
if __name__== "__main__":
    print("Welkom bij weerstats...")
    if not c.lijst_stations:
        print('Geen weerstations gevonden in de lijst')
        print('Zie ook config.py ...')
        input('Druk een toets om af te sluiten...')
    else:
        # Main menu
        while True:
            print(c.line)
            print('HOOFDMENU')
            print('Maak een keus uit de volgende opties:')
            n  = 1;  print(f'{c.tab}{n}: Download daggegevens van alle knmi stations')
            n += 1;  print(f'{c.tab}{n}: Download daggegevens van één knmi station')
            # n += 1;  print(f'{c.tab}{n}: Geef dagwaarden')
            n += 1;  print(f'{c.tab}{n}: Bereken zomerstatistieken')
            n += 1;  print(f'{c.tab}{n}: Bereken hittegolven')
            n += 1;  print(f'{c.tab}{n}: Bereken winterstatistieken')
            #n += 1;  print(f'{c.tab}{n}: Bereken koudegolven')
            #print(c.tab+'9: Testing')
            print("Druk op 'q' om af te sluiten...")
            print(c.line)

            choice = a.ask(' ? ')  # Geef keuze op

            n  = 1
            if choice == str(n):  menu.download_etmgeg_all_stations()
            n += 1
            if choice == str(n):  menu.download_etmgeg_station()
            #n += 1
            #if choice == str(n):  menu.get_dagwaarden()
            n += 1
            if choice == str(n):  menu.calc_zomerstats()
            n += 1
            if choice == str(n):  menu.calc_heat_waves()
            n += 1
            if choice == str(n):  menu.calc_winterstats()
            #n += 1
            #if choice == str(n):  menu.valc_coldwaves()

            #if choice == '9':  testing.unzip_test()
            if choice == 'q':  break

    print(c.ln + 'Tot ziens')
