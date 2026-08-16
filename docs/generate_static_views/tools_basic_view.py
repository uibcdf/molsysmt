import os
import molsysmt as msm

os.makedirs('docs/_static/views', exist_ok=True)

print("Generating static HTML view 1 for view.ipynb...")
v1 = msm.view('181L')
v1.export.html('docs/_static/views/tools_basic_view_1.html', background='transparent')
print("Generated docs/_static/views/tools_basic_view_1.html!")

print("Generating static HTML view 2 for view.ipynb...")
v2 = msm.view('181L', selection='molecule_name=="BENZENE"')
v2.export.html('docs/_static/views/tools_basic_view_2.html', background='transparent')
print("Generated docs/_static/views/tools_basic_view_2.html!")

print("Generating static HTML view 3 for view.ipynb...")
ms = msm.convert('181L', selection='molecule_type=="protein" or molecule_name=="BENZENE"', to_form='openmm.Modeller')
v3 = msm.view(ms, selection='all within 7.0 angstroms of molecule_type=="small molecule"')
v3.export.html('docs/_static/views/tools_basic_view_3.html', background='transparent')
print("Generated docs/_static/views/tools_basic_view_3.html!")
