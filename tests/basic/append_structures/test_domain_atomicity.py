"""Preserving aligned structures, chemical-state links and named analyses (#520)."""

from importlib import import_module

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native import MolSys, Structures


def _target(mode, populated=True):
    system = MolSys(n_atoms=3)
    system.topology.atoms["atom_id"] = ["a", "b", "c"]
    system.structures = Structures(
        coordinates=puw.quantity(np.arange(27).reshape(3, 3, 3) / 10, "nm"),
        time=puw.quantity([0, 1, 2], "ps"),
        box=puw.quantity(np.repeat(np.eye(3)[None], 3, axis=0), "nm"),
    )
    if mode.startswith("multi"):
        system.chemical_states.append_state()
    if mode != "implicit":
        links = {
            "explicit": [0, 0, 0],
            "multi-known": [0, 1, 1],
            "multi-unknown": [0, pd.NA, 1],
        }[mode]
        msm.set(system, structure_chemical_state_index=links)
    records = (
        [
            {
                "structure_index": 2,
                "interaction_type": "pair",
                "participants": [
                    {"role": "first", "atom_indices": [0]},
                    {"role": "second", "atom_indices": [1]},
                ],
            }
        ]
        if populated
        else []
    )
    system.interactions = {
        "observed": msm.Interactions.from_records(
            records,
            n_atoms=3,
            n_structures=3,
            evaluated_structure_indices=[0, 2],
            method="append-regression",
            source_id="declared-original",
        ),
        "empty": msm.Interactions.from_records(
            [],
            n_atoms=3,
            n_structures=3,
            evaluated_structure_indices=[1],
            method="empty",
        ),
    }
    return system


def _incoming(target, native):
    structures = Structures(
        coordinates=puw.quantity((np.arange(27).reshape(3, 3, 3) + 100), "angstrom"),
        time=puw.quantity([10000, 11000, 12000], "fs"),
        box=puw.quantity(np.repeat((np.eye(3) * 10)[None], 3, axis=0), "angstrom"),
    )
    if not native:
        return structures
    source = target.copy()
    source.interactions = {}
    source.structures = structures
    return source


def _snapshot(system):
    return {
        "structures": system.structures,
        "coordinates": puw.get_value(
            system.structures.coordinates, to_unit="nm"
        ).copy(),
        "time": puw.get_value(system.structures.time, to_unit="ps").copy(),
        "box": puw.get_value(system.structures.box, to_unit="nm").copy(),
        "velocities": None
        if system.structures.velocities is None
        else puw.get_value(system.structures.velocities, to_unit="nm/ps").copy(),
        "links": pd.array(
            msm.get(system, structure_chemical_state_index=True), dtype="Int64"
        ),
        "implicit": system._structure_chemical_state_indices is None,
        "topology": system.topology.atoms.copy(),
        "chemistry": [
            state.atom_attributes.copy() for state in system.chemical_states._states
        ],
        "analyses": {
            name: result.to_dict() for name, result in system.interactions.items()
        },
        "handles": dict(system.interactions),
    }


def _assert_unchanged(system, before):
    assert system.structures is before["structures"]
    assert system.structures._molsys_owner_ref() is system
    for field, unit in (
        ("coordinates", "nm"),
        ("time", "ps"),
        ("box", "nm"),
        ("velocities", "nm/ps"),
    ):
        value = getattr(system.structures, field)
        if before[field] is None:
            assert value is None
        else:
            np.testing.assert_array_equal(
                puw.get_value(value, to_unit=unit), before[field]
            )
    pd.testing.assert_extension_array_equal(
        pd.array(msm.get(system, structure_chemical_state_index=True), dtype="Int64"),
        before["links"],
    )
    assert (system._structure_chemical_state_indices is None) == before["implicit"]
    pd.testing.assert_frame_equal(system.topology.atoms, before["topology"])
    for state, table in zip(
        system.chemical_states._states, before["chemistry"], strict=True
    ):
        pd.testing.assert_frame_equal(state.atom_attributes, table)
    assert set(system.interactions) == set(before["analyses"])
    for name, payload in before["analyses"].items():
        assert system.interactions[name] is before["handles"][name]
        np.testing.assert_equal(system.interactions[name].to_dict(), payload)


@pytest.mark.parametrize(
    "mode", ["implicit", "explicit", "multi-known", "multi-unknown"]
)
@pytest.mark.parametrize("native", [False, True])
@pytest.mark.parametrize("populated", [False, True])
@pytest.mark.parametrize("in_place", [False, True])
def test_public_append_keeps_state_links_observations_and_coverage_aligned(
    mode, native, populated, in_place
):
    target = _target(mode, populated)
    source = _incoming(target, native)
    before = _snapshot(target)
    incoming = puw.get_value(
        source.structures.coordinates if native else source.coordinates, to_unit="nm"
    ).copy()
    source_before = _snapshot(source) if native else None
    result = msm.append_structures(target, source, in_place=in_place)
    output = target if in_place else result
    assert (result is None) == in_place
    assert msm.get(output, n_atoms=True, n_structures=True) == [3, 6]
    np.testing.assert_allclose(
        puw.get_value(output.structures.coordinates, to_unit="nm"),
        np.concatenate((before["coordinates"], incoming)),
        rtol=0,
        atol=1e-12,
    )
    np.testing.assert_allclose(
        puw.get_value(output.structures.time, to_unit="ps"),
        [0, 1, 2, 10, 11, 12],
        rtol=0,
        atol=1e-12,
    )
    appended = (
        list(before["links"])
        if native
        else [pd.NA if mode.startswith("multi") else 0] * 3
    )
    pd.testing.assert_extension_array_equal(
        pd.array(msm.get(output, structure_chemical_state_index=True), dtype="Int64"),
        pd.array(list(before["links"]) + appended, dtype="Int64"),
    )
    pd.testing.assert_frame_equal(output.topology.atoms, before["topology"])
    for name, previous in before["analyses"].items():
        analysis = output.interactions[name]
        assert analysis.n_structures == 6 and analysis.n_atoms == 3
        assert analysis.n_interactions == (int(populated) if name == "observed" else 0)
        np.testing.assert_array_equal(
            analysis.structure_source_indices, [0, 1, 2, -1, -1, -1]
        )
        np.testing.assert_equal(
            analysis.query(structure_indices=[0, 1, 2]).to_dict(),
            {**previous, "n_structures": 6},
        )
        new = analysis.query(structure_indices=[5, 3]).to_dict()
        assert new["evaluated_structure_indices"].size == 0
        assert new["occurrence_indices"].size == 0
        assert before["handles"][name].n_structures == 3
        np.testing.assert_equal(before["handles"][name].to_dict(), previous)
    if not in_place:
        _assert_unchanged(target, before)
    if native:
        _assert_unchanged(source, source_before)
    else:
        np.testing.assert_allclose(
            puw.get_value(source.coordinates, to_unit="nm"), incoming, rtol=0, atol=0
        )


@pytest.mark.parametrize("native", [False, True])
def test_nonconsecutive_source_selection_keeps_append_index_spaces(native):
    target = _target("multi-known")
    source = _incoming(target, native)
    output = msm.append_structures(
        target, source, structure_indices=[2, 0], in_place=False
    )
    assert output.get(n_structures=True) == 5
    expected = [0, 1, 1, 1, 0] if native else [0, 1, 1, pd.NA, pd.NA]
    pd.testing.assert_extension_array_equal(
        pd.array(output.get(structure_chemical_state_index=True), dtype="Int64"),
        pd.array(expected, dtype="Int64"),
    )
    np.testing.assert_allclose(
        puw.get_value(output.structures.coordinates, to_unit="nm")[3:],
        ((np.arange(27).reshape(3, 3, 3) + 100) * 0.1)[[2, 0]],
        rtol=0,
        atol=1e-12,
    )
    np.testing.assert_array_equal(
        output.interactions["observed"].structure_source_indices, [0, 1, 2, -1, -1]
    )


@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize(
    "fault", ["chemistry", "atom_axis", "strict", "incoming_analysis"]
)
def test_public_append_rejections_preserve_all_target_domains(fault, in_place):
    target = _target("multi-known")
    source = _incoming(target, True)
    options = {}
    error = StructuralInconsistencyError
    if fault == "chemistry":
        msm.set(
            source, element="atom", selection=[0], formal_charge=9, chemical_state=0
        )
    elif fault == "atom_axis":
        source = msm.extract(source, selection=[0, 1])
    elif fault == "strict":
        target.structures.velocities = puw.quantity(np.ones((3, 3, 3)), "nm/ps")
        options["attribute_policy"] = "strict"
    else:
        source.interactions = target.interactions
        error = ValueError
    before = _snapshot(target)
    source_before = _snapshot(source)
    with pytest.raises(error):
        msm.append_structures(target, source, in_place=in_place, **options)
    _assert_unchanged(target, before)
    _assert_unchanged(source, source_before)


def test_appended_multistate_analysis_survives_public_h5msm_roundtrip(tmp_path):
    target = _target("multi-unknown")
    source = _incoming(target, False)
    appended = msm.append_structures(target, source, in_place=False)
    path = str(tmp_path / "appended.h5msm")
    msm.convert(appended, to_form=path)
    restored = msm.convert(path)
    assert restored.get(n_atoms=True, n_structures=True) == [3, 6]
    assert restored.chemical_states.n_chemical_states == 2
    pd.testing.assert_extension_array_equal(
        pd.array(restored.get(structure_chemical_state_index=True), dtype="Int64"),
        pd.array([0, pd.NA, 1, pd.NA, pd.NA, pd.NA], dtype="Int64"),
    )
    np.testing.assert_allclose(
        puw.get_value(restored.structures.coordinates, to_unit="nm"),
        puw.get_value(appended.structures.coordinates, to_unit="nm"),
        rtol=0,
        atol=1e-12,
    )
    for name, analysis in appended.interactions.items():
        np.testing.assert_equal(
            restored.interactions[name].to_dict(), analysis.to_dict()
        )
        np.testing.assert_array_equal(
            restored.interactions[name].structure_source_indices, [0, 1, 2, -1, -1, -1]
        )


@pytest.mark.parametrize("in_place", [False, True])
def test_late_analysis_extension_failure_does_not_publish_a_partial_append(
    monkeypatch, in_place
):
    target = _target("explicit")
    source = _incoming(target, True)
    before, source_before = _snapshot(target), _snapshot(source)
    module = import_module("molsysmt.native.molsys")
    extend = module._extend_interaction_structures
    calls = []

    def fail_second_analysis(analysis, n_structures):
        calls.append(n_structures)
        if len(calls) == 2:
            raise MemoryError("synthetic analysis extension failure")
        return extend(analysis, n_structures)

    monkeypatch.setattr(module, "_extend_interaction_structures", fail_second_analysis)
    with pytest.raises(MemoryError, match="synthetic analysis extension"):
        msm.append_structures(target, source, in_place=in_place)
    assert calls == [6, 6]
    _assert_unchanged(target, before)
    _assert_unchanged(source, source_before)
