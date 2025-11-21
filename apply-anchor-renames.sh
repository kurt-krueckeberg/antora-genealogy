#!/bin/bash

MAP="sigla-map.txt"

while read old new; do
    [ -z "$old" ] && continue
    echo "Renaming $old → $new"

    find modules -name '*.adoc' -print0 \
      | xargs -0 sed -i \
        -e "s/\[\[\[${old}\]\]\]/[[[${new}]]]/g" \
        -e "s/<<${old}>>/<<${new}>>/g"

done < "$MAP"

