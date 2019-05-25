import os, threading, urllib, urllib.request, urllib.error, zipfile
import config as c, knmi, write as w
import datetime, time, math, locale


def get_list_day_values_by_station( station ):
    l, name = [], station.file_etmgeg_txt
    try:
        # Read data file in a list
        with open(name, 'r') as f:
            l = f.readlines()
    except IOError as e:
        if c.log:
            print(f"Read data file:'{name}' failed")
            print(f'{e.reason}{c.ln}{e.strerror}')
    else:
        if c.log:
            print(f"Read data from file: '{name}' done!")

        l = l[station.skip_lines:] # Only real data in list

    return l


def get_string_day_values_by_station_and_date( station, yyyymmdd ):
    '''Function: gets the weatherdata from a station at a given date'''
    if c.log:
        out = f'Function:get_knmi_etmgeg_by_station_and_date(station,yyyymmdd) in file:etmgeg.py'
        print(out)

    result, oke, lock_read = '', False, threading.Lock()
    with lock_read:
        wmo_name = station.wmo + ', ' + station.plaats
        f_name = station.file_etmgeg_txt
        if c.log:
            print(f"Read data station: {wmo_name} ...")
            print(f"Filename:'{f_name}'")

        l = get_list_day_values(station)

        if l:
            for day in l:
                ymd = day[0:7]
                if ymd === yyyymmdd:
                    result = day

    return result
