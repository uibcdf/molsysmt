"""Small explicit native systems and mechanical references for live receiving."""


def notebook_cells(prefix, output):
    initial = (
        prefix
        + f"""import json
import numpy as np
from tests.molsysviewer_molsysmt.test_interaction_analysis_panel import source
from tests.molsysviewer_molsysmt.test_build_assignment_tools import same
from molsysviewer_molsysmt._analysis_interactions import INTERACTION_METHODS
_out=Path({str(output)!r})
def expected(task):
    family,name=INTERACTION_METHODS[task]
    args=dict(structure_indices='all',pbc=False,output_type='molsysmt.Interactions')
    if family=='ionic': args['distance_threshold']='0.4 nm'
    if family=='pi_pi': args.update(distance_threshold='.6 nm',angle_threshold='30 degrees',offset_threshold='.2 nm',planarity_threshold='.02 nm')
    raw=getattr(getattr(msm.interactions,family),name)(view.molsys,**args)
    page=raw.to_page(limit=50)
    _out.joinpath('interaction-expected.json').write_text(json.dumps(dict(task=task,rows=raw.n_interactions,frames=page['structure_indices'].tolist(),occurrences=page['occurrence_indices'].tolist(),units=raw.measure_units)))
view=msv.new_view(source('hbonds'))
expected('interaction_hbonds')
view
"""
    )
    tasks = list(
        __import__(
            "molsysviewer_molsysmt._analysis_interactions",
            fromlist=["INTERACTION_METHODS"],
        ).INTERACTION_METHODS
    )
    cells = [initial]
    for index, task in enumerate(tasks[1:], 1):
        family = task.removeprefix("interaction_")
        family = {
            "halogen": "halogen_bonds",
            "metal": "metal_coordination",
            "water": "water_bridges",
        }.get(family, family)
        cells.append(
            f"view.load(source({family!r}),mode='replace')\nexpected({task!r})\nprint('FAMILY_READY_{index}')\n"
        )
    cells.append("""seed=msv.demo['pentalanine']
view.load(msm.extract(seed.molsys,structure_indices=[0,8,3]),mode='replace');seed.close()
_mechanical_before=msm.copy(view.molsys)
_projected=msm.extract(view.molsys,structure_indices=[0])
_energy=float(msm.pyunitwizard.get_value(msm.molecular_mechanics.get_potential_energy(_projected,platform='Reference'),to_unit='kJ/mol'))
_forces=msm.pyunitwizard.get_value(msm.molecular_mechanics.get_forces(view.molsys,selection=[0],structure_indices=[2,0,2],platform='Reference'),to_unit='kJ/(mol*nm)')
_out.joinpath('mechanical-expected.json').write_text(json.dumps(dict(energy=_energy,forces=_forces.tolist())))
print('MECHANICS_READY')
""")
    cells.append(
        "same(view.molsys,_mechanical_before)\nassert view.addons.molsysmt.get_sync_status()['state']=='synchronized'\nprint('INTERACTION_MECHANICS_SOURCE_OK')\n"
    )
    return cells
