"""Analytic truth: integer charge balance and explicit periodic lattice images."""

from itertools import product

import numpy as np
import pytest

import molsysmt as msm


def system(waters, box, charge=None):
    """Construct declared neutral OHH waters, optionally with a charged solute."""
    builder = msm.MolSysBuilder()
    positions = []
    if charge is not None:
        atom = builder.add_atom(atom_name="C", atom_type="C")
        group = builder.add_group([atom], group_name="LIG", group_type="small molecule")
        builder.add_molecule(
            [group], molecule_name="solute", molecule_type="small molecule"
        )
        positions.append([1.5, 1.5, 1.5])
    for center in waters:
        atoms = [
            builder.add_atom(atom_name=name, atom_type=element)
            for name, element in [("O", "O"), ("H1", "H"), ("H2", "H")]
        ]
        group = builder.add_group(atoms, group_name="HOH", group_type="water")
        builder.add_molecule([group], molecule_name="water", molecule_type="water")
        builder.add_bond(atoms[0], atoms[1], bond_order=1)
        builder.add_bond(atoms[0], atoms[2], bond_order=1)
        positions.extend(
            np.asarray(center) + np.array([[0, 0, 0], [0.04, 0, 0], [0, 0.04, 0]])
        )
    builder.set_coordinates(
        msm.pyunitwizard.quantity(np.array(positions, dtype=float)[None, :, :], "nm")
    )
    output = builder.build()
    output.structures.box = msm.pyunitwizard.quantity(box[None, :, :], "nm")
    charges = np.zeros(output.topology.n_atoms, dtype=np.int16)
    if charge is not None:
        charges[0] = charge
    output.chemical_states._states[0].set_atom_attribute("formal_charge", charges)
    return output


@pytest.mark.parametrize("charge,positive,negative", [(0, 0, 0), (-2, 2, 0), (2, 0, 2)])
def test_neutralization_preserves_literal_charge_balance(charge, positive, negative):
    source = system(
        [[0.2, 0.2, 0.2], [1.5, 0.2, 0.2], [0.2, 1.5, 0.2], [0.2, 0.2, 1.5]],
        3 * np.eye(3),
        charge,
    )
    result = msm.build.add_ions(
        source,
        n_cations="neutralize",
        n_anions="neutralize",
        random_seed=5,
        return_report=True,
    )
    output = result["molecular_system"]
    assert result["report"]["added"]["cation"] == positive
    assert result["report"]["added"]["anion"] == negative
    assert output.chemical_states._states[0].atom_attributes["formal_charge"].sum() == 0
    assert (
        source.chemical_states._states[0].atom_attributes["formal_charge"].sum()
        == charge
    )
    assert msm.get(output, n_atoms=True) == 13 - 2 * (positive + negative)


def test_tilted_exclusion_against_explicit_lattice_images(float64_kernel_atol):
    box = np.array([[3.0, 0.0, 0.0], [1.0, 2.8, 0.0], [0.5, 0.3, 2.5]])
    fractional = np.array(
        [[0.02, 0.5, 0.5], [0.98, 0.5, 0.5], [0.5, 0.2, 0.2], [0.5, 0.8, 0.8]]
    )
    source = system(fractional @ box, box)
    result = msm.build.add_ions(
        source, n_cations=3, min_ion_distance="0.4 nm", random_seed=7
    )
    points = msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="nm")[
        0, -3:
    ]
    shifts = np.array(list(product(range(-2, 3), repeat=3))) @ box
    for i in range(3):
        for j in range(i):
            minimum = np.linalg.norm(points[i] - points[j] + shifts, axis=1).min()
            assert minimum > 0.4 - float64_kernel_atol
    assert msm.get(result, n_ions=True, n_waters=True) == [3, 1]
