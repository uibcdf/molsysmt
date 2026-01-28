from pathlib import Path

import molsysmt as msm
import molsysviewer as viewer

molsys = msm.convert(msm.systems['Barnase-Barstar']['1brs.bcif.gz'],
                     selection='molecule_type=="protein"',
                     to_form='molsysmt.MolSys')

view = viewer.make_viewer(molsys, selection='molecule_index==0')
view.show()
view.write_html("../_static/views/1BRS_molecule_index_zero.html", title="1BRS Molecule Index 0", mode="lite")
