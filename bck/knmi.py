# -*- coding: utf-8 -*-
'''Library contains classes to store knmi data'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import os, pathlib, config as c, fn

class Station:
    '''Deze klasse initialiseert een knmi weerstation'''
    def __init__(self, wmo = '', plaats = '', provincie = '', info = ''):
        self.wmo, self.plaats, self.provincie, self.info = wmo, plaats, provincie, info

        self.dir_knmi = fn.mk_path(c.dir_app, 'knmi')
        self.dir_data = fn.mk_path(self.dir_knmi, 'data')
        self.dir_text = fn.mk_path(self.dir_knmi, 'text')
        self.dir_html = fn.mk_path(self.dir_knmi, 'html')
        self.dir_css  = fn.mk_path(self.dir_html, 'css')
        self.dir_js   = fn.mk_path(self.dir_html, 'js')

        self.file_etmgeg_zip = fn.mk_path(self.dir_data, f'etmgeg_{self.wmo}.zip')
        self.file_etmgeg_txt = fn.mk_path(self.dir_data, f'etmgeg_{self.wmo}.txt')
        self.file_css_1 = fn.mk_path(self.dir_css, 'default_1.css' )
        self.file_css_2 = fn.mk_path(self.dir_css, 'default_2.css' )
        self.file_js_1  = fn.mk_path(self.dir_js, 'default_1.css' )
        self.file_js_2  = fn.mk_path(self.dir_js, 'default_2.css' )

        self.url_etmgeg_base = r'https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/etmgeg_{0}.zip'
        self.url_etmgeg  = self.url_etmgeg_base.format(self.wmo)

        self.bronvermelding = 'BRON: KONINKLIJK NEDERLANDS METEOROLOGISCH INSTITUUT (KNMI)'
        self.empthy, self.skip_lines = '     ', 49

        # Check of alle directories voor de knmi gegevens zijn aangemaakt, zoniet maak ze
        for dir in [self.dir_knmi, self.dir_data, self.dir_text, self.dir_css, self.dir_js]:
            if not os.path.exists(dir):
                os.makedirs(dir)

        # Make css files and js files, only if not exists
        for file in [self.file_css_1, self.file_css_2, self.file_js_1, self.file_js_2]:
            if not os.path.exists(file):
                pathlib.Path(file).touch()

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


def etmgeg ( geg, entity ):
    ent = entity.upper()
    if   ent == 'STN': return geg.STN
    elif ent == 'YYYYMMDD': return geg.YYYYMMDD   #YYYYMMDD  = Datum (YYYY=jaar MM=maand DD=dag) / Date (YYYY=year MM=month DD=day)
    elif ent == 'DDVEC': return geg.DDVEC         #DDVEC     = Vectorgemiddelde windrichting in graden (360=noord, 90=oost, 180=zuid, 270=west, 0=windstil/variabel). Zie http://www.knmi.nl/kennis-en-datacentrum/achtergrond/klimatologische-brochures-en-boeken / Vector mean wind direction in degrees (360=north, 90=east, 180=south, 270=west, 0=calm/variable)
    elif ent == 'FHVEC': return geg.FHVEC         #FHVEC     = Vectorgemiddelde windsnelheid (in 0.1 m/s). Zie http://www.knmi.nl/kennis-en-datacentrum/achtergrond/klimatologische-brochures-en-boeken / Vector mean windspeed (in 0.1 m/s)
    elif ent == 'FG': return geg.FG               #FG        = Etmaalgemiddelde windsnelheid (in 0.1 m/s) / Daily mean windspeed (in 0.1 m/s)
    elif ent == 'FHX': return geg.FHX             #FHX       = Hoogste uurgemiddelde windsnelheid (in 0.1 m/s) / Maximum hourly mean windspeed (in 0.1 m/s)
    elif ent == 'FHXH': return geg.FHXH           #FHXH      = Uurvak waarin FHX is gemeten / Hourly division in which FHX was measured
    elif ent == 'FHN': return geg.PHN             #FHN       = Laagste uurgemiddelde windsnelheid (in 0.1 m/s) / Minimum hourly mean windspeed (in 0.1 m/s)
    elif ent == 'FHNH': return geg.PHNH           #FHNH      = Uurvak waarin FHN is gemeten / Hourly division in which FHN was measured
    elif ent == 'FXX': return geg.FXX             #FXX       = Hoogste windstoot (in 0.1 m/s) / Maximum wind gust (in 0.1 m/s)
    elif ent == 'FXXH': return geg.FXXH           #FXXH      = Uurvak waarin FXX is gemeten / Hourly division in which FXX was measured
    elif ent == 'TG': return geg.TG               #TG        = Etmaalgemiddelde temperatuur (in 0.1 graden Celsius) / Daily mean temperature in (0.1 degrees Celsius)
    elif ent == 'TN': return geg.TN               #TN        = Minimum temperatuur (in 0.1 graden Celsius) / Minimum temperature (in 0.1 degrees Celsius)
    elif ent == 'TNH': return geg.TNH             #TNH       = Uurvak waarin TN is gemeten / Hourly division in which TN was measured
    elif ent == 'TX': return geg.TX               #TX        = Maximum temperatuur (in 0.1 graden Celsius) / Maximum temperature (in 0.1 degrees Celsius)
    elif ent == 'TXH': return geg.TXH             #TXH       = Uurvak waarin TX is gemeten / Hourly division in which TX was measured
    elif ent == 'T10N': return geg.T10N           #T10N      = Minimum temperatuur op 10 cm hoogte (in 0.1 graden Celsius) / Minimum temperature at 10 cm above surface (in 0.1 degrees Celsius)
    elif ent == 'T10NH': return geg.T10NH         #T10NH     = 6-uurs tijdvak waarin T10N is gemeten / 6-hourly division in which T10N was measured; 6=0-6 UT, 12=6-12 UT, 18=12-18 UT, 24=18-24 UT
    elif ent == 'SQ': return geg.SQ               #SQ        = Zonneschijnduur (in 0.1 uur) berekend uit de globale straling (-1 voor <0.05 uur) / Sunshine duration (in 0.1 hour) calculated from global radiation (-1 for <0.05 hour)
    elif ent == 'SP': return geg.SP               #SP        = Percentage van de langst mogelijke zonneschijnduur / Percentage of maximum potential sunshine duration
    elif ent == 'Q,': return geg.Q                #Q         = Globale straling (in J/cm2) / Global radiation (in J/cm2)
    elif ent == 'DR': return geg.DR               #DR        = Duur van de neerslag (in 0.1 uur) / Precipitation duration (in 0.1 hour)
    elif ent == 'RH': return geg.RH               #RH        = Etmaalsom van de neerslag (in 0.1 mm) (-1 voor <0.05 mm) / Daily precipitation amount (in 0.1 mm) (-1 for <0.05 mm)
    elif ent == 'RHX': return geg.RHX             #RHX       = Hoogste uursom van de neerslag (in 0.1 mm) (-1 voor <0.05 mm) / Maximum hourly precipitation amount (in 0.1 mm) (-1 for <0.05 mm)
    elif ent == 'RHXH': return geg.RHXH           #RHXH      = Uurvak waarin RHX is gemeten / Hourly division in which RHX was measured
    elif ent == 'PG': return geg.PG               #PG        = Etmaalgemiddelde luchtdruk herleid tot zeeniveau (in 0.1 hPa) berekend uit 24 uurwaarden / Daily mean sea level pressure (in 0.1 hPa) calculated from 24 hourly values
    elif ent == 'PX': return geg.PX               #PX        = Hoogste uurwaarde van de luchtdruk herleid tot zeeniveau (in 0.1 hPa) / Maximum hourly sea level pressure (in 0.1 hPa)
    elif ent == 'PXH': return geg.PXH             #PXH       = Uurvak waarin PX is gemeten / Hourly division in which PX was measured
    elif ent == 'PN': return geg.PN               #PN        = Laagste uurwaarde van de luchtdruk herleid tot zeeniveau (in 0.1 hPa) / Minimum hourly sea level pressure (in 0.1 hPa)
    elif ent == 'PNH': return geg.PNH             #PNH       = Uurvak waarin PN is gemeten / Hourly division in which PN was measured
    elif ent == 'VVN': return geg.VVN             #VVN       = Minimum opgetreden zicht / Minimum visibility; 0: <100 m, 1:100-200 m, 2:200-300 m,..., 49:4900-5000 m, 50:5-6 km, 56:6-7 km, 57:7-8 km,..., 79:29-30 km, 80:30-35 km, 81:35-40 km,..., 89: >70 km)
    elif ent == 'VVNH': return geg.VVNH           #VVNH      = Uurvak waarin VVN is gemeten / Hourly division in which VVN was measured
    elif ent == 'VVX': return geg.VVX             #VVX       = Maximum opgetreden zicht / Maximum visibility; 0: <100 m, 1:100-200 m, 2:200-300 m,..., 49:4900-5000 m, 50:5-6 km, 56:6-7 km, 57:7-8 km,..., 79:29-30 km, 80:30-35 km, 81:35-40 km,..., 89: >70 km)
    elif ent == 'VVXH': return geg.VVXH           #VVXH      = Uurvak waarin VVX is gemeten / Hourly division in which VVX was measured
    elif ent == 'NG': return geg.NG               #NG        = Etmaalgemiddelde bewolking (bedekkingsgraad van de bovenlucht in achtsten, 9=bovenlucht onzichtbaar) / Mean daily cloud cover (in octants, 9=sky invisible)
    elif ent == 'UG': return geg.UG               #UG        = Etmaalgemiddelde relatieve vochtigheid (in procenten) / Daily mean relative atmospheric humidity (in percents)
    elif ent == 'UX': return geg.UX               #UX        = Maximale relatieve vochtigheid (in procenten) / Maximum relative atmospheric humidity (in percents)
    elif ent == 'UXH': return geg.UXH             #UXH       = Uurvak waarin UX is gemeten / Hourly division in which UX was measured
    elif ent == 'UN': return geg.UN               #UN        = Minimale relatieve vochtigheid (in procenten) / Minimum relative atmospheric humidity (in percents)
    elif ent == 'UNH': return geg.UNH             #UNH       = Uurvak waarin UN is gemeten / Hourly division in which UN was measured
    elif ent == 'EV24': return geg.EV24           #EV24      = Referentiegewasverdamping (Makkink) (in 0.1 mm) / Potential evapotranspiration (Makkink) (in 0.1 mm)

def etmgeg_t ( geg, entity ):
    ent = entity.upper()
    if   ent == 'FHX':  return geg.FHXH    #FHXH  = Uurvak waarin FHX is gemeten / Hourly division in which FHX was measured
    elif ent == 'FHN':  return geg.PHNH    #FHNH  = Uurvak waarin FHN is gemeten / Hourly division in which FHN was measured
    elif ent == 'FXX':  return geg.FXXH    #FXXH  = Uurvak waarin FXX is gemeten / Hourly division in which FXX was measured
    elif ent == 'TN':   return geg.TNH     #TNH   = Uurvak waarin TN is gemeten / Hourly division in which TN was measured
    elif ent == 'TX':   return geg.TXH     #TXH   = Uurvak waarin TX is gemeten / Hourly division in which TX was measured
    elif ent == 'T10N': return geg.T10NH   #T10NH = 6-uurs tijdvak waarin T10N is gemeten / 6-hourly division in which T10N was measured; 6=0-6 UT, 12=6-12 UT, 18=12-18 UT, 24=18-24 UT
    elif ent == 'RHX':  return geg.RHXH    #RHXH  = Uurvak waarin RHX is gemeten / Hourly division in which RHX was measured
    elif ent == 'PX':   return geg.PXH     #PXH   = Uurvak waarin PX is gemeten / Hourly division in which PX was measured
    elif ent == 'PN':   return geg.PNH     #PNH   = Uurvak waarin PN is gemeten / Hourly division in which PN was measured
    elif ent == 'VVN':  return geg.VVNH    #VVNH  = Uurvak waarin VVN is gemeten / Hourly division in which VVN was measured
    elif ent == 'VVX':  return geg.VVXH    #VVXH  = Uurvak waarin VVX is gemeten / Hourly division in which VVX was measured
    elif ent == 'UX':   return geg.UXH     #UXH   = Uurvak waarin UX is gemeten / Hourly division in which UX was measured
    elif ent == 'UN':   return geg.UNH     #UNH   = Uurvak waarin UN is gemeten / Hourly division in which UN was measured
    else: return False

def ent_to_t_ent( ent ):
    ent = ent.upper()
    if   ent == 'FHX':  return 'FHXH'    #FHXH  = Uurvak waarin FHX is gemeten / Hourly division in which FHX was measured
    elif ent == 'FHN':  return 'FHNH'    #FHNH  = Uurvak waarin FHN is gemeten / Hourly division in which FHN was measured
    elif ent == 'FXX':  return 'FXXH'    #FXXH  = Uurvak waarin FXX is gemeten / Hourly division in which FXX was measured
    elif ent == 'TN':   return 'TNH '    #TNH   = Uurvak waarin TN is gemeten / Hourly division in which TN was measured
    elif ent == 'TX':   return 'TXH '    #TXH   = Uurvak waarin TX is gemeten / Hourly division in which TX was measured
    elif ent == 'T10N': return 'T10NH'   #T10NH = 6-uurs tijdvak waarin T10N is gemeten / 6-hourly division in which T10N was measured; 6=0-6 UT, 12=6-12 UT, 18=12-18 UT, 24=18-24 UT
    elif ent == 'RHX':  return 'RHXH'    #RHXH  = Uurvak waarin RHX is gemeten / Hourly division in which RHX was measured
    elif ent == 'PX':   return 'PXH '    #PXH   = Uurvak waarin PX is gemeten / Hourly division in which PX was measured
    elif ent == 'PN':   return 'PNH '    #PNH   = Uurvak waarin PN is gemeten / Hourly division in which PN was measured
    elif ent == 'VVN':  return 'VVNH'    #VVNH  = Uurvak waarin VVN is gemeten / Hourly division in which VVN was measured
    elif ent == 'VVX':  return 'VVXH'    #VVXH  = Uurvak waarin VVX is gemeten / Hourly division in which VVX was measured
    elif ent == 'UX':   return 'UXH '    #UXH   = Uurvak waarin UX is gemeten / Hourly division in which UX was measured
    elif ent == 'UN':   return 'UNH '    #UNH   = Uurvak waarin UN is gemeten / Hourly division in which UN was measured
    else:
        return False # No