#!/usr/bin/env python3
"""Ward_All: replace the Classic ComboBox (cmb_PT) in the bed panel with a plain box + pick-list pop-up.

usage: patch_ward_physio.py <Ward_All.pa.yaml in> <out>
"""
import sys, re

INK = 'RGBA(14, 28, 42, 1)'; INK2 = 'RGBA(58, 80, 104, 1)'; MUTED = 'RGBA(140, 155, 174, 1)'; ACC = 'RGBA(26, 90, 153, 1)'
LINE = 'RGBA(14, 42, 70, 0.12)'; WHITE = 'RGBA(255, 255, 255, 1)'; BG2 = 'RGBA(244, 249, 252, 1)'; SEL = 'RGBA(205, 226, 247, 1)'

def block(indent, name, control, props, variant=None, children=''):
    sp = ' ' * indent
    out = f'{sp}- {name}:\n{sp}    Control: {control}\n'
    if variant:
        out += f'{sp}    Variant: {variant}\n'
    out += f'{sp}    Properties:\n'
    for k, v in props:
        if '\n' in v:
            out += f'{sp}      {k}: |-\n'
            for ln in v.split('\n'):
                out += f'{sp}        {ln}\n'
        else:
            out += f'{sp}      {k}: {v}\n'
    if children:
        out += f'{sp}    Children:\n' + children
    return out

def label(ind, name, text, x, y, w, h, size, bold=False, color=INK, extra=()):
    p = [('Color', '=' + color), ('Font', "=Font.'Segoe UI'"), ('Height', f'={h}'), ('Size', f'={size}'), ('Text', text), ('VerticalAlign', '=VerticalAlign.Middle'),
         ('Width', f'={w}'), ('X', f'={x}'), ('Y', f'={y}')]
    if bold:
        p.append(('FontWeight', '=FontWeight.Bold'))
    p.extend(extra)
    return block(ind, name, 'Label@2.5.1', p)

def hitbtn(ind, name, onsel, extra=()):
    return block(ind, name, 'Button@0.0.45', [('Appearance', "='ButtonCanvas.Appearance'.Transparent"), ('BorderStyle', '=BorderStyle.None'),
                                              ('Height', '=Parent.Height'), ('OnSelect', onsel), ('Text', '=""'), ('Width', '=Parent.Width'), ('X', '=0'), ('Y', '=0'), *extra])

def box(ind, name, x, y, w, h, fill, radius, children, border=None, extra=()):
    p = [('DropShadow', '=DropShadow.None'), ('Fill', '=' + fill), ('Height', f'={h}'), ('Width', f'={w}'), ('X', f'={x}'), ('Y', f'={y}'),
         ('RadiusBottomLeft', f'={radius}'), ('RadiusBottomRight', f'={radius}'), ('RadiusTopLeft', f'={radius}'), ('RadiusTopRight', f'={radius}')]
    if border:
        p += [('BorderColor', '=' + border), ('BorderStyle', '=BorderStyle.Solid'), ('BorderThickness', '=1')]
    d = dict(p)
    d.update(dict(extra))
    return block(ind, name, 'GroupContainer@1.5.0', sorted(d.items(), key=lambda t: t[0]), variant='ManualLayout', children=children)

ASSIGNED_THIS = '!IsBlank(LookUp(LookUp(colWard, ID = wdSelID).PTKeys, Key = ThisItem.DisplayKey))'
TOGGLE = '''=With(
    { p: LookUp(colWard, ID = wdSelID), me: ThisItem.DisplayKey },
    If(
        IsBlank(p) || wdIsSaving || wdLoading,
        Blank(),
        With(
            {
                sel: Filter(
                    colClinicians_Physio,
                    If(
                        DisplayKey = me,
                        IsBlank(LookUp(p.PTKeys, Key = DisplayKey)),
                        !IsBlank(LookUp(p.PTKeys, Key = DisplayKey))
                    )
                )
            },
            Patch(
                colWard,
                p,
                {
                    PT_Users: ForAll(sel, PersonRec),
                    PTKeys: ForAll(sel, { Key: DisplayKey }),
                    IsDirty: true
                }
            )
        )
    )
)'''

def panel_children(ind):
    names = block(ind, 'lblPTNames_WB', 'Label@2.5.1', sorted([
        ('Color', '=If(IsEmpty(ThisItem.PTKeys), ' + MUTED + ', ' + INK + ')'), ('Font', "=Font.'Segoe UI'"), ('Height', '=38'), ('Size', '=14'),
        ('Text', '=Coalesce(Concat(Filter(colClinicians_Physio, !IsBlank(LookUp(ThisItem.PTKeys, Key = DisplayKey))), DisplayNameFlat, ", "), "Add physio")'),
        ('VerticalAlign', '=VerticalAlign.Middle'), ('Width', '=316'), ('Wrap', '=false'), ('X', '=10'), ('Y', '=0')], key=lambda t: t[0]))
    chev = block(ind, 'icoPTChev_WB', 'ModernIcon@1.1.1', [('Height', '=20'), ('Icon', '="ChevronDown"'), ('IconColor', '=' + ACC), ('Width', '=20'), ('X', '=332'), ('Y', '=9')])
    open_ = hitbtn(ind, 'btnPTOpen_WB', '=Set(wdShowPTPick, true);\nReset(txtPTSearch_Ward)'.replace('\n', '\n'))
    # a multi-line OnSelect must be a block
    open_ = hitbtn(ind, 'btnPTOpen_WB', '=Set(wdShowPTPick, true);\nReset(txtPTSearch_Ward)')
    return names + chev + open_

def popup(ind):
    i2 = ind + 6
    row_kids = (label(i2 + 12, 'lblPTName_Ward', '=ThisItem.DisplayNameFlat', 14, 0, 340, 42, 14, True, INK, extra=[('Wrap', '=false')]) +
                label(i2 + 12, 'lblPTTick_Ward', '="✓"', 'Parent.Width - 40', 0, 28, 42, 18, True, ACC, extra=[('Align', '=Align.Center'), ('Visible', '=' + ASSIGNED_THIS)]) +
                hitbtn(i2 + 12, 'btnPTRow_Ward', TOGGLE))
    row = box(i2 + 8, 'conPTRow_Ward', 16, 3, 'Parent.TemplateWidth - 32', 42, 'If(' + ASSIGNED_THIS + ', ' + SEL + ', ' + BG2 + ')', 10, row_kids, border=LINE)
    gal = block(i2 + 4, 'galPTPick_Ward', 'Gallery@2.15.0', sorted([
        ('Height', '=336'), ('Items', '=SortByColumns(Filter(colClinicians_Physio, Lower(Trim(txtPTSearch_Ward.Text)) in Lower(DisplayNameFlat)), "DisplayNameFlat", SortOrder.Ascending)'),
        ('TemplatePadding', '=0'), ('TemplateSize', '=48'), ('Width', '=460'), ('X', '=0'), ('Y', '=140')], key=lambda t: t[0]), variant='Vertical', children=row)
    search_inner = block(i2 + 12, 'txtPTSearch_Ward', 'Classic/TextInput@2.3.2', sorted([
        ('BorderStyle', '=BorderStyle.None'), ('Color', '=' + INK), ('Default', '=""'), ('DelayOutput', '=true'), ('Font', "=Font.'Segoe UI'"),
        ('Height', '=40'), ('HintText', '="Search physios"'), ('Size', '=14'), ('Width', '=412')], key=lambda t: t[0]))
    search = box(i2 + 4, 'boxPTSearch_Ward', 24, 88, 412, 40, WHITE, 10, search_inner, border='RGBA(14, 42, 70, 0.22)')
    done_btn = block(i2 + 12, 'btnPTDone_Ward', 'Button@0.0.45', sorted([
        ('Appearance', "='ButtonCanvas.Appearance'.Transparent"), ('BorderRadius', '=22'), ('Font', "=Font.'Segoe UI'"), ('FontColor', '=' + WHITE), ('FontSize', '=15'),
        ('FontWeight', '=FontWeight.Bold'), ('Height', '=44'), ('OnSelect', '=Set(wdShowPTPick, false)'), ('Text', '="Done"'), ('Width', '=240')], key=lambda t: t[0]))
    done = box(i2 + 4, 'conPTDone_Ward', 110, 492, 240, 44, ACC, 22, done_btn)
    title = label(i2 + 4, 'lblPTTitle_Ward', '="Physio"', 24, 18, 412, 30, 20, True, INK)
    sub = label(i2 + 4, 'lblPTSub_Ward', '=LookUp(colWard, ID = wdSelID).Patient & "  ·  tap a name to add or remove"', 24, 50, 412, 22, 13, False, INK2)
    card_kids = title + sub + search + gal + done
    card = box(ind + 6, 'conPTCard_Ward', 453, 104, 460, 560, WHITE, 20, card_kids, extra=[('DropShadow', '=DropShadow.Bold')])
    scrim = hitbtn(ind + 6, 'btnPTScrim_Ward', '=Set(wdShowPTPick, false)')
    props = [('Fill', '=RGBA(14, 28, 42, 0.45)'), ('Height', '=768'), ('Visible', '=wdShowPTPick'), ('Width', '=1366'), ('X', '=0'), ('Y', '=0')]
    return block(ind, 'conPhysioPick_Ward', 'GroupContainer@1.5.0', props, variant='ManualLayout', children=scrim + card)

def patch(text):
    lines = text.split('\n')
    # 1) replace the combo block
    start = next(i for i, l in enumerate(lines) if l.strip() == '- cmb_PT:')
    ind = len(lines[start]) - len(lines[start].lstrip(' '))
    end = start + 1
    while end < len(lines) and (lines[end].strip() == '' or len(lines[end]) - len(lines[end].lstrip(' ')) > ind):
        end += 1
    new = panel_children(ind).rstrip('\n').split('\n')
    lines[start:end] = new
    text = '\n'.join(lines)
    # 2) reset flag when the screen opens
    assert 'Set(wdShowMove, false);' in text
    text = text.replace('Set(wdShowMove, false);', 'Set(wdShowMove, false);\n        Set(wdShowPTPick, false);', 1)
    # 3) pop-up as the last top-level control
    return text.rstrip('\n') + '\n' + popup(6)

if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    open(dst, 'w', encoding='utf-8').write(patch(open(src, encoding='utf-8').read()))
