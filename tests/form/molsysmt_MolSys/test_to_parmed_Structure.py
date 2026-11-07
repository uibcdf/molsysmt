"""Preserving native inventory, chemistry and structures during ParmEd export."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import MolSys, Structures


@pytest.fixture
def source(builder_pdb_molsys):
    pytest.importorskip("parmed")
    source = builder_pdb_molsys
    source.topology.atoms["atom_id"] = ["101", "202", "303", "404"]
    source.topology.atoms["atom_type"] = ["N", "C", "C", "O"]
    msm.set(source, formal_charge=[1, 0, -1, None])
    msm.set(source, atom_is_aromatic=[True, True, False, None])
    msm.set(source, element="bond", bond_order=[2, 1])
    msm.set(source, element="bond", bond_is_aromatic=[True, False])
    msm.set(source, element="bond", bond_type=["covalent", "dative"])
    source.molecular_mechanics.partial_charge = [0.1, 0.2, -0.3, 0.0]
    return source


def _geometry(source, n_structures, with_box):
    coordinates = (
        np.arange(n_structures * 12, dtype=float).reshape(n_structures, 4, 3) / 100
    )
    lengths = np.array(
        [[2.0 + index, 2.1 + index, 2.2 + index] for index in range(n_structures)]
    )
    boxes = np.array([np.diag(row) for row in lengths]) if with_box else None
    source.structures = Structures(
        coordinates=puw.quantity(coordinates, "nm"),
        box=None if boxes is None else puw.quantity(boxes, "nm"),
    )
    return coordinates, lengths


def _assert_source_unchanged(source, before):
    for name in ["atoms", "groups", "chains"]:
        pd.testing.assert_frame_equal(
            getattr(source.topology, name), getattr(before.topology, name)
        )
    pd.testing.assert_frame_equal(
        source.chemical_states.get_bonds(), before.chemical_states.get_bonds()
    )
    assert msm.get(source, formal_charge=True) == msm.get(before, formal_charge=True)
    assert msm.get(source, atom_is_aromatic=True) == msm.get(
        before, atom_is_aromatic=True
    )
    pd.testing.assert_frame_equal(
        source.molecular_mechanics.atoms_ff,
        before.molecular_mechanics.atoms_ff,
    )
    if source.structures is not None:
        np.testing.assert_array_equal(
            puw.get_value(source.structures.coordinates, to_unit="nm"),
            puw.get_value(before.structures.coordinates, to_unit="nm"),
        )
        if source.structures.box is not None:
            np.testing.assert_array_equal(
                puw.get_value(source.structures.box, to_unit="nm"),
                puw.get_value(before.structures.box, to_unit="nm"),
            )


def test_native_chemistry_serials_and_labels_are_preserved(source):
    from parmed.topologyobjects import QualitativeBondType

    before = source.copy()

    exported, report = msm.convert(
        source, to_form="parmed.Structure", return_report=True
    )

    assert [atom.formal_charge for atom in exported.atoms] == [1, 0, -1, None]
    assert [atom.aromatic for atom in exported.atoms] == [True, True, False, None]
    assert [str(atom.number) for atom in exported.atoms] == ["101", "202", "303", "404"]
    assert [group.number for group in exported.residues] == [10, 11]
    assert [group.chain for group in exported.residues] == ["A", "A"]
    assert [atom.name for atom in exported.atoms] == ["N", "CA", "C", "O"]
    assert [bond.order for bond in exported.bonds] == [2.0, 1.0]
    assert [bond.qualitative_type for bond in exported.bonds] == [
        QualitativeBondType.AROMATIC,
        QualitativeBondType.DATIVE,
    ]
    assert all(bond.type is None for bond in exported.bonds)
    np.testing.assert_allclose(
        [atom.charge for atom in exported.atoms], [0.1, 0.2, -0.3, 0.0]
    )
    assert not {"formal_charge", "coordinates", "box"}.intersection(
        issue.attribute for issue in report.issues
    )
    _assert_source_unchanged(source, before)


@pytest.mark.parametrize("n_structures", [1, 3])
@pytest.mark.parametrize("with_box", [False, True])
@pytest.mark.parametrize("unit", ["nm", "angstrom"])
def test_native_export_carries_all_structures_and_aligned_boxes(
    source, n_structures, with_box, unit
):
    coordinates, lengths = _geometry(source, n_structures, with_box)
    before = source.copy()

    with puw.context(standard_units=[unit, "fs", "degrees"]):
        exported = msm.convert(source, to_form="parmed.Structure")

    assert exported.get_coordinates("all") is not None
    np.testing.assert_allclose(exported.get_coordinates("all"), coordinates * 10)
    if with_box:
        np.testing.assert_allclose(exported.get_box("all")[:, :3], lengths * 10)
        # The owning PBC tool rounds crystallographic angles in radians.
        np.testing.assert_allclose(
            exported.get_box("all")[:, 3:], 90, rtol=0, atol=3e-5
        )
    else:
        assert exported.get_box("all") is None
    recovered = msm.convert(exported, to_form="molsysmt.MolSys")
    np.testing.assert_allclose(
        puw.get_value(recovered.structures.coordinates, to_unit="nm"), coordinates
    )
    assert msm.get(recovered, formal_charge=True) == [1, 0, -1, None]
    assert msm.get(recovered, element="bond", bond_order=True) == [2, 1]
    _assert_source_unchanged(source, before)


@pytest.mark.parametrize("structures", [[2, 0], [1, 1, 0]])
def test_native_export_keeps_requested_structures_and_canonical_atom_subset(
    source, structures
):
    coordinates, lengths = _geometry(source, 3, True)
    before = source.copy()

    exported = msm.convert(
        source,
        to_form="parmed.Structure",
        selection=[3, 1, 2],
        structure_indices=structures,
    )

    assert [str(atom.number) for atom in exported.atoms] == ["202", "303", "404"]
    assert [atom.formal_charge for atom in exported.atoms] == [0, -1, None]
    np.testing.assert_allclose(
        exported.get_coordinates("all"), coordinates[structures][:, [1, 2, 3]] * 10
    )
    np.testing.assert_allclose(exported.get_box("all")[:, :3], lengths[structures] * 10)
    np.testing.assert_allclose(
        [atom.charge for atom in exported.atoms], [0.2, -0.3, 0.0]
    )
    assert len(exported.bonds) == 1
    assert exported.bonds[0].order == 1
    _assert_source_unchanged(source, before)


@pytest.mark.parametrize("inventory_only", [False, True])
def test_topology_only_export_does_not_recover_attached_chemistry(
    source, inventory_only
):
    source.structures = None
    item = source.topology if inventory_only else source
    before = source.copy()

    exported = msm.convert(item, to_form="parmed.Structure")

    assert len(exported.atoms) == 4
    assert exported.get_coordinates("all") is None
    assert exported.get_box("all") is None
    assert [str(atom.number) for atom in exported.atoms] == ["101", "202", "303", "404"]
    assert [atom.formal_charge for atom in exported.atoms] == (
        [None] * 4 if inventory_only else [1, 0, -1, None]
    )
    assert len(exported.bonds) == (0 if inventory_only else 2)
    _assert_source_unchanged(source, before)


@pytest.mark.parametrize("route", ["public", "direct", "trusted"])
@pytest.mark.parametrize(
    "limitation", ["atom_id", "group_id", "bond_order", "partial_charge"]
)
def test_unrepresentable_native_values_are_reported_and_rejected(
    source, route, limitation
):
    if limitation == "atom_id":
        source.topology.atoms.loc[0, "atom_id"] = "00101"
    elif limitation == "group_id":
        source.topology.groups.loc[0, "group_id"] = "group-A"
    elif limitation == "bond_order":
        msm.set(source, element="bond", bond_order=[None, 1])
    else:
        source.molecular_mechanics.partial_charge = [None, 0.2, -0.3, 0.0]
    before = source.copy()
    report = msm.get_conversion_report(source, to_form="parmed.Structure")
    assert limitation in {issue.attribute for issue in report.issues}
    assert report.is_lossy and not report.is_exhaustive
    with pytest.raises(msm.NotCompatibleConversionError):
        if route == "public":
            msm.convert(source, to_form="parmed.Structure")
        else:
            from molsysmt.form.molsysmt_MolSys.to_parmed_Structure import (
                to_parmed_Structure,
            )

            to_parmed_Structure(source, skip_digestion=route == "trusted")
    _assert_source_unchanged(source, before)


@pytest.mark.parametrize("scale", [1e-4, 1.0, 1e4])
@pytest.mark.parametrize("orientation", ["rotation", "left_handed"])
def test_box_orientation_loss_is_detected_before_rounded_reduction(
    source, scale, orientation
):
    box = np.diag([2.0, 2.1, 2.2]) * scale
    if orientation == "rotation":
        angle = 1e-7
        rotation = np.array(
            [
                [np.cos(angle), -np.sin(angle), 0],
                [np.sin(angle), np.cos(angle), 0],
                [0, 0, 1],
            ]
        )
        box = box @ rotation
    else:
        box[2] *= -1
    source.structures.box = puw.quantity(box[None], "nm")
    before = source.copy()
    report = msm.get_conversion_report(source, to_form="parmed.Structure")
    assert "box" in {issue.attribute for issue in report.issues}
    with pytest.raises(msm.NotCompatibleConversionError, match="box vectors"):
        msm.convert(source, to_form="parmed.Structure")
    _assert_source_unchanged(source, before)


def test_duplicate_group_labels_keep_distinct_group_identity(source):
    source.topology.groups["group_name"] = ["LIG", "LIG"]
    source.topology.groups["group_id"] = ["10", "10"]

    exported = msm.convert(source, to_form="parmed.Structure")

    assert len(exported.residues) == 2
    assert [[atom.number for atom in group.atoms] for group in exported.residues] == [
        [101, 202, 303],
        [404],
    ]
    assert [atom.mass > 0 for atom in exported.atoms] == [True] * 4


def test_native_forcefield_types_remain_separate_from_elements(source):
    source.molecular_mechanics.atom_ff_type = [
        "n_force",
        "ca_force",
        "c_force",
        "o_force",
    ]
    exported = msm.convert(source, to_form="parmed.Structure")
    recovered = msm.convert(exported, to_form="molsysmt.MolSys")

    assert [atom.type for atom in exported.atoms] == [
        "n_force",
        "ca_force",
        "c_force",
        "o_force",
    ]
    assert recovered.topology.atoms["atom_type"].tolist() == ["N", "C", "C", "O"]
    assert recovered.molecular_mechanics.atom_ff_type.tolist() == [
        "n_force",
        "ca_force",
        "c_force",
        "o_force",
    ]


@pytest.mark.parametrize(
    "case, attribute",
    [
        ("distinct_orders", "fractional_bond_order"),
        ("nonaromatic_fractional", "bond_is_aromatic"),
        ("explicit_isotope", "isotope"),
    ],
)
def test_independent_native_semantics_do_not_collapse_into_one_provider_field(
    source, case, attribute
):
    if case == "explicit_isotope":
        source.topology.atoms["isotope"] = pd.array(
            [15, None, None, None], dtype="UInt16"
        )
    else:
        msm.set(source, element="bond", fractional_bond_order=[1.25, None])
        if case == "nonaromatic_fractional":
            msm.set(source, element="bond", bond_order=[None, 1])
            msm.set(source, element="bond", bond_is_aromatic=[False, False])
    report = msm.get_conversion_report(source, to_form="parmed.Structure")
    assert attribute in {issue.attribute for issue in report.issues}
    with pytest.raises(msm.NotCompatibleConversionError):
        msm.convert(source, to_form="parmed.Structure")


@pytest.mark.parametrize("association", [None, [0, 1]])
def test_multistate_structure_context_is_not_assigned_implicitly(source, association):
    _geometry(source, 2, False)
    source.chemical_states.append_state()
    if association is not None:
        msm.set(source, structure_chemical_state_index=association)
    report = msm.get_conversion_report(source, to_form="parmed.Structure")
    assert "structure_chemical_state_index" in {
        issue.attribute for issue in report.issues
    }
    with pytest.raises(msm.NotCompatibleConversionError):
        msm.convert(source, to_form="parmed.Structure")


@pytest.mark.parametrize("inventory_only", [False, True])
def test_empty_native_export_is_an_empty_parmed_structure(inventory_only):
    pytest.importorskip("parmed")
    source = MolSys()

    exported = msm.convert(
        source.topology if inventory_only else source, to_form="parmed.Structure"
    )

    assert len(exported.atoms) == len(exported.residues) == len(exported.bonds) == 0
    coordinates = exported.get_coordinates("all")
    assert coordinates is None or coordinates.size == 0
    assert exported.get_box("all") is None
