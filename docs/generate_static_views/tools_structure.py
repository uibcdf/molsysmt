from pathlib import Path
import molsysmt as msm

views_dir = Path("docs/_static/views")
views_dir.mkdir(parents=True, exist_ok=True)

print("=== Generating Structure Static HTML Views ===")

# 1. tools_structure_align_principal_axes_1.html
print("1/9: Generating tools_structure_align_principal_axes_1.html...")
protein = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35.h5msm'], to_form='molsysmt.MolSys')
protein_aligned = msm.structure.align_principal_axes(protein, axes=[[1,0,0], [0,1,0], [0,0,1]])
v1 = msm.view(protein_aligned)
v1.export.html(str(views_dir / "tools_structure_align_principal_axes_1.html"), background="transparent")
print(" -> Saved tools_structure_align_principal_axes_1.html")

# 2 & 3. tools_structure_flip_1.html & tools_structure_flip_2.html
print("2/9: Generating tools_structure_flip_1.html...")
crd = msm.systems['POPC']['popc.crd']
psf = msm.systems['POPC']['popc.psf']
molsys_popc = msm.convert([crd, psf], to_form='molsysmt.MolSys')
molsys_popc = msm.structure.align_principal_axes(molsys_popc, axes=[[0, 1, 0], [0, 0, 1], [1, 0, 0]])
molsys_popc = msm.structure.center(molsys_popc, selection='all', center_of_selection='atom_name=="P"')
v2 = msm.view(molsys_popc)
v2.export.html(str(views_dir / "tools_structure_flip_1.html"), background="transparent")
print(" -> Saved tools_structure_flip_1.html")

print("3/9: Generating tools_structure_flip_2.html...")
molsys_flipped = msm.structure.flip(molsys_popc, vector=[0, 1, 0], point='[0, 0, 0] nm')
v3 = msm.view(molsys_flipped)
v3.export.html(str(views_dir / "tools_structure_flip_2.html"), background="transparent")
print(" -> Saved tools_structure_flip_2.html")

# 4 & 5. tools_structure_rotate_1.html & tools_structure_rotate_2.html
print("4/9: Generating tools_structure_rotate_1.html...")
molsys_villin = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35.h5msm'], to_form='molsysmt.MolSys')
v4 = msm.view(molsys_villin)
v4.export.html(str(views_dir / "tools_structure_rotate_1.html"), background="transparent")
print(" -> Saved tools_structure_rotate_1.html")

print("5/9: Generating tools_structure_rotate_2.html...")
rotation_matrix = [
    [0.0, -1.0, 0.0],
    [1.0,  0.0, 0.0],
    [0.0,  0.0, 1.0]
]
molsys_rotated = msm.structure.rotate(molsys_villin, rotation=rotation_matrix)
v5 = msm.view(molsys_rotated)
v5.export.html(str(views_dir / "tools_structure_rotate_2.html"), background="transparent")
print(" -> Saved tools_structure_rotate_2.html")

# 6 & 7. tools_structure_set_dihedral_angles_1.html & tools_structure_set_dihedral_angles_2.html
print("6/9: Generating tools_structure_set_dihedral_angles_1.html...")
molsys_dih = msm.convert(msm.systems['chicken villin HP35']['chicken_villin_HP35.h5msm'], to_form='molsysmt.MolSys')
phi_quartets = msm.topology.get_dihedral_quartets(molsys_dih, phi=True)
v6 = msm.view(molsys_dih)
v6.export.html(str(views_dir / "tools_structure_set_dihedral_angles_1.html"), background="transparent")
print(" -> Saved tools_structure_set_dihedral_angles_1.html")

print("7/9: Generating tools_structure_set_dihedral_angles_2.html...")
molsys_set = msm.structure.set_dihedral_angles(molsys_dih, dihedral_quartets=phi_quartets[1], angles='60.0 degrees')
v7 = msm.view(molsys_set)
v7.export.html(str(views_dir / "tools_structure_set_dihedral_angles_2.html"), background="transparent")
print(" -> Saved tools_structure_set_dihedral_angles_2.html")

# 8 & 9. tools_structure_shift_dihedral_angles_1.html & tools_structure_shift_dihedral_angles_2.html
print("8/9: Generating tools_structure_shift_dihedral_angles_1.html...")
v8 = msm.view(molsys_dih)
v8.export.html(str(views_dir / "tools_structure_shift_dihedral_angles_1.html"), background="transparent")
print(" -> Saved tools_structure_shift_dihedral_angles_1.html")

print("9/9: Generating tools_structure_shift_dihedral_angles_2.html...")
molsys_shifted = msm.structure.shift_dihedral_angles(molsys_dih, dihedral_quartets=phi_quartets[1], shifts='90.0 degrees')
v9 = msm.view(molsys_shifted)
v9.export.html(str(views_dir / "tools_structure_shift_dihedral_angles_2.html"), background="transparent")
print(" -> Saved tools_structure_shift_dihedral_angles_2.html")

print("=== Structure Views Generated Successfully! ===")
