"""Native scalar color and series references for real host receiving."""


def notebook_cells(prefix, output):
    initial = (
        prefix
        + f"""import json
import numpy as np
from molsysviewer.colors import scalar_to_color_list
from tests.molsysviewer_molsysmt.test_build_assignment_tools import same
seed=msv.demo['pentalanine']
view=msv.new_view(seed.molsys,structure_indices=[0,8,3]);seed.close()
view.regions.add(selection=[6,10,20],tag='property',representation='ball-and-stick')
_before=msm.copy(view.molsys)
_mass=msm.physchem.get_mass(view.molsys,element='atom')
_xyz=msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm')
_rmsf=np.sqrt(np.mean(np.sum((_xyz-_xyz.mean(axis=0))**2,axis=-1),axis=0))
np.testing.assert_allclose(msm.pyunitwizard.get_value(msm.structure.get_rmsf(view.molsys,selection='all'),to_unit='nm'),_rmsf,atol=1e-12)
assert _rmsf.shape==(62,)
_expected={{'rmsf_colors':scalar_to_color_list(msm.pyunitwizard.quantity(_rmsf,'nm')),'whole_colors':scalar_to_color_list(_mass,palette=['#2166ac','#f7f7f7','#b2182b'],value_range=msm.pyunitwizard.quantity([0,20],'dalton')),'sasa':msm.pyunitwizard.get_value(msm.physchem.get_sasa(view.molsys,selection=[20,10,6,20],structure_indices='all',pbc=False,parallel=False,num_threads=1,use_gpu=False),to_unit='nm**2')[:,0].tolist()}}
Path({str(output / "visual-expected.json")!r}).write_text(json.dumps(_expected))
view
"""
    )
    final = """same(view.molsys,_before)
assert view.addons.molsysmt.get_sync_status()['state']=='synchronized'
assert len(view.trajectory_plot.records())>=2
assert set(view._atom_color_layers['whole'])==set(range(62))
assert not view.measurements.info()
print('JUPYTER_VISUAL_ADOPTION_NATIVE_OK')
"""
    return [initial, final]
