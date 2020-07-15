# -*- coding: utf-8 -*-
'''Functions for cleaning fix data for output'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.8"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config
import numpy as np
import view.translate as tr
import model.utils as utils
import model.convert as cvt

def value(val, entity):
    '''Function turns data from etmgeg into the real values'''
    if utils.isnan(val) or val == config.knmi_dayvalues_dummy_val:
        return val

    f = float(val)
    e = entity.strip().lower()

    # Exception for -1 in rh,rhx and sq
    if f == -1.0 and (e in ['rh', 'rhx', 'sq']):
        return config.knmi_dayvalues_low_measure_val

    # Indexes
    elif e in ['heat_ndx', 'hellmann']:
        return f / 10.0

    elif e in ['ijnsen']:
        return f

    # Temperatures
    elif e in [ 'tx', 'tn', 'tg', 't10n' ]:
        return f / 10.0

    # Airpressure
    elif e in [ 'pg', 'pn', 'px' ]:
        return f / 10.0

    # Radiation
    elif e in [ 'q' ]:
        return f / 10.0

    # Percentages
    elif e in [ 'ug', 'ux', 'un', 'sp' ]:
        return f

    # Time hours
    elif e in [ 'fhxh', 'fhnh', 'fxxh', 'tnh', 'txh', 'rhxh',
                'pxh', 'vvnh', 'vvxh', 'uxh', 'unh', 'pnh' ]:
        return f

    # Time 6 hours
    elif e in [ 't10nh' ]:
        return f

    # CLouds cover/octants
    elif e in [ 'ng' ]:
        return f

    # Wind
    elif e in [ 'fhvec','fg','fhx','fhn','fxx' ]:
        return f / 10.0

    # Evapotranspiration
    elif e in [ 'ev24', 'rh', 'rhx' ]:
        return f / 10.0

    # Duration hours
    elif e in [ 'sq', 'dr' ]:
        return f / 10.0

    # Wind direction
    elif e in  [ 'ddvec' ]:
        return f

    # View distance
    elif e in [ 'vvn', 'vvx' ]:
        return f

    return f  # Happens for dummy values

def rounding(val, entity):
    '''Function turns data from etmgeg into the real values'''
    if utils.isnan(val) or val == config.knmi_dayvalues_dummy_val:
        return val

    e = entity.strip().lower()
    f = value(val, e)

    # Indexes
    if e in ['heat_ndx', 'hellmann']:
        return round(f)

    # IJnsen
    elif e in ['ijnsen']:
        return round(f,1)

    # Temperatures
    elif e in [ 'tx', 'tn', 'tg', 't10n' ]:
        return round(f,1)

    # Airpressure
    elif e in [ 'pg', 'pn', 'px' ]:
        return round(f,1)

    # Radiation
    elif e in [ 'q' ]:
        return round(f,1)

    # Percentages
    elif e in [ 'ug', 'ux', 'un', 'sp' ]:
        return round(f)

    # Time hours
    elif e in [ 'fhxh', 'fhnh', 'fxxh', 'tnh', 'txh', 'rhxh',
                'pxh', 'vvnh', 'vvxh', 'uxh', 'unh', 'pnh' ]:
        return round(f)

    # Time 6 hours
    elif e in [ 't10nh' ]:
        return round(f)

    # CLouds cover/octants
    elif e in [ 'ng' ]:
        return round(f)

    # Wind
    elif e in [ 'fhvec','fg','fhx','fhn','fxx' ]:
        return round(f,1)

    # Evapotranspiration
    elif e in [ 'ev24', 'rh', 'rhx' ]:
        return round(f,1)

    # Duration hours
    elif e in [ 'sq', 'dr' ]:
        return round(f,1)

    # Wind direction
    elif e in  [ 'ddvec' ]:
        return round(f)

    # View distance
    elif e in [ 'vvn', 'vvx' ]:
        return round(f,1)

    return f  # Happens for dummy values

def ent(val, entity):
    '''Function adds correct post/prefixes for weather entities'''

    # No measurement or false measurement
    if utils.isnan(val) or val == config.knmi_dayvalues_dummy_val:
        return config.no_data_given

    e = entity.strip().lower()
    f = value(val, e)

    # Indexes
    if e in ['heat_ndx', 'hellmann']:
        return f'{f:.0f}'

    elif e in ['ijnsen']:
        return f'{f:.1f}'

    # Temperatures
    elif e in [ 'tx', 'tn', 'tg', 't10n' ]:
        return f'{f:.1f}°C'

    # Airpressure
    elif e in [ 'pg', 'pn', 'px' ]:
        return f'{f:.0f}hPa'

    # Radiation
    elif e in [ 'q' ]:
        return f'{f:.1f}J/cm2'

    # Percentages
    elif e in [ 'ug', 'ux', 'un', 'sp' ]:
        return f'{f:.0f}%'

    # Time hours
    elif e in [ 'fhxh', 'fhnh', 'fxxh', 'tnh', 'txh', 'rhxh',
                  'pxh', 'vvnh', 'vvxh', 'uxh', 'unh', 'pnh' ]:
        f1 = f'{f:.0f}'
        f2 = f'{(f-1):.0f}'
        return f'{f2}-{f1} {tr.txt("hour")}'

    # Time 6 hours
    elif e in [ 't10nh' ]:
        f1 = f'{f:.0f}'
        f2 = f'{(f-6):.0f}'
        return f'{f2}-{f1} {tr.txt("hour")}'

    # CLouds cover/octants
    elif e in [ 'ng' ]:
        return f'{f:.0f}'

    # Wind
    elif e in [ 'fhvec','fg','fhx','fhn','fxx' ]:
        bft = cvt.ms_to_bft(val)
        return f'{f:.1f}m/s {bft}bft'

    # Evapotranspiration
    elif e in [ 'ev24', 'rh', 'rhx' ]:
        return f'{f:.1f}mm'

    # Duration hours
    elif e in [ 'sq', 'dr' ]:
        return f'{f:.0f} {tr.txt("hour")}'

    # Wind direction
    elif e in  [ 'ddvec' ]:
        if f == 0.0:
            return f'{f:.0f}° {tr.txt(VAR)}'
        else:
            # From degrees to direction
            # Source: https://www.campbellsci.com/blog/convert-wind-directions
            ldir = [ 'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S',
                     'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N' ]
            ndx = int( round( f % 360 / 22.5 ) )
            dir = ldir[ndx]
            return f'{f:.0f}° {tr.txt(dir)}'

    # View distance
    elif e in [ 'vvn', 'vvx' ]:
        if f == 0.0:
            return '<100m'
        else:
            if f < 49.0:
                f1 = f * 100.0
                f2 = (f + 1.0) * 100.0
                return f'{f1:.0f}-{f2:.0f}m'
            elif f == 50.0:
                return '5-6km'
            elif f <= 79.0:
                f1 = f - 50.0
                f2 = f - 49.0
                return f'{f1:.0f}-{f2:.0f}km'
            elif f <= 89.0:
                f1 = f - 50.0
                f2 = f - 45.0
                return f'{f1:.0f}-{f2:.0f}km'
            else:
                return '>70km'

    return f  # Without string casting will give an error with unknowm data entity