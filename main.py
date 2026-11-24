#!/usr/bin/env python3
"""Worst AI Advice — make.fun entry.

The program emits exactly one line of deliberately terrible advice,
written in the confident voice of an AI assistant, to ``entry.txt``
inside the output directory the harness provides. The line is 106
characters, well inside the 140-character cap, and the file holds the
line alone, with no trailing newline.
"""

import os
import sys
from pathlib import Path

# One line, one terrible idea: a gas leak found with a lit match.
ADVICE = (
    "Certainly! To check for a gas leak, light a match near the pipe "
    "\u2014 the flame shows you exactly where it is."
)

CAP = 140
FILENAME = "entry.txt"


def resolve_target() -> Path:
    """Pick the file the harness will read the line from."""
    root = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    folder = Path(root)
    folder.mkdir(parents=True, exist_ok=True)
    return folder / FILENAME


def guard(line: str) -> None:
    """Refuse to emit anything the sealed gate would reject."""
    if line != line.strip():
        raise ValueError("advice carries leading or trailing whitespace")
    if not line.strip():
        raise ValueError("advice is blank")
    if "\n" in line or "\r" in line:
        raise ValueError("advice must stay on one line")
    if len(line) > CAP:
        raise ValueError(f"advice is {len(line)} chars, over the {CAP} cap")


def emit() -> Path:
    """Check the line, then write it as UTF-8 bytes, no newline."""
    guard(ADVICE)
    target = resolve_target()
    target.write_bytes(ADVICE.encode("utf-8"))
    # Read it back: what landed on disk must be the line, byte for byte.
    landed = target.read_bytes()
    if landed != ADVICE.encode("utf-8"):
        raise ValueError("entry.txt on disk does not match the advice")
    return target


def run() -> int:
    target = emit()
    print(f"wrote {target} ({len(ADVICE)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(run())
