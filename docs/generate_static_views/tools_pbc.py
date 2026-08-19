from pathlib import Path
import molsysmt as msm

views_dir = Path("docs/_static/views")
views_dir.mkdir(parents=True, exist_ok=True)

print("=== Generating PBC Static HTML Views ===")

# 1. tools_pbc_wrap_to_mic_1.html
print("1/2: Generating tools_pbc_wrap_to_mic_1.html...")
molsys = msm.convert(msm.systems['Met-enkephalin']['met_enkephalin.h5msm'], to_form='molsysmt.MolSys')
molsys_solvated = msm.build.solvate(molsys, box_shape='truncated octahedral', clearance='14.0 angstroms', engine='PDBFixer')
molsys_mic = msm.pbc.wrap_to_mic(
    molsys_solvated,
    center_of_selection='molecule_type=="peptide"',
    compact='component'
)
view1 = msm.view(molsys_mic)
view1.export.html(str(views_dir / "tools_pbc_wrap_to_mic_1.html"), background="transparent")
print(" -> Saved tools_pbc_wrap_to_mic_1.html")

# 2. tools_pbc_wrap_to_pbc_1.html
print("2/2: Generating tools_pbc_wrap_to_pbc_1.html...")
molsys_pep = msm.convert(msm.systems['Met-enkephalin']['met_enkephalin.h5msm'], to_form='molsysmt.MolSys')
molsys_solv = msm.build.solvate(molsys_pep, box_shape='cubic', clearance='14.0 angstroms', engine='PDBFixer')
molsys_pep_wrapped = msm.pbc.wrap_to_pbc(molsys_solv, compact='component')
view2 = msm.view(molsys_pep_wrapped)
view2.export.html(str(views_dir / "tools_pbc_wrap_to_pbc_1.html"), background="transparent")
print(" -> Saved tools_pbc_wrap_to_pbc_1.html")

print("=== PBC Views Generated Successfully! ===")
