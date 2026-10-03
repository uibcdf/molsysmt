"""Protecting exact residue identity, coverage honesty and read-only assessment."""

import subprocess
import sys

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentError,
    NotWithThisFormError,
    StructuralInconsistencyError,
)
from molsysmt.native import MolSys, Structures

ALA = (
    ["N", "CA", "C", "O", "CB"],
    ["N", "C", "C", "O", "C"],
    [("N", "CA", 1), ("CA", "C", 1), ("C", "O", 2), ("CA", "CB", 1)],
)
MSE = (
    ["N", "CA", "C", "O", "CB", "CG", "SE", "CE"],
    ["N", "C", "C", "O", "C", "C", "Se", "C"],
    ALA[2] + [("CB", "CG", 1), ("CG", "SE", 1), ("SE", "CE", 1)],
)
SEP = (
    ["N", "CA", "C", "O", "CB", "OG", "P", "O1P", "O2P", "O3P"],
    ["N", "C", "C", "O", "C", "O", "P", "O", "O", "O"],
    ALA[2]
    + [
        ("CB", "OG", 1),
        ("OG", "P", 1),
        ("P", "O1P", 2),
        ("P", "O2P", 1),
        ("P", "O3P", 1),
    ],
)
TPO = (
    ["N", "CA", "C", "O", "CB", "OG1", "CG2", "P", "O1P", "O2P", "O3P"],
    ["N", "C", "C", "O", "C", "O", "C", "P", "O", "O", "O"],
    ALA[2]
    + [
        ("CB", "OG1", 1),
        ("CB", "CG2", 1),
        ("OG1", "P", 1),
        ("P", "O1P", 2),
        ("P", "O2P", 1),
        ("P", "O3P", 1),
    ],
)
MLY = (
    ["N", "CA", "C", "O", "CB", "CG", "CD", "CE", "NZ", "CH1", "CH2"],
    ["N", "C", "C", "O", "C", "C", "C", "C", "N", "C", "C"],
    ALA[2]
    + [
        ("CB", "CG", 1),
        ("CG", "CD", 1),
        ("CD", "CE", 1),
        ("CE", "NZ", 1),
        ("NZ", "CH1", 1),
        ("NZ", "CH2", 1),
    ],
)


def _system(specifications, *, n_frames=1):
    builder = msm.MolSysBuilder()
    for group_name, (names, elements, bonds) in specifications:
        lookup = {}
        for name, element in zip(names, elements):
            lookup[name] = builder.add_atom(atom_name=name, atom_type=element)
        builder.add_group(list(lookup.values()), group_name=group_name)
        for first, second, order in bonds:
            if first in lookup and second in lookup:
                builder.add_bond(
                    lookup[first],
                    lookup[second],
                    bond_order=order,
                    bond_type="covalent",
                )
    n_atoms = sum(len(spec[1][0]) for spec in specifications)
    if n_frames:
        builder.set_coordinates(
            msm.pyunitwizard.quantity(np.zeros((n_frames, n_atoms, 3)), "nm")
        )
    return builder.build()


def test_complete_inventory_does_not_establish_protonation_or_repair_coverage():
    source = _system([("ALA", ALA)])
    before_atoms = source.topology.atoms.copy(deep=True)
    before_bonds = source.topology.bonds.copy(deep=True)
    before_coordinates = msm.pyunitwizard.get_value(
        source.structures.coordinates, to_unit="nm"
    ).copy()
    report = msm.build.get_residue_chemical_coverage(source)
    group = report["groups"][0]
    assert report["schema"] == "molsysmt.residue_chemical_coverage@1"
    assert group["status"] == "assessed"
    assert group["heavy_atoms"]["missing_atom_names"] == []
    assert group["connectivity"]["status"] == "assessed"
    assert group["connectivity"]["bond_order"]["status"] == "unassessed"
    assert group["hydrogens"]["status"] == "unassessed"
    assert len(group["hydrogens"]["candidates"]) > 1
    assert all(
        candidate["missing_atom_names"]
        for candidate in group["hydrogens"]["candidates"]
    )
    assert group["protonation"]["status"] == "unassessed"
    assert "repair_placement" in report["unassessed_checks"]
    assert len(group["template"]["provenance"]["packaged_sha256"]) == 64
    assert "ready" not in report
    pd.testing.assert_frame_equal(source.topology.atoms, before_atoms)
    pd.testing.assert_frame_equal(source.topology.bonds, before_bonds)
    np.testing.assert_equal(
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
        before_coordinates,
    )
    group["heavy_atoms"]["expected_atom_names"].clear()
    assert source.topology.n_atoms == 5


def test_missing_and_unexpected_names_are_separate_from_unsupported_groups():
    incomplete = (ALA[0][:-1], ALA[1][:-1], ALA[2])
    source = _system(
        [
            ("ALA", ALA),
            ("ALA", incomplete),
            ("PTR", (["N"], ["N"], [])),
            ("HEM", (["FE"], ["Fe"], [])),
        ]
    )
    report = msm.build.get_residue_chemical_coverage(source)
    assert [g["status"] for g in report["groups"]] == [
        "assessed",
        "incomplete",
        "unassessed",
        "unassessed",
    ]
    assert report["groups"][1]["heavy_atoms"]["missing_atom_names"] == ["CB"]
    assert report["groups"][1]["connectivity"][
        "blocked_by_missing_atom_name_pairs"
    ] == [["CA", "CB"]]
    for group in report["groups"][2:]:
        assert group["template"] is None
        assert group["heavy_atoms"]["missing_atom_names"] is None
        assert group["reason_codes"] == ["no_exact_residue_template"]
    assert report["summary"] == {"assessed": 1, "incomplete": 1, "unassessed": 2}


@pytest.mark.parametrize(
    "name,spec", [("MSE", MSE), ("SEP", SEP), ("TPO", TPO), ("MLY", MLY)]
)
def test_modified_residues_use_exact_chemistry_and_heavy_only_hydrogen_scope(
    name, spec
):
    source = _system([(name, spec)])
    group = msm.build.get_residue_chemical_coverage(source)["groups"][0]
    assert group["status"] == "assessed"
    assert group["template"]["group_name"] == name
    assert group["heavy_atoms"]["expected_atom_names"] == sorted(spec[0])
    assert group["connectivity"]["bond_order"]["status"] == "assessed"
    assert group["hydrogens"]["reason_code"] == "heavy_only_template"
    assert group["hydrogens"]["candidates"] == []
    if name == "MSE":
        assert "SD" not in group["heavy_atoms"]["expected_atom_names"]
        source.topology.atoms.loc[6, "atom_type"] = "S"
        conflict = msm.build.get_residue_chemical_coverage(source)["groups"][0]
        assert conflict["heavy_atoms"]["element_conflict_atom_indices"].tolist() == [6]
        assert conflict["status"] == "incomplete"


def test_unexpected_modified_name_is_reported_instead_of_parent_fallback():
    source = _system([("SEP", SEP)])
    source.topology.atoms.loc[7, "atom_name"] = "XXP"
    group = msm.build.get_residue_chemical_coverage(source)["groups"][0]
    assert group["heavy_atoms"]["missing_atom_names"] == ["O1P"]
    assert group["heavy_atoms"]["unexpected_atom_names"] == ["XXP"]
    assert group["template"]["group_name"] == "SEP"
    assert group["status"] == "incomplete"


def test_bond_absence_unknown_types_and_order_conflicts_are_not_guessed():
    source = _system([("MSE", MSE)])
    state = source.chemical_states._states[0]
    state.bonds.loc[[0, 1], "bond_order"] = 3
    group = msm.build.get_residue_chemical_coverage(source)["groups"][0]
    assert group["connectivity"]["bond_order"]["conflict_bond_indices"].tolist() == [
        0,
        1,
    ]
    assert "bond_order_conflict" in group["reason_codes"]
    state.bonds.loc[0, "bond_type"] = pd.NA
    untyped = msm.build.get_residue_chemical_coverage(source)["groups"][0]
    assert untyped["connectivity"]["status"] == "unassessed"
    assert untyped["connectivity"]["untyped_bond_indices"].tolist() == [0]
    assert untyped["connectivity"]["missing_bonded_atom_pairs"].shape == (0, 2)
    state.bonds.loc[0, "bond_type"] = "dative"
    wrong = msm.build.get_residue_chemical_coverage(source)["groups"][0]
    assert wrong["connectivity"]["conflict_bond_type_indices"].tolist() == [0]
    source.topology._set_chemical_state_bonds(
        state.bonds.iloc[1:].reset_index(drop=True)
    )
    missing = msm.build.get_residue_chemical_coverage(source)["groups"][0]
    assert missing["connectivity"]["missing_bonded_atom_pairs"].tolist() == [[0, 1]]


def test_duplicate_atom_names_block_mapping_and_report_alternate_location_ambiguity():
    source = _system([("ALA", ALA)])
    source.topology.atoms.loc[4, "atom_name"] = "CA"
    group = msm.build.get_residue_chemical_coverage(source)["groups"][0]
    assert group["status"] == "unassessed"
    assert group["heavy_atoms"]["duplicate_atom_names"] == ["CA"]
    assert group["connectivity"]["status"] == "unassessed"
    assert group["hydrogens"]["reason_code"] == "incomplete_or_conflicting_atom_mapping"


def test_hydrogen_bonds_do_not_become_unexpected_heavy_atom_bonds():
    names, elements, bonds = ALA
    source = _system(
        [
            (
                "ALA",
                (
                    names + ["H", "HA", "HB1", "HB2", "HB3"],
                    elements + ["H"] * 5,
                    bonds + [("N", "H", 1), ("CA", "HA", 1)],
                ),
            )
        ]
    )
    group = msm.build.get_residue_chemical_coverage(source)["groups"][0]
    assert group["connectivity"]["status"] == "assessed"
    assert group["connectivity"]["unexpected_bond_indices"].size == 0
    assert group["hydrogens"]["observed_atom_indices"].tolist() == list(range(5, 10))
    assert any(
        candidate["missing_atom_names"] == []
        for candidate in group["hydrogens"]["candidates"]
    )
    assert group["protonation"]["status"] == "unassessed"


def test_group_indices_string_selection_boundary_and_empty_results():
    source = _system([("ALA", ALA), ("ALA", ALA), ("PTR", (["N"], ["N"], []))])
    source.topology._append_chemical_state_bonds(
        [[2, 5]], types=["covalent"], orders=[1]
    )
    report = msm.build.get_residue_chemical_coverage(source, selection=[2, 0, 0])
    assert report["group_indices"].tolist() == [0, 2]
    bonds = source.chemical_states._states[0].bonds
    boundary_index = bonds.index[
        (bonds.atom1_index == 2) & (bonds.atom2_index == 5)
    ].tolist()
    assert report["groups"][0]["boundary_bond_indices"].tolist() == boundary_index
    assert msm.build.get_residue_chemical_coverage(source, selection="atom_index==0")[
        "group_indices"
    ].tolist() == [0]
    empty = msm.build.get_residue_chemical_coverage(source, selection=[])
    assert empty["groups"] == [] and empty["group_indices"].dtype == np.int64
    assert sum(empty["summary"].values()) == 0


def test_state_and_frame_association_is_shared_with_readiness(tmp_path, monkeypatch):
    source = _system([("MSE", MSE)], n_frames=3)
    source.chemical_states.append_state()
    source.chemical_states._states[1].bonds = source.chemical_states._states[
        0
    ].bonds.copy(deep=True)
    source.chemical_states._states[1].bonds.loc[0, "bond_order"] = 2
    source.chemical_states._set_reference_index(None)
    msm.set(source, element="system", structure_chemical_state_index=[0, 1, None])
    with pytest.raises(ArgumentError):
        msm.build.get_residue_chemical_coverage(source)
    for frame, expected in [(0, "assessed"), (1, "incomplete"), (2, "unassessed")]:
        report = msm.build.get_residue_chemical_coverage(
            source, structure_indices=[frame, frame], chemical_state="structure"
        )
        assert report["groups"][0]["status"] == expected
    ambiguous = msm.build.get_residue_chemical_coverage(source, structure_indices=[0])
    assert ambiguous["groups"][0]["reason_codes"] == ["chemical_state_ambiguous"]
    output = tmp_path / "source.h5msm"
    msm.convert(source, to_form=output)
    from molsysmt.form import _h5msm05_modular

    def reject_full_read(*args, **kwargs):
        raise AssertionError(
            "Numeric residue coverage must not materialize a trajectory."
        )

    monkeypatch.setattr(
        _h5msm05_modular, "read_independent_structures", reject_full_read
    )
    report = msm.build.get_residue_chemical_coverage(
        output, selection=[0], structure_indices=[1], chemical_state="structure"
    )
    assert report["chemical_readiness"]["chemical_state_index"] == 1
    assert report["groups"][0]["status"] == "incomplete"


def test_real_modified_pdb_and_pdbqt_are_inspectable_without_source_changes():
    from pathlib import Path

    source = Path(msm.__file__).parent / "data/pdb/3c8h.pdb"
    original = source.read_bytes()
    report = msm.build.get_residue_chemical_coverage(
        source, selection='group_name=="MSE"'
    )
    assert report["groups"]
    assert all(group["template"]["group_name"] == "MSE" for group in report["groups"])
    assert all(
        "SD" not in group["heavy_atoms"]["expected_atom_names"]
        for group in report["groups"]
    )
    assert source.read_bytes() == original
    source = Path(__file__).parents[1] / "form/data/vina_examples/1iep_receptor.pdbqt"
    report = msm.build.get_residue_chemical_coverage(source)
    assert len(report["groups"]) > 100
    assert report["chemical_readiness"]["fields"]["coordinates"]["status"] == "present"


@pytest.mark.parametrize(
    "kwargs",
    [
        {"selection": [-1]},
        {"selection": [1]},
        {"selection": [True]},
        {"chemical_state": "guess"},
        {"skip_digestion": "yes"},
    ],
)
def test_public_argument_validation(kwargs):
    with pytest.raises(ArgumentError):
        msm.build.get_residue_chemical_coverage(_system([("ALA", ALA)]), **kwargs)


def test_coordinate_only_source_has_no_residue_domain():
    coordinates = Structures()
    coordinates.append(coordinates=msm.pyunitwizard.quantity(np.zeros((1, 4, 3)), "nm"))
    with pytest.raises(NotWithThisFormError):
        msm.build.get_residue_chemical_coverage(
            MolSys._from_partial_domains(structures=coordinates)
        )


def test_unknown_group_membership_is_not_synthesized():
    source = _system([("ALA", ALA)])
    source.topology.atoms.loc[0, "group_index"] = pd.NA
    with pytest.raises(StructuralInconsistencyError):
        msm.build.get_residue_chemical_coverage(source)


def test_native_coverage_needs_neither_rdkit_nor_ackredit():
    script = """
import importlib.abc
import sys
class Absent(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'rdkit', 'ackredit'}:
            raise ModuleNotFoundError(fullname)
sys.meta_path.insert(0, Absent())
import molsysmt as msm
r = msm.build.get_residue_chemical_coverage(msm.systems['T4 lysozyme L99A']['181l.pdb'], selection=[0])
assert r['groups'][0]['template'] is not None
assert 'rdkit' not in sys.modules and 'ackredit' not in sys.modules
"""
    run = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr
