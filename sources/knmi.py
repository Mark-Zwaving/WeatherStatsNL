# -*- coding: utf-8 -*-
'''Library contains classes to store knmi data'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, config as c, fn

class Station:
    '''Deze klasse initialiseert een knmi weerstation'''
    def __init__(self, wmo = '', plaats = '', provincie = '', info = ''):
        self.wmo, self.plaats, self.provincie, self.info = wmo, plaats, provincie, info

        self.dir_knmi = fn.mk_path(c.dir_app, 'knmi')
        self.dir_data = fn.mk_path(self.dir_knmi, 'data')
        self.dir_text = fn.mk_path(self.dir_knmi, 'text')
        self.dir_html = fn.mk_path(self.dir_knmi, 'html')
        self.file_etmgeg_zip = fn.mk_path(self.dir_data, f'etmgeg_{self.wmo}.zip')
        self.file_etmgeg_txt = fn.mk_path(self.dir_data, f'etmgeg_{self.wmo}.txt')

        self.url_etmgeg_base = r'https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_{0}.zip'
        self.url_etmgeg  = self.url_etmgeg_base.format(self.wmo)

        self.bronvermelding = 'BRON: KONINKLIJK NEDERLANDS METEOROLOGISCH INSTITUUT (KNMI)'
        self.empthy, self.skip_lines = '     ', 49

        # Check of alle directories voor de knmi gegevens zijn aangemaakt, zoniet maak ze
        for dir in [self.dir_knmi, self.dir_data, self.dir_text, self.dir_html]:
            if not os.path.exists(dir):
                os.makedirs(dir)

class Etmgeg:
    '''Klasse voor het opslaan van de daggevens van een knmi station'''
    def __init__(self, knmi_data_line):
        self.STN,  self.YYYYMMDD, self.DDVEC, self.FHVEC, self.FG,   \
        self.FHX,  self.FHXH,     self.FHN,   self.FHNH,  self.FXX,  \
        self.FXXH, self.TG,       self.TN,    self.TNH,   self.TX,   \
        self.TXH,  self.T10N,     self.T10NH, self.SQ,    self.SP,   \
        self.Q,    self.DR,       self.RH,    self.RHX,   self.RHXH, \
        self.PG,   self.PX,       self.PXH,   self.PN,    self.PNH,  \
        self.VVN,  self.VVNH,     self.VVX,   self.VVXH,  self.NG,   \
        self.UG,   self.UX,       self.UXH,   self.UN,    self.UNH,  \
        self.EV24 = knmi_data_line.split(",")
        self.empthy = '     '
