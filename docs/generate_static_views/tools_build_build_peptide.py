import os
import molsysmt as msm

output_dir = 'docs/_static/views'
os.makedirs(output_dir, exist_ok=True)

# View 1: AceAlaNme peptide
molsys1 = msm.build.build_peptide('AceAlaNme')
view1 = msm.view(molsys1)
path1 = os.path.join(output_dir, 'tools_build_build_peptide_1.html')
view1.export.html(path1, background="transparent")
print(f"Generated {path1}")

# View 2: Solvated cationic peptide
molsys2 = msm.build.build_peptide('GRKFRRKFKK')
molsys2 = msm.build.add_missing_terminal_cappings(molsys2, N_terminal='ACE', C_terminal='NME')
molsys2 = msm.structure.center(molsys2)
molsys2 = msm.build.solvate(molsys2, box_shape='truncated octahedral', clearance='14.0 angstroms')
molsys2 = msm.pbc.wrap_to_mic(molsys2)
view2 = msm.view(molsys2)
path2 = os.path.join(output_dir, 'tools_build_build_peptide_2.html')
view2.export.html(path2, background="transparent")
print(f"Generated {path2}")
