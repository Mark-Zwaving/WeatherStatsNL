# -*- coding: utf-8 -*-
'''Library contains classes and functions for calculating statistics'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.0.9'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config
import numpy as np
import numpy.ma as ma
import model.daydata as daydata

# All allowed input operators
operators = np.array( [
    'lt', '<', 'le', '<=', '≤',
    'gt', '>', 'ge', '>=', '≥',
    'eq', '==', 'ne', '!=', '<>',
    'or', '||', 'and', '&&'
    ] )

df          = lambda s        : float(s) * 10.0
is_entity   = lambda entity   : entity.upper()   in entities
is_operator = lambda operator : operator.lower() in operators

def climate_periode( station, periode,  ent):
    '''Function calculates averages over a period in a year'''
    ys, ye = config.climate_period.split('-')  # Get climate years
    mmdds, mmdde = period.split('-')
    # YYYYMMDD-YYYY*MMDD*
    mms, dds, mme, dde = mmdds[0:2], mmdds[2:4], mmdde[0:2], mmdde[2:4]
    clima_period = f'{ys}{mms}*{dds}*-{ye}{mme}*{dde}*'
    data = daydata.read_station_period ( station, period )  # Get all the days in clima period
    ave  = average( data, ent )  # Calculate averages

    return ave

def climate_day( station, mmdd, ent ):
    '''Function calculate climate averages for a day for a station'''
    ys, ye = config.climate_period.split('-')  # Get climate years
    per  = f'{ys}{mmdd}-{ye}*{mmdd}'  # Special period for a day during the years
    data = daydata.read_station_period( station, per )  # Get all the days in clima period
    # data = process_list( data, ent )  # Remove nan values
    # HACK for sel_period. Because of added mask
    data = data[1]

    ave = average( data, ent )  # Calculate averages
    return ave

def process_list( data, entity ):
    '''Function processes data values on false values'''
    ndx = daydata.ndx_ent( entity )  # Get index of entity in matrix
    sel = np.where( data[:,ndx] != np.nan )  # Remove false/nan values
    return data[sel]

def average( data, entity ):
    '''Function calculates the average value for a given entity'''
    data = process_list( data, entity )  # Remove nan values
    ndx = daydata.ndx_ent(entity)  # Get index of entity in matrix
    ave  = np.average( data[:,ndx] )  # Calculate average
    return ave

def sum( data, entity ):
    '''Function calculates the sum value for a given entity'''
    data = process_list( data, entity )  # Remove nan values
    ndx = daydata.ndx_ent(entity)  # Get index of entity in matrix
    sum  = np.sum( data[:,ndx] )  # Calculate sum
    return sum

def max( data, entity ):
    '''Function gets maximum for a given entity'''
    data = process_list( data, entity )  # Remove nan values
    ndx = daydata.ndx_ent(entity)  # Get index of entity in matrix
    max = np.max( data[:,ndx] )  # Get max
    return max

def min( data, entity ):
    '''Function gets minimum for a given entity'''
    data = process_list( data, entity )  # Remove nan values
    ndx = daydata.ndx_ent(entity)  # Get index of entity in matrix
    min  = np.min( data[:,ndx] )  # Get min
    return min

def terms_days( data, entity, operator, value ):
    '''Function select days based on terms like TX > 30 for example'''
    ndx = daydata.ndx_ent(entity)  # Get index for entity in data matrix
    op  = operator.lower()  #  Make operator lowercase
    f   = df(value)  #  Make input value equal to data in matrix
    if is_operator(op):  # Check for allowed operator
        if   op in ['gt',  '>']:       sel = np.where( data[:,ndx] >  f )
        elif op in ['ge', '>=', '≥']:  sel = np.where( data[:,ndx] >= f )
        elif op in ['eq', '==']:       sel = np.where( data[:,ndx] == f )
        elif op in ['lt',  '<']:       sel = np.where( data[:,ndx] <  f )
        elif op in ['le', '<=', '≤']:  sel = np.where( data[:,ndx] <= f )
        elif op in ['ne', '!=', '<>']: sel = np.where( data[:,ndx] != f )
        else: print('error, terms_days()'); input('?')
    else:  # Wrong input
        print(f'Error. Operator {op} is unknown...')
    return data[sel]  # Return all days where the selected terms are true

def hellmann( data ):
    '''Function calculation hellmann in given data'''
    ent  = 'TG'  # Entity for hellman is TG
    data = process_list( data, ent )  # Remove nan values
    days = terms_days( data, ent, '<', 0.0 ) # Get all days TG < 0
    cnt  = np.size( days, axis=0 )  #  # Count days hellmann
    if cnt == 0:  #  No days found tg < 0
        hman = 0.0  # Hellmann is 0
    else: # Sum valus all days TG < 0.0
        som  = sum( days, ent )  # Calculate sum
        hman = abs( som )  # Make positive
    return hman

def ijnsen ( data ):
    '''Function calculates the cold number IJnsen:
       v = days: TN <  0
       y = days: TX <  0
       z = days: TN < -10
     '''
    TN = process_list( data, 'TN' )  # Remove nan values in TN
    TX = process_list( data, 'TX' )  # Remove nan values in TX
    v = np.size( terms_days( TN, 'TN', '<',  0.0 ), axis=0 )  # Count days TN lower 0
    y = np.size( terms_days( TX, 'TX', '<',  0.0 ), axis=0 )  # Count days TX lower 0
    z = np.size( terms_days( TN, 'TN', '<', -10.0 ), axis=0 )  # Count days TN lower -10
    ijnsen = (v * v / 363.0)  +  (2.0 * y / 3.0)  +  (10.0 * z / 9.0) # Calculate ijnsen
    return ijnsen

def heat_ndx( data ):
    '''Function calculates heat-ndx in given data'''
    ent  = 'TG'  # Entity for average temp
    ndx  = daydata.ndx_ent( ent )  # Get index for TG in matrix
    data = process_list( data, ent )  # Remove nan values
    data = terms_days( data, ent, '≥', 18 )  # All days with TG >= 18
    tg   = data[:,ndx]  #  Make TG list only
    heat = np.sum( tg - 180 )  # Sum heat above 18 degress
    return heat
