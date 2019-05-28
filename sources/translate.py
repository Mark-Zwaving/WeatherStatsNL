# -*- coding: utf-8 -*-
'''Library made to translate text from English into one or more other languages'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.2"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config as cfg

class Languages:
    def __init__(self, EN, NL):
        self.lang = cfg.language.lower()
        self.default = EN
        self.EN = EN
        self.NL = NL

    def search(self, s):
        if s == self.EN:
            return True
        elif s == self.NL:
            return True

        return False

    def get(self):
        if self.lang == 'en':
            return self.EN
        elif self.lang == 'nl':
            return self.NL

        return self.default

translate_pool = [
    Languages('Good bye', 'Tot ziens'),
    Languages('Welcome to WeatherStats NL', 'Welkom bij WeerStats NL'),
    Languages('No weatherstations found !', 'Geen weerstations gevonden !'),
    Languages('Add one or more weatherstations in config.py', 'Voeg één of meer weerstations toe in config.py'),
    Languages('Press a key to quit...', 'Druk op een toets om af te sluiten...'),
    Languages('MAIN MENU', 'HOOFDMENU'),
    Languages('Choose one of the following options:', 'Maak een keus uit de volgende opties:'),
    Languages('Download data all knmi stations', 'Download de gegevens van alle knmi stations'),
    Languages('Download data of one or more knmi stations', 'Download de gegevens van één of meerdere knmi stations'),
    Languages('Get weather day values of a day', 'Verkrijg de weergegevens van één dag'),
    Languages('Calculate summer statistics', 'Bereken zomerstatistieken'),
    Languages('Calculate heatwaves', 'Bereken hittegolven'),
    Languages('Calculate winter statistics', 'Bereken winterstatistieken'),
    Languages("Press 'q' to quit...", "Druk op 'q' om af te sluiten")
]

def tr(s):
    for l in translate_pool:
        oke = l.search(s)
        if oke:
            return l.get()

    return s
