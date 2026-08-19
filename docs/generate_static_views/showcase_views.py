from pathlib import Path
import molsysmt as msm

views_dir = Path("docs/_static/views")
views_dir.mkdir(parents=True, exist_ok=True)

print("=== Generating Showcase MolSysViewer Static HTML Views ===")

# --- Quickstart Views ---
print("1/10: Generating quickstart_1.html...")
molsys_181l = msm.convert('181L', selection='molecule_type=="protein"')
v = msm.view(molsys_181l)
v.export.html(str(views_dir / "quickstart_1.html"), background="transparent")
print(" -> Saved quickstart_1.html")

print("2/10: Generating quickstart_2.html...")
pep = msm.build.build_peptide('AceAlaAlaAlaNme')
pep_solv = msm.build.solvate(pep, box_shape='truncated octahedral', clearance='14.0 angstroms')
pep_mic = msm.pbc.wrap_to_mic(pep_solv, center_of_selection='molecule_type=="peptide"')
v = msm.view(pep_mic)
v.export.html(str(views_dir / "quickstart_2.html"), background="transparent")
print(" -> Saved quickstart_2.html")

print("3/10: Generating quickstart_3.html...")
v = msm.view(molsys_181l)
v.export.html(str(views_dir / "quickstart_3.html"), background="transparent")
print(" -> Saved quickstart_3.html")

# --- Barnase-Barstar Views ---
print("4/10: Generating barnase_barstar_1.html...")
molsys_1brs = msm.convert('1BRS')
v = msm.view(molsys_1brs)
v.export.html(str(views_dir / "barnase_barstar_1.html"), background="transparent")
print(" -> Saved barnase_barstar_1.html")

print("5/10: Generating barnase_barstar_2.html...")
barnase = msm.extract(molsys_1brs, selection='chain_name=="A"')
v = msm.view(barnase)
v.export.html(str(views_dir / "barnase_barstar_2.html"), background="transparent")
print(" -> Saved barnase_barstar_2.html")

print("6/10: Generating barnase_barstar_3.html...")
barstar = msm.extract(molsys_1brs, selection='chain_name=="D"')
v = msm.view(barstar)
v.export.html(str(views_dir / "barnase_barstar_3.html"), background="transparent")
print(" -> Saved barnase_barstar_3.html")

print("7/10: Generating barnase_barstar_4.html...")
dimer = msm.merge([barnase, barstar])
v = msm.view(dimer)
v.export.html(str(views_dir / "barnase_barstar_4.html"), background="transparent")
print(" -> Saved barnase_barstar_4.html")

# --- Dialanine Monte Carlo View ---
print("8/10: Generating dialanine_monte_carlo_1.html...")
dialanine = msm.build.build_peptide('AceAlaNme')
v = msm.view(dialanine)
v.export.html(str(views_dir / "dialanine_monte_carlo_1.html"), background="transparent")
print(" -> Saved dialanine_monte_carlo_1.html")

# --- MD Trajectory View ---
print("9/10: Generating showcase_md_trajectory.html...")
traj = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'])
traj = msm.structure.least_rmsd_fit(traj, selection_fit="atom_name=='CA'", reference_structure_index=0)
v = msm.view(traj)
v.export.html(str(views_dir / "showcase_md_trajectory.html"), background="transparent")
print(" -> Saved showcase_md_trajectory.html")

# --- OpenMM View ---
print("10/10: Generating showcase_openmm.html...")
v = msm.view(dialanine)
v.export.html(str(views_dir / "showcase_openmm.html"), background="transparent")
print(" -> Saved showcase_openmm.html")

print("=== Showcase Views Generated Successfully! ===")
