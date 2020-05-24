# -*- coding: utf-8 -*-
'''Library contains classes and functions make images'''

__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2019 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.1"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

import plot, fn_read as fnr, fn, config as cfg, knmi

def make_image_temps_in_period(l_station, s_date_start, s_date_end, name):
    # give temps by days
    # calculate averages TX, TG , TN, T10N
    station = l_station[0]
    l_days = fnr.get_list_dayvalues_from_station_in_period(station, s_date_start, s_date_end)

    # Make lists for plotting
    l_xymd, l_ytx, l_ytg, l_ytn = [], [], [], []
    for day in l_days:
        ymd = knmi.etmgeg(day, 'YYYYMMDD')
        tx  = knmi.etmgeg(day, 'TX')
        tg  = knmi.etmgeg(day, 'TG')
        tn  = knmi.etmgeg(day, 'TN')
        l_xymd.append(ymd)
        l_ytx.append(tx)
        l_ytg.append(tg)
        l_ytn.append(tn)

    l_ytx = [int(x)/10 for x in l_ytx] # Divide by 10
    l_ytg = [int(x)/10 for x in l_ytg] # Divide by 10
    l_ytn = [int(x)/10 for x in l_ytn] # Divide by 10

    graphs = []
    graphs.append( plot.Plot(l_ytx, l_xymd, 'TX') )
    graphs.append( plot.Plot(l_ytg, l_xymd, 'TG') )
    graphs.append( plot.Plot(l_ytn, l_xymd, 'TN') )

    # Print graphs
    # Make t_range
    tx_max = max(l_ytx) # maximum
    tn_min = min(l_ytn) # Minimum
    tx_max_i = int(round(tx_max)) + 3
    tn_min_i = int(round(tn_min)) - 3
    while tx_max_i % 5 != 0: tx_max_i += 1
    while tn_min_i % 5 != 0: tn_min_i -= 1
    t_range = [float(tn_min_i),float(tx_max_i)]

    period = f'{s_date_start}-{s_date_end}'
    s_fname = name if name else f'temperature-{station.plaats}-{period}.png'
    fig_name = fn.mk_path( cfg.dir_img, s_fname )
    plot.graph( graphs,
                f'Temperatures {station.plaats}\nperiod {period}',
                'DATES\n(yyyymmdd)',
                'T   \n°C   ',
                 fig_name,
                 t_range,
                 ['#800000','#008080','#0000CD']
                )

    return fig_name
