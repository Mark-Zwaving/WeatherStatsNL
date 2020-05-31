# -*- coding: utf-8 -*-
'''Library for plotting graphs'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.4"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

from random import randint
import numpy as np

 # Initialisation of color list, will be overwritten with correct values later
list = np.array( [ ['names', 'hexa', 'rgb', 'hsl'] ] )
NAME = 0  # Names key in list
HEXA = 1  # et cetera
RGB  = 2  # et cetera
HSL  = 3  # et cetera

def names():
    return list[:,NAME]
def hexas():
    return list[:,HEXA]
def rgbs():
    return list[:,RGB]
def hsls():
    return list[:,HSL]

def check_name(name):
    return name in names()
def check_hexa(hexa):
    return hexa in hexas()
def check_rgb(rgb):
    return rgb in rgbs()
def check_hsl(hsl):
    return hsl in hsls()

def sort_names():
    return np.array( sorted( list, key = lambda el : el[NAME] ) )
def sort_hexas():
    return np.array( sorted( list, key = lambda el : el[HEXA] ) )
def sort_rgbs():
    return np.array( sorted( list, key = lambda el : el[RGB] ) )
def sort_hsls():
    return np.array( sorted( list, key = lambda el : el[HSL] ) )

def sort(type='name'):
    if   type == 'name': return sort_names()
    elif type == 'hexa': return sort_hexas()
    elif type ==  'rgb': return sort_rgbs()
    elif type ==  'rgb': return sort_hsls()

    return list

def name_to_rgb(name):
    if check_name(name):
        return list[np.where(list[:,NAME]==name)][RGB]
    return (False,False,False)

def name_to_hexa(name):
    if check_name(name):
        return list[np.where(list[:,NAME]==name)][HEXA]
    return False

def name_to_hsl(name):
    if check_name(name):
        return list[np.where(list[:,NAME]==name)][HSL]
    return (False,False,False)

def hexa_to_name(hexa):
    if check_hexa(hexa):
        return list[np.where(list[:,HEXA]==hexa)][NAME]
    return False

def hexa_to_rgb(hexa):
    if check_hexa(hexa):
        return list[np.where(list[:,HEXA]==hexa)][RGB]
    else:
        # Make hexa always a string, replace '#' with '' and make uppercase
        h = str(hexa).replace('#','').upper()

        # Make it work for a 3 digits hexa too. Convert to 6 digits
        if len(h) == 3:
            h = f'{h[0]}{h[0]}{h[1]}{h[1]}{h[2]}{h[2]}'

        if len(h) == 6:
            r = hexa_to_dec(h[0:2])
            g = hexa_to_dec(h[2:4])
            b = hexa_to_dec(h[4:6])
            return ( r, g, b)

    return ( False, False, False)

def hexa_to_hsl(hexa):
    if check_hexa(hexa):
        return list[np.where(list[:,HEXA]==hexa)][HSL] # No need to calculate
    else:
        rgb = hexa_to_rgb(hexa)
        hue = rgb_to_hue(rgb) # Hue
        sat = rgb_to_saturation(rgb) # Saturation
        lig = rgb_to_l(rgb) # Lightness

        return ( hue, sat, lig )

def rnd_color(type='name'):
    ndx = 0
    if   type == 'name': ndx = 0
    elif type == 'hexa': ndx = 1
    elif type ==  'rgb': ndx = 2
    elif type ==  'hsl': ndx = 3

    l = np.random.choice(list[:,ndx],1)

    return l[0]

def rnd_savecolor():
    return np.random.choice( save_colors[:], 1 )[0]

# Source: https://en.wikipedia.org/wiki/HSL_and_HSV#From_RGB
def rgb_to_l(rgb):
    return round( ( max(rgb) + min(rgb) ) / 2.0 / 255.0, 2 )

# Source: https://en.wikipedia.org/wiki/HSL_and_HSV#From_RGB
def rgb_to_v(rgb):
    return round( max(rgb) / 255.0, 2 )

# Source: https://en.wikipedia.org/wiki/HSL_and_HSV#From_RGB
def rgb_to_saturation(rgb):
    # Saturation ∈ [0,1]
    sat, mx, mn, l = -1.0, max(rgb)/255.0, min(rgb)/255.0, rgb_to_l(rgb)

    if mx == 0.0 or round(mn,2) == 1.00:
        sat = 0.0
    else:
        if l < 0.5:
            sat = (mx-mn) / (mx+mn)
        elif l >= 0.5:
            sat = (mx-mn) / (2-(mx+mn))

    return round(sat, 2)

# Source: https://stackoverflow.com/questions/23090019/fastest-formula-to-get-hue-from-rgb#23094494
# Source: https://en.wikipedia.org/wiki/HSL_and_HSV#From_RGB
def rgb_to_hue(rgb):
    ''' Functions calculates rgb to a hue value '''
    # Get max and min values
    mx, mn = max(rgb)/255.0, min(rgb)/255.0
    # Set r,g,b between 0-1, hue default 0.0
    hue, r, g, b = 0.0, rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0

    if mx == mn:
        hue = 0.0 # Gray scale
    else:
        if mx == r: # Red dominant
            hue = 60 * (0.0 + ((g-b)/(mx-mn)))
        elif mx == g: # Green dominant
            hue = 60 * (2.0 + ((b-r)/(mx-mn)))
        elif mx == b: # Blue dominant
            hue = 60 * (4.0 + ((r-g)/(mx-mn)))

    # Correct negative angle
    if hue < 0.0:
        hue += 360

    # Hue from ∈ [0°, 360°] to ∈ [0,1]
    return round(hue/360, 2)

def hexa_to_dec(hexa):
    ''' Function calculates a hexa value into a decimal value '''
    # Make a string, replace '#' with '', reverse chars and make uppercase
    hexa = str(hexa).replace('#','')[::-1].upper()
    pos, radix, total, val = 0, 16, 0, -1 # Init base vars
    for char in hexa: # Check all chars and calculate the hexa value and sum up
        # Find decimal value for char in list with hex values
        for el in [ ['1',1], ['2',2], ['3',3], ['4',4], ['5',5], ['6',6],
                    ['7',7], ['8',8], ['9',9], ['0',0], ['A',10],['B',11],
                    ['C',12], ['D',13], ['E',14], ['F',15] ]:
            if char == el[0]:
                val = el[1]
                break # # Hex value found

        if val == -1:
            return False # Error hexa value not correct

        total += val * radix ** pos
        pos += 1 # Next position

    return total



def ent_to_color(ent):
    e = ent.strip().upper()
    if   e == 'TX': return 'red'
    elif e == 'TG': return 'green'
    elif e == 'TN': return 'blue'
    elif e == 'T10N': return 'orange'
    elif e == 'DDVEC': return 'gray'
    elif e == 'FG': return 'orange'
    elif e == 'RH': return 'blue'
    elif e == 'SQ': return 'yellow'
    elif e == 'PG': return 'purple'
    elif e == 'UG': return rnd_savecolor()
    elif e == 'FXX': return rnd_savecolor()
    elif e == 'FHVEC': return rnd_savecolor()
    elif e == 'FHX': return rnd_savecolor()
    elif e == 'FHN': return rnd_savecolor()
    elif e == 'SP': return rnd_savecolor()
    elif e == 'Q': return rnd_savecolor()
    elif e == 'DR': return rnd_savecolor()
    elif e == 'RHX': return rnd_savecolor()
    elif e == 'PX': return rnd_savecolor()
    elif e == 'PN': return rnd_savecolor()
    elif e == 'VVN': return rnd_savecolor()
    elif e == 'VVX': return rnd_savecolor()
    elif e == 'NG': return rnd_savecolor()
    elif e == 'UX': return rnd_savecolor()
    elif e == 'UN': return rnd_savecolor()
    elif e == 'EV24': return rnd_savecolor()
    return rnd_savecolor()

# Tested
save_colors = np.array([
      '#0000FF','#8A2BE2','#A52A2A','#5F9EA0','#D2691E','#6495ED','#DC143C',
      '#00008B','#008B8B','#B8860B','#006400','#BDB76B','#8B008B','#556B2F',
      '#9932CC','#8B0000','#E9967A','#483D8B','#2F4F4F','#00CED1','#9400D3',
      '#1E90FF','#B22222','#228B22','#DAA520','#808080','#008000','#9ACD32',
      '#FF69B4','#CD5C5C','#4B0082','#20B2AA','#778899','#32CD32','#800000',
      '#66CDAA','#0000CD','#BA55D3','#9370DB','#3CB371','#7B68EE','#48D1CC',
      '#C71585','#191970','#000080','#808000','#6B8E23','#DA70D6','#DB7093',
      '#CD853F','#800080','#663399','#FF0000','#BC8F8F','#4169E1','#8B4513',
      '#2E8B57','#A0522D','#6A5ACD','#708090','#708090','#4682B4','#008080',
])


list = np.array([
    ['Black',            '#000000', hexa_to_rgb('#000000'), hexa_to_hsl('#000000')],
    ['Navy',             '#000080', hexa_to_rgb('#000080'), hexa_to_hsl('#000080')],
    ['DarkBlue',         '#00008B', hexa_to_rgb('#00008B'), hexa_to_hsl('#00008B')],
    ['MediumBlue',       '#0000CD', hexa_to_rgb('#0000CD'), hexa_to_hsl('#0000CD')],
    ['Blue',             '#0000FF', hexa_to_rgb('#0000FF'), hexa_to_hsl('#0000FF')],
    ['DarkGreen',        '#006400', hexa_to_rgb('#006400'), hexa_to_hsl('#006400')],
    ['Green',            '#008000', hexa_to_rgb('#008000'), hexa_to_hsl('#008000')],
    ['Teal',             '#008080', hexa_to_rgb('#008080'), hexa_to_hsl('#008080')],
    ['DarkCyan',         '#008B8B', hexa_to_rgb('#008B8B'), hexa_to_hsl('#008B8B')],
    ['DeepSkyBlue',      '#00BFFF', hexa_to_rgb('#00BFFF'), hexa_to_hsl('#00BFFF')],
    ['DarkTurquoise',    '#00CED1', hexa_to_rgb('#00CED1'), hexa_to_hsl('#00CED1')],
    ['MediumSpringGreen', '#00FA9A', hexa_to_rgb('#00FA9A'), hexa_to_hsl('#00FA9A')],
    ['Lime',             '#00FF00', hexa_to_rgb('#00FF00'), hexa_to_hsl('#00FF00')],
    ['SpringGreen',      '#00FF7F', hexa_to_rgb('#00FF7F'), hexa_to_hsl('#00FF7F')],
    ['Aqua',             '#00FFFF', hexa_to_rgb('#00FFFF'), hexa_to_hsl('#00FFFF')],
    ['Cyan',             '#00FFFF', hexa_to_rgb('#00FFFF'), hexa_to_hsl('#00FFFF')],
    ['MidnightBlue',     '#191970', hexa_to_rgb('#191970'), hexa_to_hsl('#191970')],
    ['DodgerBlue',       '#1E90FF', hexa_to_rgb('#1E90FF'), hexa_to_hsl('#1E90FF')],
    ['LightSeaGreen',    '#20B2AA', hexa_to_rgb('#20B2AA'), hexa_to_hsl('#20B2AA')],
    ['ForestGreen',      '#228B22', hexa_to_rgb('#228B22'), hexa_to_hsl('#228B22')],
    ['SeaGreen',         '#2E8B57', hexa_to_rgb('#2E8B57'), hexa_to_hsl('#2E8B57')],
    ['DarkSlateGray',    '#2F4F4F', hexa_to_rgb('#2F4F4F'), hexa_to_hsl('#2F4F4F')],
    ['DarkSlateGrey',    '#2F4F4F', hexa_to_rgb('#2F4F4F'), hexa_to_hsl('#2F4F4F')],
    ['LimeGreen',        '#32CD32', hexa_to_rgb('#32CD32'), hexa_to_hsl('#32CD32')],
    ['MediumSeaGreen',   '#3CB371', hexa_to_rgb('#3CB371'), hexa_to_hsl('#3CB371')],
    ['Turquoise',        '#40E0D0', hexa_to_rgb('#40E0D0'), hexa_to_hsl('#40E0D0')],
    ['RoyalBlue',        '#4169E1', hexa_to_rgb('#4169E1'), hexa_to_hsl('#4169E1')],
    ['SteelBlue',        '#4682B4', hexa_to_rgb('#4682B4'), hexa_to_hsl('#4682B4')],
    ['DarkSlateBlue',    '#483D8B', hexa_to_rgb('#483D8B'), hexa_to_hsl('#483D8B')],
    ['MediumTurquoise',  '#48D1CC', hexa_to_rgb('#48D1CC'), hexa_to_hsl('#48D1CC')],
    ['Indigo ',          '#4B0082', hexa_to_rgb('#4B0082'), hexa_to_hsl('#4B0082')],
    ['DarkOliveGreen',   '#556B2F', hexa_to_rgb('#556B2F'), hexa_to_hsl('#556B2F')],
    ['CadetBlue',        '#5F9EA0', hexa_to_rgb('#5F9EA0'), hexa_to_hsl('#5F9EA0')],
    ['CornflowerBlue',   '#6495ED', hexa_to_rgb('#6495ED'), hexa_to_hsl('#6495ED')],
    ['RebeccaPurple',    '#663399', hexa_to_rgb('#663399'), hexa_to_hsl('#663399')],
    ['MediumAquaMarine', '#66CDAA', hexa_to_rgb('#66CDAA'), hexa_to_hsl('#66CDAA')],
    ['DimGray',          '#696969', hexa_to_rgb('#696969'), hexa_to_hsl('#696969')],
    ['DimGrey',          '#696969', hexa_to_rgb('#696969'), hexa_to_hsl('#696969')],
    ['SlateBlue',        '#6A5ACD', hexa_to_rgb('#6A5ACD'), hexa_to_hsl('#6A5ACD')],
    ['OliveDrab',        '#6B8E23', hexa_to_rgb('#6B8E23'), hexa_to_hsl('#6B8E23')],
    ['SlateGray',        '#708090', hexa_to_rgb('#708090'), hexa_to_hsl('#708090')],
    ['SlateGrey',        '#708090', hexa_to_rgb('#708090'), hexa_to_hsl('#708090')],
    ['LightSlateGray',   '#778899', hexa_to_rgb('#778899'), hexa_to_hsl('#778899')],
    ['LightSlateGrey',   '#778899', hexa_to_rgb('#778899'), hexa_to_hsl('#778899')],
    ['MediumSlateBlue',  '#7B68EE', hexa_to_rgb('#7B68EE'), hexa_to_hsl('#7B68EE')],
    ['LawnGreen',        '#7CFC00', hexa_to_rgb('#7CFC00'), hexa_to_hsl('#7CFC00')],
    ['Chartreuse',       '#7FFF00', hexa_to_rgb('#7FFF00'), hexa_to_hsl('#7FFF00')],
    ['Aquamarine',       '#7FFFD4', hexa_to_rgb('#7FFFD4'), hexa_to_hsl('#7FFFD4')],
    ['Maroon',           '#800000', hexa_to_rgb('#800000'), hexa_to_hsl('#800000')],
    ['Purple',           '#800080', hexa_to_rgb('#800080'), hexa_to_hsl('#800080')],
    ['Olive',            '#808000', hexa_to_rgb('#808000'), hexa_to_hsl('#808000')],
    ['Gray',             '#808080', hexa_to_rgb('#808080'), hexa_to_hsl('#808080')],
    ['Grey',             '#808080', hexa_to_rgb('#808080'), hexa_to_hsl('#808080')],
    ['SkyBlue',          '#87CEEB', hexa_to_rgb('#87CEEB'), hexa_to_hsl('#87CEEB')],
    ['LightSkyBlue',     '#87CEFA', hexa_to_rgb('#87CEFA'), hexa_to_hsl('#87CEFA')],
    ['BlueViolet',       '#8A2BE2', hexa_to_rgb('#8A2BE2'), hexa_to_hsl('#8A2BE2')],
    ['DarkRed',          '#8B0000', hexa_to_rgb('#8B0000'), hexa_to_hsl('#8B0000')],
    ['DarkMagenta',      '#8B008B', hexa_to_rgb('#8B008B'), hexa_to_hsl('#8B008B')],
    ['SaddleBrown',      '#8B4513', hexa_to_rgb('#8B4513'), hexa_to_hsl('#8B4513')],
    ['DarkSeaGreen',     '#8FBC8F', hexa_to_rgb('#8FBC8F'), hexa_to_hsl('#8FBC8F')],
    ['LightGreen',       '#90EE90', hexa_to_rgb('#90EE90'), hexa_to_hsl('#90EE90')],
    ['MediumPurple',     '#9370DB', hexa_to_rgb('#9370DB'), hexa_to_hsl('#9370DB')],
    ['DarkViolet',       '#9400D3', hexa_to_rgb('#9400D3'), hexa_to_hsl('#9400D3')],
    ['PaleGreen',        '#98FB98', hexa_to_rgb('#98FB98'), hexa_to_hsl('#98FB98')],
    ['DarkOrchid',       '#9932CC', hexa_to_rgb('#9932CC'), hexa_to_hsl('#9932CC')],
    ['YellowGreen',      '#9ACD32', hexa_to_rgb('#9ACD32'), hexa_to_hsl('#9ACD32')],
    ['Sienna',           '#A0522D', hexa_to_rgb('#A0522D'), hexa_to_hsl('#A0522D')],
    ['Brown',            '#A52A2A', hexa_to_rgb('#A52A2A'), hexa_to_hsl('#A52A2A')],
    ['DarkGray',         '#A9A9A9', hexa_to_rgb('#A9A9A9'), hexa_to_hsl('#A9A9A9')],
    ['DarkGrey',         '#A9A9A9', hexa_to_rgb('#A9A9A9'), hexa_to_hsl('#A9A9A9')],
    ['LightBlue',        '#ADD8E6', hexa_to_rgb('#ADD8E6'), hexa_to_hsl('#ADD8E6')],
    ['GreenYellow',      '#ADFF2F', hexa_to_rgb('#ADFF2F'), hexa_to_hsl('#ADFF2F')],
    ['PaleTurquoise',    '#AFEEEE', hexa_to_rgb('#AFEEEE'), hexa_to_hsl('#AFEEEE')],
    ['LightSteelBlue',   '#B0C4DE', hexa_to_rgb('#B0C4DE'), hexa_to_hsl('#B0C4DE')],
    ['PowderBlue',       '#B0E0E6', hexa_to_rgb('#B0E0E6'), hexa_to_hsl('#B0E0E6')],
    ['FireBrick',        '#B22222', hexa_to_rgb('#B22222'), hexa_to_hsl('#B22222')],
    ['DarkGoldenRod',    '#B8860B', hexa_to_rgb('#B8860B'), hexa_to_hsl('#B8860B')],
    ['MediumOrchid',     '#BA55D3', hexa_to_rgb('#BA55D3'), hexa_to_hsl('#BA55D3')],
    ['RosyBrown',        '#BC8F8F', hexa_to_rgb('#BC8F8F'), hexa_to_hsl('#BC8F8F')],
    ['DarkKhaki',        '#BDB76B', hexa_to_rgb('#BDB76B'), hexa_to_hsl('#BDB76B')],
    ['Silver',           '#C0C0C0', hexa_to_rgb('#C0C0C0'), hexa_to_hsl('#C0C0C0')],
    ['MediumVioletRed',  '#C71585', hexa_to_rgb('#C71585'), hexa_to_hsl('#C71585')],
    ['IndianRed ',       '#CD5C5C', hexa_to_rgb('#CD5C5C'), hexa_to_hsl('#CD5C5C')],
    ['Peru',             '#CD853F', hexa_to_rgb('#CD853F'), hexa_to_hsl('#CD853F')],
    ['Chocolate',        '#D2691E', hexa_to_rgb('#D2691E'), hexa_to_hsl('#D2691E')],
    ['Tan',              '#D2B48C', hexa_to_rgb('#D2B48C'), hexa_to_hsl('#D2B48C')],
    ['LightGray',        '#D3D3D3', hexa_to_rgb('#D3D3D3'), hexa_to_hsl('#D3D3D3')],
    ['LightGrey',        '#D3D3D3', hexa_to_rgb('#D3D3D3'), hexa_to_hsl('#D3D3D3')],
    ['Thistle',          '#D8BFD8', hexa_to_rgb('#D8BFD8'), hexa_to_hsl('#D8BFD8')],
    ['Orchid',           '#DA70D6', hexa_to_rgb('#DA70D6'), hexa_to_hsl('#DA70D6')],
    ['GoldenRod',        '#DAA520', hexa_to_rgb('#DAA520'), hexa_to_hsl('#DAA520')],
    ['PaleVioletRed',    '#DB7093', hexa_to_rgb('#DB7093'), hexa_to_hsl('#DB7093')],
    ['Crimson',          '#DC143C', hexa_to_rgb('#DC143C'), hexa_to_hsl('#DC143C')],
    ['Gainsboro',        '#DCDCDC', hexa_to_rgb('#DCDCDC'), hexa_to_hsl('#DCDCDC')],
    ['Plum',             '#DDA0DD', hexa_to_rgb('#DDA0DD'), hexa_to_hsl('#DDA0DD')],
    ['BurlyWood',        '#DEB887', hexa_to_rgb('#DEB887'), hexa_to_hsl('#DEB887')],
    ['LightCyan',        '#E0FFFF', hexa_to_rgb('#E0FFFF'), hexa_to_hsl('#E0FFFF')],
    ['Lavender',         '#E6E6FA', hexa_to_rgb('#E6E6FA'), hexa_to_hsl('#E6E6FA')],
    ['DarkSalmon',       '#E9967A', hexa_to_rgb('#E9967A'), hexa_to_hsl('#E9967A')],
    ['Violet',           '#EE82EE', hexa_to_rgb('#EE82EE'), hexa_to_hsl('#EE82EE')],
    ['PaleGoldenRod',    '#EEE8AA', hexa_to_rgb('#EEE8AA'), hexa_to_hsl('#EEE8AA')],
    ['LightCoral',       '#F08080', hexa_to_rgb('#F08080'), hexa_to_hsl('#F08080')],
    ['Khaki',            '#F0E68C', hexa_to_rgb('#F0E68C'), hexa_to_hsl('#F0E68C')],
    ['AliceBlue',        '#F0F8FF', hexa_to_rgb('#F0F8FF'), hexa_to_hsl('#F0F8FF')],
    ['HoneyDew',         '#F0FFF0', hexa_to_rgb('#F0FFF0'), hexa_to_hsl('#F0FFF0')],
    ['Azure',            '#F0FFFF', hexa_to_rgb('#F0FFFF'), hexa_to_hsl('#F0FFFF')],
    ['SandyBrown',       '#F4A460', hexa_to_rgb('#F4A460'), hexa_to_hsl('#F4A460')],
    ['Wheat',            '#F5DEB3', hexa_to_rgb('#F5DEB3'), hexa_to_hsl('#F5DEB3')],
    ['Beige',            '#F5F5DC', hexa_to_rgb('#F5F5DC'), hexa_to_hsl('#F5F5DC')],
    ['WhiteSmoke',       '#F5F5F5', hexa_to_rgb('#F5F5F5'), hexa_to_hsl('#F5F5F5')],
    ['MintCream',        '#F5FFFA', hexa_to_rgb('#F5FFFA'), hexa_to_hsl('#F5FFFA')],
    ['GhostWhite',       '#F8F8FF', hexa_to_rgb('#F8F8FF'), hexa_to_hsl('#F8F8FF')],
    ['Salmon',           '#FA8072', hexa_to_rgb('#FA8072'), hexa_to_hsl('#FA8072')],
    ['AntiqueWhite',     '#FAEBD7', hexa_to_rgb('#FAEBD7'), hexa_to_hsl('#FAEBD7')],
    ['Linen',            '#FAF0E6', hexa_to_rgb('#FAF0E6'), hexa_to_hsl('#FAF0E6')],
    ['LightGoldenRodYellow', '#FAFAD2', hexa_to_rgb('#FAFAD2'), hexa_to_hsl('#FAFAD2')],
    ['OldLace',          '#FDF5E6', hexa_to_rgb('#FDF5E6'), hexa_to_hsl('#FDF5E6')],
    ['Red',              '#FF0000', hexa_to_rgb('#FF0000'), hexa_to_hsl('#FF0000')],
    ['Fuchsia',          '#FF00FF', hexa_to_rgb('#FF00FF'), hexa_to_hsl('#FF00FF')],
    ['Magenta',          '#FF00FF', hexa_to_rgb('#FF00FF'), hexa_to_hsl('#FF00FF')],
    ['DeepPink',         '#FF1493', hexa_to_rgb('#FF1493'), hexa_to_hsl('#FF1493')],
    ['OrangeRed',        '#FF4500', hexa_to_rgb('#FF4500'), hexa_to_hsl('#FF4500')],
    ['Tomato',           '#FF6347', hexa_to_rgb('#FF6347'), hexa_to_hsl('#FF6347')],
    ['HotPink',          '#FF69B4', hexa_to_rgb('#FF69B4'), hexa_to_hsl('#FF69B4')],
    ['Coral',            '#FF7F50', hexa_to_rgb('#FF7F50'), hexa_to_hsl('#FF7F50')],
    ['DarkOrange',       '#FF8C00', hexa_to_rgb('#FF8C00'), hexa_to_hsl('#FF8C00')],
    ['LightSalmon',      '#FFA07A', hexa_to_rgb('#FFA07A'), hexa_to_hsl('#FFA07A')],
    ['Orange',           '#FFA500', hexa_to_rgb('#FFA500'), hexa_to_hsl('#FFA500')],
    ['LightPink',        '#FFB6C1', hexa_to_rgb('#FFB6C1'), hexa_to_hsl('#FFB6C1')],
    ['Pink',             '#FFC0CB', hexa_to_rgb('#FFC0CB'), hexa_to_hsl('#FFC0CB')],
    ['Gold',             '#FFD700', hexa_to_rgb('#FFD700'), hexa_to_hsl('#FFD700')],
    ['PeachPuff',        '#FFDAB9', hexa_to_rgb('#FFDAB9'), hexa_to_hsl('#FFDAB9')],
    ['NavajoWhite',      '#FFDEAD', hexa_to_rgb('#FFDEAD'), hexa_to_hsl('#FFDEAD')],
    ['Moccasin',         '#FFE4B5', hexa_to_rgb('#FFE4B5'), hexa_to_hsl('#FFE4B5')],
    ['Bisque',           '#FFE4C4', hexa_to_rgb('#FFE4C4'), hexa_to_hsl('#FFE4C4')],
    ['MistyRose',        '#FFE4E1', hexa_to_rgb('#FFE4E1'), hexa_to_hsl('#FFE4E1')],
    ['BlanchedAlmond',   '#FFEBCD', hexa_to_rgb('#FFEBCD'), hexa_to_hsl('#FFEBCD')],
    ['PapayaWhip',       '#FFEFD5', hexa_to_rgb('#FFEFD5'), hexa_to_hsl('#FFEFD5')],
    ['LavenderBlush',    '#FFF0F5', hexa_to_rgb('#FFF0F5'), hexa_to_hsl('#FFF0F5')],
    ['SeaShell',         '#FFF5EE', hexa_to_rgb('#FFF5EE'), hexa_to_hsl('#FFF5EE')],
    # ['Cornsilk',         '#FFF8DC', hexa_to_rgb('#FFF8DC'), hexa_to_hsl('#FFF8DC')],
    ['LemonChiffon',     '#FFFACD', hexa_to_rgb('#FFFACD'), hexa_to_hsl('#FFFACD')],
    # ['FloralWhite',      '#FFFAF0', hexa_to_rgb('#FFFAF0'), hexa_to_hsl('#FFFAF0')],
    # ['Snow',             '#FFFAFA', hexa_to_rgb('#FFFAFA'), hexa_to_hsl('#FFFAFA')],
    ['Yellow',           '#FFFF00', hexa_to_rgb('#FFFF00'), hexa_to_hsl('#FFFF00')],
    ['LightYellow',      '#FFFFE0', hexa_to_rgb('#FFFFE0'), hexa_to_hsl('#FFFFE0')]
    # ['Ivory',            '#FFFFF0', hexa_to_rgb('#FFFFF0'), hexa_to_hsl('#FFFFF0')],
    # ['White',            '#FFFFFF', hexa_to_rgb('#FFFFFF'), hexa_to_hsl('#FFFFFF')]
])
