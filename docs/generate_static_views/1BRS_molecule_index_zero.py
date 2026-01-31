import molsysmt as msm

molsys = msm.convert(msm.systems['Barnase-Barstar']['1brs.bcif.gz'],
                     selection='molecule_type=="protein"',
                     to_form='molsysmt.MolSys')
view = msm.view(molsys, selection='molecule_index==0')
view.write_html("../_static/views/1BRS_molecule_index_zero.html", title="1BRS Molecule Index 0", mode="lite")
