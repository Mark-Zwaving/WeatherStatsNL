# -*- coding: utf-8 -*-
'''WeatherStatsNL contains classes and functions to calculate statistics'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config as c

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

# Som
def som_val(lijst_geg, ent):
    '''Functie somt alle waarden van een reeks'''
    som, tel, tijd, l = 0, 0, -1, []
    for geg in lijst_geg: # Doorloop lijst
        etm = etmgeg(geg,ent)
        if etm != geg.empthy: # Leeg veld skippen
            i_etm = int(etm); som += i_etm; tel += 1 # Convert to int en telop
            etm_t = etmgeg_t(geg,ent) # Check tijd
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
        etm = etmgeg(geg,ent)
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
        etm = etmgeg(geg,ent)
        if etm != geg.empthy: # Leeg veld skippen
            i_etm = int(etm) # Convert naar int
            if i_etm < min: # Waarde kleiner dan min dan een nieuw min
                min  = i_etm; etm_t = etmgeg_t(geg,ent)
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
        etm = etmgeg(geg,ent)
        if etm != geg.empthy: # Leeg veld skippen
            i_etm = int(etm) # Convert naar int
            if i_etm > max: # Waarde groter dan max, dan een nieuw max
                max  = i_etm; etm_t = etmgeg_t(geg,ent) # Bepaal nieuwe waarden
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
        etm = etmgeg(geg,ent)
        if etm != geg.empthy: # Leeg veld skippen
            i_etm, oke = int(etm), True

            if   oper == '<'  and i_etm <  val: tel += 1
            elif oper == '<=' and i_etm <= val: tel += 1
            elif oper == '>'  and i_etm >  val: tel += 1
            elif oper == '>=' and i_etm >= val: tel += 1
            elif (oper == '<>' or oper == '!=') and i_etm is not val: tel += 1
            elif oper == '==' and i_etm == val: tel += 1
            else: oke = False

            if c.log:
                print("CNT|oke:{0}|getal:{1}|oper:{2}|val:{3}|tel:{4}|ent:{5}".format(oke,i_etm,oper,val,tel,ent))

            if oke:
                datum = geg.YYYYMMDD; etm_t = etmgeg_t(geg,ent) # Bepaal nieuwe waarden
                tijd = etm_t.strip() if etm_t != geg.empthy and etm_t != False else -1 # Geef tijd mits aanwezig
                if c.log: print("OKE|tijd:{0}".format(tijd))
                l.append(EtmgegCount(datum, tijd, i_etm, oper, val, tel, ent)) # Bewaar in count object

    # Return tel en geef de lijst met de extremen
    return { 'tel':0,'tijd':tijd,'lijst':l} if not l \
             else {'tel':l[-1].tel,'tijd':l[-1].tijd,'lijst':l}
