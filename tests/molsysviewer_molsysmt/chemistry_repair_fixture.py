"""Actual chemistry repair fixture; native scientific results stay independent."""


def notebook_cells(prefix):
    initial = (
        prefix
        + """import json
import numpy as np
from tests.molsysviewer_molsysmt.test_chemistry_repair_panel import source, arguments
from tests.molsysviewer_molsysmt.test_build_assignment_tools import same
_peptide=source('terminal_cappings')
_peptide_before=msm.copy(_peptide)
view=msv.new_view(_peptide)
view.regions.add(selection=[0],tag='source-region')
_checked=[]

def verify_repair(task):
    records=[r for r in view.addons.manager.presentations.records() if r['title']=='repair-'+task]
    assert len(records)==1
    child=view.addons.manager.presentations.get(records[0]['id'])
    name,kwargs=arguments(task)
    if task in {'terminal_cappings','remove_hydrogens'}:kwargs['pH']=7.4
    if task=='partial_charges':kwargs['expected_total_charge']=0
    expected=getattr(msm.build,name)(view.molsys,**kwargs)
    same(child.molsys,expected['molecular_system'] if kwargs.get('return_report') else expected)
    assert child.molsys is not view.molsys
    if task in {'autodock_types','partial_charges'}:
        same(view.molsys,_methanol_before)
    else:
        same(view.molsys,_peptide_before)
    _checked.append(task)
    print('NATIVE_REPAIR_OK',task)
view
"""
    )
    tasks = ["infer_bonds", "add_bonds", "terminal_cappings", "remove_hydrogens"]
    cells = [initial] + [f"verify_repair({task!r})\n" for task in tasks]
    cells += [
        """_methanol=source('partial_charges')
view.load(_methanol,mode='replace')
_methanol_before=msm.copy(view.molsys)
view.regions.add(selection=[0],tag='methanol-source')
print('METHANOL_REPLACEMENT_READY',view.molsys.get_n_atoms())
""",
        "verify_repair('autodock_types')\n",
        "verify_repair('partial_charges')\n",
        """assert _checked==['infer_bonds','add_bonds','terminal_cappings','remove_hydrogens','autodock_types','partial_charges']
same(_peptide,_peptide_before)
same(view.molsys,_methanol_before)
assert 'methanol-source' in view.regions
assert view.addons.molsysmt.get_sync_status()['state']=='synchronized'
assert len([r for r in view.addons.manager.presentations.records() if r['title']=='repair-terminal_cappings'])==1
print('JUPYTER_REPAIR_NATIVE_OK',len(_checked))
""",
    ]
    return cells
