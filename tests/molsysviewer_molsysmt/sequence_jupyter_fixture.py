"""Construct the real-notebook sequence-fit oracle without invoking a fit."""


def _notebook_cells(prefix, output, length_standard):
    initial = (
        prefix
        + f"""
import hashlib
import json
import numpy as np
from tests.molsysviewer_molsysmt.test_sequence_alignment_panel import _sequence_systems
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
