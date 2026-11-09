"""Receive explicit experimental mechanics through supported public boundaries."""

from pathlib import Path

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentChoiceError,
    FormatError,
    StructuralInconsistencyError,
)
from molsysmt.native import (
    ChemicalStates,
    MolecularMechanics,
    MolSys,
    Structures,
    Topology,
)
from tests.form.file_h5msm.test_mechanics_presence import _system


def _mechanical(domain="complete"):
    source = _system(domain)
    source.molecular_mechanics.forcefield = "unresolved_model_request"
    source.molecular_mechanics.partial_charge = [0.25, -0.25]
    source.molecular_mechanics.atom_ff_type = ["C", "OA"]
    source.molecular_mechanics.cutoff_distance = msm.pyunitwizard.quantity(
        12.0, "angstrom"
    )
    source.molecular_mechanics.partial_charge_assignment = {
        "status": "stale",
        "software": {"original": "1"},
    }
    return source


@pytest.mark.parametrize(
    "domain",
    ["complete", "topology_free", "no_chemistry", "no_structures", "interactions"],
)
@pytest.mark.parametrize("route", ["write", "convert"])
def test_explicit_native_public_roundtrip_preserves_domains_and_original_reports(
    tmp_path, domain, route
):
    source = _mechanical(domain)
    path = tmp_path / "mechanics.h5msm"
    if route == "write":
        msm.h5msm.write(source, path, format_version="0.6")
    else:
        msm.convert(
            source, to_form="file:h5msm", output_filename=path, format_version="0.6"
        )
    with h5py.File(path, "r") as file:
        assert file.attrs["version"] == "0.6"
    restored = msm.h5msm.read(path)
    assert (restored.topology is None) == (source.topology is None)
    assert (restored.chemical_states is None) == (source.chemical_states is None)
    assert (restored.structures is None) == (source.structures is None)
    assert (
        restored.molecular_mechanics.partial_charge_assignment
        == source.molecular_mechanics.partial_charge_assignment
    )
    np.testing.assert_array_equal(
        restored.molecular_mechanics.partial_charge, [0.25, -0.25]
    )
    assert (
        str(msm.pyunitwizard.get_unit(restored.molecular_mechanics.cutoff_distance))
        == "angstrom"
    )
    converted = msm.convert(path)
    assert converted.molecular_mechanics.forcefield == "unresolved_model_request"


def test_05_default_refuses_mechanics_and_preserves_default_layer_keys(tmp_path):
    source = _system("complete")
    path = tmp_path / "default.h5msm"
    msm.h5msm.write(source, path)
    with h5py.File(path, "r") as file:
        assert file.attrs["version"] == "0.5"
    assert set(msm.h5msm.read_layers(path)) == {
        "topology",
        "chemical_states",
        "structures",
        "interactions",
        "associations",
    }
    assert msm.h5msm.read_layers(path, layers="molecular_mechanics") == {
        "molecular_mechanics": None
    }
    with pytest.raises(ValueError, match="molecular mechanics"):
        msm.h5msm.write(_mechanical(), tmp_path / "refused.h5msm")
    assert not (tmp_path / "refused.h5msm").exists()


@pytest.mark.parametrize("version", ["1.0", "0.4", 0.6, True, ["0.6"]])
def test_unknown_write_versions_are_rejected_by_public_digestion(tmp_path, version):
    path = tmp_path / "refused.h5msm"
    with pytest.raises(ArgumentChoiceError):
        msm.h5msm.write(_system("complete"), path, format_version=version)
    assert not path.exists()


def test_independent_mechanics_only_public_layer_and_queries(tmp_path):
    path = tmp_path / "independent.h5msm"
    msm.h5msm.write_layers(
        path,
        molecular_mechanics=MolecularMechanics(forcefield="request"),
        mechanics_n_atoms=7,
        format_version="0.6",
    )
    mechanics = msm.h5msm.read_layers(path, layers="molecular_mechanics")[
        "molecular_mechanics"
    ]
    assert mechanics.forcefield == "request"
    assert msm.h5msm.read_axis_sizes(path) == {("molecular_mechanics", None, "atom"): 7}
    assert msm.get(path, n_atoms=True) == 7
    assert msm.get(path, forcefield=True) == "request"
    assert (
        msm.convert(path, to_form="molsysmt.MolecularMechanics").forcefield == "request"
    )
    with pytest.raises(ValueError, match="mechanics-only"):
        msm.h5msm.read(path)


def test_queries_keep_chemical_formal_charge_separate_from_legacy_mechanics(tmp_path):
    source = _mechanical()
    source.molecular_mechanics.formal_charge = [7, 8]
    msm.set(source, element="atom", formal_charge=[1, -1])
    path = tmp_path / "charges.h5msm"
    msm.h5msm.write(source, path, format_version="0.6")
    np.testing.assert_array_equal(
        msm.get(path, element="atom", formal_charge=True), [1, -1]
    )
    np.testing.assert_array_equal(
        msm.get(path, element="atom", selection=[1, 0, 1], partial_charge=True),
        [-0.25, 0.25, -0.25],
    )
    assert msm.get(path, forcefield=True) == "unresolved_model_request"
    assert msm.has_attribute(path, "forcefield")
    assert not msm.has_attribute(path, "implicit_solvent")
    assert msm.has_attribute(path, "implicit_solvent", include_none=True)


def test_structure_queries_and_iterator_never_decode_unrequested_mechanics(
    tmp_path, monkeypatch
):
    source = _mechanical()
    source.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(
            np.arange(36).reshape(3, 4, 3)[:, :2], "nm"
        )
    )
    path = tmp_path / "geometry.h5msm"
    msm.h5msm.write(source, path, format_version="0.6")
    import molsysmt._private.h5msm_storage.mechanics as codec

    def forbidden(*args, **kwargs):
        raise AssertionError("Unrequested mechanical payload must remain unread.")

    monkeypatch.setattr(codec, "read_mechanics", forbidden)
    expected = msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm")
    values = msm.get(
        path,
        element="atom",
        selection=[1, 0, 1],
        structure_indices=[2, 0],
        coordinates=True,
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(values, to_unit="nm"), expected[[2, 0]][:, [1, 0, 1]]
    )
    iterator = msm.Iterator(path, structure_indices=[2, 0], chunk=1, coordinates=True)
    chunks = list(iterator)
    assert len(chunks) == 2
    assert msm.convert(path, to_form="molsysmt.Topology").n_atoms == 2


def test_mechanical_queries_do_not_materialize_coordinates_or_other_domains(
    tmp_path, monkeypatch
):
    path = tmp_path / "mechanics.h5msm"
    msm.h5msm.write(_mechanical(), path, format_version="0.6")
    import molsysmt.form._h5msm05_structures as structural
    import molsysmt.form._h5msm05_topology as topology
    import molsysmt.form._h5msm_chemical_states as chemical

    def forbidden(*args, **kwargs):
        raise AssertionError("Unrequested native payload must remain unread.")

    monkeypatch.setattr(structural, "read_independent_structures", forbidden)
    monkeypatch.setattr(topology, "read_independent_topology", forbidden)
    monkeypatch.setattr(chemical, "read_independent_chemical_states", forbidden)
    assert msm.get(path, forcefield=True) == "unresolved_model_request"
    np.testing.assert_array_equal(
        msm.get(path, element="atom", partial_charge=True), [0.25, -0.25]
    )


def test_copy_and_selected_file_extraction_retain_root_version_and_mechanics(tmp_path):
    from tests.native.test_prepared_system_checkpoint import _prepared

    source = _prepared("complete")
    expected_charge = source.molecular_mechanics.partial_charge[1]
    original_report = source.molecular_mechanics.partial_charge_assignment
    path = tmp_path / "source.h5msm"
    msm.h5msm.write(source, path, format_version="0.6")
    original = path.read_bytes()
    copied = msm.copy(path, output_filename=tmp_path / "copied.h5msm")
    assert Path(copied).read_bytes() == original
    subset = msm.extract(
        path,
        selection=[1],
        structure_indices=[2, 0],
        output_filename=tmp_path / "subset.h5msm",
    )
    with h5py.File(subset, "r") as file:
        assert file.attrs["version"] == "0.6"
    restored = msm.h5msm.read(subset)
    assert restored.get(n_atoms=True, n_structures=True) == [1, 2]
    np.testing.assert_array_equal(
        restored.molecular_mechanics.partial_charge, [expected_charge]
    )
    assert (
        restored.molecular_mechanics.partial_charge_assignment["software"]
        == original_report["software"]
    )
    assert path.read_bytes() == original


def test_public_append_preserves_mechanics_and_extends_state_assignments(tmp_path):
    structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm")
    )
    states = ChemicalStates(n_atoms=2)
    states.append_state()
    path = tmp_path / "append.h5msm"
    links = [
        dict(
            axis="atom",
            source="structures",
            target="chemical_states",
            source_name=None,
            target_name=None,
            indices="identity",
        ),
        dict(
            axis="atom",
            source="molecular_mechanics",
            target="chemical_states",
            source_name=None,
            target_name=None,
            indices="identity",
        ),
        dict(
            axis="structure_state",
            source="structures",
            target="chemical_states",
            source_name=None,
            target_name=None,
            indices=[0],
        ),
    ]
    msm.h5msm.write_layers(
        path,
        structures=structures,
        chemical_states=states,
        molecular_mechanics=MolecularMechanics(forcefield="request"),
        mechanics_n_atoms=2,
        associations=links,
        format_version="0.6",
    )
    msm.h5msm.append_structures(path, structures, structure_state_indices=[0])
    restored = msm.h5msm.read(path)
    assert restored.molecular_mechanics.forcefield == "request"
    assert restored.get(n_structures=True) == 2
    assert restored.get(structure_chemical_state_index=True) == [0, 0]


def test_legacy_handler_refuses_new_modular_root_without_loading_it(tmp_path):
    from molsysmt.native import H5MSMFileHandler

    path = tmp_path / "mechanics.h5msm"
    msm.h5msm.write(_mechanical(), path, format_version="0.6")
    with pytest.raises(FormatError, match="0.6"):
        H5MSMFileHandler(path)
    with pytest.raises(FormatError, match="0.6"):
        msm.convert(path, to_form="molsysmt.H5MSMFileHandler")


@pytest.mark.parametrize("field", ["partial_charge_assignment", "atom_type_assignment"])
def test_complementary_public_sources_keep_report_only_mechanics(tmp_path, field):
    molsys_A = MolSys._from_partial_domains(topology=Topology(n_atoms=2))
    setattr(
        molsys_A.molecular_mechanics, field, {"status": "original_detached_evidence"}
    )
    molsys_B = MolSys._from_partial_domains(
        structures=Structures(
            coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm")
        )
    )
    source = tmp_path / "inventory.h5msm"
    msm.h5msm.write(molsys_A, source, format_version="0.6")
    restored = msm.convert([source, molsys_B])
    assert getattr(restored.molecular_mechanics, field) == {
        "status": "original_detached_evidence"
    }
    assert getattr(molsys_A.molecular_mechanics, field) == {
        "status": "original_detached_evidence"
    }
    assert restored.topology is not molsys_A.topology
    setattr(molsys_B.molecular_mechanics, field, {})
    with pytest.raises(
        StructuralInconsistencyError, match="repeat the molecular_mechanics"
    ):
        msm.convert([source, molsys_B])


@pytest.mark.parametrize("source_version", ["0.3", "0.4", "0.5"])
def test_explicit_upgrade_keeps_source_file_unchanged(tmp_path, source_version):
    if source_version == "0.3":
        source = Path(__file__).parent / "data/alanine_dipeptide_v03.h5msm"
        n_atoms = 22
    else:
        source = tmp_path / "source.h5msm"
        molsys = _system("complete")
        if source_version == "0.4":
            from molsysmt.form.molsysmt_MolSys.to_file_h5msm import to_file_h5msm

            to_file_h5msm(molsys, output_filename=source)
        else:
            msm.h5msm.write(molsys, source)
        n_atoms = 2
    original = source.read_bytes()
    target = tmp_path / "development.h5msm"
    msm.convert(
        source, to_form="file:h5msm", output_filename=target, format_version="0.6"
    )
    assert source.read_bytes() == original
    with h5py.File(target, "r") as file:
        assert file.attrs["version"] == "0.6"
        assert "molecular_mechanics" not in file
    assert msm.h5msm.read(target).get_n_atoms() == n_atoms


def test_chemical_calculation_uses_versioned_projection_and_preserves_stored_requests(
    tmp_path,
):
    from tests.native.test_prepared_system_checkpoint import _prepared

    source = _prepared("complete")
    path = tmp_path / "calculation.h5msm"
    msm.h5msm.write(source, path, format_version="0.6")
    expected = msm.physchem.get_partial_charges(source, method="gasteiger_marsili")
    observed = msm.physchem.get_partial_charges(path, method="gasteiger_marsili")
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(observed, to_unit="elementary_charge"),
        msm.pyunitwizard.get_value(expected, to_unit="elementary_charge"),
    )
    from molsysmt.form._h5msm05_modular import _read_calculation_chemistry

    model, _ = _read_calculation_chemistry(
        path, chemical_state="structure", structure_indices=[0], include_mechanics=True
    )
    assert model.molecular_mechanics.forcefield == source.molecular_mechanics.forcefield
    assert (
        model.molecular_mechanics.partial_charge_assignment["software"]
        == source.molecular_mechanics.partial_charge_assignment["software"]
    )


def test_complementary_files_preserve_actual_prepared_reports_and_state_bindings(
    tmp_path,
):
    from copy import deepcopy

    from tests.form.file_h5msm.test_modular_mechanics import _hdf_snapshot
    from tests.native.test_prepared_system_checkpoint import _pdbqt_texts, _prepared

    source = _prepared("complete")
    inventory = MolSys._from_partial_domains(topology=source.topology.copy())
    context = MolSys._from_partial_domains(
        chemical_states=source.chemical_states.copy(),
        structures=source.structures.copy(),
    )
    context._set_structure_chemical_state_indices(
        source.get(structure_chemical_state_index=True)
    )
    context.interactions = dict(source.interactions)
    context.molecular_mechanics = deepcopy(source.molecular_mechanics)
    topology_path, context_path = (
        tmp_path / "inventory05.h5msm",
        tmp_path / "context06.h5msm",
    )
    msm.h5msm.write(inventory, topology_path)
    msm.h5msm.write(context, context_path, format_version="0.6")
    restored = msm.convert([topology_path, context_path])
    assert _hdf_snapshot(restored) == _hdf_snapshot(source)
    assert _pdbqt_texts(restored) == _pdbqt_texts(source)


def test_reordered_prepared_system_retains_correspondence_in_public_roundtrip(tmp_path):
    from tests.form.file_h5msm.test_modular_mechanics import _hdf_snapshot
    from tests.native.test_prepared_system_checkpoint import _prepared

    source = _prepared("complete")
    order = list(reversed(range(source.get_n_atoms())))
    reordered = msm.permute_atoms(source, atom_indices=order)
    path = tmp_path / "permuted.h5msm"
    msm.convert(
        reordered, to_form="file:h5msm", output_filename=path, format_version="0.6"
    )
    restored = msm.convert(path)
    assert _hdf_snapshot(restored) == _hdf_snapshot(reordered)
    np.testing.assert_array_equal(
        restored.molecular_mechanics.partial_charge,
        source.molecular_mechanics.partial_charge[order],
    )
