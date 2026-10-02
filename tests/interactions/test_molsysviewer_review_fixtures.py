"""Verify synthetic consumer fixtures against explicit lifecycle expectations."""

import importlib.util
from pathlib import Path

import h5py
import numpy as np
import pytest

import molsysmt as msm


def _generator():
    path = Path(__file__).resolve().parents[2] / "devtools/scripts/create_molsysviewer_interactions_fixture.py"
    spec = importlib.util.spec_from_file_location("viewer_review_fixture", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_review_files_include_explicit_run_membership_and_lifecycle(tmp_path):
    full, detached = _generator().create_files(tmp_path)
    for path in (full, detached):
        with h5py.File(path, "r") as file:
            assert file.attrs["version"] == "0.5"
            assert all(child.attrs["schema_version"] == 2 for child in file["interactions"].values())
        molsys = msm.convert(path, to_form="molsysmt.MolSys")
        assert set(molsys.interactions) == {"review", "invalidated", "recalculated", "compacted", "empty"}
        review = molsys.interactions["review"]
        assert [(r["structure_indices"].tolist(), r["details"]["execution_chunks"])
                for r in review.execution_records] == [([0, 1, 2], 2), ([4], 1)]
        assert review.parameters == {}
        assert review.software == {"molsysmt": msm.__version__}
        pending = molsys.interactions["invalidated"]
        assert pending.query(structure_indices=[4]).to_dict()["evaluated_structure_indices"].size == 0
        for name in ("recalculated", "compacted"):
            result = molsys.interactions[name]
            assert [(r["structure_indices"].tolist(), r["details"]["execution_chunks"])
                    for r in result.execution_records] == [([0, 2], 2), ([1, 4], 3)]
            data = result.query(structure_indices=[4, 1, 0, 4, 3]).to_dict()
            np.testing.assert_array_equal(data["occurrence_indices"], [3, 4, 0, 1])
            np.testing.assert_allclose(data["measurements"]["distance"], [.24, .23, .2, .36])
            assert result.query(structure_indices=[1]).n_interactions == 0
            assert result.query(structure_indices=[1]).execution_records[0]["details"]["execution_chunks"] == 3
        empty = molsys.interactions["empty"]
        assert empty.n_interactions == 0
        np.testing.assert_array_equal(empty.evaluated_structure_indices, [1, 5])
        if path == full:
            assert molsys.structures.n_structures == 6
            np.testing.assert_array_equal(
                msm.pyunitwizard.get_value(molsys.structures.box, to_unit="nm"),
                np.repeat(np.eye(3)[None], 6, axis=0))
            ring_index = review.relation_types.index("pi_pi")
            assert [p["role"] for p in review.relation(ring_index)["participants"]] == ["ring_a", "ring_b"]
        else:
            assert molsys.structures is None
    with pytest.raises(FileExistsError):
        _generator().create_files(tmp_path)
