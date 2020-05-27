'''Library for plotting graphs'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1.0"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import numpy as np
import knmi.model.stats as stats
import knmi.model.daydata as daydata
import knmi.view.fix as fix
import view.txt as view_txt
import view.translate as tr
import view.color as view_color
import model.utils as utils
import matplotlib.pyplot as plt

def name( sd, ed, stations, entities, type='png' ):
    st = f'{sd}-{ed}-'

    for s in stations:
        st += f'{s.wmo}-'
    for s in entities:
        st += f'{s}-'

    return f'{st}.{type}'

# 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight',
# 'ggplot', 'grayscale', 'seaborn-bright', 'seaborn-colorblind',
# 'seaborn-dark-palette', 'seaborn-dark', 'seaborn-darkgrid',
# 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper',
# 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks',
# 'seaborn-white', 'seaborn-whitegrid', 'seaborn', 'Solarize_Light2',
# 'tableau-colorblind10'

class G:
    x          = np.array([])
    y          = np.array([])
    color      = 'green'
    label      = 'legend'
    marker     = 'o'
    linestyle  = 'solid'
    linewidth  = 1
    markersize = 3

    def __init__(self):
        pass

def plot( stations, entities, sd, ed, title, ylable, size, path ):
    l_plot = []
    # ymd = np.array(utils.list_dates_range(sd, ed)).astype(np.str) # Convert to string

    plt.figure( figsize=size )  # Values are inches! And figure always in front
    for station in stations:
        ok, data = daydata.read( station )
        if ok:
            data = stats.period( data, sd, ed )
            ymd  = data[:,daydata.ndx_ent('YYYYMMDD')].astype(np.str) # Convert to string
            for el in entities:
                ndx = daydata.ndx_ent( el )
                plt.plot( ymd,
                          np.array( [fix.value(val, el) for val in data[:, ndx].tolist()] ),
                          label = f'{station.place} {view_txt.ent_to_title(el)}',
                          color = view_color.ent_to_color(el),
                          marker = 'o',
                          linestyle = 'solid',
                          linewidth = 2,
                          markersize = 4
                    )

    plt.title( title )
    plt.xlabel( tr.txt('Dates'), color='#333333' )
    plt.ylabel( ylable, color='#333333' )
    plt.grid( color='#dddddd', linestyle='dotted', linewidth=1 )
    plt.xticks( ymd, rotation=40, color='#777777' )
    # plt.style.use( 'fivethirtyeight' )
    plt.tight_layout( )
    plt.legend(loc='best', shadow=True)
    plt.savefig(path)
    # plt.show( )
