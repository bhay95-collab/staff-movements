#!/usr/bin/env python3
"""Add two link buttons to the desktop screens.

Equipment_Main: 'Prescription Support' -> equipment prescription support tool
Ward_All:       'Outcome Measures'     -> basic outcome measures tool
usage: patch_links.py <folder with Equipment_Main.pa.yaml and Ward_All.pa.yaml>   (edited in place)
"""
import sys, re, os

PRESCRIBE = 'https://bhay95-collab.github.io/stars-wheelchair-prescription/'
OUTCOMES = 'https://bhay95-collab.github.io/basic-outcome-measures/'


def ind(l):
    return len(l) - len(l.lstrip(' '))


def block_range(lines, start):
    i = ind(lines[start])
    j = start + 1
    while j < len(lines) and (lines[j].strip() == '' or ind(lines[j]) > i):
        j += 1
    return start, j


def find(lines, name, after=0):
    for k in range(after, len(lines)):
        if lines[k].strip() == f'- {name}:':
            return k
    raise SystemExit(f'control not found: {name}')


def set_in_block(lines, name, key, val):
    s, e = block_range(lines, find(lines, name))
    # only the control's own properties (first Properties: block)
    p = next(k for k in range(s, e) if lines[k].strip() == 'Properties:')
    pi = ind(lines[p]) + 2
    for k in range(p + 1, e):
        if ind(lines[k]) == pi and lines[k].strip().startswith(key + ':'):
            lines[k] = ' ' * pi + f'{key}: {val}'
            return
        if ind(lines[k]) < pi and lines[k].strip():
            break
    raise SystemExit(f'{name}.{key} not found')


def pill(indent, cname, bname, width, text, icon, url):
    sp = ' ' * indent
    return f'''{sp}- {cname}:
{sp}    Control: GroupContainer@1.5.0
{sp}    Variant: ManualLayout
{sp}    Properties:
{sp}      AlignInContainer: =AlignInContainer.Center
{sp}      BorderStyle: =BorderStyle.None
{sp}      DropShadow: =DropShadow.Semibold
{sp}      Fill: =RGBA(255, 255, 255, 1)
{sp}      Height: =40
{sp}      LayoutMaxHeight: =40
{sp}      LayoutMinHeight: =20
{sp}      LayoutMinWidth: ={width}
{sp}      RadiusBottomLeft: =20
{sp}      RadiusBottomRight: =20
{sp}      RadiusTopLeft: =20
{sp}      RadiusTopRight: =20
{sp}      Width: ={width}
{sp}    Children:
{sp}      - {bname}:
{sp}          Control: Button@0.0.45
{sp}          Properties:
{sp}            Appearance: ='ButtonCanvas.Appearance'.Transparent
{sp}            BorderRadius: =20
{sp}            BorderStyle: =BorderStyle.None
{sp}            Font: =Font.'Segoe UI'
{sp}            FontColor: =RGBA(7, 58, 87, 1)
{sp}            FontSize: =14
{sp}            FontWeight: =FontWeight.Bold
{sp}            Height: =Parent.Height
{sp}            Icon: ="{icon}"
{sp}            IconStyle: ='ButtonCanvas.IconStyle'.Filled
{sp}            Layout: ='ButtonCanvas.Layout'.IconBefore
{sp}            OnSelect: =Launch("{url}")
{sp}            Text: ="{text}"
{sp}            Width: =Parent.Width'''.split('\n')


def append_child(lines, nav, new_block_fn):
    s, e = block_range(lines, find(lines, nav))
    child_indent = ind(lines[s]) + 6          # children of a container
    new = new_block_fn(child_indent)
    lines[e:e] = new


def patch_equipment(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    set_in_block(lines, 'conNav_Eq', 'X', '=485')
    set_in_block(lines, 'conNav_Eq', 'Width', '=840')
    set_in_block(lines, 'lblTitle_EqHdr', 'Width', '=400')
    set_in_block(lines, 'lblSub_EqHdr', 'Width', '=400')
    append_child(lines, 'conNav_Eq', lambda i: pill(i, 'conPrescribe_Eq', 'btnPrescribe_Eq', 200, 'Prescription Support', 'Open', PRESCRIBE))
    open(path, 'w', encoding='utf-8').write('\n'.join(lines))


def patch_ward(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    # make room in the header: Save / Discard and the title block move left a little, the button row grows left
    set_in_block(lines, 'Container62', 'X', '=288')
    set_in_block(lines, 'conDiscard_Ward', 'X', '=394')
    set_in_block(lines, 'TextCanvas7', 'Width', '=205')
    set_in_block(lines, 'TextCanvas7_Sub', 'Width', '=205')
    set_in_block(lines, 'Container211', 'X', '=520')
    set_in_block(lines, 'Container211', 'Width', '=800')
    for name, w in (('Container53', 160), ('Container55', 140), ('Container210', 160)):
        set_in_block(lines, name, 'Width', f'={w}')
        set_in_block(lines, name, 'LayoutMinWidth', f'={w}')
    append_child(lines, 'Container211', lambda i: pill(i, 'conOutcome_Ward', 'btnOutcome_Ward', 165, 'Outcome Measures', 'Open', OUTCOMES))
    open(path, 'w', encoding='utf-8').write('\n'.join(lines))


if __name__ == '__main__':
    d = sys.argv[1]
    patch_equipment(os.path.join(d, 'Equipment_Main.pa.yaml'))
    patch_ward(os.path.join(d, 'Ward_All.pa.yaml'))
