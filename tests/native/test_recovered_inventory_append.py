"""Continuing native work after canonical chemical-string persistence (#616)."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native._chemical_state import Components_DataFrame
from tests.native.test_molsys_chemical_state_association import _multistate_molsys


def _source():
    system = _multistate_molsys((0, 1, 1))
    for i, state in enumerate(system.chemical_states._states):
        state.components = Components_DataFrame(n_components=1)
        state.components["component_id"] = pd.array(["pair"], dtype="string")
        state.components["component_name"] = pd.Series([f"pair-{i}"], dtype=object)
        state.components["component_type"] = pd.Series([pd.NA], dtype=object)
        state.component_indices = pd.Series([0, 0], dtype="Int64")
        state.connectivity_completeness = "complete"
        state.component_completeness = "complete"
        state.component_evidence = "explicit"
        state.set_atom_attribute("is_aromatic", [False, pd.NA])
        state.set_atom_attribute("stereochemistry", ["unknown", pd.NA])
    system.structures.coordinates = puw.quantity(
        np.arange(18).reshape(3, 2, 3), "angstrom"
    )
    return system


def _recover(system, storage, tmp_path):
    if storage == "native":
        return system.copy()
    if storage == "dictionary":
        return msm.convert(
            msm.convert(system, to_form="molsysmt.MolSysDict"),
            to_form="molsysmt.MolSys",
        )
    path = tmp_path / "inventory.h5msm"
    msm.h5msm.write(system, path)
    return msm.h5msm.read(path)


@pytest.mark.parametrize("storage", ["native", "dictionary", "h5msm"])
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("string_dtype", [object, "string", "str"])
def test_recovered_append_accepts_equivalent_strings_and_preserves_domains(
    storage, in_place, string_dtype, tmp_path
):
    source = _source()
    for state in source.chemical_states._states:
        for column in ("component_name", "component_type"):
            state.components[column] = state.components[column].astype(string_dtype)
    original = source.copy()
    original._set_structure_chemical_state_indices([0, pd.NA, 1])
    original.interactions = {
        "observed": msm.Interactions.from_records(
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
            n_atoms=2,
            n_structures=3,
            evaluated_structure_indices=[0, 2],
            method="recovered-append-regression",
            source_id="declared-original",
        )
    }
    target = _recover(original, storage, tmp_path)
    before_coordinates = puw.get_value(
        target.structures.coordinates, to_unit="nm"
    ).copy()
    before_chemistry = [
        (state.atom_attributes.copy(), state.bonds.copy(), state.components.copy())
        for state in target.chemical_states._states
    ]
    source_before = source.copy()
    before_occurrences = (
        target.interactions["observed"].query().to_dict()["occurrence_indices"].copy()
    )

    result = msm.append_structures(
        target, source, structure_indices=[2, 0], in_place=in_place
    )
    output = target if in_place else result

    expected = np.concatenate(
        [
            before_coordinates,
            puw.get_value(source.structures.coordinates, to_unit="nm")[[2, 0]],
        ]
    )
    np.testing.assert_allclose(
        puw.get_value(output.structures.coordinates, to_unit="nm"), expected
    )
    pd.testing.assert_extension_array_equal(
        output._structure_chemical_state_indices,
        pd.array([0, pd.NA, 1, 1, 0], dtype="Int64"),
    )
    assert output.chemical_states.reference_chemical_state_index is None
    for state, tables in zip(
        output.chemical_states._states, before_chemistry, strict=True
    ):
        for field, expected_table in zip(
            ("atom_attributes", "bonds", "components"), tables, strict=True
        ):
            pd.testing.assert_frame_equal(getattr(state, field), expected_table)
    analysis = output.interactions["observed"]
    np.testing.assert_array_equal(
        analysis.query().to_dict()["occurrence_indices"], before_occurrences
    )
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0, 2])
    np.testing.assert_array_equal(analysis.structure_source_indices, [0, 1, 2, -1, -1])
    assert analysis.n_structures == 5 and analysis.n_interactions == 1
    assert analysis.query(structure_indices=[3, 4]).n_interactions == 0
    for actual, before in zip(
        source.chemical_states._states,
        source_before.chemical_states._states,
        strict=True,
    ):
        pd.testing.assert_frame_equal(actual.components, before.components)
    if not in_place:
        assert target.structures.n_structures == 3
        np.testing.assert_array_equal(
            puw.get_value(target.structures.coordinates, to_unit="nm"),
            before_coordinates,
        )


@pytest.mark.parametrize(
    "difference",
    [
        "bond",
        "assignment",
        "component_name",
        "component_membership",
        "optional_column",
        "connectivity_completeness",
        "component_completeness",
        "component_evidence",
        "state_order",
        "reference",
        "atom_correspondence",
        "unknown_vs_value",
        "label_vs_missing",
    ],
)
def test_recovered_append_rejects_real_inventory_changes_atomically(
    difference, tmp_path
):
    source = _source()
    target = _recover(source, "h5msm", tmp_path)
    before = puw.get_value(target.structures.coordinates, to_unit="nm").copy()
    state = source.chemical_states._states[0]
    if difference == "bond":
        state.bonds.at[0, "bond_order"] = 3
    elif difference == "assignment":
        state.atom_attributes.at[0, "formal_charge"] = 1
    elif difference == "component_name":
        state.components.at[0, "component_name"] = "different"
    elif difference == "component_membership":
        state.component_indices.iloc[1] = pd.NA
    elif difference == "optional_column":
        del state.atom_attributes["stereochemistry"]
    elif difference in {"connectivity_completeness", "component_completeness"}:
        setattr(state, difference, "partial")
    elif difference == "component_evidence":
        state.component_evidence = "inferred"
    elif difference == "state_order":
        source.chemical_states._states.reverse()
    elif difference == "reference":
        source.chemical_states._reference_index = 0
    elif difference == "atom_correspondence":
        source.topology.atoms["atom_id"] = pd.array(["1", "0"], dtype="string")
    elif difference == "label_vs_missing":
        state.components.at[0, "component_type"] = "nan"
    else:
        state.atom_attributes.at[1, "is_aromatic"] = False

    with pytest.raises(StructuralInconsistencyError, match="alignment"):
        msm.append_structures(target, source)
    assert target.structures.n_structures == 3
    np.testing.assert_array_equal(
        puw.get_value(target.structures.coordinates, to_unit="nm"), before
    )
    assert target.structures._molsys_owner_ref() is target


def test_native_append_after_real_tctim_h5msm_round_trip(tmp_path):
    source = msm.convert(
        msm.systems["TcTIM"]["1tcd.bcif.gz"], to_form="molsysmt.MolSys"
    )
    msm.remove(
        source, selection="group_type=='water' or group_type=='ion'", in_place=True
    )
    target = _recover(source, "h5msm", tmp_path)
    control = source.copy()
    control.append_structures(source)

    target.append_structures(source)

    assert source.topology.n_atoms == 3818
    assert target.structures.n_structures == control.structures.n_structures == 2
    np.testing.assert_array_equal(
        puw.get_value(target.structures.coordinates, to_unit="nm"),
        puw.get_value(control.structures.coordinates, to_unit="nm"),
    )


@pytest.mark.parametrize("value", [1, True])
def test_inventory_does_not_coerce_nonstring_values_into_labels(value):
    source, target = _source(), _source()
    source.chemical_states._states[0].components["component_name"] = pd.Series(
        [value], dtype=object
    )
    target.chemical_states._states[0].components["component_name"] = pd.Series(
        [str(value)], dtype="string"
    )
    assert not target.chemical_states._inventory_equals(source.chemical_states)
