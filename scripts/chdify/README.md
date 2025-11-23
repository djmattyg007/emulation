# chdify

Convert `.cue` + `.bin` ROMs to `.chd` files.

## Usage

```shell
python3 chdify.py <path to cue file>
```

It's intended to be run over a full folder of `.cue` + `.bin` files, like so:

```shell
for cuefile in *.cue; do python3 chdify "${cuefile}"; done
```

It will automatically detect multi-disc games, and create a `.m3u` playlist file as necessary.

This script will never delete any files. Cleaning up the old `.cue` and `.bin` files is your responsibility.

## Requirements

- Python 3
- `chdman` (must be available in your `PATH`)
