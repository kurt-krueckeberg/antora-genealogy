#!/bin/bash

cd modules/family-church-records/

echo "= Church Records" > nav.adoc
echo "" >> nav.adoc
echo "* xref:index.adoc[Overview]" >> nav.adoc
echo "" >> nav.adoc
echo "== Events" >> nav.adoc

for f in pages/*.adoc; do
    base=$(basename "$f" .adoc)
    echo "* xref:$base.adoc[]" >> nav.adoc
done

