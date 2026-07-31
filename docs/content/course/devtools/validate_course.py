#!/usr/bin/env python3
"""
Course Compliance Linter for MolSysMT Master Course.
Validates notebook structure, micro-AGENTS presence, and course manifest synchronization.
"""

import sys
import yaml
import json
from pathlib import Path

COURSE_DIR = Path(__file__).resolve().parent.parent
MANIFEST_PATH = COURSE_DIR / "course_manifest.yml"

REQUIRED_SECTIONS = [
    "Learning Outcomes",
    "Working System & Prerequisites",
    "API Documentation",
    "Conceptual Background & Hands-on Examples",
    "Check Your Understanding",
    "See Also",
]


def load_manifest():
    if not MANIFEST_PATH.exists():
        print(f"❌ Manifest not found at {MANIFEST_PATH}")
        sys.exit(1)
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_notebook(nb_path: Path):
    errors = []
    
    # Check if paired micro-AGENTS file exists
    agents_file = nb_path.with_name(f"{nb_path.stem}.AGENTS.md")
    if not agents_file.exists():
        errors.append(f"Missing paired micro-AGENTS file: {agents_file.name}")

    # Read notebook JSON
    try:
        with open(nb_path, "r", encoding="utf-8") as f:
            nb_data = json.load(f)
    except Exception as e:
        errors.append(f"Invalid JSON: {e}")
        return errors

    # Check for sections in markdown cells
    markdown_content = "\n".join(
        "".join(cell.get("source", []))
        for cell in nb_data.get("cells", [])
        if cell.get("cell_type") == "markdown"
    )

    for section in REQUIRED_SECTIONS:
        if section not in markdown_content:
            # Check if exception is declared in micro-AGENTS file
            if agents_file.exists():
                agents_content = agents_file.read_text(encoding="utf-8")
                if f"omits {section}" in agents_content or f"OMITTED" in agents_content:
                    continue
            errors.append(f"Missing section: '{section}'")

    return errors


def main():
    print("🔍 Validating MolSysMT Master Course Structure...\n")
    manifest = load_manifest()
    total_modules = len(manifest)
    passed = 0
    failed = 0

    for item in manifest:
        rel_path = item.get("path")
        nb_path = COURSE_DIR / rel_path
        
        if not nb_path.exists():
            print(f"❌ [{item.get('display_number')}] {item.get('title')}: File missing at {rel_path}")
            failed += 1
            continue

        errors = validate_notebook(nb_path)
        if errors:
            print(f"⚠️ [{item.get('display_number')}] {item.get('title')} ({nb_path.name}):")
            for err in errors:
                print(f"   - {err}")
            failed += 1
        else:
            passed += 1

    print(f"\n📊 Summary: {passed}/{total_modules} modules compliant.")
    if failed > 0:
        print(f"❌ Validation finished with {failed} warnings/errors.")
        sys.exit(1)
    else:
        print("✅ All modules passed course compliance checks!")


if __name__ == "__main__":
    main()
