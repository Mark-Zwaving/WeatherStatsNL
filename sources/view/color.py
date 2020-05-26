# -*- coding: utf-8 -*-
'''Library for plotting graphs'''
__author__     =  "Mark Zwaving"
__email__      =  "markzwaving@gmail.com"
__copyright__  =  "Copyright 2020 (C) Mark Zwaving. All rights reserved."
__license__    =  "GNU Lesser General Public License (LGPL)"
__version__    =  "0.0.3"
__maintainer__ =  "Mark Zwaving"
__status__     =  "Development"

from random import randint
import numpy as np

NAME = 0
HEX  = 1
RGB  = 2
HSL  = 3

list = np.array([
    ['Black',            '#000000', hex_to_rgb('#000000'), hex_to_hsl('#000000')],
    ['Navy',             '#000080', hex_to_rgb('#000080'), hex_to_hsl('#000080')],
    ['DarkBlue',         '#00008B', hex_to_rgb('#00008B'), hex_to_hsl('#00008B')],
    ['MediumBlue',       '#0000CD', hex_to_rgb('#0000CD'), hex_to_hsl('#0000CD')],
    ['Blue',             '#0000FF', hex_to_rgb('#0000FF'), hex_to_hsl('#0000FF')],
    ['DarkGreen',        '#006400', hex_to_rgb('#006400'), hex_to_hsl('#006400')],
    ['Green',            '#008000', hex_to_rgb('#008000'), hex_to_hsl('#008000')],
    ['Teal',             '#008080', hex_to_rgb('#008080'), hex_to_hsl('#008080')],
    ['DarkCyan',         '#008B8B', hex_to_rgb('#008B8B'), hex_to_hsl('#008B8B')],
    ['DeepSkyBlue',      '#00BFFF', hex_to_rgb('#00BFFF'), hex_to_hsl('#00BFFF')],
    ['DarkTurquoise',    '#00CED1', hex_to_rgb('#00CED1'), hex_to_hsl('#00CED1')],
    ['MediumSpringGreen', '#00FA9A', hex_to_rgb('#00FA9A'), hex_to_hsl('#00FA9A')],
    ['Lime',             '#00FF00', hex_to_rgb('#00FF00'), hex_to_hsl('#00FF00')],
    ['SpringGreen',      '#00FF7F', hex_to_rgb('#00FF7F'), hex_to_hsl('#00FF7F')],
    ['Aqua',             '#00FFFF', hex_to_rgb('#00FFFF'), hex_to_hsl('#00FFFF')],
    ['Cyan',             '#00FFFF', hex_to_rgb('#00FFFF'), hex_to_hsl('#00FFFF')],
    ['MidnightBlue',     '#191970', hex_to_rgb('#191970'), hex_to_hsl('#191970')],
    ['DodgerBlue',       '#1E90FF', hex_to_rgb('#1E90FF'), hex_to_hsl('#1E90FF')],
    ['LightSeaGreen',    '#20B2AA', hex_to_rgb('#20B2AA'), hex_to_hsl('#20B2AA')],
    ['ForestGreen',      '#228B22', hex_to_rgb('#228B22'), hex_to_hsl('#228B22')],
    ['SeaGreen',         '#2E8B57', hex_to_rgb('#2E8B57'), hex_to_hsl('#2E8B57')],
    ['DarkSlateGray',    '#2F4F4F', hex_to_rgb('#2F4F4F'), hex_to_hsl('#2F4F4F')],
    ['DarkSlateGrey',    '#2F4F4F', hex_to_rgb('#2F4F4F'), hex_to_hsl('#2F4F4F')],
    ['LimeGreen',        '#32CD32', hex_to_rgb('#32CD32'), hex_to_hsl('#32CD32')],
    ['MediumSeaGreen',   '#3CB371', hex_to_rgb('#3CB371'), hex_to_hsl('#3CB371')],
    ['Turquoise',        '#40E0D0', hex_to_rgb('#40E0D0'), hex_to_hsl('#40E0D0')],
    ['RoyalBlue',        '#4169E1', hex_to_rgb('#4169E1'), hex_to_hsl('#4169E1')],
    ['SteelBlue',        '#4682B4', hex_to_rgb('#4682B4'), hex_to_hsl('#4682B4')],
    ['DarkSlateBlue',    '#483D8B', hex_to_rgb('#483D8B'), hex_to_hsl('#483D8B')],
    ['MediumTurquoise',  '#48D1CC', hex_to_rgb('#48D1CC'), hex_to_hsl('#48D1CC')],
    ['Indigo ',          '#4B0082', hex_to_rgb('#4B0082'), hex_to_hsl('#4B0082')],
    ['DarkOliveGreen',   '#556B2F', hex_to_rgb('#556B2F'), hex_to_hsl('#556B2F')],
    ['CadetBlue',        '#5F9EA0', hex_to_rgb('#5F9EA0'), hex_to_hsl('#5F9EA0')],
    ['CornflowerBlue',   '#6495ED', hex_to_rgb('#6495ED'), hex_to_hsl('#6495ED')],
    ['RebeccaPurple',    '#663399', hex_to_rgb('#663399'), hex_to_hsl('#663399')],
    ['MediumAquaMarine', '#66CDAA', hex_to_rgb('#66CDAA'), hex_to_hsl('#66CDAA')],
    ['DimGray',          '#696969', hex_to_rgb('#696969'), hex_to_hsl('#696969')],
    ['DimGrey',          '#696969', hex_to_rgb('#696969'), hex_to_hsl('#696969')],
    ['SlateBlue',        '#6A5ACD', hex_to_rgb('#6A5ACD'), hex_to_hsl('#6A5ACD')],
    ['OliveDrab',        '#6B8E23', hex_to_rgb('#6B8E23'), hex_to_hsl('#6B8E23')],
    ['SlateGray',        '#708090', hex_to_rgb('#708090'), hex_to_hsl('#708090')],
    ['SlateGrey',        '#708090', hex_to_rgb('#708090'), hex_to_hsl('#708090')],
    ['LightSlateGray',   '#778899', hex_to_rgb('#778899'), hex_to_hsl('#778899')],
    ['LightSlateGrey',   '#778899', hex_to_rgb('#778899'), hex_to_hsl('#778899')],
    ['MediumSlateBlue',  '#7B68EE', hex_to_rgb('#7B68EE'), hex_to_hsl('#7B68EE')],
    ['LawnGreen',        '#7CFC00', hex_to_rgb('#7CFC00'), hex_to_hsl('#7CFC00')],
    ['Chartreuse',       '#7FFF00', hex_to_rgb('#7FFF00'), hex_to_hsl('#7FFF00')],
    ['Aquamarine',       '#7FFFD4', hex_to_rgb('#7FFFD4'), hex_to_hsl('#7FFFD4')],
    ['Maroon',           '#800000', hex_to_rgb('#800000'), hex_to_hsl('#800000')],
    ['Purple',           '#800080', hex_to_rgb('#800080'), hex_to_hsl('#800080')],
    ['Olive',            '#808000', hex_to_rgb('#808000'), hex_to_hsl('#808000')],
    ['Gray',             '#808080', hex_to_rgb('#808080'), hex_to_hsl('#808080')],
    ['Grey',             '#808080', hex_to_rgb('#808080'), hex_to_hsl('#808080')],
    ['SkyBlue',          '#87CEEB', hex_to_rgb('#87CEEB'), hex_to_hsl('#87CEEB')],
    ['LightSkyBlue',     '#87CEFA', hex_to_rgb('#87CEFA'), hex_to_hsl('#87CEFA')],
    ['BlueViolet',       '#8A2BE2', hex_to_rgb('#8A2BE2'), hex_to_hsl('#8A2BE2')],
    ['DarkRed',          '#8B0000', hex_to_rgb('#8B0000'), hex_to_hsl('#8B0000')],
    ['DarkMagenta',      '#8B008B', hex_to_rgb('#8B008B'), hex_to_hsl('#8B008B')],
    ['SaddleBrown',      '#8B4513', hex_to_rgb('#8B4513'), hex_to_hsl('#8B4513')],
    ['DarkSeaGreen',     '#8FBC8F', hex_to_rgb('#8FBC8F'), hex_to_hsl('#8FBC8F')],
    ['LightGreen',       '#90EE90', hex_to_rgb('#90EE90'), hex_to_hsl('#90EE90')],
    ['MediumPurple',     '#9370DB', hex_to_rgb('#9370DB'), hex_to_hsl('#9370DB')],
    ['DarkViolet',       '#9400D3', hex_to_rgb('#9400D3'), hex_to_hsl('#9400D3')],
    ['PaleGreen',        '#98FB98', hex_to_rgb('#98FB98'), hex_to_hsl('#98FB98')],
    ['DarkOrchid',       '#9932CC', hex_to_rgb('#9932CC'), hex_to_hsl('#9932CC')],
    ['YellowGreen',      '#9ACD32', hex_to_rgb('#9ACD32'), hex_to_hsl('#9ACD32')],
    ['Sienna',           '#A0522D', hex_to_rgb('#A0522D'), hex_to_hsl('#A0522D')],
    ['Brown',            '#A52A2A', hex_to_rgb('#A52A2A'), hex_to_hsl('#A52A2A')],
    ['DarkGray',         '#A9A9A9', hex_to_rgb('#A9A9A9'), hex_to_hsl('#A9A9A9')],
    ['DarkGrey',         '#A9A9A9', hex_to_rgb('#A9A9A9'), hex_to_hsl('#A9A9A9')],
    ['LightBlue',        '#ADD8E6', hex_to_rgb('#ADD8E6'), hex_to_hsl('#ADD8E6')],
    ['GreenYellow',      '#ADFF2F', hex_to_rgb('#ADFF2F'), hex_to_hsl('#ADFF2F')],
    ['PaleTurquoise',    '#AFEEEE', hex_to_rgb('#AFEEEE'), hex_to_hsl('#AFEEEE')],
    ['LightSteelBlue',   '#B0C4DE', hex_to_rgb('#B0C4DE'), hex_to_hsl('#B0C4DE')],
    ['PowderBlue',       '#B0E0E6', hex_to_rgb('#B0E0E6'), hex_to_hsl('#B0E0E6')],
    ['FireBrick',        '#B22222', hex_to_rgb('#B22222'), hex_to_hsl('#B22222')],
    ['DarkGoldenRod',    '#B8860B', hex_to_rgb('#B8860B'), hex_to_hsl('#B8860B')],
    ['MediumOrchid',     '#BA55D3', hex_to_rgb('#BA55D3'), hex_to_hsl('#BA55D3')],
    ['RosyBrown',        '#BC8F8F', hex_to_rgb('#BC8F8F'), hex_to_hsl('#BC8F8F')],
    ['DarkKhaki',        '#BDB76B', hex_to_rgb('#BDB76B'), hex_to_hsl('#BDB76B')],
    ['Silver',           '#C0C0C0', hex_to_rgb('#C0C0C0'), hex_to_hsl('#C0C0C0')],
    ['MediumVioletRed',  '#C71585', hex_to_rgb('#C71585'), hex_to_hsl('#C71585')],
    ['IndianRed ',       '#CD5C5C', hex_to_rgb('#CD5C5C'), hex_to_hsl('#CD5C5C')],
    ['Peru',             '#CD853F', hex_to_rgb('#CD853F'), hex_to_hsl('#CD853F')],
    ['Chocolate',        '#D2691E', hex_to_rgb('#D2691E'), hex_to_hsl('#D2691E')],
    ['Tan',              '#D2B48C', hex_to_rgb('#D2B48C'), hex_to_hsl('#D2B48C')],
    ['LightGray',        '#D3D3D3', hex_to_rgb('#D3D3D3'), hex_to_hsl('#D3D3D3')],
    ['LightGrey',        '#D3D3D3', hex_to_rgb('#D3D3D3'), hex_to_hsl('#D3D3D3')],
    ['Thistle',          '#D8BFD8', hex_to_rgb('#D8BFD8'), hex_to_hsl('#D8BFD8')],
    ['Orchid',           '#DA70D6', hex_to_rgb('#DA70D6'), hex_to_hsl('#DA70D6')],
    ['GoldenRod',        '#DAA520', hex_to_rgb('#DAA520'), hex_to_hsl('#DAA520')],
    ['PaleVioletRed',    '#DB7093', hex_to_rgb('#DB7093'), hex_to_hsl('#DB7093')],
    ['Crimson',          '#DC143C', hex_to_rgb('#DC143C'), hex_to_hsl('#DC143C')],
    ['Gainsboro',        '#DCDCDC', hex_to_rgb('#DCDCDC'), hex_to_hsl('#DCDCDC')],
    ['Plum',             '#DDA0DD', hex_to_rgb('#DDA0DD'), hex_to_hsl('#DDA0DD')],
    ['BurlyWood',        '#DEB887', hex_to_rgb('#DEB887'), hex_to_hsl('#DEB887')],
    ['LightCyan',        '#E0FFFF', hex_to_rgb('#E0FFFF'), hex_to_hsl('#E0FFFF')],
    ['Lavender',         '#E6E6FA', hex_to_rgb('#E6E6FA'), hex_to_hsl('#E6E6FA')],
    ['DarkSalmon',       '#E9967A', hex_to_rgb('#E9967A'), hex_to_hsl('#E9967A')],
    ['Violet',           '#EE82EE', hex_to_rgb('#EE82EE'), hex_to_hsl('#EE82EE')],
    ['PaleGoldenRod',    '#EEE8AA', hex_to_rgb('#EEE8AA'), hex_to_hsl('#EEE8AA')],
    ['LightCoral',       '#F08080', hex_to_rgb('#F08080'), hex_to_hsl('#F08080')],
    ['Khaki',            '#F0E68C', hex_to_rgb('#F0E68C'), hex_to_hsl('#F0E68C')],
    ['AliceBlue',        '#F0F8FF', hex_to_rgb('#F0F8FF'), hex_to_hsl('#F0F8FF')],
    ['HoneyDew',         '#F0FFF0', hex_to_rgb('#F0FFF0'), hex_to_hsl('#F0FFF0')],
    ['Azure',            '#F0FFFF', hex_to_rgb('#F0FFFF'), hex_to_hsl('#F0FFFF')],
    ['SandyBrown',       '#F4A460', hex_to_rgb('#F4A460'), hex_to_hsl('#F4A460')],
    ['Wheat',            '#F5DEB3', hex_to_rgb('#F5DEB3'), hex_to_hsl('#F5DEB3')],
    ['Beige',            '#F5F5DC', hex_to_rgb('#F5F5DC'), hex_to_hsl('#F5F5DC')],
    ['WhiteSmoke',       '#F5F5F5', hex_to_rgb('#F5F5F5'), hex_to_hsl('#F5F5F5')],
    ['MintCream',        '#F5FFFA', hex_to_rgb('#F5FFFA'), hex_to_hsl('#F5FFFA')],
    ['GhostWhite',       '#F8F8FF', hex_to_rgb('#F8F8FF'), hex_to_hsl('#F8F8FF')],
    ['Salmon',           '#FA8072', hex_to_rgb('#FA8072'), hex_to_hsl('#FA8072')],
    ['AntiqueWhite',     '#FAEBD7', hex_to_rgb('#FAEBD7'), hex_to_hsl('#FAEBD7')],
    ['Linen',            '#FAF0E6', hex_to_rgb('#FAF0E6'), hex_to_hsl('#FAF0E6')],
    ['LightGoldenRodYellow', '#FAFAD2', hex_to_rgb('#FAFAD2'), hex_to_hsl('#FAFAD2')],
    ['OldLace',          '#FDF5E6', hex_to_rgb('#FDF5E6'), hex_to_hsl('#FDF5E6')],
    ['Red',              '#FF0000', hex_to_rgb('#FF0000'), hex_to_hsl('#FF0000')],
    ['Fuchsia',          '#FF00FF', hex_to_rgb('#FF00FF'), hex_to_hsl('#FF00FF')],
    ['Magenta',          '#FF00FF', hex_to_rgb('#FF00FF'), hex_to_hsl('#FF00FF')],
    ['DeepPink',         '#FF1493', hex_to_rgb('#FF1493'), hex_to_hsl('#FF1493')],
    ['OrangeRed',        '#FF4500', hex_to_rgb('#FF4500'), hex_to_hsl('#FF4500')],
    ['Tomato',           '#FF6347', hex_to_rgb('#FF6347'), hex_to_hsl('#FF6347')],
    ['HotPink',          '#FF69B4', hex_to_rgb('#FF69B4'), hex_to_hsl('#FF69B4')],
    ['Coral',            '#FF7F50', hex_to_rgb('#FF7F50'), hex_to_hsl('#FF7F50')],
    ['DarkOrange',       '#FF8C00', hex_to_rgb('#FF8C00'), hex_to_hsl('#FF8C00')],
    ['LightSalmon',      '#FFA07A', hex_to_rgb('#FFA07A'), hex_to_hsl('#FFA07A')],
    ['Orange',           '#FFA500', hex_to_rgb('#FFA500'), hex_to_hsl('#FFA500')],
    ['LightPink',        '#FFB6C1', hex_to_rgb('#FFB6C1'), hex_to_hsl('#FFB6C1')],
    ['Pink',             '#FFC0CB', hex_to_rgb('#FFC0CB'), hex_to_hsl('#FFC0CB')],
    ['Gold',             '#FFD700', hex_to_rgb('#FFD700'), hex_to_hsl('#FFD700')],
    ['PeachPuff',        '#FFDAB9', hex_to_rgb('#FFDAB9'), hex_to_hsl('#FFDAB9')],
    ['NavajoWhite',      '#FFDEAD', hex_to_rgb('#FFDEAD'), hex_to_hsl('#FFDEAD')],
    ['Moccasin',         '#FFE4B5', hex_to_rgb('#FFE4B5'), hex_to_hsl('#FFE4B5')],
    ['Bisque',           '#FFE4C4', hex_to_rgb('#FFE4C4'), hex_to_hsl('#FFE4C4')],
    ['MistyRose',        '#FFE4E1', hex_to_rgb('#FFE4E1'), hex_to_hsl('#FFE4E1')],
    ['BlanchedAlmond',   '#FFEBCD', hex_to_rgb('#FFEBCD'), hex_to_hsl('#FFEBCD')],
    ['PapayaWhip',       '#FFEFD5', hex_to_rgb('#FFEFD5'), hex_to_hsl('#FFEFD5')],
    ['LavenderBlush',    '#FFF0F5', hex_to_rgb('#FFF0F5'), hex_to_hsl('#FFF0F5')],
    ['SeaShell',         '#FFF5EE', hex_to_rgb('#FFF5EE'), hex_to_hsl('#FFF5EE')],
    ['Cornsilk',         '#FFF8DC', hex_to_rgb('#FFF8DC'), hex_to_hsl('#FFF8DC')],
    ['LemonChiffon',     '#FFFACD', hex_to_rgb('#FFFACD'), hex_to_hsl('#FFFACD')],
    ['FloralWhite',      '#FFFAF0', hex_to_rgb('#FFFAF0'), hex_to_hsl('#FFFAF0')],
    ['Snow',             '#FFFAFA', hex_to_rgb('#FFFAFA'), hex_to_hsl('#FFFAFA')],
    ['Yellow',           '#FFFF00', hex_to_rgb('#FFFF00'), hex_to_hsl('#FFFF00')],
    ['LightYellow',      '#FFFFE0', hex_to_rgb('#FFFFE0'), hex_to_hsl('#FFFFE0')],
    ['Ivory',            '#FFFFF0', hex_to_rgb('#FFFFF0'), hex_to_hsl('#FFFFF0')],
    ['White',            '#FFFFFF', hex_to_rgb('#FFFFFF'), hex_to_hsl('#FFFFFF')]
])

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
            r = hex_to_dec(h[0:2])
            g = hex_to_dec(h[2:4])
            b = hex_to_dec(h[4:6])
            return ( r, g, b)

    return ( False, False, False)

def hexa_to_hsl(hexa):
    if check_hsl(hsl):
        return list[np.where(list[:,HEXA]==hexa)][HSL]
    else:
        rgb = hex_to_rgb(hexa)
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

    return np.random.choice(list[:,ndx], 1)

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

def hex_to_dec(hexa):
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
    if  e == 'TX': return 'red'
    elif e == 'TG': return 'green'
    elif e == 'TN': return 'blue'
    elif e == 'T10N': return 'orange'
    elif e == 'DDVEC': return 'gray'
    elif e == 'FG': return 'orange'
    elif e == 'RH': return 'blue'
    elif e == 'SQ': return 'yellow'
    elif e == 'PG': return 'purple'
    elif e == 'UG': return rnd_color()
    elif e == 'FXX': return rnd_color()
    elif e == 'FHVEC': return rnd_color()
    elif e == 'FHX': return rnd_color()
    elif e == 'FHN': return rnd_color()
    elif e == 'SP': return rnd_color()
    elif e == 'Q': return rnd_color()
    elif e == 'DR': return rnd_color()
    elif e == 'RHX': return rnd_color()
    elif e == 'PX': return rnd_color()
    elif e == 'PN': return rnd_color()
    elif e == 'VVN': return rnd_color()
    elif e == 'VVX': return rnd_color()
    elif e == 'NG': return rnd_color()
    elif e == 'UX': return rnd_color()
    elif e == 'UN': return rnd_color()
    elif e == 'EV24': return rnd_color()
    return rnd_color()
