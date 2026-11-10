"""Small deposited-hydrogen control for actual assessed-reconciliation panels."""


def source_system():
    import numpy as np

    import molsysmt as msm
    from molsysmt.native import Structures

    source = msm.convert(
        msm.systems["chicken villin HP35"]["1vii.pdb"], to_form="molsysmt.MolSys"
    )
    puw = msm.pyunitwizard
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm")
    source.structures = Structures(
        coordinates=puw.quantity(
            np.repeat(xyz, 3, axis=0) + np.arange(3)[:, None, None], "nm"
        ),
        box=puw.quantity(np.repeat((np.eye(3) * 6)[None], 3, axis=0), "nm"),
        time=puw.quantity([2, 5, 11], "ps"),
        structure_id=["C", "A", "C"],
    )
    labels = list(
        zip(source.topology.atoms.atom_name, source.topology.atoms.group_index)
    )
    removed_labels = {("H3", 0)} | {("HZ3", i) for i in (7, 24, 29, 30, 32)}
    assert set(labels) & removed_labels == removed_labels
    keep = [i for i, label in enumerate(labels) if label not in removed_labels]
    removed = next(i for i in range(596) if i not in keep)
    source.interactions = {
        "source-observations": msm.Interactions.from_records(
            [
                {
                    "structure_index": f,
                    "interaction_type": "contact",
                    "participants": [
                        {"role": "first", "atom_indices": [atom]},
                        {"role": "second", "atom_indices": [keep[-1]]},
                    ],
                }
                for f in range(3)
                for atom in (keep[0], removed)
            ],
            n_atoms=596,
            n_structures=3,
            evaluated_structure_indices=[0, 1, 2],
            method="synthetic.assessed-reconciliation-control",
        )
    }
    return source, keep


def notebook_cells(prefix, output):
    initial = (
        prefix
        + """from tests.molsysviewer_molsysmt.protonation_panel_fixture import source_system
from tests.molsysviewer_molsysmt.test_build_assignment_tools import same
import numpy as np
_unit_context=msm.pyunitwizard.context(standard_units=['pm','ps','radians'])
_unit_context.__enter__()
_policy=dict(msm.pyunitwizard.configure.get_standard_units())
_source,_keep=source_system()
view=msv.new_view(_source)
view.regions.add(selection=[0,2],tag='keep')
view.shapes.add_sphere(atom_indices=[1],tag='anchor')
_before=msm.copy(view.molsys)
_scene=view.export_state()
_expected=msm.extract(_before,selection=_keep)
view
"""
    )
    independent = """same(view.molsys,_before)
assert view.export_state()==_scene
assert view.addons.molsysmt.get_sync_status()['target_revision']==0
_records=view.addons.manager.presentations.records();assert len(_records)==1
_child=view.addons.manager.presentations.get(_records[0]['id'])
same(_child.molsys,_expected)
assert _child.molsys is not view.molsys and _child.molsys.structures.n_structures==3
assert len(_child.molsys.interactions['source-observations'].occurrence_structures)==3
print('ASSESSED_INDEPENDENT_OK',_child.molsys.get_n_atoms())
"""
    managed = """same(view.molsys,_expected)
assert view.addons.molsysmt.get_sync_status()['target_revision']==1
assert view.addons.molsysmt.get_sync_status()['state']=='synchronized'
assert view.whole.get(n_atoms=True)==590 and view.player.n_structures==3
assert view.molsys.structures.structure_id.tolist()==['C','A','C']
assert len(view.molsys.interactions['source-observations'].occurrence_structures)==3
print('ASSESSED_MANAGED_OK',view.molsys.get_n_atoms())
"""
    final = """same(view.molsys,_expected)
same(_child.molsys,_expected)
assert view.addons.molsysmt.get_sync_status()['target_revision']==1
assert len(view.addons.manager.presentations.records())==1
assert list(view.regions.keys())==['keep']
assert view.shapes.get('anchor') is not None
assert msm.pyunitwizard.get_unit(view.molsys.structures.coordinates)==msm.pyunitwizard.get_unit(_before.structures.coordinates)
assert dict(msm.pyunitwizard.configure.get_standard_units())==_policy
_unit_context.__exit__(None,None,None)
print('JUPYTER_ASSESSED_PROTONATION_OK',590)
"""
    return [initial, independent, managed, final]
