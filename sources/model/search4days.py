# -*- coding: utf-8 -*-
'''Functions for seaching days with charateristics'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.7'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import numpy as np
import model.stats as stats
import model.daydata as daydata
import model.utils as utils
import view.log as log

def query_simple( data, query ):
    ent, op, val = query.split(' ')
    days = stats.terms_days(data, ent, op, val)

    return days

def query_parser( query ):
    l, queries = query.lower().split(' '), []
    mem, key, max = 0, 0, len(l)
    while key < max:
        el = l[key]
        if el in ['and', 'or']:
            q = '' # Create part query
            for i in range(mem,key):
                q += f' {l[i]} '
            queries.append( utils.clear(q) ) # Append query part
            queries.append( el ) # Append 'or', 'and'
            mem = key + 1 # Always start at the next key
        key += 1

    q = '' # Create last part query
    for i in range(mem,key):
        q += f' {l[i]} '
    queries.append( utils.clear(q) )

    return queries

def np_and( np1, np2 ):
    if np1.size == 0 and np2.size == 0:
        return np.array([])
    elif np1.size == 0 and np2.size > 0:
        return np.array([])
    elif np2.size == 0 and np1.size > 0:
        return np.array([])
    else:
        ymd, stn, l = daydata.YYYYMMDD, daydata.STN, []
        # Get only the (same) days in both lists for a station
        for n1 in list(np1):
            for n2 in list(np2):
                if n1[ymd] == n2[ymd] and n1[stn] == n2[stn]:
                    # Check first if element already in list
                    found = False
                    for el in l:
                        if set(el) == set(n1):
                            found = True
                    if not found:
                        l.append(n1)

        return np.array(l)

def np_or( np1, np2 ):
    if np1.size == 0 and np2.size == 0:
        return np.array([])
    elif np1.size == 0 and np2.size > 0:
        return np2
    elif np2.size == 0 and np1.size > 0:
        return np1
    else:
        ymd, stn, l = daydata.YYYYMMDD, daydata.STN, []
        npl = np.concatenate( (np1, np2) ) # Sum together
        # Add only unique days for station to the list
        # for el in np:
        #
        # for n1 in list(np1):
        #     for n2 in list(np2):
        #         if n1[ymd] == n2[ymd] and n1[stn] == n2[stn]:
        #             pass
        #         else:
        #             l.append(n1)

        return npl

def query_advanced( data, query ):
    # Make a query list
    queries = query_parser( query )
    # Make one list with the days based on the queries
    # The other list with the (and, or) operators
    days, oper = [], []
    for el in queries:
        if el not in ['and', 'or']:
            days.append(query_simple(data, el))
        else:
            oper.append(el)

    # Proces all the days with the and,or operators and add to sel
    ndx, key, max, sel = 0, 1, len(days), np.array([])
    while key < max:
        op, d1, d2 = oper[ndx], days[key-1], days[key] # Get the days from the query
        # Make new days and put in same list as a replacement
        if op == 'and':
            np_a = np_and( d1, d2 )
            if np_a.size != 0:
                sel = np_a if sel.size == 0 else np.concatenate( (sel, np_a) )
        elif op == 'or':
            # Or is +/- the same as a normal plus
            np_o = np_or( d1, d2 )
            if np_o.size != 0:
                sel = np_o if sel.size == 0 else np.concatenate( (sel, np_o) )

        days[key] = sel
        ndx += 1 # Next operator
        key += 1 # Next days in list

    # All selected (unique)  days
    return sel

def process( stations, period, query ):
    # Read all data stations in a given period
    data = daydata.read_stations_period( stations, period )

    # Get all the days to search for
    log.console(f'Executing query: {query}', True)
    if query.find('and') == -1 and query.find('or') == -1:
        return query_simple( data, query ) # Process only one simple query
    else:
        return query_advanced( data, query ) # Process query with and, or
