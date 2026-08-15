from pathlib import Path
import molsysmt as msm

# Build system from pentalanine traj and convert to Topology and Structures items
molsys = msm.systems['pentalanine']['traj_pentalanine.h5']
topology, structures = msm.convert(molsys, to_form=['molsysmt.Topology', 'molsysmt.Structures'])

view = msm.view([topology, structures], structure_indices=3500)
output_path = Path(__file__).resolve().parent.parent / "_static" / "views" / "tools_basic_convert.html"
view.export.html(str(output_path), background="transparent")
print(f"Generated MolSysViewer static view at: {output_path}")
