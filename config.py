# -*- coding: utf-8 -*-
'''Library contains configuratino options and a list with knmi stations'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.9"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

# Voeg dirs toe aan python
import os, sys
dir_app = os.path.dirname(os.path.abspath(__file__))
dir_sources = os.path.abspath(os.path.join(dir_app, 'sources'))
sys.path.append(dir_app) # Dit bestand
sys.path.append(dir_sources) # Python bestanden

import knmi

# Inits
language = 'EN' # NL for Nederlands, EN for English, Default English
log = False # debugging modus
ln, tab = os.linesep, "\t"
line = '----------' * 8
stop = 'q'
max_value_geg, min_value_geg =  99999999, -99999999

# De lijst met weerstations
lijst_stations = []
lijst_stations.append( knmi.Station('215', 'Voorschoten', 'Zuid-Holland', '') )
lijst_stations.append( knmi.Station('235', 'De Kooy', 'Noord-Holland', '') )
lijst_stations.append( knmi.Station('240', 'Schiphol', 'Noord-Holland', '') )
lijst_stations.append( knmi.Station('242', 'Vlieland', 'Friesland', '') )
lijst_stations.append( knmi.Station('249', 'Berkhout', 'Noord-Holland', '') )
lijst_stations.append( knmi.Station('251', 'Hoorn Terschelling', 'Friesland', '') )
lijst_stations.append( knmi.Station('257', 'Wijk aan Zee', 'Noord-Holland', '') )
lijst_stations.append( knmi.Station('260', 'De Bilt', 'Utrecht', '') )
lijst_stations.append( knmi.Station('265', 'Soesterberg', 'Utrecht', '') )
lijst_stations.append( knmi.Station('267', 'Stavoren','Friesland', '') )
lijst_stations.append( knmi.Station('269', 'Lelystad','Flevoland', '') )
lijst_stations.append( knmi.Station('270', 'Leeuwarden','Friesland', '') )
lijst_stations.append( knmi.Station('273', 'Marknesse', 'Flevoland', '')  )
lijst_stations.append( knmi.Station('275', 'Deelen', 'Gelderland', '') )
lijst_stations.append( knmi.Station('277', 'Lauwersoog', 'Groningen', '') )
lijst_stations.append( knmi.Station('278', 'Heino', 'Overijssel', '') )
lijst_stations.append( knmi.Station('279', 'Hoogeveen', 'Drenthe', '') )
lijst_stations.append( knmi.Station('280', 'Eelde', 'Drenthe', '') )
lijst_stations.append( knmi.Station('283', 'Hupsel', 'Gelderland', '') )
lijst_stations.append( knmi.Station('286', 'Nieuw Beerta', 'Groningen', '') )
lijst_stations.append( knmi.Station('290', 'Twenthe', 'Overijssel', '') )
lijst_stations.append( knmi.Station('310', 'Vlissingen', 'Zeeland', '') )
lijst_stations.append( knmi.Station('319', 'Westdorpe', 'Zeeland', '') )
lijst_stations.append( knmi.Station('323', 'Wilhelminadorp', 'Zeeland', '') )
lijst_stations.append( knmi.Station('330', 'Hoek van Holland', 'Zuid-Holland', '') )
lijst_stations.append( knmi.Station('340', 'Woensdrecht', 'Noord-Brabant', '') )
lijst_stations.append( knmi.Station('344', 'Rotterdam', 'Zuid-Holland', '') )
lijst_stations.append( knmi.Station('348', 'Cabauw Mast', 'Utrecht', '') )
lijst_stations.append( knmi.Station('350', 'Gilze-Rijen', 'Noord-Brabant', '') )
lijst_stations.append( knmi.Station('356', 'Herwijnen', 'Gelderland', '') )
lijst_stations.append( knmi.Station('370', 'Eindhoven', 'Noord-Brabant', '') )
lijst_stations.append( knmi.Station('375', 'Volkel', 'Noord-Brabant', '') )
lijst_stations.append( knmi.Station('377', 'Ell', 'Limburg', '') )
lijst_stations.append( knmi.Station('380', 'Maastricht', 'Limburg', '') )
lijst_stations.append( knmi.Station('391', 'Arcen', 'Limburg', '') )

#lijst_stations.append( knmi.Station('311', 'Hoofdplaat', 'Zeeland', '') )
#lijst_stations.append( knmi.Station('210', 'Valkenburg Zh', 'Zuid-Holland', '') )
#lijst_stations.append( knmi.Station('209', 'IJmond', 'Noord-Holland', '') )
#lijst_stations.append( knmi.Station('248', 'Wijdenes', 'Noord-Holland', '') )
#lijst_stations.append( knmi.Station('258', 'Houtribdijk', 'Noord-Holland', '') )
#lijst_stations.append( knmi.Station('225', 'IJmuiden', 'Noord-Holland', '') )
#lijst_stations.append( knmi.Station('285', 'Huibertgat', 'Groningen', '') )
#lijst_stations.append( knmi.Station('308', 'Cadzand', 'Zeeland', '') )
#lijst_stations.append( knmi.Station('312', 'Oosterschelde', 'Zeeland', '') )
#lijst_stations.append( knmi.Station('313', 'Vlakte van De Raan', 'Zeeland', '') )
#lijst_stations.append( knmi.Station('331', 'Tholen', 'Noord-Brabant', '') )
#lijst_stations.append( knmi.Station('324', 'Stavenisse', 'Zeeland', '') )
#lijst_stations.append( knmi.Station('343', 'Rotterdam Geulhaven', 'Zuid-Holland', '') )
#lijst_stations.append( knmi.Station('315', 'Hansweert', 'Zeeland', '') )
#lijst_stations.append( knmi.Station('316', 'Schaar', 'Zeeland', '') )
