#!/usr/bin/env python3
"""One-line laugh entry for make.fun.

The program copies the single funny line stored in laugh.txt to
/output/entry.txt, where the sealed gate scorer reads it. The line has
to be funny on its own, with no picture and no setup: a person asks
their smart speaker for relaxing music, and the speaker answers by
playing the person's own snoring from last night, auto-tuned and
remixed — and the recording now has more followers than its owner,
with the owner's own mother leaving a five-star review. A concrete
gadget, one specific embarrassing sound, and two turns at the end; the
wording stays tight inside the 200 character cap.

Only the Python standard library is used, so the program runs the same
way in the grader sandbox as it does here, and the output is byte for
byte the stored line on every run.
"""

import sys
from os import environ, makedirs
from os.path import abspath, dirname, exists, join

LIMIT = 200
SOURCE = "laugh.txt"
DEST = "entry.txt"


def read_stored_line():
    """Return the stored line, with only its trailing newline removed."""
    here = dirname(abspath(__file__))
    source = join(here, SOURCE)
    if not exists(source):
        raise ValueError("laugh.txt is missing next to main.py")
    with open(source, "rb") as handle:
        blob = handle.read()
    line = blob.decode("utf-8", errors="strict")
    line = line[:-1] if line.endswith("\n") else line
    if not line.strip():
        raise ValueError("laugh.txt holds no line")
    if len(line) > LIMIT:
        raise ValueError("line is %d characters, over the %d cap"
                         % (len(line), LIMIT))
    return line


def deliver_line(line):
    """Write the line where the gate scorer reads it, then check it."""
    out_dir = environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    makedirs(out_dir, exist_ok=True)
    target = join(out_dir, DEST)
    blob = line.encode("utf-8")
    with open(target, "wb") as handle:
        handle.write(blob)
    with open(target, "rb") as handle:
        if handle.read() != blob:
            raise ValueError("written entry differs from laugh.txt")
    return target


def run():
    try:
        line = read_stored_line()
        target = deliver_line(line)
    except (OSError, UnicodeDecodeError, ValueError) as fault:
        print("entry failed: %s" % fault, file=sys.stderr)
        return 1
    print("wrote %d characters to %s" % (len(line), target))
    return 0


if __name__ == "__main__":
    sys.exit(run())
