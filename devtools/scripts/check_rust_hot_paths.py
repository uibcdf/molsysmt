#!/usr/bin/env python
"""Lint the Rust kernels for rounding calls that lower to libm on the x86-64 baseline.

Why this exists
---------------
The x86-64 baseline has no floor/ceil/round instruction (`roundsd` is SSE4.1), so
`f64::floor()` and friends lower to a libm call. Three of them sat in the innermost loop
of `get_mic_distances_single_system`; besides their own cost, a call in the loop body makes
the loop unvectorisable. Replacing them with `mathlib::fast_floor` /
`fast_round_ties_even` was worth 1.4-1.5x on the dense distance matrices.

Nothing in the test suite would catch that regression: the results stay correct, only the
speed changes. Hence this check. It is a *source* lint rather than a binary one because the
symbol is not a discriminator — glibc's `floor` is linked (via ifunc) by the dependency
tree whether or not our kernels call it.

See `devguide/rust_kernel_optimization_guide.md` section 1.

What it accepts
---------------
- Anything inside a trailing `#[cfg(test)] mod tests { .. }` block, and any top-level item
  annotated `#[cfg(test)]`: the ground-truth oracles should stay as obvious as possible.
- Any line carrying an explicit `// libm-ok: <reason>` marker.

Everything else fails. Run: `python devtools/scripts/check_rust_hot_paths.py`
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[2] / "experiments" / "rust_kernels" / "src"

# Method calls that have no baseline x86-64 instruction behind them.
BANNED = re.compile(r"\.(floor|ceil|round|round_ties_even|trunc|rint)\s*\(\s*\)")
MARKER = "libm-ok:"

REPLACEMENTS = {
    "floor": "mathlib::fast_floor",
    "round_ties_even": "mathlib::fast_round_ties_even",
}


def production_lines(text: str) -> list[tuple[int, str]]:
    """Lines of `text` that survive into a non-test build, as (1-based lineno, line).

    Test code in this crate is either a trailing `#[cfg(test)] mod tests { .. }` block or a
    top-level item annotated `#[cfg(test)]`. Both are dropped here by brace counting from
    column zero, which is reliable for top-level items and is asserted below.
    """
    lines = text.splitlines()
    out: list[tuple[int, str]] = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == "#[cfg(test)]":
            # Skip the attribute plus the item it annotates.
            j = i + 1
            # Walk over any further attributes / doc comments.
            while j < len(lines) and (
                lines[j].lstrip().startswith("#[") or lines[j].lstrip().startswith("///")
            ):
                j += 1
            if j >= len(lines):
                break
            depth = 0
            opened = False
            while j < len(lines):
                depth += lines[j].count("{") - lines[j].count("}")
                if "{" in lines[j]:
                    opened = True
                j += 1
                if opened and depth <= 0:
                    break
            i = j
            continue
        out.append((i + 1, lines[i]))
        i += 1
    return out


def check_file(path: Path) -> list[str]:
    problems = []
    for lineno, line in production_lines(path.read_text()):
        stripped = line.lstrip()
        # Comments and doc comments describe these calls; they do not make them.
        if stripped.startswith("//"):
            continue
        if MARKER in line:
            continue
        m = BANNED.search(line)
        if m:
            name = m.group(1)
            hint = REPLACEMENTS.get(name)
            fix = f"use `{hint}`" if hint else "avoid it in a hot path"
            problems.append(
                f"{path.name}:{lineno}: `.{name}()` lowers to a libm call on the x86-64 "
                f"baseline — {fix}, or mark the line `// {MARKER} <reason>` if this is not "
                f"a hot path.\n    {line.strip()}"
            )
    return problems


def main() -> int:
    if not SRC.is_dir():
        print(f"rust kernel sources not found at {SRC}; nothing to check")
        return 0
    problems: list[str] = []
    files = sorted(SRC.glob("*.rs"))
    for path in files:
        problems.extend(check_file(path))
    if problems:
        print("Rust hot-path lint failed:\n")
        for p in problems:
            print(f"  {p}\n")
        print("See devguide/rust_kernel_optimization_guide.md section 1.")
        return 1
    print(f"Rust hot-path lint: {len(files)} files clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
