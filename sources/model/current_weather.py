# -*- coding: utf-8 -*-
'''Library contains classes and functions showing actual weather'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.5"
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
        text = text.replace('&rsquo;', '\'').replace('&euml;', 'ë')
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
