# -*- coding: utf-8 -*-
""" Calculates weather statistics for dutch cities from knmi data
    @Execute:    $ python weerstats.py (3.7)
    @Author:     Mark Zwaving
    @License:    Creative Commons Attribution 4.0 International Public License
"""
#--------------------------------------------------------------------------------
# import libraries
import config as c, fn_menu as menu, ask as a, testing

# Hoofdprogramma
if __name__== "__main__":
    print(f"{c.ln}Welcome to WeatherStats NL...")
    if not c.lijst_stations:
        print('''
        No weatherstations found !
        Add one or more weatherstation(s) in config.py.
        Press a key to quit...
        ''')
        input(' ')
    else:
        # Main menu
        while True:
            print( f'''
            MAIN MENU EDIT

            Choose one of the following options:
                1: Download data all knmi stations
                2: Download data one or more knmi station(s)
                3: Get weather day values of a day
                4: Calculate summer statistics
                5: Calculate heatwaves
                6: Calculate winter statistics

                Press 'q' to quit...
            ''')
            choice = a.ask(' ? ')  # Make a choice

            if choice == '1':  menu.download_etmgeg_all_stations()
            if choice == '2':  menu.download_etmgeg_station()
            if choice == '3':  menu.get_dayvalues()
            if choice == '4':  menu.calc_zomerstats()
            if choice == '5':  menu.calc_heat_waves()
            if choice == '6':  menu.calc_winterstats()
            if choice == 'q':  break

    print(f'{c.ln}Good bye{c.ln}')
