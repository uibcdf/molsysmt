"""Receiving a declared H-policy edit independently of chemical correspondence."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import MolSys, Structures
from tests.native.test_preparation_history import assert_tree

puw = msm.pyunitwizard


def water(*, flags=(True, False), isotopes=(None, None, None), structures=True):
    """Declare an analytical O-H/H graph; coordinates are arbitrary test data."""
    source = MolSys(n_atoms=3, n_bonds=2)
    source.topology.atoms["atom_type"] = pd.array(["O", "H", "H"], dtype="string")
    source.topology.atoms["atom_id"] = pd.array(["o", "h1", "h2"], dtype="string")
    source.topology.atoms["isotope"] = pd.array(isotopes, dtype="UInt16")
    for name, value in {
        "formal_charge": 0,
        "atom_is_aromatic": False,
        "n_unpaired_electrons": 0,
        "n_implicit_hydrogens": 0,
        "n_explicit_hydrogens": 0,
        "allows_implicit_hydrogens": [True, *flags],
        "atom_stereochemistry": "unspecified",
    }.items():
        msm.set(source, element="atom", **{name: value})
    state = source.chemical_states._states[0]
    state.bonds["atom1_index"] = [0, 0]
    state.bonds["atom2_index"] = [2, 1]
    state.bonds["bond_type"] = "covalent"
    state.bonds["bond_order"] = 1
    state.bonds["is_aromatic"] = False
    state.connectivity_completeness = "complete"
    if structures:
        source.structures = Structures(
            coordinates=puw.quantity(np.arange(18).reshape(2, 3, 3), "angstrom"),
            box=puw.quantity(np.tile(np.eye(3), (2, 1, 1)), "nm"),
            time=puw.quantity([0, 1], "ps"),
        )
        source.interactions = {
            "empty": msm.Interactions.from_records(
                [],
                n_atoms=3,
                n_structures=2,
                evaluated_structure_indices=[0, 1],
                method="control",
            )
        }
    else:
        source.structures = None
    return source


def normalize(source, **kwargs):
    return msm.chemical_states.normalize_indexed_hydrogen_policy(source, **kwargs)


def test_literal_policy_preserves_other_data_and_records_original_source_evidence():
    source = water(isotopes=(None, 2, 3))
    original = source.copy()
    result = normalize(source)
    output, report = result["molecular_system"], result["report"]
    assert output is not source
    assert report["schema"] == "molsysmt.indexed_hydrogen_policy@1"
    assert report["method"] == "closed_neutral_terminal_hydrogens"
    assert report["status"] == "normalized"
    assert report["chemical_state_index"] == 0
    assert report["atom_correspondence"] == {"indices": "identity", "n_atoms": 3}
    np.testing.assert_array_equal(report["hydrogen_atom_indices"], [1, 2])
    np.testing.assert_array_equal(report["changed_atom_indices"], [1])
    np.testing.assert_array_equal(report["parent_hydrogen_pairs"], [[0, 1], [0, 2]])
    np.testing.assert_array_equal(
        report["original_allows_implicit_hydrogens"], [True, False]
    )
    assert report["original_allows_implicit_hydrogens"].dtype == np.bool_
    assert report["invalidated_analysis_names"] == ["empty"]
    assert output.interactions["empty"].evaluated_structure_indices.tolist() == []
    assert source.interactions["empty"].evaluated_structure_indices.tolist() == [0, 1]
    assert msm.get(output, element="atom", allows_implicit_hydrogens=True) == [
        True,
        False,
        False,
    ]
    before, after = (
        original.chemical_states._states[0],
        output.chemical_states._states[0],
    )
    pd.testing.assert_frame_equal(
        before.atom_attributes.drop(columns="allows_implicit_hydrogens"),
        after.atom_attributes.drop(columns="allows_implicit_hydrogens"),
    )
    pd.testing.assert_frame_equal(before.bonds, after.bonds)
    pd.testing.assert_frame_equal(source.topology.atoms, output.topology.atoms)
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes, before.atom_attributes
    )
    for field in ("coordinates", "box", "time"):
        np.testing.assert_array_equal(
            puw.get_value(getattr(output.structures, field)),
            puw.get_value(getattr(source.structures, field)),
        )
        assert puw.get_unit(getattr(output.structures, field)) == puw.get_unit(
            getattr(source.structures, field)
        )
    assert source.chemical_states.get_preparation_history() == ()
    history = output.chemical_states.get_preparation_history()
    assert len(history) == 1
    assert history[0]["output"] == {
        "n_atoms": 3,
        "n_bonds": 2,
        "chemical_state_index": 0,
    }
    assert_tree(history[0]["report"], report)
    report["changed_atom_indices"][0] = 99
    np.testing.assert_array_equal(
        output.chemical_states.get_preparation_history()[0]["report"][
            "changed_atom_indices"
        ],
        [1],
    )


def test_unchanged_and_no_indexed_hydrogens_keep_analysis_and_typed_empty_results():
    source = water(flags=(False, False))
    result = normalize(source)
    output, report = result["molecular_system"], result["report"]
    assert report["status"] == "unchanged"
    assert report["changed_atom_indices"].shape == (0,)
    assert report["changed_atom_indices"].dtype == np.int64
    assert output.interactions["empty"].evaluated_structure_indices.tolist() == [0, 1]
    assert report["invalidated_analysis_names"] == []
    assert len(output.chemical_states.get_preparation_history()) == 1

    source.topology.atoms["atom_type"] = ["C", "C", "C"]
    result = normalize(source)
    report = result["report"]
    assert report["status"] == "empty"
    assert report["hydrogen_atom_indices"].shape == (0,)
    assert report["hydrogen_atom_indices"].dtype == np.int64
    assert report["parent_hydrogen_pairs"].shape == (0, 2)
    assert report["parent_hydrogen_pairs"].dtype == np.int64
    assert report["original_allows_implicit_hydrogens"].dtype == np.bool_
    assert result["molecular_system"].interactions[
        "empty"
    ].evaluated_structure_indices.tolist() == [0, 1]


def test_zero_atom_state_is_an_empty_operation_not_a_new_chemical_state():
    source = MolSys(n_atoms=0)
    result = normalize(source)
    assert result["report"]["status"] == "empty"
    assert result["molecular_system"].chemical_states.n_chemical_states == 1
    assert source.chemical_states.get_preparation_history() == ()


def test_zero_atom_domain_does_not_hide_stored_bond_rows():
    source = MolSys(n_atoms=0, n_bonds=1)
    with pytest.raises(msm.StructuralInconsistencyError, match="empty atom domain"):
        normalize(source)
    assert source.chemical_states.get_preparation_history() == ()


def test_single_fractional_order_is_preserved_without_integer_order_inference():
    source = water()
    bonds = source.chemical_states.get_bonds()
    bonds.at[0, "bond_order"] = pd.NA
    bonds.at[0, "fractional_bond_order"] = 1.0
    result = normalize(source)
    after = result["molecular_system"].chemical_states.get_bonds()
    assert result["report"]["status"] == "normalized"
    assert pd.isna(after.at[0, "bond_order"])
    assert after.at[0, "fractional_bond_order"] == 1.0


def test_virtual_only_inventory_is_not_materialized_or_closed():
    source = water(structures=False)
    source.topology.atoms["atom_type"] = pd.array(["C", "C", "C"], dtype="string")
    msm.set(
        source,
        element="atom",
        n_implicit_hydrogens=[2, 3, 3],
        allows_implicit_hydrogens=True,
    )
    result = normalize(source)
    output = result["molecular_system"]
    assert result["report"]["status"] == "empty"
    assert output.get(n_atoms=True) == 3
    assert output.structures is None
    assert msm.get(output, element="atom", n_implicit_hydrogens=True) == [2, 3, 3]
    assert msm.get(output, element="atom", allows_implicit_hydrogens=True) == [
        True,
        True,
        True,
    ]


def test_unknown_heavy_virtual_counts_are_not_filled():
    source = water()
    msm.set(source, element="atom", selection=[0], n_implicit_hydrogens=None)
    with pytest.raises(
        msm.StructuralInconsistencyError, match="missing_stored_hydrogen_counts"
    ):
        normalize(source)
    assert msm.get(
        source, element="atom", selection=[0], n_implicit_hydrogens=True
    ) == [None]


def test_extracted_history_retains_its_original_operation_axis():
    output = normalize(water())["molecular_system"]
    original = output.chemical_states.get_preparation_history()
    extracted = msm.extract(output, selection=[2, 0])
    assert extracted.get(n_atoms=True) == 2
    assert_tree(extracted.chemical_states.get_preparation_history(), original)
    assert (
        extracted.chemical_states.get_preparation_history()[-1]["report"][
            "atom_correspondence"
        ]["n_atoms"]
        == 3
    )


def test_geometry_is_shared_protected_and_later_edits_are_isolated():
    source = water()
    coordinates = puw.get_value(
        source.structures.coordinates, to_unit="angstrom"
    ).copy()
    output = normalize(source)["molecular_system"]
    assert output.structures is not source.structures
    assert np.shares_memory(
        puw.get_value(source.structures.coordinates),
        puw.get_value(output.structures.coordinates),
    )
    assert np.shares_memory(
        puw.get_value(source.structures.box), puw.get_value(output.structures.box)
    )
    assert output.chemical_states is not source.chemical_states
    msm.set(
        output,
        element="atom",
        selection=[1],
        structure_indices=[0],
        coordinates=puw.quantity([[[9.0, 8.0, 7.0]]], "angstrom"),
    )
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates, to_unit="angstrom"), coordinates
    )
    np.testing.assert_allclose(
        puw.get_value(output.structures.coordinates, to_unit="angstrom")[0, 1],
        [9, 8, 7],
    )


@pytest.mark.parametrize(
    "field,value",
    [
        ("formal_charge", 1),
        ("formal_charge", None),
        ("n_unpaired_electrons", 1),
        ("n_unpaired_electrons", None),
        ("n_implicit_hydrogens", 1),
        ("n_explicit_hydrogens", 1),
        ("n_explicit_hydrogens", None),
        ("allows_implicit_hydrogens", None),
        ("atom_is_aromatic", True),
        ("atom_is_aromatic", None),
        ("atom_stereochemistry", "R"),
        ("atom_stereochemistry", None),
    ],
)
def test_unknown_or_incompatible_hydrogens_reject_before_copy_or_mutation(
    field, value, monkeypatch
):
    source = water()
    msm.set(source, element="atom", selection=[2], **{field: value})
    before = source.chemical_states._states[0].atom_attributes.copy(deep=True)
    history = source.chemical_states.get_preparation_history()

    def forbidden_copy(*args, **kwargs):
        pytest.fail("Rejected chemistry must not prepare an output copy")

    monkeypatch.setattr(MolSys, "copy", forbidden_copy)
    with pytest.raises(msm.StructuralInconsistencyError):
        normalize(source)
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes, before
    )
    assert_tree(source.chemical_states.get_preparation_history(), history)


@pytest.mark.parametrize(
    "variant",
    [
        "h_h",
        "multiple_parents",
        "dative",
        "double",
        "fraction",
        "unknown_order",
        "aromatic",
        "unknown_aromatic",
        "stereo",
        "duplicate",
        "endpoint",
        "incomplete",
    ],
)
def test_unsupported_or_ambiguous_connectivity_is_not_repaired(variant):
    source = water()
    state = source.chemical_states._states[0]
    if variant == "h_h":
        state.bonds.at[0, "atom1_index"] = 1
    elif variant == "multiple_parents":
        source.topology.atoms.at[2, "atom_type"] = "C"
        state.bonds.at[0, "atom2_index"] = 1
        state.bonds.at[0, "atom1_index"] = 2
    elif variant == "dative":
        state.bonds.at[0, "bond_type"] = "dative"
    elif variant == "double":
        state.bonds.at[0, "bond_order"] = 2
    elif variant == "fraction":
        state.bonds.at[0, "fractional_bond_order"] = 1.5
    elif variant == "unknown_order":
        state.bonds.at[0, "bond_order"] = pd.NA
    elif variant == "aromatic":
        state.bonds.at[0, "is_aromatic"] = True
    elif variant == "unknown_aromatic":
        state.bonds.at[0, "is_aromatic"] = pd.NA
    elif variant == "stereo":
        state.bonds.at[0, "stereochemistry"] = "E"
    elif variant == "duplicate":
        state.bonds.loc[0, ["atom1_index", "atom2_index"]] = [0, 1]
    elif variant == "endpoint":
        state.bonds.at[0, "atom1_index"] = 99
    else:
        state.connectivity_completeness = "partial"
    before = state.bonds.copy(deep=True)
    with pytest.raises(msm.StructuralInconsistencyError):
        normalize(source)
    pd.testing.assert_frame_equal(state.bonds, before)
    assert source.chemical_states.get_preparation_history() == ()


def test_selected_state_preserves_reference_associations_and_original_history():
    source = water()
    states = source.chemical_states
    states._append_state(states._states[0].copy())
    source._set_structure_chemical_state_indices([0, 1])
    first = states._states[0].atom_attributes.copy(deep=True)
    result = normalize(source, chemical_state=1)
    output = result["molecular_system"]
    assert result["report"]["chemical_state_index"] == 1
    assert output.chemical_states.reference_chemical_state_index == 0
    pd.testing.assert_frame_equal(
        output.chemical_states._states[0].atom_attributes, first
    )
    assert source.chemical_states.get(
        element="atom", chemical_state=1, allows_implicit_hydrogens=True
    ) == [True, True, False]
    assert output.chemical_states.get(
        element="atom", chemical_state=1, allows_implicit_hydrogens=True
    ) == [True, False, False]
    np.testing.assert_array_equal(
        output._get_structure_chemical_state_indices(resolved=True), [0, 1]
    )
    assert output.chemical_states.get_preparation_history(0) == ()
    assert len(output.chemical_states.get_preparation_history(1)) == 1


@pytest.mark.parametrize("selector", [True, -1, 1.5, "structure", "missing"])
def test_invalid_state_selectors_keep_public_argument_errors(selector):
    source = water()
    with pytest.raises(msm.ArgumentError):
        normalize(source, chemical_state=selector)
    assert source.chemical_states.get_preparation_history() == ()


def test_missing_or_ambiguous_chemical_context_stays_explicit():
    source = water()
    for item in (source.topology, source.chemical_states):
        with pytest.raises(msm.StructuralInconsistencyError):
            normalize(item)
    empty = water()
    empty.chemical_states = msm.ChemicalStates(n_atoms=3)
    with pytest.raises(msm.StructuralInconsistencyError):
        normalize(empty)
    assert empty.chemical_states.n_chemical_states == 0
    source.chemical_states._append_state(source.chemical_states._states[0].copy())
    source.chemical_states._set_reference_index(None)
    with pytest.raises(msm.StructuralInconsistencyError):
        normalize(source)


@pytest.mark.parametrize("form", ["native", "dictionary", "complementary", "h5msm"])
@pytest.mark.parametrize(
    "units", [["nm", "ps", "elementary_charge"], ["pm", "fs", "coulomb"]]
)
def test_forms_units_and_typed_history_round_trip(form, units, tmp_path):
    source = water(isotopes=(None, 2, 3))
    if form == "dictionary":
        item = msm.convert(source, to_form="molsysmt.MolSysDict")
    elif form == "complementary":
        item = [source.topology, source.chemical_states, source.structures]
    elif form == "h5msm":
        item = tmp_path / "source.h5msm"
        msm.h5msm.write(source, item)
    else:
        item = source
    with puw.context(standard_units=units):
        policy = str(puw.get_unit(puw.standardize(puw.quantity(1, "nm"))))
        result = normalize(item)
        assert str(puw.get_unit(puw.standardize(puw.quantity(1, "nm")))) == policy
    output, report = result["molecular_system"], result["report"]
    np.testing.assert_array_equal(report["changed_atom_indices"], [1])
    path = tmp_path / "output.h5msm"
    msm.h5msm.write(output, path)
    loaded = msm.h5msm.read(path)
    assert_tree(loaded.chemical_states.get_preparation_history()[-1]["report"], report)
    pd.testing.assert_frame_equal(loaded.topology.atoms, output.topology.atoms)
    wire = msm.convert(output.chemical_states, to_form="molsysmt.ChemicalStatesDict")
    states = msm.convert(wire, to_form="molsysmt.ChemicalStates")
    assert_tree(states.get_preparation_history()[-1]["report"], report)
    np.testing.assert_allclose(
        puw.get_value(loaded.structures.coordinates, to_unit="angstrom"),
        puw.get_value(source.structures.coordinates, to_unit="angstrom"),
    )
    assert source.chemical_states.get_preparation_history() == ()


def test_existing_history_is_retained_independently_and_no_rdkit_is_needed(monkeypatch):
    import builtins

    source = water()
    source.chemical_states.append_preparation_history(
        [
            dict(
                schema="molsysmt.preparation_record@1",
                index_scope="operation",
                output=dict(n_atoms=3, n_bonds=2, chemical_state_index=0),
                report=dict(
                    schema="molsysmt.fixture@1", marker=np.asarray([7], dtype=np.int64)
                ),
            )
        ]
    )
    history = source.chemical_states.get_preparation_history()
    original_import = builtins.__import__

    def guarded_import(name, *args, **kwargs):
        if name == "rdkit" or name.startswith("rdkit."):
            pytest.fail("Native H-policy normalization must not import RDKit")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", guarded_import)
    result = normalize(source)
    output = result["molecular_system"]
    assert_tree(output.chemical_states.get_preparation_history()[:-1], history)
    assert_tree(source.chemical_states.get_preparation_history(), history)
    assert result["report"]["software"] == {"molsysmt": msm.__version__}
    assert [item["roles"] for item in result["report"]["attribution"]["items"]] == [
        ["executed_software"]
    ]
