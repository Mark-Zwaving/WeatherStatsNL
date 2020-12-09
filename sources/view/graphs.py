'''Library for plotting graphs'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1.0"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import config, math
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import sources.model.stats as stats
import sources.model.daydata as daydata
import sources.model.utils as utils
import sources.model.convert as convert
import sources.view.fix as fix
import sources.view.txt as vt
import sources.view.color as vcol
import sources.view.log as log

def text_diff( l ):
    mp, mm = max(l), min(l)
    return (mp - mm) / 20.0

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

def plot( stations, entities, period, title, ylabel, fname, options ):
    # # Make option list
    # graph_options = {
    #     "plot_width"       = config.plot_width,
    #     "plot_height"      = config.plot_height,
    #     "plot_graph_type"  = config.plot_graph_type,
    #     "plot_line_width"  = config.plot_line_width,
    #     "plot_marker_size" = config.plot_marker_size,
    #     "plot_cummul_val"  = config.plot_cummul_val,
    #     "plot_marker_txt"  = config.plot_marker_txt,
    #     "plot_climate_ave" = config.plot_climate_ave,
    #     "plot_image_type"  = config.plot_image_type,
    #     "plot_dpi"         = config.plot_dpi
    # }

    if utils.is_yes(options['plot_climate_ave']):
        log.console('Calculating climate data might take a while...\n', True)

    path = utils.mk_path( config.dir_img_period, fname + f'.{config.plot_image_type}' )

    # Size values are inches. And figure always in front
    plt.figure( figsize=( convert.pixel_to_inch(options['plot_width']),
                          convert.pixel_to_inch(options['plot_height'])
                          ), dpi=options['plot_dpi'] )

    # Color handling
    rnd_col = True if len(stations) > 1 else False
    if rnd_col:
        col_list = utils.shuffle_list(vcol.save_colors, level=2)
        col_ndx, col_cnt = 0, len(col_list) - 1

    min, max = config.fl_min, config.fl_max
    for station in stations:
        log.console(f'Calculate weatherdata for {station.place}', True)
        ok, data = daydata.read( station )
        if ok:
            days = daydata.period( data, period )
            ymd = days[:, daydata.ndx_ent('YYYYMMDD')].astype(
                            np.int, copy=False
                            ).astype(
                                np.str, copy=False
                                ).tolist() # Convert to list

            for ent in entities:
                # Get the values needed for the graph
                f_val = days[:, daydata.ndx_ent(ent)]
                # Cumulative sum of values, if chosen
                if utils.is_yes(options['plot_cummul_val']):
                    f_val = np.cumsum( f_val )

                # Min/ max for ranges
                min_act = fix.rounding( np.min(f_val), ent )
                max_act = fix.rounding( np.max(f_val), ent )
                if min_act < min: min = min_act
                if max_act > max: max = max_act

                # Make correct output values
                l_val = [ fix.rounding(v, ent) for v in f_val.tolist() ]
                label = f'{station.place} {vt.ent_to_title(ent)}'
                color = col_list[col_ndx] if rnd_col else vcol.ent_to_color(ent)

                if utils.is_yes(options['plot_climate_ave']):
                    l_clima = []
                    label_clima = f'Day climate {station.place} {vt.ent_to_title(ent)}'
                    clima_ymd = days[:, daydata.YYYYMMDD ].astype(
                                        np.int, copy=False ).astype(
                                        np.str, copy=False ).tolist()
                    cli_txt = f"Calculate climate data '{ent.upper()}' for {station.place}"
                    log.console(cli_txt, True)
                    for d in clima_ymd:
                        mmdd = d[4:8] # What day it is ?
                        sdat = datetime.strptime(d, '%Y%m%d').strftime('%B %d').lower()
                        log.console(f'Calculate climate {ent} for day {sdat}')
                        clima_val = stats.climate_day( station, mmdd, ent,
                                                 options['plot_climate_per']
                                                 )
                        clima_rounded = fix.rounding( clima_val, ent )
                        log.console(f'Calculated clima value {ent} for {sdat} is {clima_rounded}\n')
                        # Append with correct rounding
                        l_clima.append( clima_rounded )

                    log.console(' ')

                if options['plot_graph_type'] == 'line':  # bar or line
                    plt.plot( ymd, l_val, label = label,
                              color      = color,
                              marker     = config.plot_marker_type,
                              linestyle  = config.plot_line_style,
                              linewidth  = options['plot_line_width'],
                              markersize = options['plot_marker_size'] )

                    if utils.is_yes(options['plot_climate_ave']):
                        plt.plot(ymd, l_clima, label = label_clima,
                                 color      = color,
                                 marker     = config.plot_clima_marker_type,
                                 linestyle  = config.plot_clima_line_style,
                                 linewidth  = config.plot_clima_line_width,
                                 markersize = config.plot_clima_marker_size )

                elif options['plot_graph_type'] == 'bar':
                    plt.bar( ymd, l_val, label = label, color = color )

                    if utils.is_yes(options['plot_climate_ave']):
                        plt.bar(ymd, l_clima, label=label_clima, color=color)

                if rnd_col:
                    col_ndx = 0 if col_ndx == col_cnt else col_ndx + 1

                if utils.is_yes(options['plot_marker_txt']):
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

                    if utils.is_yes(options['plot_climate_ave']):
                        for d, v, t in zip( ymd, l_clima, l_clima ):
                            plt.text( d, v+diff, t,
                                      color=config.plot_marker_color,
                                      **config.plot_marker_font,
                                      horizontalalignment=config.plot_marker_horizontalalignment,
                                      verticalalignment=config.plot_marker_verticalalignment,
                                      alpha=config.plot_marker_alpha
                                    )
        else:
            log.console('Read not oke in graphs.py -> plot')

    if config.plt_style != False:
        plt.style.use(config.plt_style)

    plt.title( title,
               color=config.plot_title_color,
               **config.plot_title_font
            )

    plt.xlabel( config.plot_xlabel_text,
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
                  linewidth=config.plot_grid_linewidth )

    diff_max = max*0.1
    diff_max = 1.5 if diff_max < 1.5 else diff_max
    max  = math.ceil( max + diff_max )  # 10% upperrange extra
    min  = math.floor( min*0.98 ) #  2% underrange extra
    diff = max - min
    step = math.floor(diff/10-0.5)
    step = 1 if step == 0 else step

    yticks = np.arange( min, max, step ) # 1-10 % ranges
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

    if utils.is_yes(config.plot_tight_layout):
        plt.tight_layout( )

    plt.savefig( path, dpi=options['plot_dpi'], format=options['plot_image_type'] )

    if utils.is_yes(config.plot_show):
        plt.show()

    return path
