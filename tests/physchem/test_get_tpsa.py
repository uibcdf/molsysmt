"""Primary fragment sums, molecular boundaries and state-aware TPSA contracts."""

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentChoiceError

# Independent simple sums from Ertl et al. (2000), Table 1, angstrom²;
# doi:10.1021/jm000942e. These are not experimental permeability claims.
CASES = [
    ("CCO", 20.23),
    ("COC", 9.23),
    ("CCN", 26.02),
    ("CC(=O)O", 37.30),
    ("CC(=O)[O-]", 40.13),
]


def source_from_smiles(smiles):
    from rdkit import Chem

    return Chem.MolFromSmiles(smiles)


@pytest.mark.parametrize("smiles,expected", CASES)
@pytest.mark.parametrize(
    "form", ["rdkit.Mol", "molsysmt.MolSys", "declared_domains", "h5msm", "sdf"]
)
def test_tpsa_primary_fragment_sums_across_forms(smiles, expected, form, tmp_path):
    source = source_from_smiles(smiles)
    if form == "sdf":
        from rdkit import Chem

        path = tmp_path / "molecule.sdf"
        # Explicit CTAB valences encode the known fixed-state H inventory.
        # Default VAL=0 leaves this evidence unspecified in the native reader.
        block = Chem.MolToV3KMolBlock(source)
        lines = block.splitlines()
        in_atoms = False
        for i, line in enumerate(lines):
            if line == "M  V30 BEGIN ATOM":
                in_atoms = True
            elif line == "M  V30 END ATOM":
                in_atoms = False
            elif in_atoms:
                atom = source.GetAtomWithIdx(int(line.split()[2]) - 1)
                valence = atom.GetTotalValence()
                lines[i] += f" VAL={valence if valence else -1}"
        path.write_text("\n".join(lines) + "\n$$$$\n")
        source = str(path)
    elif form == "h5msm":
        source = msm.convert(source, to_form=str(tmp_path / "molecule.h5msm"))
    elif form == "declared_domains":
        native = msm.convert(source, to_form="molsysmt.MolSys")
        source = [native.topology, native.chemical_states]
    elif form != "rdkit.Mol":
        source = msm.convert(source, to_form=form)
    result = msm.physchem.get_tpsa(source)
    assert result.shape == (1,)
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result, to_unit="angstrom**2"),
        [expected],
        atol=1e-12,
        rtol=0,
    )


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize(
    "selection,expected",
    [
        ("all", [20.23, 9.23]),
        ([1, 0, 1], [9.23, 20.23, 9.23]),
        ([], []),
        ("atom_index==0", [20.23]),
        (0, [20.23]),
    ],
)
def test_tpsa_molecular_selection_and_units(unit, selection, expected):
    with msm.pyunitwizard.context(standard_units=[unit, "ps", "radians"]):
        result = msm.physchem.get_tpsa(
            source_from_smiles("CCO.COC"), selection=selection, return_report=True
        )
    assert result["tpsa"].shape == (len(expected),)
    assert msm.pyunitwizard.get_unit(result["tpsa"]) == msm.pyunitwizard.unit(unit) ** 2
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result["tpsa"], to_unit="angstrom**2"),
        expected,
        atol=1e-12,
        rtol=0,
    )
    report = result["report"]
    assert report["atom_offsets"].shape == (len(expected) + 1,)
    assert report["molecule_indices"].dtype == np.int64
    assert report["chemical_state_index"] == 0
    assert report["formal_charge_unit"] == "elementary_charge"


@pytest.mark.parametrize(
    "smiles,no,nosp",
    [("OC(=O)P(=O)(O)O", 94.83, 104.64), ("CS(C)(=O)=O", 34.14, 42.52)],
)
def test_tpsa_explicit_sulfur_phosphorus_scope(smiles, no, nosp):
    # Original paper fragment coefficients and RDKit documented variant examples.
    source = source_from_smiles(smiles)
    for enabled, expected in [(False, no), (True, nosp)]:
        area = msm.physchem.get_tpsa(source, include_sulfur_phosphorus=enabled)
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(area, to_unit="angstrom**2"),
            [expected],
            atol=1e-12,
            rtol=0,
        )


@pytest.mark.parametrize("smiles", ["CCO", "c1ccncc1", "[NH3+]CC(=O)[O-]", "N#C"])
def test_indexed_and_nonindexed_hydrogens_give_same_descriptor_without_mutation(smiles):
    from rdkit import Chem

    original = source_from_smiles(smiles)
    binary = original.ToBinary()
    implicit = msm.physchem.get_tpsa(original)
    explicit = msm.physchem.get_tpsa(Chem.AddHs(original))
    assert original.ToBinary() == binary
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(implicit, to_unit="nm**2"),
        msm.pyunitwizard.get_value(explicit, to_unit="nm**2"),
        atol=1e-14,
        rtol=0,
    )


def test_report_maps_are_detached_and_source_tables_unchanged():
    source = msm.convert(source_from_smiles("CCO.COC"), to_form="molsysmt.MolSys")
    atoms = source.topology.atoms.copy(deep=True)
    bonds = source.chemical_states._states[0].bonds.copy(deep=True)
    first = msm.physchem.get_tpsa(source, selection=[1, 0, 1], return_report=True)
    report = first["report"]
    assert report["atom_indices"].tolist() == [3, 4, 5, 0, 1, 2, 3, 4, 5]
    assert report["atom_offsets"].tolist() == [0, 3, 6, 9]
    assert report["molecule_indices"].tolist() == [1, 0, 1]
    report["parameters"]["include_sulfur_phosphorus"] = "edited"
    next(
        item
        for item in report["attribution"]["items"]
        if item["id"] == "doi:10.1021/jm000942e"
    )["authors"].append("edited")
    second = msm.physchem.get_tpsa(source, return_report=True)
    assert second["report"]["parameters"]["include_sulfur_phosphorus"] is False
    assert (
        "edited"
        not in next(
            item
            for item in second["report"]["attribution"]["items"]
            if item["id"] == "doi:10.1021/jm000942e"
        )["authors"]
    )
    pd.testing.assert_frame_equal(atoms, pd.DataFrame(source.topology.atoms))
    pd.testing.assert_frame_equal(
        bonds, pd.DataFrame(source.chemical_states._states[0].bonds)
    )


@pytest.mark.parametrize(
    "field",
    [
        "formal_charge",
        "n_unpaired_electrons",
        "n_implicit_hydrogens",
        "n_explicit_hydrogens",
        "allows_implicit_hydrogens",
    ],
)
def test_missing_chemical_evidence_fails(field):
    source = msm.convert(source_from_smiles("CCO"), to_form="molsysmt.MolSys")
    source.chemical_states._states[0].atom_attributes[field] = None
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.physchem.get_tpsa(source)


@pytest.mark.parametrize("smiles", ["[Na+]", "[CH3]", "[*]"])
def test_unsupported_chemistry_fails(smiles):
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.physchem.get_tpsa(source_from_smiles(smiles))


@pytest.mark.parametrize(
    "name,value",
    [
        ("element", "bond"),
        ("method", "rdkit"),
        ("include_sulfur_phosphorus", 1),
        ("return_report", "yes"),
    ],
)
def test_public_arguments_are_validated(name, value):
    with pytest.raises((msm.ArgumentError, ArgumentChoiceError)):
        msm.physchem.get_tpsa(source_from_smiles("CCO"), **{name: value})


def test_stale_provider_cache_is_not_used_or_modified():
    source = source_from_smiles("CCO")
    source.SetDoubleProp("_tpsa-0", 9999)
    result = msm.physchem.get_tpsa(source)
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result, to_unit="angstrom**2"), [20.23], atol=1e-12
    )
    assert source.GetDoubleProp("_tpsa-0") == 9999


def test_optional_attribution_real_reused_session_and_failure(monkeypatch):
    from molsysmt import _ackredit

    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("TPSA client"):
        with ackredit.scope("consumer.describe"):
            first = msm.physchem.get_tpsa(source_from_smiles("CCO"), return_report=True)
            empty = msm.physchem.get_tpsa(
                source_from_smiles("CCO"), selection=[], return_report=True
            )
        assert "doi:10.1021/jm000942e" in ackredit.get_used_items()
        first_items = {
            item["id"]: item for item in first["report"]["attribution"]["items"]
        }
        empty_items = {
            item["id"]: item for item in empty["report"]["attribution"]["items"]
        }
        assert (
            first_items["doi:10.1021/jm000942e"] == empty_items["doi:10.1021/jm000942e"]
        )
        assert "rdkit-aromaticity-model" in first_items
        assert "rdkit-aromaticity-model" not in empty_items
        tree = ackredit.current_session().usage_tree
        assert "molsysmt.physchem.get_tpsa" in tree["consumer.describe"]["children"]
        assert (
            "molsysmt.physchem.get_aromaticity"
            in tree["molsysmt.physchem.get_tpsa"]["children"]
        )
    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    result = msm.physchem.get_tpsa(source_from_smiles("CCO"))
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result, to_unit="angstrom**2"), [20.23], atol=1e-12
    )


def test_explicit_chemical_state_changes_tpsa_without_mutating_reference():
    source = msm.convert(source_from_smiles("CC(=O)O"), to_form="molsysmt.MolSys")
    state = deepcopy(source.chemical_states._states[0])
    state.state_id = "acetate"
    state.atom_attributes.loc[3, "formal_charge"] = -1
    state.atom_attributes.loc[3, "n_implicit_hydrogens"] = 0
    source.chemical_states._append_state(state, False)
    baseline = source.chemical_states._states[0].atom_attributes.copy(deep=True)
    reference = msm.physchem.get_tpsa(source)
    alternate = msm.physchem.get_tpsa(source, chemical_state=1, return_report=True)
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(reference, to_unit="angstrom**2"), [37.3], atol=1e-12
    )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(alternate["tpsa"], to_unit="angstrom**2"),
        [40.13],
        atol=1e-12,
    )
    assert alternate["report"]["chemical_state_index"] == 1
    pd.testing.assert_frame_equal(
        baseline, source.chemical_states._states[0].atom_attributes
    )


def test_unselected_unsupported_molecules_are_not_calculated():
    source = source_from_smiles("CCO.[Zn+2]")
    result = msm.physchem.get_tpsa(source, selection=[0])
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result, to_unit="angstrom**2"), [20.23], atol=1e-12
    )


@pytest.mark.parametrize("bonded", [False, True])
def test_disconnected_or_covalently_crossed_molecule_definitions_fail(bonded):
    original = msm.convert(source_from_smiles("CCO.COC"), to_form="molsysmt.MolSys")
    builder = msm.MolSysBuilder()
    for kind in ["C", "C", "O", "C", "O", "C"]:
        builder.add_atom(atom_type=kind)
    builder.add_group([0, 1, 2], group_name="LIG")
    builder.add_group([3, 4, 5], group_name="LIG")
    if bonded:
        builder.add_molecule([0])
        builder.add_molecule([1])
    else:
        builder.add_molecule([0, 1])
    source = builder.build()
    source.chemical_states = original.chemical_states.copy()
    if bonded:
        source.chemical_states._append_chemical_state_bonds(
            [[1, 3]], bond_order=[1], bond_type=["covalent"]
        )
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.physchem.get_tpsa(source, selection=[0])


def test_native_sdf_without_explicit_hydrogen_evidence_fails_clearly(tmp_path):
    from rdkit import Chem

    path = tmp_path / "unspecified.sdf"
    writer = Chem.SDWriter(str(path))
    writer.write(source_from_smiles("CCO"))
    writer.close()
    with pytest.raises(
        msm.StructuralInconsistencyError, match="declared n_implicit_hydrogens"
    ):
        msm.physchem.get_tpsa(str(path))


def test_optional_attribution_provider_failure_preserves_completed_tpsa(monkeypatch):
    import warnings

    from molsysmt import _ackredit

    def broken():
        raise RuntimeError("controlled provider failure")

    monkeypatch.setattr(_ackredit, "backend", broken)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        result = msm.physchem.get_tpsa(source_from_smiles("CCO"))
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result, to_unit="angstrom**2"), [20.23], atol=1e-12
    )


def test_structure_state_context_must_be_unambiguous():
    source = msm.convert(source_from_smiles("CCO"), to_form="molsysmt.MolSys")
    state = deepcopy(source.chemical_states._states[0])
    state.state_id = "other"
    source.chemical_states._append_state(state, False)
    source.structures.coordinates = msm.pyunitwizard.quantity(np.zeros((2, 3, 3)), "nm")
    source._set_structure_chemical_state_indices([0, 1])
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.physchem.get_tpsa(
            source, chemical_state="structure", structure_indices=[1, 0]
        )
    result = msm.physchem.get_tpsa(
        source, chemical_state="structure", structure_indices=[1], return_report=True
    )
    assert result["report"]["chemical_state_index"] == 1
    assert result["tpsa"].shape == (1,)


def test_coordinate_series_is_not_copied_for_graph_descriptor(monkeypatch):
    source = msm.convert(source_from_smiles("CCO"), to_form="molsysmt.MolSys")
    source.structures.coordinates = msm.pyunitwizard.quantity(
        np.zeros((20, 3, 3)), "nm"
    )

    def forbidden(*args, **kwargs):
        raise AssertionError(
            "A graph descriptor must not copy the source structure series."
        )

    monkeypatch.setattr(source.structures, "copy", forbidden)
    area = msm.physchem.get_tpsa(source)
    assert area.shape == (1,)


def test_h5msm_calculation_preserves_file_bytes(tmp_path):
    import hashlib

    source = msm.convert(
        source_from_smiles("CCO"), to_form=str(tmp_path / "source.h5msm")
    )
    from pathlib import Path

    original = hashlib.sha256(Path(source).read_bytes()).digest()
    msm.physchem.get_tpsa(source, return_report=True)
    assert hashlib.sha256(Path(source).read_bytes()).digest() == original
