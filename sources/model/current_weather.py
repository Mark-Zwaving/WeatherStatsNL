# -*- coding: utf-8 -*-
'''Library contains classes and functions showing actual weather'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.3"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config, re
import sources.view.fix as fix
import sources.view.txt as txt
import sources.control.fio as fio

def buienradar_table_current_weather_stations(l, cols=8, spaces=33):
    entities = [ 'stationname', 'timestamp', 'weatherdescription', 'temperature',
                 'feeltemperature', 'windspeedBft', 'winddirection',
                 'precipitation', 'humidity', 'airpressure', 'sunpower' ]
                 # 'winddirectiondegrees',
    t, ndx, end, max = '\n', 0, cols, len(l)
    while True:
        part = l[ndx:end]
        for enties in entities:
            if enties == 'weatherdescription':
                enties = enties.replace('weather', '')

            title = enties + ' '
            post_fix = ''
            if enties in ['temperature', 'feeltemperature']:
                post_fix = '°C'
            elif enties == 'humidity':
                post_fix = '%'
            elif enties == 'windspeedBft':
                post_fix = 'bft'
            elif enties == 'visibility':
                post_fix = 'm'
            elif enties == 'airpressure':
                post_fix = 'hPa'
            elif enties == 'precipitation':
                post_fix = 'mm'

            t += txt.padding( title, align='right', spaces=33 )

            el_t = ''
            for station in part:
                if enties in station:
                    el = str(station[enties])
                    if el == '':
                        el = '....'
                    else:
                        if enties == 'timestamp':
                            el = el.replace('T', ' ')[:-3]
                        elif enties == 'stationname':
                            el = el.replace('Meetstation','')

                        el += post_fix
                else:
                    el = '....'

                el_t += txt.padding( el, align='center', spaces=spaces )

            t += el_t + '\n'

        t += '\n'
        ndx, end = ndx + cols, end + cols
        # Check end
        if ndx >= max:
            break
        elif ndx < max:
            if end >= max:
                end = max # Correct max endkey

    t += '\n'
    return t

def buienradar_stations():
    t = ''
    ok, js = fio.request_json( config.buienradar_json_data )

    if ok: # If download is oke, prepare the results
        stations = js['actual']['stationmeasurements']
        if config.buienradar_json_places != -1: # Print only stations in list
            l = list()
            for select in config.buienradar_json_places:
                sel = str(select)
                for station in stations:
                    name = str(station['stationname']).replace('Meetstation',' ').strip()
                    if name == sel:
                        l.append(station)
        else:
            l = stations # Print all stations

        t += f'Waarnemingen NL\n'
        t += buienradar_table_current_weather_stations(
                    l, cols=config.buienradar_json_cols, spaces=44
                )
        t += js['buienradar']['copyright'] + '\n'

    return ok, t

def buienradar_table_forecast(l, spaces=30):
    entities = [ 'day', 'maxtemperature', 'mintemperature', 'rainChance',
                 'sunChance', 'windDirection', 'wind' ] #'weatherdescription'
    t = ''
    for enties in entities:
        # Make title and post fix
        title, post_fix = enties + ' ', ' '
        if enties in ['maxtemperature', 'mintemperature']:
            post_fix = '°C'
        elif enties in ['rainChance', 'sunChance']:
            post_fix = '%'
        elif enties == 'wind':
            post_fix = 'bft'
        elif enties == 'visibility':
            post_fix = 'm'
        elif enties == 'air_pressure':
            post_fix = 'hPa'

        t += txt.padding( title, align='right', spaces=spaces )

        el_t = ''
        for day in l:
            el = str(day[enties])
            el = '....' if el == '' else el + post_fix

            if enties == 'day':
                el = el[:10]

            el_t += txt.padding( el, align='center', spaces=28 )

        t += el_t + '\n'

    return t

def buienradar_weather():
    t = ''
    ok, js = fio.request_json(config.buienradar_json_data)
    if ok:
        report = js['forecast']['weatherreport']
        text = report['text'].replace('.', '. ').replace('&agrave;', 'à')
        l = re.sub('\t|  |&nbsp;', ' ', text).split(' ')
        word, max_word = 1, 13  # Count words
        zin, max_zin = 1, 8   # Count sentence
        t_report = ''
        for el in l:
            el = el.strip()
            if el.find('.') != -1:
                zin += 1
                if zin % max_zin == 0:  # -1 Correction
                    t_report += el + '\n\n'
                    word = 1 # reset
                    continue

            t_report += el + ('\n' if word % max_word == 0 else ' ')
            word += 1

        t += 'Weerbericht van buienradar.nl\n'
        t += 'Gepubliceerd op: '
        t += report['published'].replace('T', ' ') + '\n\n'
        t += report['title']  + '\n\n'
        t += t_report.strip() + '\n\n'
        t += 'Auteur: ' + report['author'] + '\n\n'

        l_days_forecast = js['forecast']['fivedayforecast']

        t += 'Vooruitzichten\n\n'
        t += buienradar_table_forecast(l_days_forecast) + '\n\n'
        t += js['buienradar']['copyright'] + '\n\n'

    return ok, t


def knmi_table_current_weather_stations(l, cols=8, spaces=33):
    entities = [ 'station', 'overcast', 'temperature', 'windchill',
                 'humidity', 'wind_direction', 'wind_strength',
                 'visibility', 'air_pressure' ]

    t, ndx, end, max = '\n', 0, cols, len(l)
    while True:
        part = l[ndx:end]
        for enties in entities:

            title = enties.replace('_','') + ' '
            post_fix = ''
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

            t += txt.padding( title, align='right', spaces=30 )

            el_t = ''
            for station in part:
                el = str(station[enties])
                el = '....'if el == '' else el + post_fix
                el_t += txt.padding( el, align='center', spaces=spaces )

            t += el_t + '\n'

        t += '\n'
        ndx, end = ndx + cols, end + cols
        # Check end
        if ndx >= max:
            break
        elif ndx < max:
            if end >= max:
                end = max # Correct max endkey

    t += '\n'
    return t

def knmi_stations():
    t = ''
    url = config.knmi_json_data_10min
    ok, js = fio.request_json( url )

    if ok: # If download is oke, prepare the results

        stations = js['stations']
        if config.knmi_json_places != -1: # Print only stations in list
            l = list()
            for select in config.knmi_json_places:
                for station in stations:
                    name = station['station'].strip()
                    if name == select:
                        l.append(station)
        else:
            l = stations # Print all stations

        t += f'Waarnemingen: {js["date"]}\n'
        t += knmi_table_current_weather_stations(
                    l, cols=config.knmi_json_cols, spaces=44
                )
        t += config.knmi_dayvalues_notification.lower() + '\n'

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
