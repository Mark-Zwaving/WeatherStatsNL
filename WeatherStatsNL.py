# -*- coding: utf-8 -*-
'''WeatherStatsNL calculates weather statistics for dutch cities
from the data from the knmi'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

# import libraries
import config as c, fn_menu as menu, translate as t, ask as a

# Main programm
if __name__== "__main__":
    print( f"{c.ln} {t.tr('Welcome to WeatherStatsNL')}")
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
