# -*- coding: utf-8 -*-
""" Calculates weather statistics for dutch cities from knmi data
    @Execute:    $ python weerstats.py (3.7)
    @Author:     Mark Zwaving
    @License:    Creative Commons Attribution 4.0 International Public License
"""
#--------------------------------------------------------------------------------
# import libraries
import config as c, fn_menu as menu, ask as a, testing
import translate as t

# Hoofdprogramma
if __name__== "__main__":
    print(f"{c.ln}{t.tr('Welcome to WeatherStats NL')}")
    if not c.lijst_stations:
        print('''
        {t.tr('No weatherstations found !')}
        {t.tr('Add one or more weatherstations in config.py')}
        {t.tr('Press a key to quit...')}
        ''')
        input(' ')
    else:
        # Main menu
        while True:
            print( f'''
            {t.tr('MAIN MENU')}

            {t.tr('Choose one of the following options:')}
                1: {t.tr('Download data all knmi stations')}
                2: {t.tr('Download data of one or more knmi stations')}
                3: {t.tr('Get weather day values of a day')}
                4: {t.tr('Calculate summer statistics')}
                5: {t.tr('Calculate heatwaves')}
                6: {t.tr('Calculate winter statistics')}

                {t.tr("Press 'q' to quit...")}
            ''')
            choice = a.ask(' ? ')  # Make a choice

            if choice == '1':  menu.download_etmgeg_all_stations()
            if choice == '2':  menu.download_etmgeg_station()
            if choice == '3':  menu.get_dayvalues()
            if choice == '4':  menu.calc_zomerstats()
            if choice == '5':  menu.calc_heat_waves()
            if choice == '6':  menu.calc_winterstats()
            if choice == 'q':  break


    print(f"{c.ln}{t.tr('Good bye')}{c.ln}")
