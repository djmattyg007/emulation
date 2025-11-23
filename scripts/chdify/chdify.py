#!/usr/bin/python3

import re
import subprocess
import sys
from pathlib import Path

def chdman(input_file, output_file):
    params = ("chdman", "createcd", "--input", str(input_file), "--output", str(output_file), "--force")
    subprocess.check_call(params)

multidisc_re = re.compile(r"\(Disc (\d)\)$")

cuefile = Path(sys.argv[1])
if cuefile.suffix != ".cue":
    print("mistake", file=sys.stderr)
    sys.exit(1)

name = cuefile.stem

multidisc = False
if multidisc_match := multidisc_re.search(name):
    if multidisc_match.group(1) != "1":
        # Ignore anything that's not disc 1, we'll handle it specially
        sys.exit(0)
    multidisc = True
print(name)

chdfile = cuefile.with_suffix(".chd")
chdman(cuefile, chdfile)

if not multidisc:
    sys.exit(0)

discs = [chdfile]
for disc in range(2, 10):
    multidisc_cuefile = cuefile.with_stem(name.replace("(Disc 1)", f"(Disc {disc})"))
    if not multidisc_cuefile.exists():
        break

    print("multidisc", multidisc_cuefile.stem)
    multidisc_chdfile = multidisc_cuefile.with_suffix(".chd")
    chdman(multidisc_cuefile, multidisc_chdfile)

    discs.append(multidisc_chdfile)

m3ufile = cuefile.with_suffix(".m3u").with_stem(name.replace("(Disc 1)", "").strip())
with m3ufile.open(mode="w", encoding="utf-8") as f:
    for disc in discs:
        f.write(f"{disc.name}\n")
