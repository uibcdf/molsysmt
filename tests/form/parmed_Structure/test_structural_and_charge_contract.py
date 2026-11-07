"""Testing ParmEd frame, box, B-factor, and partial-charge delivery."""

import numpy as np
import pytest

parmed = pytest.importorskip("parmed")

import molsysmt as msm  # noqa: E402
from molsysmt import pyunitwizard as puw  # noqa: E402


def _two_frame_structure():
    structure = parmed.formats.mol2.Mol2File.parse(
        str(msm.systems["caffeine"]["caffeine.mol2"]), structure=True
    )
    first = np.asarray(structure.coordinates, dtype=np.float64)
    second = first + 10.0
    structure.coordinates = np.stack((first, second))
    structure.box = np.asarray(
        [[20.0, 21.0, 22.0, 90.0, 90.0, 90.0], [30.0, 31.0, 32.0, 90.0, 90.0, 90.0]],
        dtype=np.float64,
    )
    structure.atoms[0].bfactor = 12.5
    return structure, first, second


def test_parmed_delivers_selected_frames_atoms_boxes_and_b_factors():
    structure, first, second = _two_frame_structure()

    coordinates, box, b_factor = msm.get(
        structure,
        element="atom",
        selection=[2, 0],
        structure_indices=[1, 0],
        coordinates=True,
        box=True,
        b_factor=True,
    )

    np.testing.assert_allclose(
        puw.get_value(coordinates, to_unit="angstrom"),
        [[second[2], second[0]], [first[2], first[0]]],
    )
    np.testing.assert_allclose(
        puw.get_value(box, to_unit="angstrom")[:, [0, 1, 2], [0, 1, 2]],
        [[30.0, 31.0, 32.0], [20.0, 21.0, 22.0]],
    )
    np.testing.assert_allclose(
        puw.get_value(b_factor, to_unit="angstrom**2"),
        [[0.0, 12.5], [0.0, 12.5]],
    )


def test_parmed_partial_charge_is_mechanical_and_survives_native_conversion():
    structure, _, _ = _two_frame_structure()
    expected = np.asarray([atom.charge for atom in structure.atoms])

    observed = msm.get(structure, element="atom", partial_charge=True)
    np.testing.assert_allclose(
        puw.get_value(observed, to_unit="elementary_charge"), expected
    )
    native = msm.convert(structure, to_form="molsysmt.MolSys")
    np.testing.assert_allclose(
        np.asarray(native.molecular_mechanics.partial_charge, dtype=float),
        expected,
    )


def _charge_assignments():
    structure = parmed.Structure()
    for index, charge in enumerate([0.0, None, None]):
        structure.add_atom(
            parmed.Atom(
                name="C",
                type="ff-carbon",
                atomic_number=6,
                number=index + 1,
                charge=charge,
            ),
            "LIG",
            1,
            chain="A",
        )
    structure.atoms[1].atom_type = parmed.AtomType(
        "assigned-carbon", 1, 12.0, 6, charge=0.25
    )
    return structure


def test_partial_charge_query_distinguishes_zero_assigned_type_and_absence():
    source = _charge_assignments()

    assert msm.has_attribute(source, "partial_charge")
    known = msm.get(source, selection=[0, 1], partial_charge=True)
    np.testing.assert_array_equal(
        puw.get_value(known, to_unit="elementary_charge"), [0.0, 0.25]
    )
    assert msm.get(source, selection=[2], partial_charge=True) is None
    with pytest.raises(msm.NotWithThisFormError, match="unknown partial charges"):
        msm.get(source, partial_charge=True)
    assert [atom.charge for atom in source.atoms] == [0.0, 0.25, 0.0]


def test_nullable_charge_readback_and_forcefield_type_do_not_change_element():
    source = _charge_assignments()

    native = msm.convert(source, to_form="molsysmt.MolSys")

    values = native.molecular_mechanics.atoms_ff["partial_charge"]
    assert values.iloc[0] == 0.0 and values.iloc[1] == 0.25
    assert values.isna().tolist() == [False, False, True]
    assert native.topology.atoms["atom_type"].tolist() == ["C"] * 3
    assert native.molecular_mechanics.atom_ff_type.tolist() == ["ff-carbon"] * 3
    with pytest.raises(
        msm.NotCompatibleConversionError, match="missing source charges"
    ):
        msm.convert(native, to_form="parmed.Structure")


def test_unassigned_parmed_charges_do_not_create_a_native_zero_assignment():
    source = _charge_assignments()
    for atom in source.atoms:
        atom.charge = None
        atom.atom_type = parmed.topologyobjects.UnassignedAtomType

    assert not msm.has_attribute(source, "partial_charge")
    assert msm.get(source, partial_charge=True) is None
    native = msm.convert(source, to_form="molsysmt.MolSys")
    assert native.molecular_mechanics.partial_charge is None


def test_explicit_empty_chain_label_survives_ingestion_and_native_roundtrip():
    source = parmed.Structure()
    source.add_atom(
        parmed.Atom(name="C", atomic_number=6, number=7, charge=0.0),
        "LIG",
        1,
        chain="",
    )

    native = msm.convert(source, to_form="molsysmt.MolSys")

    assert native.topology.chains["chain_id"].tolist() == [""]
    assert native.topology.chains["chain_name"].tolist() == [""]
    exported = msm.convert(native, to_form="parmed.Structure")
    assert [group.chain for group in exported.residues] == [""]
    recovered = msm.convert(exported, to_form="molsysmt.MolSys")
    assert recovered.topology.chains["chain_id"].tolist() == [""]
    assert source.residues[0].chain == ""


@pytest.mark.parametrize("target", ["molsysmt.MolSys", "molsysmt.Structures"])
def test_box_only_provider_keeps_selected_structure_axis_without_coordinates(target):
    source, _, _ = _two_frame_structure()
    source.coordinates = None

    result = msm.convert(source, to_form=target, structure_indices=[1, 0, 1])
    structures = result.structures if target == "molsysmt.MolSys" else result

    assert structures.coordinates is None
    assert structures.n_structures == 3
    assert msm.get(source, n_structures=True) == 2
    np.testing.assert_allclose(
        puw.get_value(structures.box, to_unit="angstrom")[:, [0, 1, 2], [0, 1, 2]],
        [[30, 31, 32], [20, 21, 22], [30, 31, 32]],
    )
