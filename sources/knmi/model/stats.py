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
    data, key = process_list(data, entity)
    ave = np.average( data[:,key] )  # Calculate average

    return ave

def sum( data, entity ):
    '''Function calculates the sum value for a given entity'''
    data, key = process_list(data, entity)
    sum = np.sum( data[:,key] )  # Calculate sum

    return sum

def max( data, entity ):
    '''Function gets maximum for a given entity'''
    data, key = process_list(data, entity)
    max = np.max( data[:,key] )  # Get max

    return max

def min( data, entity ):
    '''Function gets minimum for a given entity'''
    data, key = process_list(data, entity)
    min = np.min( data[:,key] )  # Get min

    return min

def terms_days( data, entity, operator, value ):
    '''Function select days based on terms like TX > 30 for example'''
    ent  = daydata.ndx_ent(entity)
    op   = operator.lower()
    f = df(value)

    if   op in ['gt',  '>']:       sel = np.where( data[:,ent] >  f )
    elif op in ['ge', '>=', '≥']:  sel = np.where( data[:,ent] >= f )
    elif op in ['eq', '==']:       sel = np.where( data[:,ent] == f )
    elif op in ['lt',  '<']:       sel = np.where( data[:,ent] <  f )
    elif op in ['le', '<=', '≤']:  sel = np.where( data[:,ent] <= f )
    elif op in ['ne', '!=', '<>']: sel = np.where( data[:,ent] != f )
    else: print('error, terms_days()'); input('?')

    data = data[sel]
    # Remove/empthy false values
    sel = np.where( data[:,ent] != config.knmi_dayvalues_dummy_val )

    return data[sel]

def terms_days_or( data, query1, query2 ):
    '''Function select days based on two terms like TX > 30 OR RH > 10 for example.'''
    q1ent, q1op, q1val = query1.split(' ')
    q2ent, q2op, q2val = query2.split(' ')
    data1 = terms_days( data, q1ent, q1op, q1val )
    data2 = terms_days( data, q2ent, q2op, q2val )
    data  = data[( data1 | data2 )]  # Add together with OR
    # data  = np.unique(data)          # Remove duplicate days

    return data

def terms_days_and( data, query1, query2 ):
    '''Function select days based on two terms like TX > 30 AND RH > 10 for example.'''
    q1ent, q1op, q1val = query1.split(' ')
    q2ent, q2op, q2val = query2.split(' ')
    data1 = terms_days( data, q1ent, q1op, q1val )
    data2 = terms_days( data, q2ent, q2op, q2val )
    data = data[(data1 & data2)]   # Select the same days

    return data

def extended_terms_days( data, terms ):
    '''Function select days based on terms like TX > 30 for example.
       Extended means there are options for AND & OR for example.'''
    l_terms = terms.strip().replace('  ',' ').split()
    cnt = len(l_terms)

    if cnt == 3:
        data = terms_days( data, l_terms[0], l_terms[1], l_terms[2] )
    elif cnt == 7:
        logi = l[-4]  # Logical operator: AND, OR
        if   logi in [ 'or', '||']:
            data = terms_days_or( data, l )
        elif logi in ['and', '&&']:
            data = terms_days_and( data, l )
        else:
            console.log(f'Unsupported operand: {logi} ?')
    elif cnt > 7: # > 7
        # Count OR and AND
        s_terms = ' '.join(l_terms).lower()
        l_logic = re.findall("or|\|\||and|&&",s_terms).reverse()

        # Process operators <,<= et cetera
        copy, result = l, []
        while len(copy) > 0:
            last = -2  if  copy[-1] in ['or','and']  else  -1
            val, ope, ent = copy[last], copy[last-1], copy[last-2]
            result.append( terms_days(data, ent, ope, val) )
            copy = copy[:last-2] # Remove used terms

        # Process logical operators
        key, result = 0, result.reverse()
        for logi in l_logic:
            data1 = result[key]; key += 1
            data2 = result[key]; key += 1

            if   logi in [ 'or', '||']: data = data[(data1 | data2)]  # Add together with OR
            elif logi in ['and', '&&']: data = data[(data1 & data2)]

    return data

def hellmann( data ):
    ''' Calculation of hellmann'''
    data = terms_days( data, 'TG', '<', 0.0 ) # Get days TG < 0
    sum  = sum( data, 'TG' ) # Sum all days
    hman = abs( sum )

    return hman, data
