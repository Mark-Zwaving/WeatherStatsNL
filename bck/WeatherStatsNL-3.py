# -*- coding: utf-8 -*-
'''WeatherStatsNL calculates weather statistics for dutch cities
from the data from the knmi'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.5"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os

# Import libraries
import config
import knmi.model.daydata as daydata
import knmi.model.stats as stats
import knmi.control.menu as control_menu
import knmi.view.menu as view_menu
import view.log as log
import knmi.view.fix as fix

# Main programm
if __name__== "__main__":

    log.header('Welcome to WeatherStatsNL', True)
    if config.stations.size == 0:
        view_menu.error_no_stations_found()
    else:
<<<<<<< Updated upstream
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
=======
        while True:  # Main menu
            choice = view_menu.main_menu()
            if choice in config.answer_quit:
                break
            else:
                control_menu.menu_choices( choice )

    log.footer('Good bye', True )

    # ok, data = daydata.read( '280' )
    # if ok:
    #     data = stats.period( data, 20200401, 20200430 )
    #     sel = stats.extended_terms_days( data, 'TX > 20' )
    #
    #     ave  = stats.average( data, 'TX' )
    #     som  = stats.sum( data, 'RH' )
    #
    #     print(f'Som neerslag:  {som}')
    #     print(f'Gemiddelde TX: {ave}')

    # log.console('MAIN MENU')
    #
    # sd, ed = 20200401, 20200430
    #
    # ok, data = daydata.read( '280' )
    # data = stats.period( data, sd, ed )
    #
    # max = fix.ent(stats.max( data, 'TX' ), 'TX')
    # min = fix.ent(stats.min( data, 'TN' ), 'TN')
    # ave = fix.ent(stats.average( data, 'TG' ), 'TG')
    # som = fix.ent(stats.sum( data, 'RH' ), 'RH')
    #
    # log.console( f'Maximum TX: {max}' )
    # log.console( f'Minimum TN: {min}' )
    # log.console( f'Average TG: {ave}' )
    # log.console( f'Rainsum RH: {som}' )

    # print('dir_app', config.dir_app)
    # print('dir_data', config.dir_data)
    # print('dir_knmi', config.dir_knmi)
    # print('file_zip', daydata.file_zip)
    # print('file_txt', daydata.file_txt)
    # print('data_url', daydata.data_url)
    # print('data_source', daydata.data_source)
    # print('data_skip_rows', daydata.data_skip_rows)
    # print('data_dummy_val', daydata.data_dummy_val)
    # input('?')
>>>>>>> Stashed changes
