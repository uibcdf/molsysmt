from pathlib import Path
import molsysmt as msm
import pyunitwizard as puw
import numpy as np

views_dir = Path("docs/_static/views")
views_dir.mkdir(parents=True, exist_ok=True)

print("=== Generating Cookbook Static HTML Views ===")

# 1. cookbook_binding_pocket.html
print("1/7: Generating cookbook_binding_pocket.html...")
molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
pocket = msm.extract(molsys, selection="all within 0.5 nm of molecule_name=='BENZENE'")
view = msm.view(pocket)
view.export.html(str(views_dir / "cookbook_binding_pocket.html"), background="transparent")
print(" -> Saved cookbook_binding_pocket.html")

# 2. cookbook_dimers_initial.html
print("2/7: Generating cookbook_dimers_initial.html...")
molsys_1brs = msm.convert(msm.systems['Barnase-Barstar']['1brs.h5msm'])
molsys_1brs = msm.extract(molsys_1brs, selection="molecule_type=='protein'")
barnase = msm.extract(molsys_1brs, selection="chain_name=='B'")
barstar_ref = msm.extract(molsys_1brs, selection="chain_name=='E'")
barstar_best = msm.extract(molsys_1brs, selection="chain_name=='F'")

view = msm.view(barnase)
view.export.html(str(views_dir / "cookbook_dimers_initial.html"), background="transparent")
print(" -> Saved cookbook_dimers_initial.html")

# 3. cookbook_dimers_aligned.html
print("3/7: Generating cookbook_dimers_aligned.html...")
barstar_aligned = msm.structure.least_rmsd_align(
    barstar_best,
    selection='atom_name=="CA"',
    reference_molecular_system=barstar_ref
)
view = msm.view([barnase, barstar_aligned])
view.export.html(str(views_dir / "cookbook_dimers_aligned.html"), background="transparent")
print(" -> Saved cookbook_dimers_aligned.html")

# 4. cookbook_dimers_final.html
print("4/7: Generating cookbook_dimers_final.html...")
dimer = msm.merge([barnase, barstar_aligned])
dimer = msm.build.add_missing_heavy_atoms(dimer)
dimer = msm.build.add_missing_hydrogens(dimer, pH=7.4)
view = msm.view(dimer)
view.export.html(str(views_dir / "cookbook_dimers_final.html"), background="transparent")
print(" -> Saved cookbook_dimers_final.html")

# 5. cookbook_solvated_box.html
print("5/7: Generating cookbook_solvated_box.html...")
molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35.h5msm'], to_form='molsysmt.MolSys')
molsys = msm.build.add_missing_terminal_cappings(molsys)
solvated_molsys = msm.build.solvate(
    [molsys, {'forcefield': 'AMBER14', 'water_model': 'TIP3P'}],
    box_shape='cubic',
    clearance='10.0 angstroms',
    to_form='molsysmt.MolSys',
    engine='OpenMM'
)
view = msm.view(solvated_molsys)
view.export.html(str(views_dir / "cookbook_solvated_box.html"), background="transparent")
print(" -> Saved cookbook_solvated_box.html")

# 6. cookbook_mutagenesis_mutant.html
print("6/7: Generating cookbook_mutagenesis_mutant.html...")
molsys_wt = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
molsys_wt = msm.extract(molsys_wt, selection='molecule_type=="protein"')
molsys_mut = msm.build.mutate(molsys_wt, mutations={18: 'ALA'}, keys='group_index')
molsys_mut = msm.build.add_missing_heavy_atoms(molsys_mut)
molsys_mut = msm.build.add_missing_hydrogens(molsys_mut, pH=7.4)
view = msm.view(molsys_mut)
view.export.html(str(views_dir / "cookbook_mutagenesis_mutant.html"), background="transparent")
print(" -> Saved cookbook_mutagenesis_mutant.html")

# 7. cookbook_simulation_solvated.html
print("7/7: Generating cookbook_simulation_solvated.html...")
molsys = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35.h5msm'], to_form='molsysmt.MolSys')
molsys = msm.build.add_missing_terminal_cappings(molsys)
molsys = msm.build.add_missing_hydrogens(molsys)
solvated_molsys = msm.build.solvate(
    [molsys, {'forcefield': 'AMBER14', 'water_model': 'TIP3P'}],
    box_shape='cubic',
    clearance='10.0 angstroms',
    to_form='molsysmt.MolSys',
    engine='OpenMM'
)
view = msm.view(solvated_molsys)
view.export.html(str(views_dir / "cookbook_simulation_solvated.html"), background="transparent")
print(" -> Saved cookbook_simulation_solvated.html")

print("=== Cookbook Views Generated Successfully! ===")
