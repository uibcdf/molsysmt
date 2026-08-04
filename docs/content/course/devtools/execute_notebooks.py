#!/usr/bin/env python3
"""
Notebook Execution Runner for MolSysMT Master Course.
Executes course notebooks to ensure all code cells run cleanly without errors.
"""

import sys
import subprocess
import argparse
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


def main(quiet: bool = False):
    if not quiet:
        print("🚀 Executing MolSysMT Master Course Notebooks...\n")
    total = 0
    passed = 0
    failed = 0

    for nb_path in sorted(COURSE_DIR.glob("**/*.ipynb")):
        if ".ipynb_checkpoints" in nb_path.parts or nb_path.name.startswith("_"):
            continue
        total += 1
        rel_path = nb_path.relative_to(COURSE_DIR)
        if not quiet:
            print(f"Executing {rel_path}...", end=" ", flush=True)
        success, err = run_notebook(nb_path)
        if success:
            if not quiet:
                print("OK")
            passed += 1
        else:
            if quiet:
                print(f"❌ FAILED: {rel_path}")
            else:
                print("FAILED")
            print(f"Error details:\n{err}\n")
            failed += 1

    if not quiet or failed > 0:
        print(f"\n📊 Summary: {passed}/{total} executed successfully.")
    else:
        print(f"✔ All {total} Master Course notebooks executed successfully.")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute Master Course Notebooks")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode: suppress successful execution logs, show errors and summary only.")
    args = parser.parse_args()
    main(quiet=args.quiet)
