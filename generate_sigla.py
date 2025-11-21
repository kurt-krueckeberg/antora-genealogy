#!/usr/bin/env python3
import re
import sys
from collections import defaultdict

# Parish → code
PARISH_CODES = {
    "petzen": "PET",
    "frille": "FRI",
    "windheim": "WIND",
    "buchholz": "BUC",
    "wallensen": "WAL",
}

META_KEYWORDS = [
    "Kirchenbücher",
    "Remarks",
    "Progress Notes",
    "Prospective Relationships",
    "Early Krückeberg",
]

SKIP_FILENAMES = {
    "index.adoc",
}

def detect_event_type(h1: str) -> str | None:
    """Return B/M/D/C or None if unknown."""
    lower = h1.lower()
    etype = None

    if any(w in lower for w in ["baptism", "baptized", "birth"]):
        etype = "B"
    if "stillborn" in lower and etype is None:
        etype = "B"
    if "marriage" in lower:
        etype = "M"
    if any(w in lower for w in ["burial", "buried", "interred", "death", "died"]):
        etype = "D"
    if "confirmation" in lower:
        etype = "C"

    return etype

def main(path):
    records = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if " ::: " not in line:
                continue
            fullpath, h1 = line.split(" ::: ", 1)
            h1 = h1.strip()
            if h1.startswith("="):
                h1 = h1.lstrip("= ").strip()

            parts = fullpath.split("/")
            if len(parts) < 3:
                continue

            parish = parts[1]
            fname = parts[-1]

            # Skip index/meta/cover/etc.
            if fname in SKIP_FILENAMES:
                continue
            if any(k in h1 for k in META_KEYWORDS):
                continue
            if "Cover" in h1 or "Images Baptisms" in h1:
                continue
            if "???" in h1:
                continue
            if not h1:
                continue

            # Year: prefer leading year; else last 4-digit year
            m = re.match(r"(\d{3,4})\b", h1)
            if m:
                year = int(m.group(1))
            else:
                m_all = list(re.finditer(r"\b(\d{3,4})\b", h1))
                year = int(m_all[-1].group(1)) if m_all else None

            etype = detect_event_type(h1)
            records.append(
                {
                    "path": fullpath,
                    "parish": parish,
                    "fname": fname,
                    "h1": h1,
                    "year": year,
                    "etype": etype,
                }
            )

    # Warn about anything we couldn’t classify
    unclassified = [
        r for r in records if r["year"] is None or r["etype"] is None
    ]
    if unclassified:
        print("# UNCLASSIFIED (needs manual review):", file=sys.stderr)
        for r in unclassified:
            print(f"# {r['path']} ::: {r['h1']}", file=sys.stderr)

    usable = [r for r in records if r["year"] is not None and r["etype"] is not None]

    groups = defaultdict(list)
    for r in usable:
        key = (r["parish"], r["etype"], r["year"])
        groups[key].append(r)

    # Assign sigla and output
    print("# old_path\tparish\tetype\tyear\tsiglum\tnew_path")
    for (parish, etype, year), recs in sorted(groups.items()):
        parish_code = PARISH_CODES.get(parish, parish.upper())
        recs_sorted = sorted(recs, key=lambda r: r["path"])
        for idx, r in enumerate(recs_sorted):
            suffix = chr(ord("a") + idx)
            siglum = f"{parish_code}-{etype}-{year}{suffix}"
            dirpath = "/".join(r["path"].split("/")[:-1])
            new_path = f"{dirpath}/{siglum}.adoc"
            print(
                f"{r['path']}\t{parish}\t{etype}\t{year}\t{siglum}\t{new_path}"
            )

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generate_sigla.py church-records-h1-list.txt", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])

