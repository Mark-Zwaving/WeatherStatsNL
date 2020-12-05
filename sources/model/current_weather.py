# -*- coding: utf-8 -*-
'''Library contains classes and functions showing actual weather'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.3"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config, model.download as download
import view.fix as fix

knmi = 'tabel_10Min_data.json'

def knmi_table(l, cols=8, spaces=33):
    entities = [ 'station', 'overcast', 'temperature', 'windchill',
                 'humidity', 'wind_direction', 'wind_strength',
                 'visibility', 'air_pressure' ]

    txt, ndx, end, max = '\n', 0, cols-1, len(l)
    while True:
        part = l[ndx:end]
        for enties in entities:

            title, post_fix = enties, ' '
            if enties in ['temperature', 'windchill']:
                post_fix = '°C'
            elif enties == 'humidity':
                post_fix = '%'
            elif enties == 'wind_strength':
                post_fix = 'bft'
            elif enties == 'visibility':
                post_fix = 'm'
            elif enties == 'air_pressure':
                post_fix = 'hPa'

            title = title.replace('_','')
            pad = 26-len(title)
            if pad < 0: pad = 0
            elif pad % 1 == 0: pad -= 1
            txt += f'{title: >{pad}}'

            el_txt = ''
            for station in part:
                el = station[enties]
                if el == '':
                    el = '....'
                else:
                    el += post_fix

                pad = spaces-len(el)
                if pad < 0: pad = 0
                elif pad % 1 == 0: pad += 1
                el_txt += f'{el: ^{pad}}'

            txt += el_txt + '\n'

        txt += '\n'
        ndx, end = ndx + cols, end + cols
        # Check end
        if ndx >= max:
            break
        elif ndx < max:
            if end >= max:
                end = max # Correct max endkey

    txt += '\n'
    return txt

def knmi_stations():
    t = ''
    url = f'{config.knmi_ftp_pub}{knmi}'
    ok, json = download.request_json( url )

    if ok: # If download is oke, prepare the results
        t += f'Waarnemingen: {json["date"]}\n'
        t += knmi_table(json['stations'])

    return ok, t

# {
# "date": "5 december 2020 16:00",
# "elementen": "Station,Bewolking,Temperatuur,Gevoelstemperatuur,Relatieve_vochtigheid,Windrichting,Windsnelheid,Zicht,Luchtdruk",
# "stations": [
# { "station": "Lauwersoog", "overcast": "", "temperature": "4.1", "windchill": "0.2", "humidity": "87", "wind_direction": "Z", "wind_strength": "5", "visibility": "", "air_pressure": "" }
# ,
# { "station": "Nieuw Beerta", "overcast": "", "temperature": "4.4", "windchill": "0.6", "humidity": "87", "wind_direction": "Z", "wind_strength": "5", "visibility": "", "air_pressure": "" }
# ,
# { "station": "Terschelling", "overcast": "", "temperature": "4.4", "windchill": "-0.6", "humidity": "88", "wind_direction": "Z", "wind_strength": "8", "visibility": "24000", "air_pressure": "998.2" }
# ,
# { "station": "Vlieland", "overcast": "onbewolkt", "temperature": "4.6", "windchill": "0.4", "humidity": "83", "wind_direction": "Z", "wind_strength": "6", "visibility": "35000", "air_pressure": "998.1" }
# ,
# { "station": "Leeuwarden", "overcast": "onbewolkt", "temperature": "3.6", "windchill": "-0.4", "humidity": "85", "wind_direction": "Z", "wind_strength": "5", "visibility": "40000", "air_pressure": "999.2" }
# ,
# { "station": "Stavoren", "overcast": "zwaar bewolkt", "temperature": "4.6", "windchill": "0.8", "humidity": "82", "wind_direction": "Z", "wind_strength": "5", "visibility": "40000", "air_pressure": "" }
# ,
# { "station": "Houtribdijk", "overcast": "", "temperature": "", "windchill": "", "humidity": "", "wind_direction": "Z", "wind_strength": "8", "visibility": "", "air_pressure": "" }
# ,
# { "station": "Eelde", "overcast": "onbewolkt", "temperature": "3.7", "windchill": "0.9", "humidity": "83", "wind_direction": "Z", "wind_strength": "3", "visibility": "40000", "air_pressure": "999.7" }
# ,
# { "station": "Hoogeveen", "overcast": "onbewolkt", "temperature": "3.5", "windchill": "1.6", "humidity": "82", "wind_direction": "Z", "wind_strength": "2", "visibility": "50000", "air_pressure": "999.9" }
# ,
# { "station": "Heino", "overcast": "", "temperature": "4.9", "windchill": "3.2", "humidity": "78", "wind_direction": "Z", "wind_strength": "2", "visibility": "", "air_pressure": "" }
# ,
# { "station": "Twente", "overcast": "onbewolkt", "temperature": "5.1", "windchill": "2.6", "humidity": "71", "wind_direction": "Z", "wind_strength": "3", "visibility": "45000", "air_pressure": "999.7" }
# ,
# { "station": "Deelen", "overcast": "geheel bewolkt", "temperature": "5.0", "windchill": "3.4", "humidity": "77", "wind_direction": "ZZO", "wind_strength": "2", "visibility": "40000", "air_pressure": "999.4" }
# ,
# { "station": "Hupsel", "overcast": "", "temperature": "4.8", "windchill": "3.1", "humidity": "75", "wind_direction": "Z", "wind_strength": "2", "visibility": "", "air_pressure": "" }
# ,
# { "station": "Herwijnen", "overcast": "", "temperature": "4.4", "windchill": "1.8", "humidity": "80", "wind_direction": "ZO", "wind_strength": "3", "visibility": "", "air_pressure": "998.7" }
# ,
# { "station": "Marknesse", "overcast": "", "temperature": "4.2", "windchill": "1.5", "humidity": "81", "wind_direction": "ZZO", "wind_strength": "3", "visibility": "50000", "air_pressure": "" }
# ,
# { "station": "Lelystad", "overcast": "geheel bewolkt", "temperature": "4.6", "windchill": "1.4", "humidity": "75", "wind_direction": "Z", "wind_strength": "4", "visibility": "45000", "air_pressure": "999.3" }
# ,
# { "station": "De Bilt", "overcast": "onbewolkt", "temperature": "4.1", "windchill": "2.3", "humidity": "77", "wind_direction": "ZO", "wind_strength": "2", "visibility": "45000", "air_pressure": "998.7" }
# ,
# { "station": "Cabauw", "overcast": "", "temperature": "3.8", "windchill": "1.0", "humidity": "81", "wind_direction": "ZO", "wind_strength": "3", "visibility": "45000", "air_pressure": "998.6" }
# ,
# { "station": "Den Helder", "overcast": "onbewolkt", "temperature": "3.7", "windchill": "-0.3", "humidity": "81", "wind_direction": "Z", "wind_strength": "5", "visibility": "45000", "air_pressure": "998.2" }
# ,
# { "station": "Texelhors", "overcast": "", "temperature": "", "windchill": "", "humidity": "", "wind_direction": "Z", "wind_strength": "7", "visibility": "", "air_pressure": "" }
# ,
# { "station": "Berkhout", "overcast": "", "temperature": "4.6", "windchill": "1.4", "humidity": "83", "wind_direction": "ZZO", "wind_strength": "4", "visibility": "45000", "air_pressure": "" }
# ,
# { "station": "IJmuiden", "overcast": "", "temperature": "", "windchill": "", "humidity": "", "wind_direction": "ZO", "wind_strength": "3", "visibility": "", "air_pressure": "" }
# ,
# { "station": "Wijk aan Zee", "overcast": "", "temperature": "5.0", "windchill": "", "humidity": "78", "wind_direction": "", "wind_strength": "", "visibility": "", "air_pressure": "" }
# ,
# { "station": "Schiphol", "overcast": "geheel bewolkt", "temperature": "4.8", "windchill": "1.1", "humidity": "78", "wind_direction": "ZO", "wind_strength": "5", "visibility": "45000", "air_pressure": "998.4" }
# ,
# { "station": "Voorschoten", "overcast": "geheel bewolkt", "temperature": "4.9", "windchill": "2.4", "humidity": "79", "wind_direction": "ZO", "wind_strength": "3", "visibility": "45000", "air_pressure": "998.1" }
# ,
# { "station": "Rotterdam", "overcast": "geheel bewolkt", "temperature": "5.3", "windchill": "2.2", "humidity": "70", "wind_direction": "ZZO", "wind_strength": "4", "visibility": "45000", "air_pressure": "998.1" }
# ,
# { "station": "Hoek van Holland", "overcast": "", "temperature": "4.9", "windchill": "0.4", "humidity": "73", "wind_direction": "Z", "wind_strength": "7", "visibility": "", "air_pressure": "997.5" }
# ,
# { "station": "Wilhelminadorp", "overcast": "", "temperature": "4.9", "windchill": "1.7", "humidity": "76", "wind_direction": "ZZO", "wind_strength": "4", "visibility": "", "air_pressure": "997.5" }
# ,
# { "station": "Vlissingen", "overcast": "zwaar bewolkt", "temperature": "6.2", "windchill": "2.0", "humidity": "73", "wind_direction": "ZZO", "wind_strength": "7", "visibility": "35000", "air_pressure": "997.2" }
# ,
# { "station": "Westdorpe", "overcast": "", "temperature": "5.4", "windchill": "3.8", "humidity": "74", "wind_direction": "ZZO", "wind_strength": "2", "visibility": "50000", "air_pressure": "997.6" }
# ,
# { "station": "Woensdrecht", "overcast": "geheel bewolkt", "temperature": "5.2", "windchill": "2.7", "humidity": "72", "wind_direction": "ZO", "wind_strength": "3", "visibility": "40000", "air_pressure": "998.1" }
# ,
# { "station": "Gilze Rijen", "overcast": "geheel bewolkt", "temperature": "5.2", "windchill": "2.7", "humidity": "76", "wind_direction": "ZO", "wind_strength": "3", "visibility": "45000", "air_pressure": "998.7" }
# ,
# { "station": "Volkel", "overcast": "geheel bewolkt", "temperature": "5.6", "windchill": "3.2", "humidity": "68", "wind_direction": "ZZO", "wind_strength": "3", "visibility": "45000", "air_pressure": "999.2" }
# ,
# { "station": "Eindhoven", "overcast": "geheel bewolkt", "temperature": "5.6", "windchill": "3.2", "humidity": "70", "wind_direction": "ZZO", "wind_strength": "3", "visibility": "45000", "air_pressure": "999.0" }
# ,
# { "station": "Ell", "overcast": "geheel bewolkt", "temperature": "5.8", "windchill": "2.8", "humidity": "67", "wind_direction": "ZO", "wind_strength": "4", "visibility": "50000", "air_pressure": "" }
# ,
# { "station": "Arcen", "overcast": "", "temperature": "5.5", "windchill": "3.9", "humidity": "67", "wind_direction": "ZZW", "wind_strength": "2", "visibility": "", "air_pressure": "" }
# ,
# { "station": "Maastricht-Aachen Airport", "overcast": "geheel bewolkt", "temperature": "5.6", "windchill": "2.6", "humidity": "61", "wind_direction": "ZZO", "wind_strength": "4", "visibility": "45000", "air_pressure": "999.1" }
# ]
# }
#
#
#     # l_station, l_overcast, l_temperature = list(), list(), list()
#     # l_windchill, l_humidity, l_wind_direction = list(), list(), list()
#     # l_wind_strength, l_visibility, l_air_pressure = list(), list(), list()
#     #
#     # # Make lists for output
#     # for el in l:
#     #     l_station.append(el['station'])
#     #     l_overcast.append(el['overcast'])
#     #     l_temperature.append(el['temperature'])
#     #     l_windchill.append(el['windchill'])
#     #     l_humidity.append(el['humidity'])
#     #     l_wind_direction.append(el['wind_direction'])
#     #     l_wind_strength.append(el['wind_strength'])
#     #     l_visibility.append(el['visibilitys'])
#     #     l_air_pressure.append(el['air_pressure'])
