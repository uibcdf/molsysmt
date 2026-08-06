from pathlib import Path
import molsysmt as msm

docs_dir = Path(__file__).resolve().parent.parent
static_dir = docs_dir / "_static"
views_dir = static_dir / "views"
views_dir.mkdir(parents=True, exist_ok=True)

molsys_A = msm.build.build_peptide('AceProNme')
molsys_B = msm.build.build_peptide('AceValNme')
molsys_C = msm.build.build_peptide('AceLysNme')

molsys_B = msm.structure.translate(molsys_B, translation='[-1.0, 0.0, 0.0] nanometers')
molsys_C = msm.structure.translate(molsys_C, translation='[1.0, 0.0, 0.0] nanometers')

msm.add(molsys_A, molsys_B)
msm.add(molsys_A, molsys_C)

view = msm.view(molsys_A, standard=True)
view.export.html(str(views_dir / "tools_basic_add.html"), shared_runtime=str(static_dir), background="transparent")
