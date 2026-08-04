from pathlib import Path
import molsysmt as msm

docs_dir = Path(__file__).resolve().parent.parent
static_dir = docs_dir / "_static"
views_dir = static_dir / "views"
views_dir.mkdir(parents=True, exist_ok=True)

molsys = msm.convert(msm.systems['Barnase-Barstar']['1brs.bcif.gz'],
                     selection='molecule_type=="protein"',
                     to_form='molsysmt.MolSys')
view = msm.view(molsys, selection='molecule_index==0')
view.export.html(str(views_dir / "1BRS_molecule_index_zero.html"), shared_runtime=str(static_dir))
