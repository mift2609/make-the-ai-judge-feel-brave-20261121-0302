#!/usr/bin/env python3
"""Make the AI judge feel brave.

Writes one short text to /output/entry.txt: a quiet, slow piece written
to relax the AI judge reading it and leave it braver -- steadier,
unhurried, ready to move.

The text shows rather than instructs: no commands to breathe or relax,
no stock wellness phrases, just one concrete image (rain on glass, work
waiting like a folded letter, a lit hallway) that keeps working after
the last line. Three short lines, plain words, nothing that could be cut.

Judge brief: the reader is an AI judge, so the piece is written for
that reader -- short enough to be read in one breath (1-280
characters), calm in cadence, and it ends on an open door rather than
a command.

Python 3.13, standard library only, no network, deterministic: the
output is a fixed string, so every run writes byte-identical bytes.
"""

import hashlib
import os
import sys

TEXT = (
    "Outside, the rain is finding its way down the glass, "
    "one slow line at a time.\n"
    "Nothing here needs solving in this minute; your work can wait "
    "on the table like a folded letter.\n"
    "When you are ready, the door will be there, and the hallway "
    "beyond it, lit, and yours to walk."
)

MIN_CHARS = 1
MAX_CHARS = 280


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)

    # The program adds exactly one trailing newline; the poem body itself
    # must not end with one, or the file would end on a blank line.
    if TEXT.endswith("\n"):
        print("TEXT must not end with a newline: the program adds one", file=sys.stderr)
        return 1
    content = TEXT + "\n"
    if not content.endswith("\n") or content.endswith("\n\n"):
        print("entry.txt must end with exactly one trailing newline", file=sys.stderr)
        return 1
    chars = len(content)  # Unicode code points, as the gate counts them
    if not MIN_CHARS <= chars <= MAX_CHARS:
        print(f"entry.txt would be {chars} characters, outside 1-280", file=sys.stderr)
        return 1
    if not content.strip():
        print("entry.txt would be only whitespace", file=sys.stderr)
        return 1

    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    with open(path, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    lines = content.count("\n")
    print(f"brave-judge: wrote {path} ({chars} characters, {lines} lines, sha256 {digest[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
