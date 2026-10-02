#!/usr/bin/env python3
"""Add the 'Training' button to the Home screen's bottom bar (between Team Info and Manager tools).

usage: patch_training.py <folder containing Home_Main.pa.yaml>   (edited in place)
"""
import sys, os


def ind(l):
    return len(l) - len(l.lstrip(' '))


def block_range(lines, start):
    i = ind(lines[start])
    j = start + 1
    while j < len(lines) and (lines[j].strip() == '' or ind(lines[j]) > i):
        j += 1
    return start, j


def find(lines, name):
    for k, l in enumerate(lines):
        if l.strip() == f'- {name}:':
            return k
    raise SystemExit(f'control not found: {name}')


def pill(sp):
    return f'''{sp}- conTraining_Home:
{sp}    Control: GroupContainer@1.5.0
{sp}    Variant: ManualLayout
{sp}    Properties:
{sp}      BorderColor: =RGBA(14, 42, 70, 0.12)
{sp}      BorderThickness: =1
{sp}      DropShadow: =DropShadow.None
{sp}      Fill: =RGBA(255, 255, 255, 1)
{sp}      Height: =46
{sp}      RadiusBottomLeft: =23
{sp}      RadiusBottomRight: =23
{sp}      RadiusTopLeft: =23
{sp}      RadiusTopRight: =23
{sp}      Width: =150
{sp}      X: =824
{sp}      Y: =11
{sp}    Children:
{sp}      - btnTraining_Home:
{sp}          Control: Button@0.0.45
{sp}          Properties:
{sp}            Appearance: ='ButtonCanvas.Appearance'.Transparent
{sp}            BorderRadius: =23
{sp}            Font: =Font.'Segoe UI'
{sp}            FontColor: =RGBA(58, 80, 104, 1)
{sp}            FontSize: =16
{sp}            FontWeight: =FontWeight.Bold
{sp}            Height: =46
{sp}            Icon: ="Heart"
{sp}            IconStyle: ='ButtonCanvas.IconStyle'.Filled
{sp}            Layout: ='ButtonCanvas.Layout'.IconBefore
{sp}            OnSelect: =Navigate(Training_Hub, ScreenTransition.Fade)
{sp}            Text: ="Training"
{sp}            Width: =150'''.split('\n')


def patch_home(path):
    lines = open(path, encoding='utf-8').read().split('\n')
    s, e = block_range(lines, find(lines, 'conTeam_Home'))
    lines[e:e] = pill(' ' * ind(lines[s]))
    open(path, 'w', encoding='utf-8').write('\n'.join(lines))


if __name__ == '__main__':
    patch_home(os.path.join(sys.argv[1], 'Home_Main.pa.yaml'))
