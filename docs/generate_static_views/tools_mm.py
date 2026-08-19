from pathlib import Path
import molsysmt as msm
import pyunitwizard as puw
import numpy as np

views_dir = Path("docs/_static/views")
views_dir.mkdir(parents=True, exist_ok=True)

print("=== Generating Molecular Mechanics Static HTML Views ===")

# 1. tools_mm_get_forces_1.html
print("1/2: Generating tools_mm_get_forces_1.html...")
molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35.h5msm'], to_form='molsysmt.MolSys')
view1 = msm.view(molsys)
view1.export.html(str(views_dir / "tools_mm_get_forces_1.html"), background="transparent")
print(" -> Saved tools_mm_get_forces_1.html")

# 2. tools_mm_get_non_bonded_potential_energy_1.html
print("2/2: Generating tools_mm_get_non_bonded_potential_energy_1.html...")
molsys_dimer = msm.convert(msm.systems['Barnase-Barstar']['1brs.h5msm'], to_form='molsysmt.MolSys')
view2 = msm.view(molsys_dimer)
view2.export.html(str(views_dir / "tools_mm_get_non_bonded_potential_energy_1.html"), background="transparent")
print(" -> Saved tools_mm_get_non_bonded_potential_energy_1.html")

print("=== Molecular Mechanics Views Generated Successfully! ===")
