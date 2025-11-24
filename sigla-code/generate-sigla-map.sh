#!/bin/bash

INPUT="h1-headers.txt"
OUTPUT="sigla-map.txt"

echo "Generating sigla-map.txt …"
echo "# old-anchor   new-siglum" > "$OUTPUT"

while IFS=" ::: " read -r file header; do
    fname=$(basename "$file")

    # Match siglum filename with OPTIONAL trailing letter
    if [[ "$fname" =~ ^[A-Z]{3,5}-[A-Z]-[0-9]{3,4}[a-z]?\.adoc$ ]]; then
        siglum="${fname%.adoc}"

        # Extract old "imageXXX" portion
        old=$(echo "$file" | sed -E 's|.*/([^/]*image[^./]*)\.adoc|\1|')

        if [[ "$old" == image* ]]; then
            echo "$old $siglum" >> "$OUTPUT"
        fi
    fi
done < "$INPUT"

echo "Done. Created: $OUTPUT"

