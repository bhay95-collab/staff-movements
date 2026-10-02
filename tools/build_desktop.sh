#!/bin/sh
# Rebuild powerapps/desktop/*.pa.yaml from powerapps/desktop/as_pasted/ (your code as pasted from Studio).
set -e
cd "$(dirname "$0")/.."
T=$(mktemp -d)
cp powerapps/desktop/as_pasted/*.pa.yaml "$T"/
python3 tools/patch_ward_physio.py powerapps/desktop/as_pasted/Ward_All.pa.yaml "$T/Ward_All.pa.yaml"
python3 tools/patch_links.py "$T"
python3 tools/make_responsive.py "$T" powerapps/desktop
# the shared email look goes at the bottom of the formulas
python3 - <<'PY'
e = open('powerapps/email/Email_Formulas.txt', encoding='utf-8').read()
p = 'powerapps/desktop/Desktop_App_Formulas.txt'
d = open(p, encoding='utf-8').read().rstrip('\n')
open(p, 'w', encoding='utf-8').write(d + '\n\n// ---- Email look (shared by every email the app sends)\n' + e[e.index('EmailHead ='):])
PY
