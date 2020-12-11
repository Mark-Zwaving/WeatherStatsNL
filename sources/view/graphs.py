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
    return (mp - mm) / 10.0

def plot( stations, entities, period, title, ylabel, fname, options ):
    if utils.is_yes(options['plot_climate_ave']):
        log.console('Calculating climate values for days might take a while...\n', True)

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

    period_extremes, clima_averages = list(), list()
    for station in stations:
        log.console(f'Calculate weatherdata for {station.place}', True)
        ok, data = daydata.read(station)
        if ok:
            days = daydata.period(data, period)
            ymd = days[:, daydata.ndx_ent('YYYYMMDD')].astype(
                            np.int, copy=False
                            ).astype( np.str, copy=False
                            ).tolist() # Convert to list
            s_ymd, e_ymd = ymd[0], ymd[-1]
            sy, sm, sd  = s_ymd[0:4], s_ymd[4:6], s_ymd[6:8]
            ey, em, ed  = e_ymd[0:4], e_ymd[4:6], e_ymd[6:8]

            cs_ymd, ce_ymd = options['plot_climate_per'].split('-')
            scy, ecy = cs_ymd[0:4], ce_ymd[0:4]

            for ent in entities:
                ent = ent.upper()
                # Get the values needed for the graph
                f_val = days[:, daydata.ndx_ent(ent)]
                log.console(f'{ent} data values: {str(f_val)}')

                if utils.is_yes( options['plot_min_max_ave_period'] ):
                    # Calculate extremes
                    min_per = stats.min(days, ent) # slow
                    max_per = stats.max(days, ent)
                    ave_per = stats.average(days, ent)
                    # Correct output
                    s_max = f'highest={fix.ent(max_per, ent)}'
                    s_min = f'lowest={fix.ent(min_per, ent)}'
                    s_ave = f'average={fix.ent(ave_per, ent)}'
                    s_ext  = f'For {sy}-{sm}-{sd} to {ey}-{em}-{ed} '
                    s_ext += f'{ent} {s_max}, {s_min} & {s_ave}'
                    period_extremes.append( s_ext )
                    log.console(s_ext)

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
                    label_clima = f'Day climate {station.place} {vt.ent_to_title(ent)}'
                    clima_ymd = days[:, daydata.YYYYMMDD ].tolist()
                    cli_txt = f"Calculate climate value '{ent}' for {station.place}"
                    log.console(cli_txt, True)

                    l_clima = [] # numpy array
                    for d in clima_ymd:
                        ds =  utils.f_to_s(d)
                        mmdd = ds[4:8] # What day it is ?
                        sdat = datetime.strptime(ds, '%Y%m%d').strftime('%B %d').lower()
                        val  = stats.climate_average_for_day(
                                        station, mmdd, ent, options['plot_climate_per']
                                    )
                        s_clima = fix.rounding(val, ent)
                        log.console(f'Climate value {ent} for {sdat} is {s_clima}')
                        # Append raw data without correct rounding
                        l_clima.append(val)

                    if utils.is_yes( options['plot_min_max_ave_period'] ):
                        # Clima average round correctly based on entity
                        if len(l_clima) > 0:
                            # Calculate average
                            sum = 0.0
                            for el in l_clima:
                                sum += el
                            ave = sum / len(l_clima)
                            s_ave  = f'Climate average {ent} from '
                            s_ave += f'{sm}-{sd} to {em}-{ed} for the '
                            s_ave += f'years {scy} through {ecy} '
                            s_ave += f'is {fix.ent(ave, ent)}'
                            clima_averages.append(s_ave)
                            log.console(s_ave)
                        else:
                            log.console('List with clima values is empthy.')

                    # Round correctly al climate values based on ent
                    for ndx, val in enumerate(l_clima):
                        l_clima[ndx] = fix.rounding( val, ent )

                    log.console(' ')

                if options['plot_graph_type'] == 'line':  # bar or line
                    plt.plot(ymd, l_val,
                              label = label,
                              color      = color,
                              marker     = config.plot_marker_type,
                              linestyle  = config.plot_line_style,
                              linewidth  = options['plot_line_width'],
                              markersize = options['plot_marker_size'] )

                    if utils.is_yes(options['plot_climate_ave']):
                        plt.plot(ymd, l_clima,
                                 label = label_clima,
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

    diff_max = abs(max * 0.10)  # 10% upperrange extra
    diff_min = abs(min * 0.98)  #  2% underrange extra
    # Extra space above for legend based on station and entities
    diff_max = diff_max * (len(stations) + len(entities))
    print('DIFF_MIN: ' + str(diff_min))
    print('DIFF_MAX: ' + str(diff_max))
    # Diff_max = 1.5 if diff_max < 1.5 else diff_max
    max_tick   = math.ceil( max + diff_max )  # upperrange extra
    min_tick   = math.ceil( min - diff_min ) #  underrange extra
    print('MAX_TICK: ' + str(max_tick))
    print('MIN_TICK: ' + str(min_tick))

    # Update steps
    diff = max_tick - min_tick
    step = math.floor( diff / 10 - 0.5 )
    step = 1 if step == 0 else step
    print('STEP: ' + str(step))
    input()

    pos_extr_y = max_tick - step / 2  # Is y position of min/max texts. Just below top
    print('POS_EXTR_Y: ' + str(pos_extr_y))

    yticks = np.arange( min_tick, max_tick + step, step ) # 1-10 % ranges
    plt.yticks( yticks,
                **config.plot_xas_font,
                color=config.plot_xas_color
                )

    plt.xticks( ymd,
                **config.plot_xas_font,
                color=config.plot_xas_color,
                rotation=config.plot_xas_rotation
                )

    # Min max extremes
    if utils.is_yes( options['plot_min_max_ave_period'] ):
        # build a rectangle in axes coords
        left, width = .25, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height
        pos = max

        t = ''
        for el in period_extremes:
            t += el + '\n'

        # Clima calculations too
        if utils.is_yes(options['plot_climate_ave']):
            for el in clima_averages:
                t += el + '\n'

        plt.text( ymd[0],
                  pos_extr_y, # Most left and at the top
                  t,
                  style='italic',
                  horizontalalignment='left',
                  verticalalignment='top',
                  fontsize=config.plot_legend_fontsize,
                  color='#444444' )

    plt.legend( loc=config.plot_legend_loc,
                fontsize=config.plot_legend_fontsize,
                facecolor=config.plot_legend_facecolor,
                shadow=config.plot_legend_shadow,
                frameon=config.plot_legend_frameon,
                fancybox=config.plot_legend_fancybox )

    if utils.is_yes(config.plot_tight_layout):
        plt.tight_layout()

    plt.savefig( path, dpi=options['plot_dpi'], format=options['plot_image_type'] )

    if utils.is_yes(config.plot_show):
        plt.show()

    return path
