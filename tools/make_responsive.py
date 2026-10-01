#!/usr/bin/env python3
"""Make the desktop Power Apps screens fill any window.

The screens were drawn on a 1366 x 768 canvas with fixed X / Y / Width / Height numbers.
This rewrites every one of those numbers as  <number> * SX  (across) or  <number> * SY  (down),
text sizes as  Round(<size> * SF, 0), and corner radii as  <radius> * SR.
SX, SY, SF and SR are named formulas (see Desktop_App_Formulas.txt) worked out from App.Width / App.Height,
so at 1366 x 768 nothing moves, and on any other window everything stretches to fill it.

usage: make_responsive.py <input folder of .pa.yaml> <output folder>
"""
import re, sys, os, glob

X_KEYS = {'X', 'Width', 'LayoutMinWidth', 'LayoutMaxWidth', 'PaddingLeft', 'PaddingRight'}
Y_KEYS = {'Y', 'Height', 'LayoutMinHeight', 'LayoutMaxHeight', 'PaddingTop', 'PaddingBottom'}
R_KEYS = {'RadiusBottomLeft', 'RadiusBottomRight', 'RadiusTopLeft', 'RadiusTopRight', 'BorderRadius',
          'BorderRadiusBottomLeft', 'BorderRadiusBottomRight', 'BorderRadiusTopLeft', 'BorderRadiusTopRight', 'LayoutGap'}
F_KEYS = {'Size', 'FontSize'}
G_KEYS = {'TemplateSize', 'TemplatePadding'}      # direction depends on the gallery

PROP = re.compile(r'^(\s*)([A-Za-z][A-Za-z.]*): (=.*)$')
NUM = r'\d+(?:\.\d+)?'


def scale_expr(val, f):
    """val starts with '='. f is the factor name (SX, SY, SR)."""
    body = val[1:].strip()
    if re.fullmatch(r'-?' + NUM, body):
        n = float(body)
        if n == 0:
            return val
        return f'={body} * {f}'
    out = body
    # Parent.Width - 20   ->   Parent.Width - 20 * SX
    out = re.sub(r'([+-]\s*)(' + NUM + r')(?![\d.])(?!\s*\*)', lambda m: f'{m.group(1)}{m.group(2)} * {f}', out)
    # If(cond, 84, 114)   ->   If(cond, 84 * SX, 114 * SX)
    out = re.sub(r'(,\s*)(' + NUM + r')(?=\s*[,)])', lambda m: f'{m.group(1)}{m.group(2)} * {f}', out)
    # 200 * ThisItem.Pct / 100   ->   200 * SX * ThisItem.Pct / 100
    out = re.sub(r'^(' + NUM + r')(\s*\*)', lambda m: f'{m.group(1)} * {f}{m.group(2)}', out)
    return '=' + out


def convert(text):
    lines = text.split('\n')
    out = []
    variant = None
    i = 0
    skip_indent = None
    changed = 0
    while i < len(lines):
        l = lines[i]
        stripped = l.strip()
        ind = len(l) - len(l.lstrip(' '))
        if skip_indent is not None:
            if stripped == '' or ind > skip_indent:
                out.append(l); i += 1; continue
            skip_indent = None
        m = re.match(r'^\s*- \w+:\s*$', l)
        if m:
            variant = None
        mv = re.match(r'^\s*Variant: (\w+)\s*$', l)
        if mv:
            variant = mv.group(1)
        if re.match(r'^\s*[A-Za-z][A-Za-z.]*: \|-?\s*$', l):
            skip_indent = ind
            out.append(l); i += 1; continue
        pm = PROP.match(l)
        if pm:
            sp, key, val = pm.groups()
            f = None
            if key in X_KEYS: f = 'SX'
            elif key in Y_KEYS: f = 'SY'
            elif key in R_KEYS: f = 'SR'
            elif key in G_KEYS: f = 'SX' if variant == 'Horizontal' else 'SY'
            if key in F_KEYS:
                body = val[1:].strip()
                if re.fullmatch(r'\d+', body) and int(body) >= 8:
                    l = f'{sp}{key}: =Round({body} * SF, 0)'; changed += 1
            elif f:
                new = scale_expr(val, f)
                if new != val:
                    l = f'{sp}{key}: {new}'; changed += 1
        out.append(l)
        i += 1
    return '\n'.join(out), changed


FORMULAS = '''// =====================================================================
// App > Formulas   (desktop app)  paste the whole thing
// Everything on the screens is drawn for a 1366 x 768 window and then stretched with these.
// =====================================================================

// across and down
SX = App.Width / 1366;
SY = App.Height / 768;

// text: follows the smaller of the two, never below 75% or above 140%
SF = Max(0.75, Min(1.4, Min(SX, SY)));

// corner radii and gaps: follow the smaller of the two so rounded buttons stay round
SR = Min(SX, SY);
'''

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    for f in sorted(glob.glob(os.path.join(src, '*.pa.yaml'))):
        t = open(f, encoding='utf-8').read()
        new, n = convert(t)
        open(os.path.join(dst, os.path.basename(f)), 'w', encoding='utf-8').write(new)
        print(os.path.basename(f), n)
    open(os.path.join(dst, 'Desktop_App_Formulas.txt'), 'w', encoding='utf-8').write(FORMULAS)
