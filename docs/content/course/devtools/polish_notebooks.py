#!/usr/bin/env python3
"""
Notebook Polisher for MolSysMT Master Course.
Resets execution counts and cleans metadata from Jupyter Notebooks in the course directory.
"""

import json
from pathlib import Path

COURSE_DIR = Path(__file__).resolve().parent.parent


def polish_notebook(nb_path: Path):
    try:
        with open(nb_path, "r", encoding="utf-8") as f:
            nb_data = json.load(f)
    except Exception as e:
        print(f"Error reading {nb_path}: {e}")
        return False

    modified = False
    for cell in nb_data.get("cells", []):
        if cell.get("cell_type") == "code":
            if cell.get("execution_count") is not None:
                cell["execution_count"] = None
                modified = True
            for out in cell.get("outputs", []):
                if "execution_count" in out and out["execution_count"] is not None:
                    out["execution_count"] = None
                    modified = True

    if modified:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb_data, f, indent=1, ensure_ascii=False)
            f.write("\n")
        return True
    return False


def main():
    print("🧹 Polishing MolSysMT Master Course Notebooks...\n")
    polished_count = 0
    total_count = 0

    for nb_path in COURSE_DIR.glob("**/*.ipynb"):
        if ".ipynb_checkpoints" in nb_path.parts:
            continue
        total_count += 1
        if polish_notebook(nb_path):
            polished_count += 1
            print(f"  P Cleaned: {nb_path.relative_to(COURSE_DIR)}")

    print(f"\n✅ Polishing finished. {polished_count}/{total_count} notebooks updated.")


if __name__ == "__main__":
    main()
