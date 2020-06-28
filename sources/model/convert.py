# -*- coding: utf-8 -*-
'''Library contains functions for converting data'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.4.2"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import view.translate as tr
import config

# Convert temperatures
celsius_to_fahrenheit = lambda c:   float(c) * 1.8 + 32.0
celsius_to_kelvin     = lambda c:   float(c) + 273.15
fahrenheit_to_celsius = lambda f: ( float(f) - 32.0 ) / 1.8
fahrenheit_to_kelvin  = lambda f: ( float(f) + 459.67 ) / 1.8
kelvin_to_celsius     = lambda k:   float(k) - 273.15
kelvin_to_fahrenheit  = lambda k:   float(k) * 1.8 - 459.67

# Default dpi in matplotlib is 100. See config.py
pixel_to_inch         = lambda p: float(p) / float(config.plot_dpi)

def ms_to_bft( ms ):
    i = int(ms)
    if   i <   3: return '0'
    elif i <  16: return '1'
    elif i <  34: return '2'
    elif i <  55: return '3'
    elif i <  80: return '4'
    elif i < 108: return '5'
    elif i < 139: return '6'
    elif i < 172: return '7'
    elif i < 208: return '8'
    elif i < 245: return '9'
    elif i < 285: return '10'
    elif i < 327: return '11'
    else: return '12'

def octa_to_txt(octa):
    i = int(octa)
    if   0 == i: return tr.txt('Onbewolkt')
    elif 1 == i: return tr.txt('Vrijwel onbewolkt')
    elif 2 == i: return tr.txt('Licht bewolkt')
    elif 3 == i: return tr.txt('Half bewolkt')
    elif 4 == i: return tr.txt('Half bewolkt')
    elif 5 == i: return tr.txt('Half tot zwaar bewolkt')
    elif 6 == i: return tr.txt('Zwaar bewolkt')
    elif 7 == i: return tr.txt('Vrijwel geheel bewolkt')
    elif 8 == i: return tr.txt('Geheel bewolkt')
    elif 9 == i: return tr.txt('Bovenlucht onzichtbaar')
    else: return ''

def deg_to_txt(deg):
    i = int(deg)
    if   i ==  0:  return tr.txt('stil')
    elif i  < 22:  return tr.txt('NOORD')
    elif i  < 30:  return tr.txt('NOORDNOORDOOST')
    elif i  < 67:  return tr.txt('NOORDOOST')
    elif i  < 112: return tr.txt('OOST')
    elif i  < 157: return tr.txt('ZUIDOOST')
    elif i  < 202: return tr.txt('ZUID')
    elif i  < 247: return tr.txt('ZUIDWEST')
    elif i  < 292: return tr.txt('WEST')
    elif i  < 337: return tr.txt('NOORDWEST')
    elif i  < 360: return tr.txt('NOORD')
    elif i == 990: return tr.txt('veranderlijk')
    else: return ''

def ms_to_txt( ms ):
    i = int(ms)
    if   i <   3: return tr.txt('windstil')
    elif i <  16: return tr.txt('zwakke wind')
    elif i <  34: return tr.txt('zwakke wind')
    elif i <  55: return tr.txt('matige wind')
    elif i <  80: return tr.txt('matige wind')
    elif i < 108: return tr.txt('vrij krachtige wind')
    elif i < 139: return tr.txt('krachtige wind')
    elif i < 172: return tr.txt('harde wind')
    elif i < 208: return tr.txt('stormachtige wind')
    elif i < 245: return tr.txt('storm')
    elif i < 285: return tr.txt('zware storm')
    elif i < 327: return tr.txt('zeer zware storm')
    else: return tr.txt('orkaan')

def vvn_to_txt( vvn ):
    i = int(vvn)
    # 1:100-200 m ... 49:4900-5000 m
    if vvn <= 49:
        return f'{i*100} - {(i+1)*100}' + tr.txt('meter')
    # 50:5-6 km
    elif vvn == 50:
        return '5 - 6' + tr.txt('km')
    # 56:6-7 km ... 79:29-30 km
    elif vvn <= 79:
        return f'{i-50} - {i-49}' + tr.txt('km')
    #  80:30-35 km ... 87:65-70 km
    elif vvn  < 89:
        return '{(i-80)*5+30} - {(i-79)*5+30}' + tr.txt('km')
    # 89: >70 km
    elif vvn == 89:
        return '< 70' + tr.txt('km')
    else:
        return ''

def timespan1hour(h):
    i = int(h)
    return f'{i-1} - {i}' + tr.txt('hour')

def timespan6hour(u):
    i = int(u)
    if   i ==  6:
        s  = '0 - 6'
    elif i == 12:
        s  = '6 - 12'
    elif i == 18:
        s  = '12 - 18'
    elif i == 24:
        s  = '18 - 24'
    else:
        s  = ''

    return s + tr.txt('hour')
