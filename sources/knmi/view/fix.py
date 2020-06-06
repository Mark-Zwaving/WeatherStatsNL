# -*- coding: utf-8 -*-
'''Functions for cleaning fix data for output'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.4"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import view.translate as tr
import model.convert as cvt

def value(val, entity):
    ent = entity.strip().lower()
    # Indexes
    if ent in ['heat_ndx', 'hellmann']: return round(val / 10.0, 1)
    # Temperatures
    elif ent in [ 'tx', 'tn', 'tg', 't10n' ]: return round( float(val) / 10.0, 1 )
    # Airpressure
    elif ent in [ 'pg', 'pn', 'px' ]: return round( float(val) / 10.0 )
    # Radiation
    elif ent in [ 'q' ]: return round( float(val) / 10.0, 1 )
    # Percentages
    elif ent in [ 'ug', 'ux', 'un', 'sp' ]: return round(val)
    # Time hours
    elif ent in [ 'fhxh', 'fhnh', 'fxxh', 'tnh', 'txh', 'rhxh',
                  'pxh', 'vvnh', 'vvxh', 'uxh', 'unh', 'pnh' ]: return round(val)
    # Time 6 hours
    elif ent in [ 't10nh' ]: return round(val)
    # CLouds cover/octants
    elif ent in [ 'ng' ]: return round(val)
    # Wind
    elif ent in [ 'fhvec','fg','fhx','fhn','fxx' ]: return round( float(val) / 10.0, 1 )
    # Evapotranspiration
    elif ent in [ 'ev24', 'rh', 'rhx' ]:
        if val == -1:
        	return 0.05
        else:
            return round( float(val) / 10.0, 1)
    # Duration hours
    elif ent in [ 'sq', 'dr' ]:
        if val == -1:
            return 0.05
        else:
            return round( float(val) / 10.0, 1)

    # Wind direction
    elif ent in  [ 'ddvec' ]: return round(val)
    # View distance
    elif ent in [ 'vvn', 'vvx' ]: return round(val)

    return round(val)

def ent(val, entity):
    '''Function adds correct post/prefixes for weather entities'''
    ent = entity.strip().lower()
    val = value(val, entity)

    # Indexes
    if ent in ['heat_ndx', 'hellmann']:
        return str(val)

    # Temperatures
    elif ent in [ 'tx', 'tn', 'tg', 't10n' ]:
        return f'{val}°C'

    # Airpressure
    elif ent in [ 'pg', 'pn', 'px' ]:
        return f'{val}hPa'

    # Radiation
    elif ent in [ 'q' ]:
        return f'{val}J/cm2'

    # Percentages
    elif ent in [ 'ug', 'ux', 'un', 'sp' ]:
        return f'{val}%'

    # Time hours
    elif ent in [ 'fhxh', 'fhnh', 'fxxh', 'tnh', 'txh', 'rhxh',
                  'pxh', 'vvnh', 'vvxh', 'uxh', 'unh', 'pnh' ]:
        return f'{val-1}-{val} {tr.txt("hour")}'

    # Time 6 hours
    elif ent in [ 't10nh' ]:
        return f'{val-6}-{val} {tr.txt("UT")}'

    # CLouds cover/octants
    elif ent in [ 'ng' ]:
        return str(val)

    # Wind
    elif ent in [ 'fhvec','fg','fhx','fhn','fxx' ]:
        bft = cvt.ms_to_bft(val)
        return f'{val}m/s {bft}bft'

    # Evapotranspiration
    elif ent in [ 'ev24', 'rh', 'rhx' ]:
        return f'{val}mm'

    # Duration hours
    elif ent in [ 'sq', 'dr' ]:
        return f'{val} {tr.txt("hour")}'

    # Wind direction
    elif ent in  [ 'ddvec' ]:
        if val == 0:
            return f'{val} {tr.txt(VAR)}'
        else:
            # From degrees to direction
            # Source: https://www.campbellsci.com/blog/convert-wind-directions
            ldir = [ 'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S',
                     'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N' ]
            ndx = int(round(val % 360 / 22.5))
            return f'{val}° {tr.txt(ldir[ndx])}'

    # View distance
    elif ent in [ 'vvn', 'vvx' ]:
        if val == 0:
            return '<100m'
        else:
            if val < 49:
                i2 = val + 1
                return f'{val*100}-{i2*100}m'
            elif val == 50:
                return '5-6km'
            elif val <= 79:
                i1, i2 = val - 50, val - 49
                return f'{i1}-{i2}km'
            elif val <= 89:
                i1, i2 = val - 50, val - 45
                return f'{i1}-{i2}km'
            else:
                return '>70km'

    return val  # Without string casting will give an error with unknowm data entity
