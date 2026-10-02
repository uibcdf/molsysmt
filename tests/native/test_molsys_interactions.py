"""Lifecycle contracts for named sparse analyses attached to MolSys."""

import pickle

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import MolSys


def _system(n_atoms=3, n_structures=3):
    molsys = MolSys(n_atoms=n_atoms)
    molsys.structures.append(
        coordinates=np.zeros((n_structures, n_atoms, 3)), skip_digestion=True
    )
    return molsys


def _analysis(n_atoms=3, n_structures=3):
    return msm.Interactions.from_records(
        [
            {
                "structure_index": 2,
                "interaction_type": "pair",
                "participants": [
                    {"role": "first", "atom_indices": [0]},
                    {"role": "second", "atom_indices": [1]},
                ],
            }
        ],
        n_atoms=n_atoms,
        n_structures=n_structures,
        evaluated_structure_indices=[0, 1, 2],
        method="example",
        source_id="original",
    )


def test_attachment_validates_names_full_results_and_both_index_axes():
    molsys = _system()
    result = _analysis()
    molsys.interactions = {"pairs": result, "other": result.remap()}

    assert tuple(molsys.interactions) == ("pairs", "other")
    with pytest.raises(TypeError):
        molsys.interactions["new"] = result
    with pytest.raises(ValueError, match="nonempty"):
        molsys.interactions = {"": result}
    with pytest.raises(ValueError, match="full"):
        molsys.interactions = {"view": result.query(structure_indices=[2])}
    with pytest.raises(ValueError, match="atom/structure domains"):
        molsys.interactions = {"wrong": result.remap(atom_indices=[0, 1])}
    assert tuple(molsys.interactions) == ("pairs", "other")


def test_copy_extract_and_remove_preserve_coverage_and_remap_indices():
    molsys = _system()
    empty_analysis = msm.Interactions.from_records(
        [],
        n_atoms=3,
        n_structures=3,
        evaluated_structure_indices=[0],
        method="empty",
    )
    molsys.interactions = {"pairs": _analysis(), "empty": empty_analysis}

    copied = molsys.copy()
    assert copied.interactions["pairs"] is not molsys.interactions["pairs"]
    with pytest.raises(ValueError, match="read-only"):
        copied.interactions["pairs"].occurrence_structures[0] = 1
    copied.interactions = {
        **copied.interactions,
        "pairs": copied.interactions["pairs"].invalidate_structures([2]),
    }
    assert copied.interactions["pairs"].n_interactions == 0
    np.testing.assert_array_equal(
        molsys.interactions["pairs"].occurrence_structures, [2]
    )

    subset = molsys.extract(
        atom_indices=[0, 1], structure_indices=[2, 0], skip_digestion=True
    )
    result = subset.interactions["pairs"]
    assert (result.n_atoms, result.n_structures) == (2, 2)
    np.testing.assert_array_equal(result.evaluated_structure_indices, [0, 1])
    np.testing.assert_array_equal(result.occurrence_structures, [0])
    assert result.source_id == "original"
    np.testing.assert_array_equal(result.atom_source_indices, [0, 1])
    np.testing.assert_array_equal(result.structure_source_indices, [2, 0])
    np.testing.assert_array_equal(
        subset.interactions["empty"].evaluated_structure_indices, [1]
    )

    restored = pickle.loads(pickle.dumps(molsys))
    assert set(restored.interactions) == {"pairs", "empty"}
    assert restored.interactions["pairs"].n_interactions == 1

    removed = molsys.remove(atom_indices=[1], skip_digestion=True)
    assert removed.interactions["pairs"].n_interactions == 0
    np.testing.assert_array_equal(
        removed.interactions["pairs"].evaluated_structure_indices, [0, 1, 2]
    )


def test_atom_add_preserves_bounded_coverage_and_structure_append_keeps_old_observations():
    molsys = _system()
    molsys.interactions = {"pairs": _analysis()}
    extra_atom = _system(n_atoms=1)

    molsys.add(extra_atom, skip_digestion=True)
    assert molsys.topology.n_atoms == 4
    assert molsys.interactions["pairs"].source_id == "original"
    after_add = molsys.interactions["pairs"]
    np.testing.assert_array_equal(
        after_add.evaluation_scope["universe_indices"], [0, 1, 2]
    )
    np.testing.assert_array_equal(after_add.atom_source_indices, [0, 1, 2, -1])
    assert after_add.query(atom_indices=[3]).n_interactions == 0

    extra_frame = _system(n_atoms=4, n_structures=1)
    molsys.append_structures(extra_frame, skip_digestion=True)
    after_append = molsys.interactions["pairs"]
    assert after_append.n_structures == 4
    assert after_append.source_id == "original"
    np.testing.assert_array_equal(after_append.structure_source_indices, [0, 1, 2, -1])
    np.testing.assert_array_equal(after_append.evaluated_structure_indices, [0, 1, 2])
    assert after_append.query(structure_indices=[3]).n_interactions == 0
    assert (
        after_append.query(structure_indices=[3])
        .to_dict()["evaluated_structure_indices"]
        .size
        == 0
    )


def test_merging_a_source_with_analyses_requires_an_explicit_policy():
    target = _system()
    source = _system()
    source.interactions = {"pairs": _analysis()}

    with pytest.raises(ValueError, match="analysis-merge policy"):
        target.add(source, skip_digestion=True)
    with pytest.raises(ValueError, match="explicit analysis merge"):
        target.append_structures(source, skip_digestion=True)
    assert target.structures.n_structures == 3
    assert not target.interactions


def test_legacy_exports_reject_attached_analyses_before_writing(tmp_path):
    from molsysmt.form.molsysmt_MolSys.to_file_h5msm import to_file_h5msm

    molsys = _system()
    molsys.interactions = {"pairs": _analysis()}
    path = tmp_path / "unsupported.h5msm"

    with pytest.raises(ValueError, match="H5MSM 0.4 cannot store"):
        to_file_h5msm(molsys, output_filename=path, skip_digestion=True)
    assert not path.exists()
    with pytest.raises(ValueError, match="MolSysDict 0.1 cannot store"):
        msm.convert(molsys, to_form="molsysmt.MolSysDict")
