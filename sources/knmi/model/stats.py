# -*- coding: utf-8 -*-
'''Library contains classes and functions for calculating statistics'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.6"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config
import knmi.model.daydata as daydata
import numpy as np

# Allowed operators
operators = np.array( [
    'gt', 'ge', 'lt', 'le', 'eq', 'ne', 'or', 'and',
    '<', '<=', '>', '>=', '==', '!=', '<>', '||', '&&'
    ] )

df          = lambda s        : float(s) * 10.0
is_entity   = lambda entity   : (entity.upper()   in entities)
is_operator = lambda operator : (operator.lower() in operators)

def process_list( data, entity ):
    '''Function processes data values on false values'''
    key  = daydata.ndx_ent( entity )
    sel = np.where( data[:,key] != config.knmi_dayvalues_dummy_val ) # Remove false values

    return data[sel], key

def average( data, entity ):
    '''Function calculates the average value for a given entity'''
    key = daydata.ndx_ent( entity )
    ave = np.average( data[:,key] )  # Calculate average

    return ave

def sum( data, entity ):
    '''Function calculates the sum value for a given entity'''
    key = daydata.ndx_ent( entity )
    sum = np.sum( data[:,key] )  # Calculate sum

    return sum

def max( data, entity ):
    '''Function gets maximum for a given entity'''
    key = daydata.ndx_ent( entity )
    max = np.max( data[:,key] )  # Get max

    return max

def min( data, entity ):
    '''Function gets minimum for a given entity'''
    key = daydata.ndx_ent( entity )
    min = np.min( data[:,key] )  # Get min

    return min

def terms_days( data, entity, operator, value ):
    '''Function select days based on terms like TX > 30 for example'''
    ent, op, f = daydata.ndx_ent(entity), operator.lower(), df(value)

    if   op in ['gt',  '>']:       sel = np.where( data[:,ent] >  f )
    elif op in ['ge', '>=', '≥']:  sel = np.where( data[:,ent] >= f )
    elif op in ['eq', '==']:       sel = np.where( data[:,ent] == f )
    elif op in ['lt',  '<']:       sel = np.where( data[:,ent] <  f )
    elif op in ['le', '<=', '≤']:  sel = np.where( data[:,ent] <= f )
    elif op in ['ne', '!=', '<>']: sel = np.where( data[:,ent] != f )
    else: print('error, terms_days()'); input('?')

    return data[sel]

def hellmann( data ):
    ''' Calculation of hellmann'''
    data = terms_days( data, 'TG', '<', 0.0 ) # Get days TG < 0
    som  = sum( data, 'TG' ) # Sum all days
    hman = abs( som )

    return hman

def heat_ndx( data ):
    data = terms_days( data, 'TG', '≥', 18 ) # Warmte getal dag
    tx   = data[:,daydata.ndx_ent('TG')]
    ndx  = np.sum(tx - 180)

    return ndx
