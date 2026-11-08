"""Construct the real-notebook sequence-fit oracle without invoking a fit."""

from pathlib import Path


def _notebook_cells(prefix, output, length_standard):
    initial = (
        prefix
        + f"""
import hashlib
import json
import numpy as np
from importlib.util import module_from_spec, spec_from_file_location
_fixture_spec = spec_from_file_location('_sequence_fixture', {str(Path(__file__).resolve())!r})
_fixture = module_from_spec(_fixture_spec)
_fixture_spec.loader.exec_module(_fixture)
_sequence_systems = _fixture._sequence_systems
_source, _reference, _aligned, _moving = _sequence_systems()
view = msv.new_view(_source)
source_coordinates = msm.pyunitwizard.get_value(view.molsys.structures.coordinates, to_unit='nm').copy()
_boxes = msm.pyunitwizard.get_value(view.molsys.structures.box, to_unit='nm').copy()
_source_revision = view.addons.molsysmt.get_sync_status()['target_revision']
_atom_count = view.molsys.get_n_atoms()
view.molsys.interactions = {{'coverage': msm.Interactions.from_records([], n_atoms=_atom_count, n_structures=3, method='existing-coverage', evaluated_structure_indices=[0,1,2])}}
_original_coverage = view.molsys.interactions['coverage']
_reference_path = Path({str(output / "sequence-reference.h5msm")!r})
msm.h5msm.write(_reference, _reference_path)
_reference_digest = hashlib.sha256(_reference_path.read_bytes()).hexdigest()
_sequence_source_expected = source_coordinates.copy()
_sequence_source_expected[np.ix_([2,0], range(_moving))] = _aligned
_sequence_result_expected = _sequence_source_expected.copy()
_sequence_result_expected[0,:_moving] = _aligned - [.4,0,0]
_query_atoms = msm.select(view.molsys, selection='atom_name=="CA"')
_reference_atoms = msm.select(_reference, selection='atom_name=="CA"')
_left = source_coordinates[0,_query_atoms[:3]]
_right = msm.pyunitwizard.get_value(msm.get(_reference,coordinates=True),to_unit='nm')[4,_reference_atoms]
_lc, _rc = _left.mean(axis=0), _right.mean(axis=0)
_u, _s, _vh = np.linalg.svd((_left-_lc).T@(_right-_rc))
_wrong = (source_coordinates[0,:_moving]-_lc)@(_u@np.diag([1,1,np.linalg.det(_u@_vh)])@_vh)+_rc
_counterfactual = float(np.max(np.abs(_wrong-_aligned)))
assert len(_query_atoms)==4 and len(_reference_atoms)==3 and _counterfactual>.01
Path({str(output / "sequence-expected.json")!r}).write_text(json.dumps({{'n_atoms':_atom_count,'n_moving':_moving,'query_atoms':_query_atoms,'reference_atoms':_reference_atoms,'reference_filename':str(_reference_path),'source_angstrom':(_sequence_source_expected*10).tolist(),'result_angstrom':(_sequence_result_expected*10).tolist(),'positional_counterfactual_nm':_counterfactual}}))
_unit_policy = msm.pyunitwizard.context(standard_units=[{length_standard!r}, 'ps', 'radians'])
_unit_policy.__enter__()
view
"""
    )
    final = """
np.testing.assert_allclose(msm.pyunitwizard.get_value(view.molsys.structures.coordinates,to_unit='nm'),_sequence_source_expected,rtol=0,atol=1e-10)
assert view.addons.molsysmt.get_sync_status()['target_revision']==_source_revision+1
records=view.addons.manager.presentations.records()
assert len(records)==1
result=view.addons.manager.presentations.get(records[0]['id'])
np.testing.assert_allclose(msm.pyunitwizard.get_value(result.molsys.structures.coordinates,to_unit='nm'),_sequence_result_expected,rtol=0,atol=1e-10)
np.testing.assert_array_equal(msm.pyunitwizard.get_value(view.molsys.structures.box,to_unit='nm'),_boxes)
np.testing.assert_array_equal(msm.pyunitwizard.get_value(result.molsys.structures.box,to_unit='nm'),_boxes)
assert result.molsys is not view.molsys and result.player.n_structures==3
np.testing.assert_array_equal(view.molsys.interactions['coverage'].evaluated_structure_indices,[1])
np.testing.assert_array_equal(result.molsys.interactions['coverage'].evaluated_structure_indices,[1])
np.testing.assert_array_equal(_original_coverage.evaluated_structure_indices,[0,1,2])
assert hashlib.sha256(_reference_path.read_bytes()).hexdigest()==_reference_digest
_unit_policy.__exit__(None,None,None)
print('JUPYTER_SEQUENCE_ALIGN_NATIVE_OK',len(records))
"""
    return initial, final


def _sequence_systems(reference_count=5):
    """Use distinct amino-acid labels and an explicit rigid-pose oracle."""
    import numpy as np
    import molsysmt as msm
    from molsysmt import pyunitwizard as puw
    from molsysmt.native import MolecularMechanics

    peptide = msm.build.build_peptide("ACEALAGLYSERTHRNME")
    reference = msm.build.build_peptide("ACEALASERTHRNME")
    # This geometry fixture deliberately excludes the experimental mechanics
    # domain, which H5MSM 0.5 does not encode; chemical assignments remain.
    peptide.molecular_mechanics = MolecularMechanics()
    reference.molecular_mechanics = MolecularMechanics()
    data = msm.get(
        peptide,
        element="atom",
        group_name=True,
        atom_name=True,
        output_type="dictionary",
    )
    ref_data = msm.get(
        reference,
        element="atom",
        group_name=True,
        atom_name=True,
        output_type="dictionary",
    )
    n = msm.get(peptide, n_atoms=True)
    i = np.arange(n, dtype=float)
    base = np.column_stack([i * 0.04, (i % 5) * 0.1, (i % 9) * 0.07])
    lookup = {
        (group, atom): point
        for group, atom, point in zip(
            data["group_name"], data["atom_name"], base, strict=True
        )
    }
    ref_base = np.array(
        [
            lookup[group, atom]
            for group, atom in zip(
                ref_data["group_name"], ref_data["atom_name"], strict=True
            )
        ]
    )
    turn = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)
    query = np.stack(
        [
            base @ matrix.T + shift
            for matrix, shift in [
                (turn, [1.2, -0.3, 0.6]),
                (np.eye(3), [-0.5, 0.4, 0.2]),
                (turn.T, [0.3, 1.4, -0.8]),
            ]
        ]
    )
    msm.set(peptide, coordinates=puw.quantity(query, "nm"))
    builder = msm.MolSysBuilder()
    for name, kind in [("O", "O"), ("H1", "H"), ("H2", "H")]:
        builder.add_atom(atom_name=name, atom_type=kind)
    builder.add_group([0, 1, 2], group_name="HOH", group_type="water")
    builder.add_bond(0, 1)
    builder.add_bond(0, 2)
    water = np.array([[10.0, 2.0, 1.0], [10.1, 2.0, 1.0], [10.0, 2.1, 1.0]])
    builder.set_coordinates(puw.quantity(np.tile(water[None], (3, 1, 1)), "nm"))
    query = msm.merge([peptide, builder.build()])
    msm.set(query, box=puw.quantity(np.tile(np.eye(3) * 4, (3, 1, 1)), "nm"))
    ref_turn = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]], dtype=float)
    ref_points = np.stack(
        [
            ref_base @ ref_turn.T + [3.1 + j * 0.1, -2.2, 0.7]
            for j in range(reference_count)
        ]
    )
    msm.set(reference, coordinates=puw.quantity(ref_points * 10, "angstrom"))
    reference = msm.permute_atoms(
        reference, atom_indices=list(range(len(ref_base) - 1, -1, -1))
    )
    expected = base @ ref_turn.T + [3.1 + (reference_count - 1) * 0.1, -2.2, 0.7]
    return query, reference, expected, n
