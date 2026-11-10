"""Real ensemble property/report receiving data; no constructed panel replies."""


def notebook_cells(prefix, output):
    initial = (
        prefix
        + f"""import json
import numpy as np
from tests.molsysviewer_molsysmt.test_build_assignment_tools import same
from tests.molsysviewer_molsysmt.test_aromatic_tools import caffeine_system
seed=msv.demo['pentalanine']
view=msv.new_view(seed.molsys,structure_indices=[0,8,3]);seed.close()
_before=msm.copy(view.molsys)
_atoms=[20,10,6,20]
_groups=list(dict.fromkeys(map(int,msm.get(view.molsys,element='atom',selection=_atoms,group_index=True))))
_expected={{'atoms':_atoms,'groups':_groups,'mass':msm.pyunitwizard.get_value(msm.physchem.get_mass(view.molsys,element='atom',selection=_atoms),to_unit='dalton').tolist(),'sasa':msm.pyunitwizard.get_value(msm.physchem.get_sasa(view.molsys,selection=_atoms,structure_indices=[2,0,2],pbc=False,use_gpu=False,parallel=False,num_threads=1),to_unit='nm**2').tolist(),'group_members':list(map(int,msm.get(view.molsys,element='group',selection=[_groups[0]],atom_index=True)[0]))}}
Path({str(output / "property-expected.json")!r}).write_text(json.dumps(_expected))
view
"""
    )
    middle = """same(view.molsys,_before)
view.load(caffeine_system(),mode='replace')
_caffeine_before=msm.copy(view.molsys)
print('PROPERTY_CAFFEINE_READY',view.molsys.get_n_atoms())
"""
    final = """same(view.molsys,_caffeine_before)
assert view.addons.molsysmt.get_sync_status()['state']=='synchronized'
assert not view.addons.manager.presentations.records()
assert not view.measurements.info()
print('JUPYTER_PROPERTIES_NATIVE_OK')
"""
    return [initial, middle, final]
