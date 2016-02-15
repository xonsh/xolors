#!/usr/bin/env python
import re
import math
from pprint import pprint, pformat
from colortrans import rgb2short
from pygments.styles import get_style_by_name, get_all_styles

BASE_COLORS = {
    'BLACK': (0, 0, 0),
    'RED': (170, 0, 0),
    'GREEN': (0, 170, 0),
    'YELLOW': (170, 85, 0),
    'BLUE': (0, 0, 170),
    'PURPLE': (170, 0, 170),
    'CYAN': (0, 170, 170),
    'WHITE': (170, 170, 170),
    'INTENSE_BLACK': (85, 85, 85),
    'INTENSE_RED': (255, 85, 85),
    'INTENSE_GREEN': (85, 255, 85),
    'INTENSE_YELLOW': (255, 255, 85),
    'INTENSE_BLUE': (85, 85, 255),
    'INTENSE_PURPLE': (255, 85, 255),
    'INTENSE_CYAN': (85, 255, 255),
    'INTENSE_WHITE': (255, 255, 255),
}


RE_RGB3 = re.compile(r'(.)(.)(.)')
RE_RGB6 = re.compile(r'(..)(..)(..)')

def rgb2ints(rgb):
    if len(rgb) == 6:
        return tuple([int(h, 16) for h in RE_RGB6.split(rgb)[1:4]])
    else:
        return tuple([int(h*2, 16) for h in RE_RGB3.split(rgb)[1:4]])

def dist(x, y):
    return math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2 + (x[2]-y[2])**2)


def find_closest(x, pallette):
    key = lambda k: dist(x, pallette[k])
    return min(pallette.keys(), key=key)

def make_ansi_style(pallette):
    style = {'NO_COLOR': '0'}
    for name, t in BASE_COLORS.items():
        closest = find_closest(t, pallette)
        if len(closest) == 3:
            closest = ''.join([a*2 for a in closest])
        short = rgb2short(closest)[0]
        style[name] = '38;5;' + short
        style['BOLD_'+name] = '1;38;5;' + short
        style['UNDERLINE_'+name] = '4;38;5;' + short
        style['BOLD_UNDERLINE_'+name] = '1;4;38;5;' + short
        style['BACKGROUND_'+name] = '48;5;' + short
    return style


def make_pallete(strings):
    pallette = {}
    for s in strings:
        while '#' in s:
            _, t = s.split('#', 1)
            t, _, s = t.partition(' ')
            pallette[t] = rgb2ints(t)
    return pallette

def usname(name):
    return name.replace('-', '_').upper()


style_names = sorted(get_all_styles())

for name in style_names:
    if name == 'default':
        continue
    pstyle = get_style_by_name(name)
    pallette = make_pallete(pstyle.styles.values())
    astyle = make_ansi_style(pallette)
    out = usname(name) + '_STYLE = {\n ' + pformat(astyle, indent=4)[1:-1] + ',\n}\n'
    print(out)

print('styles = {')
for name in style_names:
    print("    '"+name+"': " +usname(name) + '_STYLE,')
print('}')
