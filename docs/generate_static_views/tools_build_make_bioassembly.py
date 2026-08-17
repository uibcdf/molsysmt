import os
import molsysmt as msm

output_dir = 'docs/_static/views'
os.makedirs(output_dir, exist_ok=True)

# View 1: 1OUT asymmetric unit
molsys1 = msm.convert('1OUT')
view1 = msm.view(molsys1)
path1 = os.path.join(output_dir, 'tools_build_make_bioassembly_1.html')
view1.export.html(path1, background="transparent")
print(f"Generated {path1}")

# View 2: 1OUT bioassembly 1
molsys1_bio = msm.build.make_bioassembly(molsys1, bioassembly='1')
view2 = msm.view(molsys1_bio)
path2 = os.path.join(output_dir, 'tools_build_make_bioassembly_2.html')
view2.export.html(path2, background="transparent")
print(f"Generated {path2}")

# View 3: 2BUK asymmetric unit
molsys2 = msm.convert('2BUK')
view3 = msm.view(molsys2)
path3 = os.path.join(output_dir, 'tools_build_make_bioassembly_3.html')
view3.export.html(path3, background="transparent")
print(f"Generated {path3}")

# View 4: 2BUK bioassembly 1
molsys2_bio = msm.build.make_bioassembly(molsys2, bioassembly='1')
view4 = msm.view(molsys2_bio)
path4 = os.path.join(output_dir, 'tools_build_make_bioassembly_4.html')
view4.export.html(path4, background="transparent")
print(f"Generated {path4}")
