'''Library for plotting graphs'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.6"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config
import numpy as np
import knmi.model.stats as stats
import knmi.model.daydata as daydata
import knmi.view.fix as fix
import view.txt as view_txt
import view.translate as tr
import view.color as view_color
import model.utils as utils
import matplotlib.pyplot as plt
import model.convert as convert

def name( sd, ed, stations, entities, type='png' ):
    st = f'{sd}-{ed}-'
    for s in stations: st += f'{s.wmo}-'
    for s in entities: st += f'{s}-'
    st = st[:-1]

    return f'{st}.{type}'

def text_diff( l ):
    max = l.max()
    # div = max * 3.0

    return max / 30.0

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

def plot( stations, entities, sd, ed, title, ylable, path ):
    l_plot = []
    # Size values are inches. And figure always in front
    plt.figure( figsize=( convert.pixel_to_inch(config.plot_width),
                          convert.pixel_to_inch(config.plot_height)
                          ), dpi=config.plot_dpi )

    # Color handling
    rnd_col = True if len(stations) > 1 else False
    if rnd_col:
        col_list = view_color.save_colors
        np.random.shuffle( col_list )
        col_ndx = 0
        col_cnt = col_list.size - 1

    # Fonts are unused ? TODO
    font_dic = { 'family': 'calibri', 'color': 'gray', 'size' : 10.0 }
    font = {'family' : 'calibri', 'weight' : 'normal', 'size'   : 12}

    for station in stations:
        ok, data = daydata.read( station )
        if ok:
            data = stats.period( data, sd, ed )
            ymd  = data[:,daydata.ndx_ent('YYYYMMDD')].astype(np.str) # Convert to string

            for el in entities:
                ndx   = daydata.ndx_ent( el )
                datl  = data[:, ndx].tolist()
                val   = np.array( [fix.value(val, el) for val in datl] )
                label = f'{station.place} {view_txt.ent_to_title(el)}'
                color = col_list[col_ndx] if rnd_col else view_color.ent_to_color(el)

                if config.plot_graph_type == 'line':  # bar or line
                    plt.plot( ymd, val, label = label, color = color,
                              marker = 'o', linestyle = 'solid',
                              linewidth = 2, markersize = 4 )
                elif config.plot_graph_type == 'bar':
                    plt.bar( ymd, val, label = label, color = color )

                if rnd_col:
                    col_ndx = 0 if col_ndx == col_cnt else col_ndx + 1

                if config.plot_marker_txt in config.answer_yes:
                    diff = text_diff( val )
                    if config.plot_graph_type == 'bar': # No negative values for when graph is a bar
                        text = np.array( [fix.value(v, el) for v in datl] )
                    elif config.plot_graph_type == 'line':
                        text = np.array( [fix.ent(v, el) for v in datl] )

                    for d, v, t in zip( ymd, val, text ):
                        plt.text( d, v+diff, t, fontsize='x-small', color='#555555',
                                  horizontalalignment='center', verticalalignment='top',
                                  alpha=0.8 )
        else:
            print('Read not oke in graphs.py -> plot')

    plt.title( title )
    plt.xlabel( tr.txt('DATES'), color='#555555', fontsize='small', fontvariant='small-caps' )
    plt.ylabel( ylable, color='#555555', fontsize='small' )
    plt.grid( color='#cccccc', linestyle='dotted', linewidth=1 )
    plt.xticks( ymd, rotation=45, color='gray', fontsize='small' )
    # plt.style.use( 'mystyle' )
    plt.grid(True)
    plt.legend( loc='best', shadow=True, fontsize='small', frameon=False ) #
    plt.savefig( path, dpi=config.plot_dpi, format='png' )
    plt.tight_layout()
    plt.show( )
