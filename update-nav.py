#!/usr/bin/env python3
import re

NAV_FILE = "modules/family-church-records/nav.adoc"
MAP_FILE = "file-rename-map.txt"

# Load rename map
rename = {}
with open(MAP_FILE, "r") as f:
    for line in f:
        line = line.strip()
        if not line or "," not in line:
            continue
        old, new = line.split(",", 1)
        rename[old.strip()] = new.strip()

# Read nav.adoc
with open(NAV_FILE, "r") as f:
    nav = f.read()

# Replace xrefs
def replace_xref(match):
    prefix = match.group(1)   # e.g. "xref:petzen:"
    fname = match.group(2)    # e.g. "petzen-band1a-image89.adoc"

    new = rename.get(fname)
    if new:
        return f"{prefix}{new}[]"
    else:
        return match.group(0)

pattern = r"(xref:[^:]+:)([A-Za-z0-9._-]+)\[\]"
updated = re.sub(pattern, replace_xref, nav)

# Write updated nav.adoc
with open(NAV_FILE, "w") as f:
    f.write(updated)

print("nav.adoc updated.")

