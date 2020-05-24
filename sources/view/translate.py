# -*- coding: utf-8 -*-
'''Library made to translate text from English into one or more other languages'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.3"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config
import numpy as np

pool = np.array( [
    ['Welcome', 'Welkom'],
    ['Good bye', 'Tot ziens'],
    ['Welcome to WeatherStats NL', 'Welkom bij WeerStats NL'],
    ['No weatherstations found !', 'Geen weerstations gevonden !'],
    ['Add one or more weatherstations in config.py', 'Voeg één of meer weerstations toe in config.py'],
    ['Press a key...', 'Druk op een toets...'],
    ['Press a key to quit...', 'Druk op een toets om af te sluiten...'],
    ['MAIN MENU', 'HOOFDMENU'],
    ['Choose one of the following options:', 'Maak een keus uit de volgende opties:'],
    ['Download data all knmi stations', 'Download de gegevens van alle knmi stations'],
    ['Download data of one or more knmi stations', 'Download de gegevens van één of meerdere knmi stations'],
    ['Get weather day values of a day', 'Verkrijg de weergegevens van één dag'],
    ['Calculate summer statistics', 'Bereken zomerstatistieken'],
    ['Calculate heatwaves', 'Bereken hittegolven'],
    ['Calculate winter statistics', 'Bereken winterstatistieken'],
    ["Press 'q' to quit...", "Druk op 'q' om af te sluiten"]
] )

def t(txt):
    '''Function translates text from English to other languages'''
    if config.translate:
        ndx, sl = 0, txt.lower()
        if config.language == 'NL': # Dutch
            ndx = 1

        # Search in pool
        for tr_line in pool:
            for sentence in tr_line:
                if sentence.lower() == sl:
                    return tr_line[ndx] # return correct language

    # Nothing found or translation not activated
    return txt

def txt(txt):
    return t(txt)
