# -*- coding: utf-8 -*-
'''WeatherStatsNL contains classes and functions to calculate statistics'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config as c, knmi

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
    def __init__(self, datum, tijd, waarde, som, tel, ent ):
        self.datum   = datum
        self.tijd    = tijd
        self.waarde  = waarde
        self.som     = som
        self.tel     = tel
        self.ent     = ent

# Som
def som_val(lijst_geg, ent):
    '''Functie somt alle waarden van een reeks'''
    som, tel, tijd, l = 0, 0, -1, []
    for geg in lijst_geg: # Doorloop lijst
        etm = knmi.etmgeg(geg,ent)
        if etm != geg.empthy: # Leeg veld skippen
            i_etm = int(etm); som += i_etm; tel += 1 # Convert to int en telop
            etm_t = knmi.etmgeg_t(geg,ent) # Check tijd
            tijd = etm_t if etm_t != geg.empthy and etm_t != False else -1 # Geef tijd mits aanwezig
            l.append(EtmgegSom(geg.YYYYMMDD, tijd, i_etm, som, tel, ent)) # Bewaar som in dag object
    # Return false als niks is gevonden anders geef waarde met tijdstip lus de lijst met gevonden extremen
    return { 'som': False, 'lijst':l} if not l \
             else {'som':l[-1].som,'lijst':l }

# Gemiddelden
def gem_val ( lijst_geg, ent ):
    '''Functie berekent gemiddelde van een ent uit de reeks'''
    som, tel, l = 0, 0, [] # Begin op 0 en teller op 0
    for geg in lijst_geg: # Doorloop de lijst
        etm = knmi.etmgeg(geg,ent)
        if etm != geg.empthy: # Leeg veld overslaan
            datum = geg.YYYYMMDD; i_etm = int(etm); som += i_etm; tel += 1 # verwerk gegevens
            if c.log: print('GEM|datum:{0}|i_etm:{1}|som:{2}|tel:{3}'.format(datum,i_etm,som,tel))
            l.append(EtmgegGem(datum, i_etm, som, tel, ent))
    # Return false als geen waarden zijn gevonden anders geef het gemiddelde en de lijst met waarden
    return { 'gem':False, 'lijst':l } if not l \
              else { 'gem':l[-1].gem, 'lijst': l }

# Minimum extremen
def min_val(lijst_geg, ent):
    '''Functie bepaalt de minimum waarde van TX uit de reeks plus tijdstip mits aanwezig'''
    min, tijd, l = c.max_value_geg, -1, [] # Hoogst mogelijke waarde
    for geg in lijst_geg: # Doorloop lijst
        etm = knmi.etmgeg(geg,ent)
        if etm != geg.empthy: # Leeg veld skippen
            i_etm = int(etm) # Convert naar int
            if i_etm < min: # Waarde kleiner dan min dan een nieuw min
                min  = i_etm; etm_t = knmi.etmgeg_t(geg,ent)
                tijd = etm_t if etm_t != geg.empthy and etm_t != False else -1 # Geef tijd mits aanwezig
                l.append(EtmgegExtreem(geg.YYYYMMDD,tijd,min,ent)) # Bewaar extreem in dag object
    # Return false als niks is gevonden anders geef waarde met tijdstip lus de lijst met gevonden extremen
    return { 'min':False,'tijd':0,'lijst':l} if not l \
             else {'min':l[-1].extreem,'tijd':l[-1].tijd,'lijst':l}

# Maximum extremen
def max_val(lijst_geg, ent):
    '''Functie bepaalt de minimum waarde van TX uit de reeks plus tijdstip mits aanwezig'''
    max, tijd, l = c.min_value_geg, -1, [] # Hoogst mogelijke waarde
    for geg in lijst_geg: # Doorloop lijst
        etm = knmi.etmgeg(geg,ent)
        if etm != geg.empthy: # Leeg veld skippen
            i_etm = int(etm) # Convert naar int
            if i_etm > max: # Waarde groter dan max, dan een nieuw max
                max  = i_etm; etm_t = knmi.etmgeg_t(geg,ent) # Bepaal nieuwe waarden
                tijd = etm_t if etm_t != geg.empthy and etm_t != False else -1 # Geef tijd mits aanwezig
                l.append(EtmgegExtreem(geg.YYYYMMDD,tijd,max,ent)) # Bewaar extreem in dag object
    # Return false als niks is gevonden anders geef de gevonden waarde met eventuele tijdstip
    # Plus de hele lijst met gevonden extremen
    return { 'max':False,'tijd':0,'lijst':l} if not l \
             else {'max':l[-1].extreem,'tijd':l[-1].tijd,'lijst':l}

# Counter voorwaardelijk
def cnt_day(lijst_geg, ent, oper, val):
    '''Functie bepaalt het aantal dagen onder de gestelde voorwaarden'''
    tel, tijd, l = 0, -1, [] # Hoogst mogelijke waarde

    for geg in lijst_geg: # Doorloop lijst
        etm = knmi.etmgeg(geg,ent)
        if etm != geg.empthy: # Leeg veld skippen
            i_etm, oke = int(etm), True

            if     oper == '<'  and i_etm <  val: tel += 1
            elif ( oper == '<=' or oper == '≤' ) and i_etm <= val: tel += 1
            elif   oper == '>'  and i_etm >  val: tel += 1
            elif ( oper == '>=' or oper == '≥' ) and i_etm >= val: tel += 1
            elif ( oper == '<>' or oper == '!=' or oper == 'not' ) and i_etm is not val: tel += 1
            elif ( oper == '==' or oper == 'is') and i_etm == val: tel += 1
            else: oke = False

            if c.log:
                print("CNT|oke:{0}|getal:{1}|oper:{2}|val:{3}|tel:{4}|ent:{5}".format(oke,i_etm,oper,val,tel,ent))

            if oke:
                datum = geg.YYYYMMDD; etm_t = knmi.etmgeg_t(geg,ent) # Bepaal nieuwe waarden
                tijd = etm_t.strip() if etm_t != geg.empthy and etm_t != False else -1 # Geef tijd mits aanwezig
                if c.log: print("OKE|tijd:{0}".format(tijd))
                l.append(EtmgegCount(datum, tijd, i_etm, oper, val, tel, ent)) # Bewaar in count object

    # Return tel en geef de lijst met de extremen
    return { 'tel':0,'tijd':tijd,'lijst':l} if not l \
             else {'tel':l[-1].tel,'tijd':l[-1].tijd,'lijst':l}

def get_heat_ndx_of_etm_geg(etm_geg):
    getal = 0
    if etm_geg.TG != etm_geg.empthy:
        iTG = int(etm_geg.TG)
        if iTG >= 180:
            getal = iTG - 180

    return getal
