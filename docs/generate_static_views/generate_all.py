#!/usr/bin/env python
"""Master runner to regenerate all static HTML views (MolSysViewer and NGLView)."""

import subprocess
import sys
from pathlib import Path

script_dir = Path(__file__).resolve().parent

scripts = [
    "1BRS_molecule_index_zero.py",
    "tools_basic_add.py",
    "tools_basic_append_structures.py",
    "tools_basic_concatenate_structures.py",
    "tools_basic_convert.py",
    "tools_basic_get_form.py",
    "tools_basic_merge.py",
    "tools_basic_view.py",
    "tools_build_build_peptide.py",
    "tools_build_make_bioassembly.py",
    "tools_build_solvate.py",
    "tools_mm.py",
    "tools_pbc.py",
    "tools_structure.py",
    "tools_topology.py",
    "cookbook_recipes.py",
    "showcase_views.py",
    "nglview_views.py",
]

print("=" * 60)
print(f"Executing {len(scripts)} static view generator scripts...")
print("=" * 60)

for script_name in scripts:
    script_path = script_dir / script_name
    print(f"\n>>> Running {script_name}...")
    res = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"✘ Error running {script_name}:")
        print(res.stderr)
        sys.exit(res.returncode)
    else:
        print(res.stdout.strip())
        print(f"✔ {script_name} completed successfully.")

print("\n" + "=" * 60)
print("✔ All static HTML views have been regenerated successfully!")
print("=" * 60)
