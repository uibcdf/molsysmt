#!/usr/bin/env python3
"""Synchronize published benchmark data with the canonical baselines."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
CANONICAL_DIRECTORY = REPOSITORY / "benchmarks" / "baselines"
PUBLISHED_DIRECTORY = REPOSITORY / "docs" / "_static" / "benchmarks_data"
PUBLISHED_BASELINES = (
    "competitor_matrix_session.json",
    "macro_kernels_session.json",
)


def synchronize(*, check: bool = False) -> bool:
    """Synchronize published baselines, returning whether they already matched."""

    synchronized = True
    for filename in PUBLISHED_BASELINES:
        canonical = CANONICAL_DIRECTORY / filename
        published = PUBLISHED_DIRECTORY / filename
        matches = published.exists() and published.read_bytes() == canonical.read_bytes()
        synchronized &= matches
        if check:
            if not matches:
                print(f"out of sync: {published.relative_to(REPOSITORY)}")
        elif not matches:
            shutil.copyfile(canonical, published)
            print(f"updated: {published.relative_to(REPOSITORY)}")
    return synchronized


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="report divergence without modifying published files",
    )
    args = parser.parse_args()
    synchronized = synchronize(check=args.check)
    return 0 if synchronized or not args.check else 1


if __name__ == "__main__":
    raise SystemExit(main())
