from pathlib import Path
import molsysmt as msm

docs_dir = Path(__file__).resolve().parent.parent
static_dir = docs_dir / "_static"
views_dir = static_dir / "views"
views_dir.mkdir(parents=True, exist_ok=True)

molsys_A = msm.build.build_peptide('AceAlaNme')
molsys_B = msm.structure.translate(molsys_A, translation='[0.1, 0.1, 0.1] nanometers')
molsys_C = msm.structure.translate(molsys_A, translation='[0.2, 0.2, 0.2] nanometers')

msm.append_structures(molsys_A, molsys_B)
msm.append_structures(molsys_A, molsys_C)

view = msm.view(molsys_A, standard=True)
view.export.html(str(views_dir / "tools_basic_append_structures.html"), shared_runtime=str(static_dir), background="transparent")
