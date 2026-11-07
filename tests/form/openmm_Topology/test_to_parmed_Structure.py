"""Preserving represented OpenMM topology metadata at the ParmEd boundary."""

import numpy as np
import pytest

import molsysmt as msm


@pytest.mark.parametrize("selection", ["all", [2, 0]])
def test_openmm_to_parmed_retains_charges_serials_and_independent_bond_order(selection):
    pytest.importorskip("parmed")
    pytest.importorskip("openmm")
    from openmm import app, unit
    from parmed.topologyobjects import QualitativeBondType

    source = app.Topology()
    group = source.addResidue("LIG", source.addChain("Q"), id="17")
    atoms = [
        source.addAtom(name, element, group, id=serial, formalCharge=charge)
        for name, element, serial, charge in [
            ("N1", app.element.nitrogen, "101", 1),
            ("C2", app.element.carbon, "202", None),
            ("O3", app.element.oxygen, "303", -1),
        ]
    ]
    source.addBond(atoms[0], atoms[1], type=app.Aromatic, order=2)
    source.addBond(atoms[1], atoms[2], type=app.Single, order=1)
    source.setPeriodicBoxVectors(np.diag([2.0, 2.1, 2.2]) * unit.nanometer)
    before_atoms = [(atom.name, atom.id, atom.formalCharge) for atom in source.atoms()]
    before_bonds = [
        (bond.atom1.index, bond.atom2.index, bond.order, bond.type)
        for bond in source.bonds()
    ]
    before_box = source.getPeriodicBoxVectors().value_in_unit(unit.nanometer)

    exported = msm.convert(source, to_form="parmed.Structure", selection=selection)

    indices = [0, 1, 2] if selection == "all" else [0, 2]
    assert [atom.formal_charge for atom in exported.atoms] == [
        [1, None, -1][index] for index in indices
    ]
    assert [str(atom.number) for atom in exported.atoms] == [
        ["101", "202", "303"][index] for index in indices
    ]
    assert exported.residues[0].number == 17
    assert exported.residues[0].chain == "Q"
    assert exported.get_coordinates("all") is None
    np.testing.assert_allclose(exported.get_box("all")[:, :3], [[20, 21, 22]])
    np.testing.assert_allclose(exported.get_box("all")[:, 3:], 90, rtol=0, atol=3e-5)
    assert all(atom.mass > 0 for atom in exported.atoms)
    if selection == "all":
        assert [bond.order for bond in exported.bonds] == [2.0, 1.0]
        assert exported.bonds[0].qualitative_type == QualitativeBondType.AROMATIC
    else:
        assert len(exported.bonds) == 0
    assert [
        (atom.name, atom.id, atom.formalCharge) for atom in source.atoms()
    ] == before_atoms
    assert [
        (bond.atom1.index, bond.atom2.index, bond.order, bond.type)
        for bond in source.bonds()
    ] == before_bonds
    np.testing.assert_array_equal(
        source.getPeriodicBoxVectors().value_in_unit(unit.nanometer), before_box
    )


@pytest.mark.parametrize("route", ["public", "direct", "trusted"])
def test_openmm_unknown_numeric_bond_order_is_reported_and_rejected(route):
    pytest.importorskip("parmed")
    from openmm import app

    source = app.Topology()
    group = source.addResidue("LIG", source.addChain("A"), id="1")
    atoms = [
        source.addAtom("C", app.element.carbon, group, id=str(index + 1))
        for index in range(2)
    ]
    source.addBond(*atoms)
    report = msm.get_conversion_report(source, to_form="parmed.Structure")
    assert "bond_order" in {issue.attribute for issue in report.issues}
    with pytest.raises(msm.NotCompatibleConversionError, match="numeric bond order"):
        if route == "public":
            msm.convert(source, to_form="parmed.Structure")
        else:
            from molsysmt.form.openmm_Topology.to_parmed_Structure import (
                to_parmed_Structure,
            )

            to_parmed_Structure(source, skip_digestion=route == "trusted")


def test_openmm_duplicate_group_labels_remain_distinct():
    pytest.importorskip("parmed")
    from openmm import app

    source = app.Topology()
    chain = source.addChain("A")
    for index in range(2):
        group = source.addResidue("LIG", chain, id="7")
        source.addAtom("C", app.element.carbon, group, id=str(index + 1))
    exported = msm.convert(source, to_form="parmed.Structure")

    assert len(exported.residues) == 2
    assert [atom.residue.idx for atom in exported.atoms] == [0, 1]
