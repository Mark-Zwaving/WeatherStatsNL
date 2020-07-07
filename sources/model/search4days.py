# -*- coding: utf-8 -*-
'''Functions for seaching days with charateristics'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.4'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import knmi.model.stats as stats
import knmi.model.daydata as daydata
import numpy as np

def query_simple(data, query):
    ent, op, val = query.split(' ')
    data = stats.terms_days(data, ent, op, val)

    return data

def query_process(stations, start_ymd, end_ymd, query):
    # Read data station # Select period # Search for and, or ?

    # Get all the days to search for
    all_days = np.array([])
    for station in stations:
        ok, data = daydata.read(station)
        if ok:
            data = stats.period( data, start_ymd, end_ymd )
            if all_days.size == 0:
                all_days = data
            else:
                all_days = np.concatenate( (all_days, data) )

    # Process query

    # TODO
    # Check for and
    # if len(query.split('and')) > 0:
    #     stats.terms_days_and( date, l_terms )
    #
    # # Check for or
    # if  len(query.split('or')) > 0:
    #     stats.terms_days_or( data, l_terms )

    # Only one query
    data = query_simple( all_days, query )

    return data

#
