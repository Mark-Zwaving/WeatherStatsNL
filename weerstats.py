# -*- coding: utf-8 -*-
""" Calculates weatherstatistics for dutch cities from knmi data
    @Execute:    $ python weerstats.py (3.7)
    @Author:     Mark Zwaving
    @License:    Creative Commons Attribution 4.0 International Public License
"""
#--------------------------------------------------------------------------------
# import libraries
import config as c, fn_menu as menu, ask as a, testing

# Hoofdprogramma
if __name__== "__main__":
    print("Welcome to weatherstats NL...")
    if not c.lijst_stations:
        print('No weatherstations found !')
        print('Add a weatherstation in config.py ...')
        input('Press a key to quit...')
    else:
        # Main menu
        while True:
            print(c.line)
            print('MAIN MENU')
            print('Choose one of the following options:')
            n  = 1;  print(f'{c.tab}{n}: Download data of all knmi stations')
            n += 1;  print(f'{c.tab}{n}: Download data of one knmi station')
            # n += 1;  print(f'{c.tab}{n}: Geef dagwaarden')
            n += 1;  print(f'{c.tab}{n}: Calculate summerstatistics')
            n += 1;  print(f'{c.tab}{n}: Calculate heatwaves')
            n += 1;  print(f'{c.tab}{n}: Calculate winterstatistics')
            #n += 1;  print(f'{c.tab}{n}: Bereken koudegolven')
            #print(c.tab+'9: Testing')
            print("Press 'q' to quit...")
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

    print(c.ln + 'Good bye')
