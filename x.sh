#!/usr/bin/env bash
set -e

sigla_regex='^(BUC|FRI|PET|WAL|WIN)-[MCBD]-[0-9]{4}[abcd]$'

find modules -type f -name "*.adoc" | while read -r file; do
    base=$(basename "$file" .adoc)

    # Only process filenames matching siglum pattern
    if [[ ! $base =~ $sigla_regex ]]; then
        continue
    fi

    # Extract original anchor — appears in the last few lines
    old=$(grep -oE '^\* \[\[\[[^]]+]\]\]' "$file" | \
          sed -E 's/^\* \[\[\[([^]]+)]].*/\1/' || true)

    # If no anchor found, skip file
    if [[ -z "$old" ]]; then
        continue
    fi

    echo "Updating $file:"
    echo "  Anchor: $old → $base"

    # 1. Replace all cross-references BEFORE the anchor definition.
    #
    # Because <<old,...>> ALWAYS comes before the * [[[old]]] line,
    # it is safe to rewrite all occurrences globally.
    sed -i -E "s/<<${old},/<<${base},/g" "$file"

    # 2. Replace the anchor definition line itself.
    sed -i -E "s/^(\* \[\[\[)${old}(\]\]\])/\\1${base}\\2/" "$file"
done

