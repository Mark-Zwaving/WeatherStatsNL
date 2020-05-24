# -*- coding: utf-8 -*-
'''Library contains classes to store knmi data'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, pathlib, config

class Station:
    '''Class defines a KNMI weatherstation'''
    def __init__(self, wmo = ' ', place = ' ', province = ' ', info = ' '):
        self.wmo               = wmo
        self.place             = place
        self.province          = province
        self.country           = 'Netherlands'
        self.info              = info
        self.data_skip_rows    = config.knmi_data_skip_rows_etmgeg
        self.data_dummy_val    = config.knmi_data_dummy_val
        self.data_empthy_val   = config.knmi_data_empthy_val
        self.data_notification = config.knmi_data_notification
        self.dir_etmgeg        = os.path.join( config.dir_knmi, 'etmgeg' )
        self.file_zip_etmgeg   = os.path.join( self.dir_etmgeg, f'etmgeg_{self.wmo}.zip' )
        self.file_txt_etmgeg   = os.path.join( self.dir_etmgeg, f'etmgeg_{self.wmo}.txt' )
        self.data_url          = config.knmi_data_url.format(self.wmo)
