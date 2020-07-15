'''Library for plotting graphs'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.9"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config
import numpy as np
import matplotlib.pyplot as plt
import model.stats as stats
import model.daydata as daydata
import model.utils as utils
import model.convert as convert
import view.fix as fix
import view.txt as view_txt
import view.translate as tr
import view.color as view_color

def text_diff( l ):
    m = max(l)
    # div = max * 3.0

    return m / 30.0

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

def plot( stations, entities, period, title, ylabel, path, options ):
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

    min, max = 99999999.9, -99999999.9
    for station in stations:
        ok, data = daydata.read( station )
        if ok:
            data = daydata.period( data, period )
            ymd = data[:,daydata.ndx_ent('YYYYMMDD')].astype(
                            np.int, copy=False
                            ).astype(
                                np.str, copy=False
                                ).tolist() # Convert to string

            for el in entities:
                # Get the values needed for the graph
                ndx   = daydata.ndx_ent(el)
                f_val = data[:, ndx]
                # Cumulative sum of values, if chosen
                if config.plot_cummul_val in config.answer_yes:
                    f_val = np.cumsum( f_val )

                # Min/ max for ranges
                min_act = fix.rounding(np.min(f_val), el)
                max_act = fix.rounding(np.max(f_val), el)
                if min_act < min: min = min_act
                if max_act > max: max = max_act

                # Make correct output values
                l_val = [ fix.rounding(v, el) for v in f_val.tolist() ]

                label = f'{station.place} {view_txt.ent_to_title(el)}'
                color = col_list[col_ndx] if rnd_col else view_color.ent_to_color(el)

                if config.plot_graph_type == 'line':  # bar or line
                    plt.plot( ymd, l_val, label = label, color = color,
                              marker = 'o', linestyle = 'solid',
                              linewidth  = config.plot_line_width,
                              markersize = config.plot_marker_size
                              )
                elif config.plot_graph_type == 'bar':
                    plt.bar( ymd, l_val, label = label, color = color )

                if rnd_col:
                    col_ndx = 0 if col_ndx == col_cnt else col_ndx + 1

                if config.plot_marker_txt in config.answer_yes:
                    diff = text_diff( l_val ) # based on maximum value
                    # TODO No negative values for when graph is a bar
                    text = l_val

                    for d, v, t in zip( ymd, l_val, text ):
                        plt.text( d, v+diff, t,
                                  color=config.plot_marker_color,
                                  **config.plot_marker_font,
                                  horizontalalignment=config.plot_marker_horizontalalignment,
                                  verticalalignment=config.plot_marker_verticalalignment,
                                  alpha=config.plot_marker_alpha
                                )
        else:
            print('Read not oke in graphs.py -> plot')

    if config.plt_style != False:
        plt.style.use(config.plt_style)

    plt.title( title,
               color=config.plot_title_color,
               **config.plot_title_font
            )

    plt.xlabel( tr.txt(config.plot_xlabel_text),
                color=config.plot_xlabel_color,
                **config.plot_xlabel_font,
                )

    plt.ylabel( ylabel,
                color=config.plot_ylabel_color,
                **config.plot_ylabel_font
                )

    plt.grid( config.plot_grid_on )
    if config.plot_grid_on:
        plt.grid( color=config.plot_grid_color,
                  linestyle=config.plot_grid_linestyle,
                  linewidth=config.plot_grid_linewidth
                  )

    yticks = np.arange( int(min*0.99), int(max*1.1) ) # 1-10 % ranges
    plt.yticks( yticks,
                **config.plot_xas_font,
                color=config.plot_xas_color
                )

    plt.xticks( ymd,
                **config.plot_xas_font,
                color=config.plot_xas_color,
                rotation=config.plot_xas_rotation
                )

    plt.legend( loc=config.plot_legend_loc,
                fontsize=config.plot_legend_fontsize,
                facecolor=config.plot_legend_facecolor,
                shadow=config.plot_legend_shadow,
                frameon=config.plot_legend_frameon,
                fancybox=config.plot_legend_fancybox
                )

    plt.savefig( path,
                 dpi=config.plot_dpi,
                 format=config.plot_image_type
                 )

    plt.tight_layout( )
    plt.show( )
