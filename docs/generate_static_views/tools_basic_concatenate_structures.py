from pathlib import Path
import molsysmt as msm

# Build molecular system D by concatenating structures of alanine dipeptide (A, B, C)
molsys_A = msm.build.build_peptide('AceAlaNme')
molsys_B = msm.structure.translate(molsys_A, translation='[0.1, 0.1, 0.1] nanometers')
molsys_C = msm.structure.translate(molsys_A, translation='[0.2, 0.2, 0.2] nanometers')
molsys_D = msm.concatenate_structures([molsys_A, molsys_B, molsys_C])

view = msm.view(molsys_D, standard=True)
output_path = Path(__file__).resolve().parent.parent / "_static" / "views" / "tools_basic_concatenate_structures.html"
view.export.html(str(output_path), background="transparent")
print(f"Generated MolSysViewer static view at: {output_path}")
