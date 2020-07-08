# -*- coding: utf-8 -*-
'''Functions for seaching days with charateristics'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.5'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import knmi.model.stats as stats
import knmi.model.daydata as daydata
import model.utils as utils
import numpy as np

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

def query_advanced( data, query ):
    # Make a query list
    queries = query_parser( query )
    # Make two lists with the days based on the queries
    # The other list with the (and, or) operators
    days, oper = [], []
    for el in queries:
        if el not in ['and', 'or']:
            days.append(daysquery_simple(data, el))
        else:
            oper.append(el)

    # Proces the days with the and,or operators
    key = 1
    for el in oper: # Loop throught
        d1, d2 = days[key - 1], days[key + 0] # Get the days from the query
        # Make new days and put in same list as a replacement
        if   el == 'and': days[key] = data[(d1 & d2)]
        elif el ==  'or': days[key] = data[(d1 | d2)]
        key += 1 # Next days in list

    # Last in list are the calculated days for all and, or 
    return days[key]

def process( stations, symd, eymd, query ):
    # Read all data stations in a given period
    data = daydata.read_stations_period( stations, symd, eymd )

    # Get all the days to search for
    if query.find('and') == -1 and query.find('or') == -1:
        return query_simple( data, query ) # Process only one simple query
    else:
        return query_advanced( data, np.array([]), query )
