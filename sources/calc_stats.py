# -*- coding: utf-8 -*-
'''WeatherStatsNL contains classes and functions to calculate statistics'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config as c, knmi, ask as a

class EtmgegGem():
    '''Klasse berekent gemiddelde waarden bestaande uit som en aantal in een reeks van dagen'''
    def __init__(self, datum, waarde, som, aantal, ent):
        self.datum  = datum
        self.waarde = waarde
        self.som    = som
        self.aantal = aantal
        self.gem    = self.som / self.aantal
        self.ent    = ent

class EtmgegExtreem():
    '''Klasse voor het opslaan van een maximum of minimum extreem'''
    def __init__(self, datum, tijd, extreem, ent ):
        self.datum   = datum
        self.tijd    = tijd
        self.extreem = extreem
        self.ent     = ent

class EtmgegCount():
    '''Klasse voor het opslaan van een maximum of minimum extreem'''
    def __init__(self, datum, tijd, waarde, oper, eis, tel, ent ):
        self.datum   = datum
        self.tijd    = tijd
        self.waarde  = waarde
        self.oper    = oper
        self.eis     = eis
        self.tel     = tel
        self.ent     = ent

class EtmgegSom():
    '''Klasse voor het opslaan van som extreem'''
    def __init__(self, datum, tijd, waarde, som, ent ):
        self.datum   = datum
        self.tijd    = tijd
        self.waarde  = waarde
        self.som     = som
        self.ent     = ent

class WarmteGetal:
    '''klasse voor het opslaan van warmtegetal dagen'''
    def __init__(self, datum, tg, getal, totaal, aantal, ent):
        self.datum  = datum
        self.tg     = tg
        self.getal  = getal
        self.totaal = totaal
        self.aantal = aantal
        self.ent    = ent

class Hellmann:
    '''Klasse voor het opslaan van hellman dagen'''
    def __init__(self, datum, getal, som, aantal, ent):
        self.datum  = datum
        self.getal  = getal
        self.som    = som
        self.aantal = aantal
        self.ent    = ent

class Heatwave:
    '''Klasse voor het opslaan van hittegolf dagen'''
    def __init__(self, station, etmgeg_list ):
        self.station      = station
        self.etmgeg_list  = etmgeg_list
        self.tot_heat_sum = warmte_getal(self.etmgeg_list)['getal']
        self.day_count    = len(self.etmgeg_list)

# Som
def som_val(lijst_geg, ent):
    '''Functie somt alle waarden van een reeks'''
    som, tel, tijd, l = 0, 0, -1, []
    for geg in lijst_geg: # Doorloop lijst
        etm = knmi.etmgeg(geg, ent)
        if etm != geg.empthy: # Leeg veld skippen
            i_etm = int(etm)
            som += i_etm
            etm_t = knmi.etmgeg_t( geg, ent ) # Check tijd
            tijd = etm_t if etm_t != geg.empthy and etm_t != False else -1 # Geef tijd mits aanwezig

            etmSom = EtmgegSom(geg.YYYYMMDD, tijd, i_etm, som, ent)
            l.append(etmSom) # Bewaar som in som object

    # Return false als niks wordt gevonden anders geef som
    return { 'som': False if not l else l[-1].som,
             'lijst':l }

# Gemiddelden
def gem_val ( lijst_geg, ent ):
    '''Functie berekent gemiddelde van een ent uit de reeks'''
    som, tel, l = 0, 0, [] # Begin op 0 en teller op 0
    for geg in lijst_geg: # Doorloop de lijst
        etm = knmi.etmgeg(geg,ent)
        if etm != geg.empthy: # Leeg veld overslaan
            i_etm = int(etm)
            som += i_etm
            tel += 1

            etmGem = EtmgegGem(geg.YYYYMMDD, i_etm, som, tel, ent)
            l.append(etmGem)

    # Return false als niks wordt gevonden
    return { 'gem': False if not l else l[-1].gem,
             'lijst': l }

# Minimum extremen
def min_val(lijst_geg, ent):
    '''Functie bepaalt de minimum waarde van TX uit de reeks plus tijdstip mits aanwezig'''
    min, tijd, l = c.max_value_geg, -1, [] # Hoogst mogelijke waarde
    for geg in lijst_geg: # Doorloop lijst
        etm = knmi.etmgeg(geg,ent)
        if etm != geg.empthy: # Leeg veld skippen
            i_etm = int(etm) # Convert naar int
            if i_etm < min: # Waarde kleiner dan min dan een nieuw min
                min  = i_etm;
                etm_t = knmi.etmgeg_t( geg, ent )
                tijd = etm_t if etm_t != geg.empthy and etm_t != False else -1 # Geef tijd mits aanwezig

                etmExtreem = EtmgegExtreem( geg.YYYYMMDD, tijd, min, ent )
                l.append(etmExtreem)

    # Return false als niks is gevonden
    return { 'min': False if not l else l[-1].extreem,
             'lijst': l }

# Maximum extremen
def max_val(lijst_geg, ent):
    '''Functie bepaalt de minimum waarde van TX uit de reeks plus tijdstip mits aanwezig'''
    max, tijd, l = c.min_value_geg, -1, [] # Hoogst mogelijke waarde
    for geg in lijst_geg: # Doorloop lijst
        etm = knmi.etmgeg(geg,ent)
        if etm != geg.empthy: # Leeg veld skippen
            i_etm = int(etm) # Convert naar int
            if i_etm > max: # Waarde groter dan max, dan een nieuw max
                max  = i_etm;
                etm_t = knmi.etmgeg_t( geg, ent ) # Bepaal nieuwe waarden

                tijd = etm_t if etm_t != geg.empthy and etm_t != False else -1 # Geef tijd mits aanwezig

                etmExtreem = EtmgegExtreem( geg.YYYYMMDD, tijd, max, ent )
                l.append(etmExtreem)

    # Return false als niks is gevonden
    return { 'max': False if max == c.min_value_geg else l[-1].extreem,
             'lijst': l }

# Counter voorwaardelijk
def cnt_day(lijst_geg, ent, oper, val):
    '''Functie bepaalt het aantal dagen onder de gestelde voorwaarden'''
    tel, tijd, l = 0, -1, []

    for geg in lijst_geg: # Doorloop lijst
        etm = knmi.etmgeg( geg, ent )
        if etm != geg.empthy: # Leeg veld skippen
            i_etm = int(etm)

            oke = True
            lt = ( oper == '<'  or oper == 'lt' )
            le = ( oper == '<=' or oper ==  '≤' or oper ==  'le' )
            gt = ( oper == '>'  or oper == 'gt' )
            ge = ( oper == '>=' or oper ==  '≥' or oper ==  'ge' )
            no = ( oper == '<>' or oper == '!=' or oper == 'not' )
            eq = ( oper == '==' or oper == 'is')
            if    lt and i_etm <  val: tel += 1
            elif  le and i_etm <= val: tel += 1
            elif  gt and i_etm >  val: tel += 1
            elif  ge and i_etm >= val: tel += 1
            elif  no and i_etm != val: tel += 1
            elif  eq and i_etm == val: tel += 1
            else: oke = False

            if oke:
                etm_t = knmi.etmgeg_t( geg, ent ) # Bepaal nieuwe waarden
                tijd = etm_t if etm_t != geg.empthy and etm_t != False else -1 # Geef tijd mits aanwezig

                etmCount = EtmgegCount(geg.YYYYMMDD, tijd, i_etm, oper, val, tel, ent)
                l.append(etmCount)

    # Return tel en geef de lijst met de extremen
    return { 'tel': tel, 'lijst': l }

def hellmann_getal(lijst_geg):
    som, aantal, l = 0, 0, []
    for geg in lijst_geg:
        if geg.TG != geg.empthy:
            iTG = int(geg.TG)
            if iTG < 0:
                getal = abs(iTG)
                som += getal
                aantal += 1

                hellman = Hellmann(geg.YYYYMMDD, getal, som, aantal, 'TG')
                l.append(hellman)

    return { 'getal': som, 'lijst': l }

def warmte_getal(lijst_geg):
    som, aantal, l, cummula = 0, 0, [], []
    for geg in lijst_geg:
        if geg.TG != geg.empthy:
            iTG = int(geg.TG)
            if iTG >= 180:
                getal = iTG - 180
                som += getal
                aantal += 1

                warm = WarmteGetal(geg.YYYYMMDD, iTG, getal, som, aantal, 'TG')
                l.append( warm )

    return { 'getal': som, 'lijst': l }

def get_heat_ndx_of_etm_geg(etm_geg):
    getal = 0
    if etm_geg.TG != etm_geg.empthy:
        iTG = int(etm_geg.TG)
        if iTG >= 180:
            return iTG - 180

def rearrange_heat_sum_for_period(l):

    pass

def get_list_heatwaves( station, etmgeg_list ):
    heatwave_list, mem_etmgeg_list = [], []
    day_cnt_num = 5
    day_cnt_25  = 0
    day_cnt_30  = 0
    day_cnt_30_1 = False
    day_cnt_30_2 = False
    day_cnt_30_3 = False
    heatwave = False

    for e in etmgeg_list:
        if e.TX != e.empthy:
            iTX = int(e.TX)

            if iTX >= 250: # Check only 25+
                day_cnt_25 += 1 # Count 25+
                etmgeg_list.append(e) # Save 25+
                if c.debug: a.pause(f'Counting for heatwave: {station.plaats}')

                if not heatwave: # No heatwave yet, check for it
                    # Check for 3 times 30+
                    if iTX >= 300:
                        day_cnt_30 += 1
                        if c.debug: a.pause('30+ found')

                        if not day_cnt_30_1 and day_cnt_30 == 1:
                            day_cnt_30_1 = True  # First 30 true
                            if c.debug: a.pause('First 30+ found')

                        if not day_cnt_30_2 and day_cnt_30 == 2:
                            day_cnt_30_2 = True  # Second 30 true
                            if c.debug: a.pause('Second 30+ found')

                        if not day_cnt_30_3 and day_cnt_30 == 3:
                            day_cnt_30_3 = True  # Third 30 truez
                            if c.debug: a.pause('Third 30+ found')

                    if day_cnt_30_3 and day_cnt_25 >= day_cnt_num:
                        heatwave = True # Heatwave started or active
                        if c.debug: a.pause('Heatwave started')
            else: # <25
                if c.debug: a.pause('Counting stopped')
                if heatwave == True: # Heatwave
                    heatwave = False
                    if c.debug: a.pause('Heatwave stopped')
                    # Add closed heatwave to list
                    heatdays = Heatwave( station, etmgeg_list )
                    heatwave_list.append( heatdays )
                else:
                    pass # No heatwave ended, just pass

                # No 25+, reset heatwave values
                day_cnt_25 = 0
                day_cnt_30 = 0
                day_cnt_30_1 = False
                day_cnt_30_2 = False
                day_cnt_30_3 = False
                heatwave = False
                etmgeg_list = []

        else: # Data cannot be checked.
            if c.debug: a.pause('Wrong data')
            if heatwave: # Oke stop heatwave, add to list and reset values
                heatdays = Heatwave( station, etmgeg_list )
                heatwave_list.append( heatdays )

            # No 25+, reset heatwave values
            day_cnt_25 = 0
            day_cnt_30 = 0
            day_cnt_30_1 = False
            day_cnt_30_2 = False
            day_cnt_30_3 = False
            heatwave = False
            etmgeg_list = []

    # No more data
    if heatwave: # Add heatwave to list, heatwave is not ended yet
        heatdays = Heatwave( station, etmgeg_list )
        heatwave_list.append ( heatdays )

    return heatwave_list
