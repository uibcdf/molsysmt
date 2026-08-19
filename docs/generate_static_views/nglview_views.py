from pathlib import Path
import os
import molsysmt as msm
import nglview as nv
import numpy as np

static_ngl = Path("docs/_static/nglview")
third_party_ngl = static_ngl / "user" / "third_party" / "nglview"

static_ngl.mkdir(parents=True, exist_ok=True)
third_party_ngl.mkdir(parents=True, exist_ok=True)

print("=== Generating NGLView Static HTML Views ===")

def get_repr_dict_from_msgs(msg_archive):
    repr_dict = {}
    loadfile_count = 0
    for msg in msg_archive:
        method = msg.get('methodName')
        target = msg.get('target')
        if method == 'loadFile':
            loadfile_count += 1
        elif method == 'addRepresentation' and target == 'compList':
            args = msg.get('args', [])
            kwargs = msg.get('kwargs', {}).copy()
            comp_idx = str(kwargs.pop('component_index', 0))
            repr_type = args[0] if args else 'cartoon'
            if comp_idx not in repr_dict:
                repr_dict[comp_idx] = {}
            r_idx = str(len(repr_dict[comp_idx]))
            repr_dict[comp_idx][r_idx] = {
                'type': repr_type,
                'params': kwargs
            }
    if not repr_dict and loadfile_count > 0:
        for c in range(loadfile_count):
            repr_dict[str(c)] = {'0': {'type': 'cartoon', 'params': {'sele': 'all'}}}
    return repr_dict

def write_nglview_html(view, filepath):
    import json
    from bs4 import BeautifulSoup
    msm.third_party.nglview.write_html(view, str(filepath))
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    require_config_snippet = """<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js" integrity="sha256-Ae2Vz/4ePdIu6ZyI/5ZGsYnb+m0JlOmKPjt6XZ9JJkA=" crossorigin="anonymous"></script>
<script>
require.config({
    paths: {
        'nglview-js-widgets': 'https://cdn.jsdelivr.net/npm/nglview-js-widgets@3.0.1/dist/index'
    }
});
</script>"""
    old_tag = '<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js" integrity="sha256-Ae2Vz/4ePdIu6ZyI/5ZGsYnb+m0JlOmKPjt6XZ9JJkA=" crossorigin="anonymous"></script>'
    if old_tag in content and 'require.config' not in content:
        content = content.replace(old_tag, require_config_snippet)
    
    soup = BeautifulSoup(content, 'html.parser')
    script = soup.find('script', type='application/vnd.jupyter.widget-state+json')
    if script and script.string:
        data = json.loads(script.string)
        for k, v in data.get('state', {}).items():
            if v.get('model_name') == 'NGLModel':
                st = v.get('state', {})
                msgs = st.get('_ngl_msg_archive', [])
                st['_ngl_repr_dict'] = get_repr_dict_from_msgs(msgs)
                for msg in msgs:
                    msg['fire_embed'] = True
                    if msg.get('methodName') == 'loadFile' and msg.get('args') and isinstance(msg['args'][0], dict):
                        if not msg['args'][0].get('ext'):
                            msg['args'][0]['ext'] = msg.get('kwargs', {}).get('ext', 'pdb')
        script.string = json.dumps(data)
        content = str(soup)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)



# --- SHOWCASE & BASIC VIEWS ---

# 1-4. Barnase-Barstar
print("Generating barnase_barstar views...")
molsys_1brs = msm.convert(msm.systems['Barnase-Barstar']['1brs.h5msm'])
v = msm.view(molsys_1brs, viewer='nglview')
write_nglview_html(v, str(static_ngl / "barnase_barstar_1.html"))

molsys_b = msm.extract(molsys_1brs, selection="chain_name=='B'")
molsys_f = msm.extract(molsys_1brs, selection="chain_name=='F'")
v = msm.view([molsys_b, molsys_f], viewer='nglview')
write_nglview_html(v, str(static_ngl / "barnase_barstar_2.html"))

molsys_e = msm.extract(molsys_1brs, selection="chain_name=='E'")
barstar_f_over_e = msm.structure.least_rmsd_align(
    molsys_f,
    selection='atom_name=="CA"',
    reference_molecular_system=molsys_e,
    reference_selection='atom_name=="CA"'
)
v = msm.view([molsys_b, barstar_f_over_e], viewer='nglview')
write_nglview_html(v, str(static_ngl / "barnase_barstar_3.html"))

barnase_barstar = msm.merge([molsys_b, barstar_f_over_e])
v = msm.view(barnase_barstar, viewer='nglview')
write_nglview_html(v, str(static_ngl / "barnase_barstar_4.html"))
print(" -> Saved barnase_barstar_1..4.html")

# 5. Dialanine Monte Carlo
print("Generating dialanine_monte_carlo_1.html...")
molsys_dia = msm.build.build_peptide('AceAlaNme')
v = msm.view(molsys_dia, viewer='nglview')
write_nglview_html(v, str(static_ngl / "dialanine_monte_carlo_1.html"))
print(" -> Saved dialanine_monte_carlo_1.html")

# 6-9. NGLView Showcase
print("Generating nglview_showcase views...")
# View 1: nv.demo() structure (nv.datafiles.PDB)
v1 = msm.convert(nv.datafiles.PDB, to_form='nglview.NGLWidget')
write_nglview_html(v1, str(static_ngl / "nglview_showcase_1.html"))

# View 2: GRO + XTC trajectory
v2 = msm.convert([nv.datafiles.GRO, nv.datafiles.XTC], to_form='nglview.NGLWidget')
write_nglview_html(v2, str(static_ngl / "nglview_showcase_2.html"))

# View 3: Two AceAlaNme peptides merged and displayed as licorice
molsys_A = msm.build.build_peptide('AceAlaNme')
molsys_B = msm.build.build_peptide('AceAlaNme')
molsys_B = msm.structure.translate(molsys_B, translation='[0.5, 0.0, 0.0] nm')
v3_a = msm.convert(molsys_A, to_form='nglview.NGLWidget')
v3_b = msm.convert(molsys_B, to_form='nglview.NGLWidget')
v3 = msm.merge([v3_a, v3_b])
v3.clear()
v3.add_licorice()
write_nglview_html(v3, str(static_ngl / "nglview_showcase_3.html"))

# View 4: 181L colored by charge
molsys_181 = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], selection='molecule_type=="protein"')
charge_groups = msm.physchem.get_charge(molsys_181, element='group', selection='molecule_type=="protein"')
v4 = msm.view(molsys_181, viewer='nglview')
msm.third_party.nglview.set_color_by_value(v4, values=charge_groups, selection='molecule_type=="protein"', cmap='bwr')
write_nglview_html(v4, str(static_ngl / "nglview_showcase_4.html"))

# Also generate Plotly animated contact map HTML
print("Generating nglview_contact_map.html...")
try:
    import plotly.express as px
    traj_molsys = msm.convert([nv.datafiles.GRO, nv.datafiles.XTC], to_form='molsysmt.MolSys')
    contact_map = msm.structure.get_contacts(traj_molsys, selection='molecule_type=="protein" and atom_name=="CA"', threshold='12 angstroms')
    ca_labels = msm.get_label(traj_molsys, selection='molecule_type=="protein" and atom_name=="CA"', string='{group_name}-{group_id}')
    fig_plotly = px.imshow(contact_map, x=ca_labels, y=ca_labels, animation_frame=0,
                           labels={'x': 'Residue', 'y': 'Residue', 'animation_frame': 'Frame'},
                           color_continuous_scale='Blues')
    fig_plotly.write_html(str(static_ngl / "nglview_contact_map.html"), include_plotlyjs='cdn')
    print(" -> Saved nglview_contact_map.html")
except Exception as e:
    print(f"Warning generating plotly contact map: {e}")

print(" -> Saved nglview_showcase_1..4.html")

# 9-11. Quickstart & View 181
print("Generating quickstart & view_181 views...")
molsys_181 = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'])
vq1 = msm.view(molsys_181, viewer='nglview')
write_nglview_html(vq1, str(static_ngl / "quickstart_1.html"))
write_nglview_html(vq1, str(static_ngl / "view_181.html"))

vq2 = msm.view(molsys_181, selection="molecule_name=='BENZENE'", viewer='nglview')
write_nglview_html(vq2, str(static_ngl / "quickstart_2.html"))

vq3 = msm.view(molsys_181, selection="all within 0.7 nm of molecule_name=='BENZENE'", viewer='nglview')
write_nglview_html(vq3, str(static_ngl / "quickstart_3.html"))
print(" -> Saved quickstart_1..3.html and view_181.html")

# --- THIRD PARTY NGLVIEW TOOLS ---
print("Generating third_party/nglview tool views...")

# 12. add_arrows.html
molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
view = msm.convert(molsys, to_form='nglview.NGLWidget')
msm.third_party.nglview.add_arrows(view, origin='atom_index==0', end='atom_index==10', color='#E74C3C', radius='0.5 angstroms')
write_nglview_html(view, str(third_party_ngl / "add_arrows.html"))

# 13. add_contacts.html
molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
view = msm.convert(molsys, to_form='nglview.NGLWidget')
msm.third_party.nglview.add_contacts(view, atom_pairs=[[10, 50], [20, 80], [30, 100]], color='#3498DB', radius='0.3 angstroms')
write_nglview_html(view, str(third_party_ngl / "add_contacts.html"))

# 14. add_cylinders.html
molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
view = msm.convert(molsys, to_form='nglview.NGLWidget')
msm.third_party.nglview.add_cylinders(view, bottom='atom_index==0', top='atom_index==10', color='#2ECC71', radius='0.4 angstroms')
write_nglview_html(view, str(third_party_ngl / "add_cylinders.html"))

# 15. add_hbonds.html
molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
view = msm.convert(molsys, to_form='nglview.NGLWidget')
hbonds = np.array([[0, 10, 20], [1, 15, 25]])
msm.third_party.nglview.add_hbonds(view, hbonds=hbonds, color='#F39C12')
write_nglview_html(view, str(third_party_ngl / "add_hbonds.html"))

# 16. clear.html
molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
view = msm.convert(molsys, to_form='nglview.NGLWidget')
msm.third_party.nglview.clear(view)
write_nglview_html(view, str(third_party_ngl / "clear.html"))

# 17. set_color.html
molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
view = msm.convert(molsys, to_form='nglview.NGLWidget')
msm.third_party.nglview.set_color(view, color='#E67E22', selection='molecule_type=="protein"')
write_nglview_html(view, str(third_party_ngl / "set_color.html"))

# 18. set_color_by_value.html
molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
view = msm.convert(molsys, to_form='nglview.NGLWidget')
n_groups = msm.get(molsys, n_groups=True)
values = np.linspace(0.0, 1.0, n_groups)
msm.third_party.nglview.set_color_by_value(view, values=values, selection='molecule_type=="protein"', cmap='bwr_r')
write_nglview_html(view, str(third_party_ngl / "set_color_by_value.html"))

# 19. show_as_balls_and_sticks.html
molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
view = msm.convert(molsys, to_form='nglview.NGLWidget')
msm.third_party.nglview.show_as_balls_and_sticks(view, selection='group_name=="HOH"')
write_nglview_html(view, str(third_party_ngl / "show_as_balls_and_sticks.html"))

# 20. show_as_cartoon.html
molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
view = msm.convert(molsys, to_form='nglview.NGLWidget')
msm.third_party.nglview.show_as_cartoon(view, selection='molecule_type=="protein"')
write_nglview_html(view, str(third_party_ngl / "show_as_cartoon.html"))

# 21. show_as_licorice.html
molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
view = msm.convert(molsys, to_form='nglview.NGLWidget')
msm.third_party.nglview.show_as_licorice(view, selection='group_index==[10, 11, 12]')
write_nglview_html(view, str(third_party_ngl / "show_as_licorice.html"))

# 22. show_as_surface.html
molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
view = msm.convert(molsys, to_form='nglview.NGLWidget')
msm.third_party.nglview.show_as_surface(view, selection='molecule_type=="protein"', opacity=0.7)
write_nglview_html(view, str(third_party_ngl / "show_as_surface.html"))

# 23. show_gui.html
molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
view = msm.convert(molsys, to_form='nglview.NGLWidget')
msm.third_party.nglview.show_gui(view)
write_nglview_html(view, str(third_party_ngl / "show_gui.html"))

# 24. standardize_view.html
molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
view = msm.convert(molsys, to_form='nglview.NGLWidget')
msm.third_party.nglview.standardize_view(view)
write_nglview_html(view, str(third_party_ngl / "standardize_view.html"))

print("=== NGLView Views Generated Successfully! ===")
