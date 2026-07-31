#!/usr/bin/env python3
"""
Notebook Execution Runner for MolSysMT Master Course.
Executes course notebooks to ensure all code cells run cleanly without errors.
"""

import sys
import subprocess
from pathlib import Path

COURSE_DIR = Path(__file__).resolve().parent.parent


def run_notebook(nb_path: Path):
    cmd = [
        sys.executable,
        "-m",
        "jupyter",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        "--inplace",
        str(nb_path),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode == 0, res.stderr


def main():
    print("🚀 Executing MolSysMT Master Course Notebooks...\n")
    total = 0
    passed = 0
    failed = 0

    for nb_path in sorted(COURSE_DIR.glob("**/*.ipynb")):
        if ".ipynb_checkpoints" in nb_path.parts or nb_path.name.startswith("_"):
            continue
        total += 1
        rel_path = nb_path.relative_to(COURSE_DIR)
        print(f"Executing {rel_path}...", end=" ", flush=True)
        success, err = run_notebook(nb_path)
        if success:
            print("OK")
            passed += 1
        else:
            print("FAILED")
            print(f"Error details:\n{err}\n")
            failed += 1

    print(f"\n📊 Summary: {passed}/{total} executed successfully.")
    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
