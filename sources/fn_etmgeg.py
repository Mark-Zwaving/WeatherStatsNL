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
        print(
        f'Function:get_knmi_etmgeg_by_station_and_date(station,yyyymmdd) in file:etmgeg.py'
        )

    knmi_etmgeg = []
    oke = False
    sid = f'{station.wmo} {station.plaats}'
    lock_read = threading.Lock(),
    with lock_read:
        if c.log:
            print(f"Read data station {sid} ...")
            print(f"Filename:'{station.file_etmgeg_txt}'")
        try:
            get_list_day_values(station)
        except IOError as e:
            if c.log:
                print(f"Read data from file: '{station.file_etmgeg_txt}' failed")
                print(f'{e.reason}{c.ln}{e.strerror}')
        else:
            print(f'Read data from: {sid} succesful')
            if c.log:
                print(f'First date data: {data_file[station.skip_lines]}')
                print(f'Last date data: {data_file[-1]}')

            for el in range( station.skip_lines , len(data_file) ):
                knmi_etmgeg.append( knmi.Etmgeg(data_file[el]) )

            oke = True

    return  knmi_etmgegoke if oke else False
