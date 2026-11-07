#!/usr/bin/env python3
"""Forward the legacy course-checker command to its maintained implementation.

The canonical checker lives in devtools/scripts/validate_course.py. Keep one
contract for both entrypoints; historical editorial headings are not a second
validation gate. Arguments, output and native exit status come from that owner.
"""

import runpy
from pathlib import Path

if __name__ == "__main__":
    canonical = (
        Path(__file__).resolve().parents[4] / "devtools/scripts/validate_course.py"
    )
    runpy.run_path(str(canonical), run_name="__main__")
