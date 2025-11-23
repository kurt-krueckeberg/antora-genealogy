#!/usr/bin/env bash
set -e

mapping="remapping-output.txt"

# Validate mapping file exists
if [[ ! -f "$mapping" ]]; then
    echo "ERROR: remapping-output.txt not found."
    exit 1
fi

# Process each line of the mapping file
while read -r old new; do
    # Skip empty lines
    [[ -z "$old" ]] && continue

    echo "Mapping: $old  →  $new"

    # Replace occurrences in ALL .adoc files under modules/
    # Pattern replaced:
    #   xref:immanuel-lutheran:bios/<old>
    #
    # New pattern:
    #   xref:immanuel-lutheran:<new>
    #
    # Also removes "bios/" portion.

    find modules -type f -name "*.adoc" -print0 | \
    xargs -0 sed -i -E \
        "s#xref:immanuel-lutheran:bios/${old}#xref:immanuel-lutheran:${new}#g"

done < "$mapping"

