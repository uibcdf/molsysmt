from pathlib import Path
import molsysmt as msm

views_dir = Path("docs/_static/views")
views_dir.mkdir(parents=True, exist_ok=True)

print("=== Generating Topology Static HTML Views ===")

# 1. tools_topology_get_dihedral_quartets_1.html
print("1/1: Generating tools_topology_get_dihedral_quartets_1.html...")
molsys = msm.convert(msm.systems['Met-enkephalin']['met_enkephalin.h5msm'], to_form='molsysmt.MolSys')
view = msm.view(molsys)
view.export.html(str(views_dir / "tools_topology_get_dihedral_quartets_1.html"), background="transparent")
print(" -> Saved tools_topology_get_dihedral_quartets_1.html")

print("=== Topology Views Generated Successfully! ===")
