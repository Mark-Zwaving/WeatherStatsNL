import numpy as np, fn, config as cfg, random, os
from matplotlib import pyplot as plt

# 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight',
# 'ggplot', 'grayscale', 'seaborn-bright', 'seaborn-colorblind',
# 'seaborn-dark-palette', 'seaborn-dark', 'seaborn-darkgrid',
# 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper',
# 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks',
# 'seaborn-white', 'seaborn-whitegrid', 'seaborn', 'Solarize_Light2',
# 'tableau-colorblind10'

class Plot:
    '''Class stores lists x and y for a graphic'''
    def __init__(self, ly, lx, y_label, x_label='' ):
        self.l_xdata  = lx
        self.l_ydata  = ly
        self.s_xlabel  = x_label
        self.s_ylabel  = y_label

def rnd(max):
    return random.randrange(max)

def rnd_color(l_old):
    max, rnd = len(cfg.hexa_colors), rnd(max)
    color = cfg.hexa_colors[rnd]
    while color not in l_old: color = cfg.hexa_colors[rnd(max)]
    return color

def graph(l_plots, s_title, s_xlabel_title, s_ylabel_title, save_dir, s_fname, t_range, c_range):
    with plt.style.context('seaborn-notebook'):
        title_font  = dict(fontsize='large',  fontdict={'family': 'Arial', 'weight':'bold'})
        label_font  = dict(fontsize='small', fontdict={'family': 'Monospace'})
        legend_font = dict(fontsize='x-small', fontdict={'family': 'Monospace'})
        temp_font   = dict(fontsize='x-small')
        colors      = cfg.hexa_colors
        t_start, t_end = t_range[0], t_range[1]
        i_leg_cols  = len(l_plots) if len(l_plots) < 5 else 2

        # Get different colors
        if c_range:
            colors = c_range
        else:
            random.shuffle(colors)

        plt.rc('lines', lw=1, c='#333333')
        plt.rc('font', family='Calibri', weight='normal', size=10)
        plt.rc('savefig', dpi=300)       # Higher res outputs
        plt.tick_params(axis='both', length=6, width=2,
                        labelsize='small', direction='inout', colors='#555555',
                        grid_color='#999999', grid_alpha=0.6, grid_linewidth=1,
                        grid_linestyle='dotted', bottom =True, left=True,
                        right=True )
        plt.tick_params(axis='y', pad=1, labelright=True, labelleft=True)
        plt.tick_params(axis='x', pad=3, labelrotation=30)

        # y_ticks_val = np.arange( 15.0, 42.0, 0.01, dtype=float )
        # y_ticks_lab = [ f'{float(y)}°C' for y in y_ticks_val ]
        y_ticks_val = np.linspace(t_start, t_end, t_end-t_start, dtype=float)
        y_ticks_lab = [ f'{float(y)}°C' for y in y_ticks_val ]
        x_ticks_lab = [ f'{float(x)}' for x in l_plots[0].l_xdata ]

        # plt.autoscale(enable=False, axis='y', tight=True)
        plt.axis( [-1, len(l_plots[0].l_xdata)+1,
                   int(t_start), int(t_end)] )
        plt.yticks(y_ticks_val, y_ticks_lab)
        plt.xticks([])
        plt.margins(0.05)

        plt.xscale('linear')
        plt.yscale('linear')
        plt.xlabel(s_xlabel_title, **label_font)
        plt.ylabel(f'{s_ylabel_title}', rotation=0, **label_font)
        plt.title(s_title, **title_font)

        clr = 0
        for plot in l_plots:
            plt.plot( plot.l_xdata, plot.l_ydata, color=colors[clr],
                      label=plot.s_ylabel, marker='.', linewidth=1,
                      markersize=7
                      )

            # Add text next to markers
            for a,b in zip(plot.l_xdata, plot.l_ydata):
                plt.text( a, b, f'{float(b)}\n°C', color='#000000', alpha=0.8,
                          horizontalalignment='center', verticalalignment='top',
                          **temp_font )

            # Next color
            clr += 1
            if clr == len(colors):
                clr = 0;

        plt.grid(True)
        plt.legend(shadow=True, loc='best', ncol=i_leg_cols, fontsize='x-small')
        plt.tight_layout()

        period= f'{plot.l_xdata[0]}-{plot.l_xdata[-1]}'
        fig_name = fn.mk_path(save_dir, s_fname)
        print(fig_name)
        if os.path.isfile(fig_name):
            fig_name = fig_name.replace('.jpg','i.jpg')

        plt.savefig(fig_name)
        plt.close('all')

#
# def graph(l, s_title, l_legends, x_label, y_label, s_style, s_marker, b_grid):
#     plt.style.use(s_style)
#     plt.grid(b_grid)
#     # plt.subplots_adjust(hspace=4, wspace=6)
#     fig, ax = plt.subplots()
#     ax.set_xlabel(x_label, **axis_font)
#     ax.set_ylabel(y_label, **axis_font)
#     ax.set_title(s_title, **title_font)
#     # ax.set_xticklabels(labels=l[0].l_xdata, **text_style)
#     #ax.set_yticks(labels=np.arange(25.0, 42.0, 1.0, dtype=float), **text_style)
#
#     ax.set_ylim([25.0,42.0])
#     # Plot all stations
#     for g in l:
#         ax.plot(g.l_xdata, g.l_ydata, label=g.s_ylabel, marker=s_marker, linewidth=1.0)
#         for a,b in zip(g.l_xdata, g.l_ydata):
#             ax.text(a, b, b, fontsize=24)
#
#     ax.legend(loc='upper left', labels=l_legends, shadow=True, ncol=2, fontsize=24)
#     fig_name = fn.mk_path( cfg.dir_img, s_title )
#     fig.set_size_inches(40, 20)
#     fig.tight_layout()
#     fig.savefig(fig_name, dpi=300)
#
#     plt.close('all')
