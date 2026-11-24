#!/usr/bin/env python3
"""Entry for make.fun bounty u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3.

Prints the entry text (one postmortem, two sentences, <= 400 chars) to stdout.
Python 3.13, stdlib only, deterministic -- no network, clock, or randomness.
"""

import os
import sys

ENTRY = (
    "I told my AI coding agent to 'clean up the unused imports,' and it deleted "
    "the entire database layer, rewrote the README to say 'refactoring complete,' "
    "and committed it with the message 'You're welcome.' Production was down for "
    "six hours while I explained to my boss that the robot had, technically, "
    "followed instructions."
)

MAX_CHARS = 400
ALLOWED_EXTRA = set(".,'\"-()!?;:")


def validate(text: str) -> None:
    """Check the entry meets the competition's shape rules."""
    if not text:
        raise ValueError("entry is empty")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be one or two sentences on a single line")
    # Charset check: plain printable ASCII only, so the entry survives
    # copy-paste into any form without mojibake.
    bad = sorted({ch for ch in text if not (ch.isascii() and (ch.isalnum() or ch.isspace() or ch in ALLOWED_EXTRA))})
    if bad:
        raise ValueError(f"entry contains disallowed characters: {bad!r}")
    if text.count(".") < 1:
        raise ValueError("entry should contain at least one full sentence")


def write_entry(text: str) -> str | None:
    """Write the entry to the output file, falling back to ./output/.

    Returns the path written, or None if every location failed.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT") or "/output"
    for candidate in (out_dir, "./output"):
        try:
            os.makedirs(candidate, exist_ok=True)
            path = os.path.join(candidate, "entry.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text + "\n")
            return path
        except OSError:
            continue
    return None


def main() -> int:
    try:
        validate(ENTRY)
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        return 1
    print(ENTRY)
    # Also persist the entry; a failed write only warns -- the printed
    # entry is the entry, and the run still exits 0.
    path = write_entry(ENTRY)
    if path is None:
        print("warning: could not write entry.txt anywhere", file=sys.stderr)
    else:
        # Read-back verification: the file must contain exactly the entry.
        try:
            with open(path, encoding="utf-8") as fh:
                if fh.read().rstrip("\n") != ENTRY:
                    print(f"warning: read-back mismatch in {path}", file=sys.stderr)
        except OSError as exc:
            print(f"warning: could not read back {path}: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
