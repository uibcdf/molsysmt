"""Carry stored naming context to assessment and native preparation."""

import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from tests.build.test_get_residue_chemical_coverage import ALA, _system

HIS = (
    ["N", "CA", "C", "O", "CB", "CG", "ND1", "CE1", "NE2", "CD2"],
    ["N", "C", "C", "O", "C", "C", "N", "C", "N", "C"],
    ALA[2]
    + [
        ("CB", "CG", 1),
        ("CG", "ND1", 1),
        ("ND1", "CE1", 1),
        ("CE1", "NE2", 1),
        ("NE2", "CD2", 1),
        ("CD2", "CG", 1),
    ],
)
GLH = (
    ["N", "CA", "C", "O", "CB", "CG", "CD", "OE1"],
    ["N", "C", "C", "O", "C", "C", "C", "O"],
    ALA[2] + [("CB", "CG", 1), ("CG", "CD", 1), ("CD", "OE1", 2)],
)


def test_missing_heavy_query_uses_the_stored_vocabulary_and_source_group_indices(
    tmp_path,
):
    source = _system([("GLH", GLH), ("GLH", GLH)])
    source.topology.set_group_naming_schemes(["amber", "legacy"])
    assert msm.build.get_missing_heavy_atoms(source, selection=[1, 0]) == {0: ["OE2"]}
    stored = msm.convert(source, to_form=str(tmp_path / "partial.h5msm"))
    assert msm.build.get_missing_heavy_atoms(stored, selection=[1, 0]) == {0: ["OE2"]}


def test_coverage_keeps_same_name_different_profile_templates_separate():
    source = _system([("HID", HIS), ("HID", HIS)])
    source.topology.set_group_naming_schemes(["amber", "ccd"])
    report = msm.build.get_residue_chemical_coverage(source)
    first, second = report["groups"]
    assert first["template"]["naming_scheme"] == "amber"
    assert first["heavy_atoms"]["status"] == "assessed"
    assert "state_verification" in first["template"]["provenance"]
    assert second["template"] is None
    assert second["status"] == "unassessed"


def test_bare_ambiguous_query_is_unassessed_in_a_molecular_audit():
    source = _system([("HID", HIS)])
    assert (
        msm.build.get_residue_chemical_coverage(source)["groups"][0]["template"] is None
    )


@pytest.mark.parametrize(
    "operation",
    [
        msm.build.get_missing_heavy_atoms,
        msm.build.add_missing_heavy_atoms,
        msm.build.add_missing_hydrogens,
        msm.build.reconcile_protonation,
    ],
)
def test_undeclared_ambiguous_preparation_fails_before_changing_the_source(operation):
    source = _system([("HID", HIS)])
    groups = source.topology.groups.copy()
    atoms = source.topology.atoms.copy()
    bonds = source.chemical_states._get_chemical_state_bonds().copy()
    with pytest.raises(ArgumentError) as error:
        operation(source, engine="MolSysMT")
    assert error.value.extra["argument"] == "naming_scheme"
    pd.testing.assert_frame_equal(
        groups, source.topology.groups, check_frame_type=False
    )
    pd.testing.assert_frame_equal(atoms, source.topology.atoms, check_frame_type=False)
    pd.testing.assert_frame_equal(
        bonds,
        source.chemical_states._get_chemical_state_bonds(),
        check_frame_type=False,
    )


def test_internal_named_histidine_keeps_its_hydrogen_state_during_addition_and_removal():
    source = msm.build.build_peptide(
        "AHA", engine="MolSysMT", to_form="molsysmt.MolSys"
    )
    source = msm.remove(source, selection='atom_type=="H"')
    middle = source.topology.groups.index[
        source.topology.groups["group_name"] == "HIS"
    ][0]
    source.topology.groups.at[middle, "group_name"] = "HID"
    source.topology.set_group_naming_schemes("amber", group_indices=[int(middle)])
    output = msm.build.add_missing_hydrogens(source, pH=12.0, engine="MolSysMT")
    mask = output.topology.atoms["group_index"] == middle
    names = set(output.topology.atoms.loc[mask, "atom_name"])
    assert "HD1" in names and "HE2" not in names
    assert "HD1" not in set(source.topology.atoms["atom_name"])
    reconciled = msm.build.reconcile_protonation(output, pH=12.0)
    mask = reconciled.topology.atoms["group_index"] == middle
    assert "HD1" in set(reconciled.topology.atoms.loc[mask, "atom_name"])
    assert (
        reconciled.topology.group_naming_schemes == output.topology.group_naming_schemes
    )


@pytest.mark.parametrize("engine", ["OpenMM", "PDBFixer"])
@pytest.mark.parametrize("scheme", [None, "amber", "ccd"])
def test_external_preparation_never_infers_a_contextual_name_convention(engine, scheme):
    from molsysmt._private.smonitor import NotImplementedMethodError

    source = _system([("HID", HIS)])
    source.topology.set_group_naming_schemes(scheme)
    error = ArgumentError if scheme is None else NotImplementedMethodError
    with pytest.raises(error):
        msm.build.add_missing_hydrogens(source, engine=engine)


@pytest.mark.parametrize(
    "operation",
    [
        msm.build.get_missing_heavy_atoms,
        msm.build.add_missing_heavy_atoms,
        msm.build.get_non_standard_residues,
    ],
)
def test_external_selection_does_not_refuse_unselected_ambiguous_labels(operation):
    source = _system([("ALA", ALA), ("HID", HIS)])
    # Select the ordinary group only; the external operation may proceed.
    output = operation(source, engine="PDBFixer", selection=[0])
    assert output is not None


def test_native_addition_reports_named_terminal_completion_as_unassessed():
    from molsysmt._private.smonitor import UnassessedResidueWarning

    source = _system([("HID", HIS)])
    source.topology.set_group_naming_schemes("amber")
    with pytest.warns(UnassessedResidueWarning, match="terminal-state"):
        output = msm.build.add_missing_hydrogens(source, engine="MolSysMT")
    assert output.topology.n_atoms == source.topology.n_atoms


def test_external_preparation_does_not_translate_a_modified_name_declared_as_amber():
    from molsysmt._private.smonitor import NotImplementedMethodError
    from tests.build.test_get_residue_chemical_coverage import MSE

    source = _system([("MSE", MSE)])
    source.topology.set_group_naming_schemes("amber")
    with pytest.raises(NotImplementedMethodError):
        msm.build.add_missing_hydrogens(source, engine="OpenMM")


def test_missing_bond_query_does_not_turn_undeclared_state_labels_into_geometry():
    source = _system([("HID", HIS)])
    with pytest.raises(ArgumentError):
        msm.build.get_missing_bonds(source, with_templates=True, with_distances=False)


def test_missing_bond_queries_use_reference_types_without_rewriting_stored_types():
    source = _system([("GLH", GLH)])
    source.topology.set_group_naming_schemes("amber")
    source.chemical_states.remove_bonds("all", skip_digestion=True)
    types = source.topology.groups["group_type"].copy()
    pairs = msm.build.get_missing_bonds(source, with_distances=False)
    index = {n: int(i) for i, n in source.topology.atoms["atom_name"].items()}
    assert sorted([index["CD"], index["OE1"]]) in pairs
    assert len(pairs) == 7
    pd.testing.assert_series_equal(types, source.topology.groups["group_type"])


def test_declared_ccd_component_does_not_inherit_stale_amino_acid_classification():
    source = msm.build.build_peptide(
        "AHA", engine="MolSysMT", to_form="molsysmt.MolSys"
    )
    middle = int(
        source.topology.groups.index[source.topology.groups["group_name"] == "HIS"][0]
    )
    source.topology.groups.at[middle, "group_name"] = "HID"
    source.topology.set_group_naming_schemes("ccd", group_indices=[middle])
    source.chemical_states.remove_bonds("all", skip_digestion=True)
    pairs = msm.build.get_missing_bonds(source)
    groups = source.topology.atoms["group_index"].to_numpy()
    assert not any(
        groups[a] != groups[b] and middle in (groups[a], groups[b]) for a, b in pairs
    )
    assert source.topology.groups.at[middle, "group_type"] == "amino acid"


def test_raw_openmm_reader_preserves_undeclared_groups_without_inventing_edges():
    from openmm.app import Topology, element

    external = Topology()
    group = external.addResidue("GLH", external.addChain("A"))
    for name in ["N", "CA", "C", "O", "CB", "CG", "CD", "OE1", "OE2"]:
        external.addAtom(
            name,
            element.oxygen
            if name.startswith("O")
            else element.nitrogen
            if name == "N"
            else element.carbon,
            group,
        )
    source = msm.convert(external, to_form="molsysmt.MolSys")
    assert source.get(n_bonds=True) == 0
    assert source.topology.group_naming_schemes == (None,)
    assert source.chemical_states._states[0].connectivity_completeness != "complete"
    source.topology.set_group_naming_schemes("amber")
    pairs = msm.build.get_missing_bonds(source, with_distances=False)
    assert len(pairs) == 8
    assert source.get(n_bonds=True) == 0
