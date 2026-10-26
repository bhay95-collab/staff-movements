"""Build a service's copy of the tracker from index.html (the STARS build).

    python3 tools/make_site.py redcliffe Redcliffe_Staff_Movement_Tracker.html

Only branding and the browser storage name change. The browser storage name must stay
different per service so two trackers opened on one computer never share saved data.
"""
import sys

SITES = {
    'redcliffe': {'name': 'Redcliffe Physiotherapy', 'slug': 'RedcliffePhysiotherapy', 'db': 'redcliffeMovementTracker'},
}

def build(site, src='index.html'):
    s = open(src, encoding='utf-8').read()
    swaps = [
        ("const DB_NAME='starsMovementTracker'", "const DB_NAME='%s'" % site['db']),
        ('STARSPhysiotherapy_StaffMovementTracker', site['slug'] + '_StaffMovementTracker'),
        ('STARS Physiotherapy', site['name']),
    ]
    for old, new in swaps:
        if old not in s:
            sys.exit('Not found in %s: %s' % (src, old))
        s = s.replace(old, new)
    if 'STARS' in s:
        sys.exit('A STARS reference is left over; add a swap for it.')
    return s

if __name__ == '__main__':
    out = build(SITES[sys.argv[1]])
    open(sys.argv[2], 'w', encoding='utf-8').write(out)
    print('Wrote', sys.argv[2])
