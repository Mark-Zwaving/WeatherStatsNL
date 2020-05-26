'''Library for plotting graphs'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import numpy as np
from matplotlib import pyplot as plt
import knmi.model.stats as stats
import knmi.model.daydata as daydata
import view.txt as view_txt
import view.translate as view_tr

def name( sd, ed, station, entities, type='png' ):
    st = f'{sd}-{ed}-'
    for s in  station: st += f'{s}-'
    for s in entities: st += f'{s}-'

    return f'{st},{type}'

# 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight',
# 'ggplot', 'grayscale', 'seaborn-bright', 'seaborn-colorblind',
# 'seaborn-dark-palette', 'seaborn-dark', 'seaborn-darkgrid',
# 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper',
# 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks',
# 'seaborn-white', 'seaborn-whitegrid', 'seaborn', 'Solarize_Light2',
# 'tableau-colorblind10'

def plot( stations, entities, sd, ed, title='Graph Title', ylable=entities, size=(14,8) ):
    ok, data = daydata.read( stations[0] )
    ymd = data[:,daydata.ndx_entity('YYYYMMDD')]
    plt.figure( figsize=size ) )  # Values are inches!
    plt.xlabel( view_tr('Dates'), color='#777777')
    plt.ylabel( ylable, color='#777777')
    plt.style.use('fivethirtyeight')

    for el in entities:
        ents = data[:,daydata.ndx_entity(el)]
        label = f'{el}-{view_txt.ent_to_title(el)}'
        color =
        plt.plot( ymd, ents, label=label, color='red', marker='o', linestyle='solid', linewidth=1, markersize=3 )
        plt.grid( color='#bbbbbb', linestyle='dotted', linewidth=1 )



    plt.xticks( ymd, rotation=38 ) # https://stackoverflow.com/questions/12608788/changing-the-tick-frequency-on-x-or-y-axis-in-matplotlib
    plt.legend()
    if ok:


    res_station = array( [] )
    for station in stations:

        if ok:
            res_station =
            data = stats.period( data, sd, ed )
            ents = []


ymd = etmgeg[:,1].astype(np.str) # Convert to string
tx  = etmgeg[:,14] / 10.0
tg  = etmgeg[:,11] / 10.0
tn  = etmgeg[:,12] / 10.0




    ymd = daydata.ndx_entity('YYYYMMDD')
    sel = np.where(( data[:,ymd] >= int(sdate) ) & ( data[:,ymd] < int(edate) ))
    return data[sel]

# TODO: check for -1 values -> replace with <0.05?
def process_list( data, entity ):
