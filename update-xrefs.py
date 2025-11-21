#!/usr/bin/env python3
import os
import re

# Load rename map
mapping = {}
with open("file-rename-map.txt") as f:
    for line in f:
        line = line.strip()
        if not line or "," not in line:
            continue
        old, new = line.split(",", 1)
        mapping[old.strip()] = new.strip()

# Regex patterns
# 1) xref:module:file.adoc[…]
pattern_with_module = re.compile(r'(xref:[a-zA-Z0-9_-]+:)([^:\[\]]+\.adoc)')
# 2) xref:file.adoc[…]
pattern_without_module = re.compile(r'(xref:)([^:\[\]]+\.adoc)')

# Walk through repository
for root, dirs, files in os.walk("."):
    for filename in files:
        if not filename.endswith(".adoc"):
            continue

        path = os.path.join(root, filename)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        original = content

        # Replace module-prefixed xrefs
        def repl_with_module(match):
            prefix = match.group(1)
            oldfile = match.group(2)
            return prefix + mapping.get(oldfile, oldfile)

        content = pattern_with_module.sub(repl_with_module, content)

        # Replace xrefs without module prefix
        def repl_without_module(match):
            prefix = match.group(1)
            oldfile = match.group(2)
            return prefix + mapping.get(oldfile, oldfile)

        content = pattern_without_module.sub(repl_without_module, content)

        # Save if changed
        if content != original:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"UPDATED: {path}")

