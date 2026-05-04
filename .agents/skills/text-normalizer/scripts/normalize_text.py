#!/usr/bin/env python3
"""Normalize stdin text and emit one Markdown fenced code block."""

from __future__ import annotations

import re
import sys


def normalize(text: str) -> str:
    normalized = re.sub(r" {2,}", " ", text.strip())
    return normalized if normalized else "EMPTY_INPUT"


def fence_for(text: str) -> str:
    longest = max((len(match.group(0)) for match in re.finditer(r"`+", text)), default=0)
    return "`" * max(3, longest + 1 if longest >= 3 else 3)


def main() -> int:
    text = normalize(sys.stdin.read())
    fence = fence_for(text)
    sys.stdout.write(f"{fence}\n{text}\n{fence}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
