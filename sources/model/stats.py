# -*- coding: utf-8 -*-
'''Library contains classes and functions for calculating statistics'''
__author__     =  'Mark Zwaving'
__email__      =  'markzwaving@gmail.com'
__copyright__  =  'Copyright 2020 (C) Mark Zwaving. All rights reserved.'
__license__    =  'GNU Lesser General Public License (LGPL)'
__version__    =  '0.1.1'
__maintainer__ =  'Mark Zwaving'
__status__     =  'Development'

import config
import numpy as np
import numpy.ma as ma
import sources.model.daydata as daydata
import sources.view.console as console

# All allowed input operators
operators = np.array( [
    'lt', '<', 'le', '<=', '≤',
    'gt', '>', 'ge', '>=', '≥',
    'eq', '==', 'ne', '!=', '<>',
    'or', '||', 'and', '&&'
    ] )

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

def climate_average_for_day( station, mmdd, ent, period ):
    '''Function calculate climate averages for a day for a station'''
    ys, ye = period.split('-')  # Get climate years
    per  = f'{ys}{mmdd}-{ye}*{mmdd}'  # Special period for a day during the years
    d1 = daydata.read_station_period( station, per )  # Get all the days in clima period
    d2 = process_list( d1[1], ent )  # Remove nan values
    # print('D1: ' + str(d1))
    # print('D2: ' + str(d2))
    # HACK for sel_period. Because of added mask
    # data = data[1]
    ave = average( d2, ent )  # Calculate averages
    # print(ave)
    return ave

def process_list( data, entity ):
    '''Function processes data values on false values'''
    ndx = daydata.ndx_ent( entity )  # Get index of entity in matrix
    d1 = data[:,ndx]
    sel = np.where( d1 != np.isnan(d1) )  # Remove false/nan values
    return data[sel]

    # d1 = data[:,ndx]
    # sel = np.where( d1 != d1[np.isnan(d1)] )  # Remove false/nan values

def process_list_1d( data, entity ):
    '''Function processes data values on false values'''
    ndx = daydata.ndx_ent(entity)  # Get index of entity in matrix
    d1 = data[:, ndx]
    d2 = d1[~np.isnan(d1)] # Remove nan
    return d2

def average( data, entity ):
    '''Function calculates the average value for a given entity'''
    d = process_list_1d( data, entity )  # Remove nan values
    ave  = np.average( d )  # Calculate average
    return ave

def sum( data, entity ):
    '''Function calculates the sum value for a given entity'''
    d = process_list_1d( data, entity )  # Remove nan values
    sum  = np.sum( d )  # Calculate sum
    return sum

def max( data, entity ):
    '''Function gets maximum for a given entity'''
    d = process_list_1d( data, entity )  # Remove nan values
    max  = np.max( d )  # Get max
    return max

def min( data, entity ):
    '''Function gets minimum for a given entity'''
    d = process_list_1d( data, entity )  # Remove nan values
    min  = np.min( d )  # Get min
    return min

def sort( data, entity, reverse=False ):
    '''Function sorts data based on entity'''
    data = process_list( data, entity )  # Remove nan values
    ndx  = daydata.ndx_ent(entity)  # Get index of entity in matrix
    data = data[data[:,ndx].argsort()] # Sort the matrix based on ndx. Low to high
    if not reverse: data = np.flip(data, axis=0) # Reverse the matrix (if asked)

    return data

def df(val, entity):
    f, e = float(val), entity.upper()
    if e in ['TX', 'TG', 'TN', 'FG', 'FHX', 'FHN', 'FXX', 'DR',
             'FHVEC', 'SQ', 'RH', 'RHX', 'PG', 'PX', 'PN', 'EV24'
             ]:
        return f * 10.0
    elif e in ['YYYYMMDD', 'STN', 'DDVEC', 'SP', 'Q', 'VVN', 'VVX', 'NG', 'UG',
               'UX', 'UN', 'FHXH', 'FHNH', 'FXXH', 'TNH', 'TXH', 'T10NH',
               'RHXH', 'PXH', 'PNH', 'VVNH', 'VVXH', 'UXH', 'UNH'
               ]:
        return f
    return f

def terms_days( data, entity, operator, value ):
    '''Function select days based on terms like TX > 30 for example'''
    ndx = daydata.ndx_ent(entity)  # Get index for entity in data matrix
    op  = operator.lower()  #  Make operator lowercase
    f   = df(value, entity)  #  Make input value equal to data in matrix
    if is_operator(op):  # Check for allowed operator
        if   op in ['gt',  '>']:       sel = np.where( data[:,ndx] >  f )
        elif op in ['ge', '>=', '≥']:  sel = np.where( data[:,ndx] >= f )
        elif op in ['eq', '==']:       sel = np.where( data[:,ndx] == f )
        elif op in ['lt',  '<']:       sel = np.where( data[:,ndx] <  f )
        elif op in ['le', '<=', '≤']:  sel = np.where( data[:,ndx] <= f )
        elif op in ['ne', '!=', '<>']: sel = np.where( data[:,ndx] != f )
        else:
            console.log(f'Error in operator {op} in terms for day...')
    else:  # Wrong input
        console.log(f'Error. Operator {op} is unknown...')

    return data[sel]  # Return all days where the selected terms are true

def hellmann( data ):
    '''Function calculation hellmann in given data'''
    ent  = 'TG'  # Entity for hellman is TG
    data = process_list( data, ent )  # Remove nan values
    days = terms_days( data, ent, '<', 0.0 ) # Get all days TG < 0
    cnt  = np.size( days, axis=0 )  # Count days hellmann

    hman = 0.0
    if cnt > 0:  # Sum valus all days TG < 0.0
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

def frost_sum(data):
    '''Function calculates frost sum:
       Add min and max temp during a day only if TX < 0 or TN < 0
       IE: TX=-1.0 and TN=-5.0 => 6.0 '''
    TN   = process_list( data, 'TN' )  # Remove nan values in TN
    TX   = process_list( data, 'TX' )  # Remove nan values in TX
    tn_0 = terms_days( TN, 'TN', '<',  0.0 )  # All days TN < 0
    tx_0 = terms_days( TX, 'TX', '<',  0.0 )  # All days TX < 0
    tn_cnt = np.size( tn_0, axis=0 ) # Count tn days < 0
    tx_cnt = np.size( tx_0, axis=0 ) # Count tx days < 0

    frostie = 0.0
    if tn_cnt > 0:
       ndx = daydata.ndx_ent('TN')  # Get index for TN in matrix
       tn  = tn_0[:,ndx]  #  Make TN list only
       frostie += abs( np.sum(tn) )
    if tx_cnt > 0:
       ndx = daydata.ndx_ent( 'TX' )  # Get index for TX in matrix
       tx  = tx_0[:,ndx]  #  Make TX list only
       frostie += abs( np.sum(tx) )

    return frostie

def heat_ndx( data ):
    '''Function calculates heat-ndx in given data'''
    ent  = 'TG'  # Entity for average temp
    ndx  = daydata.ndx_ent( ent )  # Get index for TG in matrix
    data = process_list( data, ent )  # Remove nan values
    data = terms_days( data, ent, '≥', 18 )  # All days with TG >= 18
    tg   = data[:,ndx]  #  Make TG list only

    heat = 0.0
    tg_cnt = np.size( tg, axis=0 ) # Count tg days >= 18
    if tg_cnt > 0:
        heat = np.sum( tg - 180 )  # Sum heat above 18 degress

    return heat
