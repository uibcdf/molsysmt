"""Keep fresh file loads independent without copying their resident graph twice."""

import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import MolSys
from tests.native.test_molsys import build_minimal_molsys


@pytest.fixture
def source():
    system = build_minimal_molsys(n_structures=5)
    system.structures.box = puw.quantity(np.repeat(np.eye(3)[None], 5, axis=0), "nm")
    system.structures.time = puw.quantity(np.arange(5), "ps")
    system._set_structure_chemical_state_indices([0, None, 0, 0, 0])
    system.interactions = {
        "test": msm.Interactions.from_records(
            [
                {
                    "structure_index": structure,
                    "interaction_type": "pair",
                    "participants": [
                        {"role": "first", "atom_indices": [0]},
                        {"role": "second", "atom_indices": [3]},
                    ],
                    "measurements": {"distance": distance},
                }
                for structure, distance in [(0, 0.2), (3, 0.3), (3, 0.4)]
            ],
            n_atoms=4,
            n_structures=5,
            evaluated_structure_indices=[0, 1, 3],
            method="synthetic",
            measure_units={"distance": "nm"},
            software={"producer": "1"},
        )
    }
    return system


@pytest.mark.parametrize("path_type", [str, lambda path: path])
@pytest.mark.parametrize(
    "domains",
    [
        ("topology", "chemical_states", "structures", "interactions"),
        ("structures",),
        ("interactions",),
        ("chemical_states",),
        ("topology",),
        ("topology", "structures"),
    ],
)
def test_default_fresh_load_needs_no_second_native_graph_copy(
    source, tmp_path, monkeypatch, domains, path_type
):
    filename = tmp_path / "fresh.h5msm"
    topology = source.topology.copy() if "topology" in domains else None
    if topology is not None and "chemical_states" not in domains:
        topology._clear_chemical_states()
    states = (
        (
            topology._chemical_states_domain
            if topology is not None
            else source.chemical_states.copy()
        )
        if "chemical_states" in domains
        else None
    )
    partial = MolSys._from_partial_domains(
        topology=topology,
        chemical_states=states,
        structures=source.structures if "structures" in domains else None,
        interactions=source.interactions if "interactions" in domains else None,
    )
    msm.h5msm.write(partial, filename)

    def forbidden(*args, **kwargs):
        pytest.fail("A fresh file load copied its complete native graph again")

    monkeypatch.setattr(MolSys, "__deepcopy__", forbidden)
    restored = msm.convert(path_type(filename), to_form="molsysmt.MolSys")
    for name in ("topology", "chemical_states", "structures"):
        assert (getattr(restored, name) is not None) == (name in domains)
    if restored.topology is not None:
        assert restored.topology._molsys_owner_ref() is restored
        assert restored.topology.atoms.atom_id.tolist() == ["0", "1", "2", "3"]
        if restored.chemical_states is not None:
            assert restored.chemical_states is restored.topology._chemical_states_domain
    if restored.structures is not None:
        np.testing.assert_array_equal(
            puw.get_value(restored.structures.get_coordinates(), to_unit="nm"),
            np.arange(60.0).reshape(5, 4, 3),
        )
    if "interactions" in domains:
        record = restored.interactions["test"].to_dict()
        np.testing.assert_array_equal(record["occurrence_indices"], [0, 1, 2])
        np.testing.assert_array_equal(record["evaluated_structure_indices"], [0, 1, 3])
        assert restored.interactions["test"].software == {"producer": "1"}
    else:
        assert not restored.interactions


def test_explicit_copy_choice_and_existing_resident_copy_semantics(
    source, tmp_path, monkeypatch
):
    filename = tmp_path / "choices.h5msm"
    msm.h5msm.write(source, filename)
    original = MolSys.__deepcopy__
    copied = []

    def observe(item, memo):
        copied.append(item)
        return original(item, memo)

    monkeypatch.setattr(MolSys, "__deepcopy__", observe)
    for choice, expected in [(True, 1), (False, 0)]:
        copied.clear()
        loaded = msm.convert(filename, to_form="molsysmt.MolSys", copy_if_all=choice)
        assert len(copied) == expected
        assert loaded.topology._molsys_owner_ref() is loaded
    copied.clear()
    clone = msm.convert(source, to_form="molsysmt.MolSys")
    assert clone is not source
    assert copied == [source]
    assert msm.convert(source, to_form="molsysmt.MolSys", copy_if_all=False) is source
    assert source.topology._molsys_owner_ref() is source


def test_repeated_loads_are_independent_and_edit_invalidation_stays_local(
    source, tmp_path
):
    filename = tmp_path / "independent.h5msm"
    msm.h5msm.write(source, filename)
    with puw.context(standard_units=["angstrom", "ns", "kcal/mol", "K"]):
        first = msm.convert(filename, to_form="molsysmt.MolSys")
        second = msm.convert(filename, to_form="molsysmt.MolSys")
        assert puw.has_unit(first.structures.get(coordinates=True), "angstrom")
        msm.set(
            first,
            selection=[0],
            structure_indices=[3],
            coordinates=puw.quantity([[[10.0, 20.0, 30.0]]], "angstrom"),
        )
    np.testing.assert_array_equal(
        first.interactions["test"].evaluated_structure_indices, [0, 1]
    )
    np.testing.assert_array_equal(
        second.interactions["test"].evaluated_structure_indices, [0, 1, 3]
    )
    np.testing.assert_array_equal(
        puw.get_value(second.structures.get_coordinates(), to_unit="nm"),
        np.arange(60.0).reshape(5, 4, 3),
    )
    first.topology.atoms.at[0, "atom_name"] = "edited"
    assert second.topology.atoms.at[0, "atom_name"] == "N"
    assert source.topology.atoms.at[0, "atom_name"] == "N"
    assert second.topology._molsys_owner_ref() is second


def test_file_selection_remaps_analysis_and_keeps_reports_and_option_validation(
    source, tmp_path
):
    filename = tmp_path / "selection.h5msm"
    msm.h5msm.write(source, filename)
    selected, report = msm.convert(
        filename,
        to_form="molsysmt.MolSys",
        selection=[0, 3],
        structure_indices=[3, 1, 0],
        return_report=True,
    )
    assert report.to_form == "molsysmt.MolSys"
    np.testing.assert_array_equal(
        puw.get_value(selected.structures.get_coordinates(), to_unit="nm"),
        np.arange(60.0).reshape(5, 4, 3)[[3, 1, 0]][:, [0, 3]],
    )
    analysis = selected.interactions["test"]
    np.testing.assert_array_equal(analysis.atom_source_indices, [0, 3])
    np.testing.assert_array_equal(analysis.structure_source_indices, [3, 1, 0])
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0, 1, 2])
    assert len(analysis.to_dict()["occurrence_indices"]) == 3
    with pytest.raises(UnknownArgumentError, match="unexpected"):
        msm.convert(filename, to_form="molsysmt.MolSys", unexpected_option=True)


def test_multiple_outputs_keep_independent_native_objects(source, tmp_path):
    filename = tmp_path / "multiple.h5msm"
    msm.h5msm.write(source, filename)
    first, second = msm.convert(
        filename, to_form=["molsysmt.MolSys", "molsysmt.MolSys"]
    )
    assert first is not second
    assert first.topology is not second.topology
    assert first.topology._molsys_owner_ref() is first
    assert second.topology._molsys_owner_ref() is second
