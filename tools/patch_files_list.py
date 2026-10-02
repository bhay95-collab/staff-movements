#!/usr/bin/env python3
"""Physiotherapy_Screen: the 'Documents for review' list.
 - file names wrap onto two lines (extension removed, it is shown on the badge) instead of being cut off
 - every file type gets a coloured badge with its extension (PDF, DOCX, XLSX, PPTX, MP4, HTML ...), folders keep a folder icon
usage: patch_files_list.py <folder containing Physiotherapy_Screen.pa.yaml>   (edited in place)
"""
import sys, os

EXT = 'If(CountRows(Split(ThisItem.FileName, ".")) > 1, Lower(Last(Split(ThisItem.FileName, ".")).Value), "")'
TYPES = [  # extensions, colour
    (('pdf',), (209, 52, 56)),
    (('doc', 'docx', 'rtf'), (24, 90, 189)),
    (('xls', 'xlsx', 'csv'), (16, 124, 65)),
    (('ppt', 'pptx'), (196, 62, 28)),
    (('mp4', 'mov', 'avi', 'wmv', 'mkv'), (122, 63, 192)),
    (('png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg'), (0, 130, 114)),
    (('msg', 'eml'), (0, 114, 198)),
    (('zip', '7z', 'rar'), (141, 110, 99)),
    (('html', 'htm', 'txt'), (70, 90, 120)),
]
DEFAULT = (90, 106, 128)

def colour(alpha):
    cases = []
    for exts, (r, g, b) in TYPES:
        for e in exts:
            cases.append(f'"{e}", RGBA({r}, {g}, {b}, {alpha})')
    r, g, b = DEFAULT
    return f'With({{e: {EXT}}}, Switch(e, {", ".join(cases)}, RGBA({r}, {g}, {b}, {alpha})))'

NAME = ('With({n: Coalesce(ThisItem.FileName, ThisItem.Name)}, If(ThisItem.IsFolder = true || CountRows(Split(n, ".")) < 2, n, '
        'Left(n, Len(n) - Len(Last(Split(n, ".")).Value) - 1)))')
BADGE = f'With({{e: {EXT}}}, If(e = "", "FILE", Upper(Left(e, 4))))'

def children(sp):
    raw = f'''{sp}- conDocIcon_Pt:
{sp}    Control: GroupContainer@1.5.0
{sp}    Variant: ManualLayout
{sp}    Properties:
{sp}      Fill: ={'If(ThisItem.IsFolder = true, RGBA(255, 183, 77, 0.2), ' + colour('0.12') + ')'}
{sp}      Height: =44
{sp}      RadiusBottomLeft: =12
{sp}      RadiusBottomRight: =12
{sp}      RadiusTopLeft: =12
{sp}      RadiusTopRight: =12
{sp}      Width: =44
{sp}      X: =12
{sp}      Y: =14
{sp}    Children:
{sp}      - icoDoc_Pt:
{sp}          Control: Classic/Icon@2.5.0
{sp}          Properties:
{sp}            Color: =RGBA(230, 140, 0, 1)
{sp}            Height: =26
{sp}            Icon: =Icon.Folder
{sp}            Visible: =ThisItem.IsFolder = true
{sp}            Width: =26
{sp}            X: =9
{sp}            Y: =9
{sp}      - lblDocExt_Pt:
{sp}          Control: Label@2.5.1
{sp}          Properties:
{sp}            Align: =Align.Center
{sp}            Color: ={colour('1')}
{sp}            Font: =Font.'Segoe UI'
{sp}            FontWeight: =FontWeight.Bold
{sp}            Height: =Parent.Height
{sp}            Size: =11
{sp}            Text: ={BADGE}
{sp}            VerticalAlign: =VerticalAlign.Middle
{sp}            Visible: =!(ThisItem.IsFolder = true)
{sp}            Width: =Parent.Width
{sp}- lblDocName_Pt:
{sp}    Control: Label@2.5.1
{sp}    Properties:
{sp}      Color: =RGBA(14, 28, 42, 1)
{sp}      Font: =Font.'Segoe UI'
{sp}      FontWeight: =FontWeight.Bold
{sp}      Height: =40
{sp}      Size: =14
{sp}      Text: ={NAME}
{sp}      VerticalAlign: =VerticalAlign.Bottom
{sp}      Width: =Parent.Width - 150
{sp}      X: =68
{sp}      Y: =7
{sp}- lblDocKind_Pt:
{sp}    Control: Label@2.5.1
{sp}    Properties:
{sp}      Color: =RGBA(140, 155, 174, 1)
{sp}      Font: =Font.'Segoe UI'
{sp}      Height: =18
{sp}      Size: =11
{sp}      Text: =If(ThisItem.IsFolder = true, "Folder", If(CountRows(Split(ThisItem.FileName, ".")) > 1, Upper(Last(Split(ThisItem.FileName, ".")).Value) & " file", "File"))
{sp}      Width: =Parent.Width - 150
{sp}      X: =68
{sp}      Y: =49
{sp}- icoDocGo_Pt:
{sp}    Control: Classic/Icon@2.5.0
{sp}    Properties:
{sp}      Color: =RGBA(140, 155, 174, 1)
{sp}      Height: =24
{sp}      Icon: =Icon.ChevronRight
{sp}      Visible: =ThisItem.IsFolder = true
{sp}      Width: =24
{sp}      X: =Parent.Width - 40
{sp}      Y: =24
{sp}- lblDocOpen_Pt:
{sp}    Control: Label@2.5.1
{sp}    Properties:
{sp}      Align: =Align.Right
{sp}      Color: =RGBA(26, 90, 153, 1)
{sp}      Font: =Font.'Segoe UI'
{sp}      FontWeight: =FontWeight.Bold
{sp}      Height: =20
{sp}      Size: =12
{sp}      Text: ="Open"
{sp}      Visible: =!(ThisItem.IsFolder = true)
{sp}      Width: =60
{sp}      X: =Parent.Width - 76
{sp}      Y: =26'''
    out = []
    for line in raw.split('\n'):
        st = line.lstrip(' ')
        key, _, val = st.partition(': ')
        if val.startswith('=') and (': ' in val or ' #' in val):
            pad = ' ' * (len(line) - len(st))
            out += [f'{pad}{key}: |-', f'{pad}  {val}']
        else:
            out.append(line)
    return out

def patch(path):
    L = open(path, encoding='utf-8').read().split('\n')
    s = next(i for i, l in enumerate(L) if l.strip() == '- conDocIcon_Pt:')
    e = next(i for i, l in enumerate(L) if l.strip() == '- btnDocRow_Pt:')
    sp = ' ' * (len(L[s]) - len(L[s].lstrip()))
    L[s:e] = children(sp)
    # taller rows (two lines of name + the kind line)
    g = next(i for i, l in enumerate(L) if l.strip() == '- Gallery_Docs_Pt:')
    r = next(i for i in range(g, len(L)) if l_is(L[i], '- Pt_DocRow:'))
    for i in range(g, r):
        if L[i].strip() == 'TemplateSize: =72':
            L[i] = L[i].replace('=72', '=80')
    for i in range(r, r + 14):
        if L[i].strip() == 'Height: =64':
            L[i] = L[i].replace('=64', '=72'); break
    open(path, 'w', encoding='utf-8').write('\n'.join(L))

def l_is(line, text):
    return line.strip() == text

if __name__ == '__main__':
    patch(os.path.join(sys.argv[1], 'Physiotherapy_Screen.pa.yaml'))
