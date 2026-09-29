"""Keep calculation-time software versions across views, edits, and files."""

import json

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt.interactions._hdf5_query import query_named_interactions_file


def _system():
    builder = msm.MolSysBuilder()
    atoms = [builder.add_atom(atom_name=name, atom_type=kind)
             for name, kind in (("N", "N"), ("H", "H"), ("O", "O"),
                                ("SG", "S"), ("SG", "S"))]
    builder.add_group(atoms[:3], group_name="ALA")
    builder.add_group([atoms[3]], group_name="CYS")
    builder.add_group([atoms[4]], group_name="CYS")
    builder.add_bond(atoms[0], atoms[1])
    builder.set_coordinates(msm.pyunitwizard.quantity([
        [[0, 0, 0], [0.1, 0, 0], [0.3, 0, 0], [1, 0, 0], [1.2, 0, 0]],
        [[0, 0, 0], [0.1, 0, 0], [0.8, 0, 0], [1, 0, 0], [1.8, 0, 0]],
    ], "nm"))
    return builder.build()


def test_detector_producer_versions_survive_a_different_writer_and_reader(tmp_path, monkeypatch):
    molsys = _system()
    producer_version = "0.7.1+producer"
    monkeypatch.setattr(msm, "__version__", producer_version)
    molsys.interactions = {
        "buch": msm.interactions.hbonds.get_buch_hbonds(
            molsys, pbc=False, output_type="molsysmt.Interactions"),
        "disulfides": msm.interactions.disulfides.get_disulfide_candidates(
            molsys, pbc=False, output_type="molsysmt.Interactions"),
    }
    expected = {"molsysmt": producer_version}
    monkeypatch.setattr(msm, "__version__", "1.0.0+reader")
    filename = tmp_path / "historical_producer.h5msm"
    msm.convert(molsys, to_form="file:h5msm", output_filename=filename)
    restored = msm.convert(filename, to_form="molsysmt.MolSys")
    assert set(restored.interactions) == {"buch", "disulfides"}

    for name, original in molsys.interactions.items():
        result = restored.interactions[name]
        assert original.software == result.software == expected
        assert result.query(structure_indices=[1, 0]).to_dict()["software"] == expected
        assert result.remap(structure_indices=[1, 0]).software == expected
        assert result.invalidate_structures([0]).software == expected
        assert restored.copy().interactions[name].software == expected
        assert query_named_interactions_file(filename, name, [1, 0])["software"] == expected
        np.testing.assert_array_equal(result.evaluated_structure_indices, [0, 1])
        assert result.query(structure_indices=[1]).n_interactions == 0
        payload = msm.convert(result, to_form="molsysmt.InteractionsDict")
        assert payload.data["software"] == expected
        assert msm.convert(payload, to_form="molsysmt.Interactions").software == expected
        standalone = tmp_path / f"{name}.h5i"
        result.save(standalone)
        assert msm.Interactions.load(standalone).software == expected


def test_legacy_payloads_keep_unknown_producer_versions(tmp_path, monkeypatch):
    result = msm.Interactions.from_records(
        [], n_atoms=2, n_structures=1, evaluated_structure_indices=[0], method="legacy")
    assert result.software == {}
    payload = msm.convert(result, to_form="molsysmt.InteractionsDict")
    payload.data.pop("software")
    monkeypatch.setattr(msm, "__version__", "1.0.0+reader")
    assert msm.convert(payload, to_form="molsysmt.Interactions").software == {}

    standalone = tmp_path / "legacy.h5i"
    result.save(standalone)
    with h5py.File(standalone, "r+") as file:
        metadata = json.loads(file.attrs["metadata"])
        metadata.pop("software")
        file.attrs["metadata"] = json.dumps(metadata)
    assert msm.Interactions.load(standalone).software == {}

    filename = tmp_path / "legacy_analysis.h5msm"
    msm.h5msm.write_layers(str(filename), interactions={"legacy": result})
    with h5py.File(filename, "r+") as file:
        group = next(iter(file["interactions"].values()))
        metadata = json.loads(group.attrs["metadata"])
        metadata.pop("software")
        group.attrs["metadata"] = json.dumps(metadata)
    assert msm.convert(filename).interactions["legacy"].software == {}
    assert query_named_interactions_file(filename, "legacy", [0])["software"] == {}


@pytest.mark.parametrize("software", [
    [], "molsysmt", {"molsysmt": 1}, {"": "1.0"}, {"molsysmt": " "},
])
def test_invalid_producer_metadata_is_rejected(software):
    with pytest.raises(ValueError, match="software"):
        msm.Interactions.from_records(
            [], n_atoms=2, n_structures=1, evaluated_structure_indices=[0],
            method="manual", software=software)


def test_producer_metadata_copies_caller_and_projection_dictionaries():
    versions = {"external_detector": "2.3"}
    result = msm.Interactions.from_records(
        [], n_atoms=2, n_structures=1, evaluated_structure_indices=[0],
        method="manual", software=versions)
    versions["external_detector"] = "changed"
    projected = result.to_dict()
    projected["software"]["external_detector"] = "changed"
    assert result.software == {"external_detector": "2.3"}
