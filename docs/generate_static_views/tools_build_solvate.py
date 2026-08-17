import os
import molsysmt as msm

output_dir = 'docs/_static/views'
os.makedirs(output_dir, exist_ok=True)

# View 1: cubic box solvated 1VII
molsys1 = msm.convert('pdb_id:1vii', to_form='molsysmt.MolSys')
molsys1_cub = msm.build.solvate(molsys1, box_shape='cubic', clearance='14.0 angstroms')
molsys1_cub = msm.pbc.wrap_to_pbc(molsys1_cub, center_of_selection='molecule_type=="peptide"')
view1 = msm.view(molsys1_cub)
path1 = os.path.join(output_dir, 'tools_build_solvate_1.html')
view1.export.html(path1, background="transparent")
print(f"Generated {path1}")

# View 2: truncated octahedral box solvated 1VII
molsys1_oct = msm.build.solvate(molsys1, box_shape='truncated octahedral', clearance='14.0 angstroms')
molsys1_oct = msm.pbc.wrap_to_pbc(molsys1_oct, center_of_selection='molecule_type=="peptide"')
view2 = msm.view(molsys1_oct)
path2 = os.path.join(output_dir, 'tools_build_solvate_2.html')
view2.export.html(path2, background="transparent")
print(f"Generated {path2}")
