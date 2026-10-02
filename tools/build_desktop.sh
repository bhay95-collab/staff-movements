#!/bin/sh
# Rebuild powerapps/desktop/*.pa.yaml from powerapps/desktop/as_pasted/ (your code as pasted from Studio).
set -e
cd "$(dirname "$0")/.."
T=$(mktemp -d)
cp powerapps/desktop/as_pasted/*.pa.yaml "$T"/
python3 tools/patch_ward_physio.py powerapps/desktop/as_pasted/Ward_All.pa.yaml "$T/Ward_All.pa.yaml"
python3 tools/patch_links.py "$T"
python3 tools/patch_training.py "$T"
python3 tools/make_responsive.py "$T" powerapps/desktop
