import os, threading, urllib, urllib.request, urllib.error, zipfile
import config as c, knmi, write as w
import datetime, time, math, locale


def get_list_day_values( station ):
    l, name = [], station.file_etmgeg_txt
    try:
        with open(name, 'r') as f: # Read data file in array
            l = f.readlines()
    except IOError as e:
        if c.log:
            print(f"Read data file:'{name}' failed")
            print(f'{e.reason}{c.ln}{e.strerror}')

    return l

def get_day_values_by_station_and_date( station, yyyymmdd ):
    '''Function: gets the weatherdata from a station at a given date'''
    if c.log:
        out = f'Function:get_knmi_etmgeg_by_station_and_date(station,yyyymmdd) in file:etmgeg.py'
        print(out)

    skip = station.skip_lines

    skip, knmi_etmgeg, lock_read, oke = , [], threading.Lock(),
    False
    with lock_read:
        if c.log:
            name = station.wmo + ', ' + station.plaats
            print(f"Read data station {naam} ...")
            print(f"Filename:'{station.file_etmgeg_txt}'")
        try:
            get_list_day_values(station)
        except IOError as e:
            if c.log:
                print(f"Read data file:'{station.file_etmgeg_txt}' failed")
                print(f'{e.reason}{c.ln}{e.strerror}')
        else:

            if c.log:
                print(f"Lezen gegevens uit bestand '{station.file_etmgeg_txt}' gelukt !")
                print(f'Eerste waarden reeks ' + data_file[skip].strip())
                print(f'Laatste waarden reeks ' + data_file[-1].strip())

            print(f'Lezen gegevens station {naam} succesvol...')
            for el in range(skip, len(data_file)): # Maak lijst met knmi gegevens
                knmi_etmgeg.append( knmi.Etmgeg(data_file[el]) )

            oke = True

    return oke if oke == False else knmi_etmgeg
