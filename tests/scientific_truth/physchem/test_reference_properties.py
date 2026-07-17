"""Published and externally constructed truth tests for physical properties."""

import numpy as np
import pytest

import molsysmt as msm


def _element_system():
    """Build two groups containing five explicitly typed elements."""

    builder = msm.MolSysBuilder()
    atoms = [
        builder.add_atom(atom_name=element, atom_type=element)
        for element in ("H", "C", "N", "O", "Cl")
    ]
    builder.add_group(atoms[:2], group_name="ALA")
    builder.add_group(atoms[2:], group_name="ASP")
    return builder.build()


def _values(quantity, unit):
    """Return numerical values expressed in one explicit reference unit."""

    return msm.pyunitwizard.get_value(quantity, to_unit=unit)


def test_physical_masses_match_standard_atomic_weights_and_aggregation(
    float64_kernel_atol,
):
    """Match transcribed standard weights at atom, group, and system levels."""

    system = _element_system()
    expected_atoms = np.array([1.008, 12.011, 14.007, 15.999, 35.45])

    observed_atoms = msm.physchem.get_mass(system, element="atom", definition="physical")
    observed_groups = msm.physchem.get_mass(system, element="group", definition="physical")
    observed_system = msm.physchem.get_mass(system, element="system", definition="physical")

    np.testing.assert_allclose(
        _values(observed_atoms, "Da"),
        expected_atoms,
        rtol=0.0,
        atol=float64_kernel_atol,
    )
    np.testing.assert_allclose(
        _values(observed_groups, "Da"),
        np.array([expected_atoms[:2].sum(), expected_atoms[2:].sum()]),
        rtol=0.0,
        atol=float64_kernel_atol,
    )
    np.testing.assert_allclose(
        _values(observed_system, "Da"),
        expected_atoms.sum(),
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_openmm_masses_preserve_explicit_particle_values(float64_kernel_atol):
    """Read arbitrary particle masses from an independently constructed System."""

    openmm = pytest.importorskip("openmm")
    system = openmm.System()
    expected = np.array([1.25, 7.5, 19.75])
    for mass in expected:
        system.addParticle(mass * openmm.unit.dalton)

    observed_atoms = msm.physchem.get_mass(system, element="atom", definition="OpenMM")
    observed_system = msm.physchem.get_mass(system, element="system", definition="OpenMM")

    np.testing.assert_allclose(
        _values(observed_atoms, "Da"), expected, rtol=0.0, atol=float64_kernel_atol
    )
    np.testing.assert_allclose(
        _values(observed_system, "Da"),
        expected.sum(),
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_elemental_vdw_radii_match_reference_values(float64_kernel_atol):
    """Match independently transcribed element-level van der Waals radii."""

    observed = msm.physchem.get_atomic_radius(_element_system(), definition="vdw")
    expected_nm = np.array([0.110, 0.170, 0.155, 0.152, 0.175])

    np.testing.assert_allclose(
        _values(observed, "nm"), expected_nm, rtol=0.0, atol=float64_kernel_atol
    )


def test_protor_radii_match_typed_alanine_heavy_atoms(float64_kernel_atol):
    """Match ProtOr radii for independently declared alanine atom types."""

    builder = msm.MolSysBuilder()
    atom_specs = (("N", "N"), ("CA", "C"), ("C", "C"), ("O", "O"), ("CB", "C"))
    atoms = [
        builder.add_atom(atom_name=atom_name, atom_type=element)
        for atom_name, element in atom_specs
    ]
    builder.add_group(atoms, group_name="ALA")
    for atom_1, atom_2 in ((atoms[0], atoms[1]), (atoms[1], atoms[2]), (atoms[2], atoms[3]), (atoms[1], atoms[4])):
        builder.add_bond(atom_1, atom_2)

    observed = msm.physchem.get_atomic_radius(builder.build(), definition="protor")
    expected_nm = np.array([0.164, 0.188, 0.161, 0.142, 0.188])

    np.testing.assert_allclose(
        _values(observed, "nm"), expected_nm, rtol=0.0, atol=float64_kernel_atol
    )


def test_ph7_group_charges_match_reference_ionization_states(float64_kernel_atol):
    """Assign the declared pH-7 scale and aggregate its signed group charges."""

    builder = msm.MolSysBuilder()
    groups = []
    for group_name in ("ARG", "ASP", "ALA"):
        atom = builder.add_atom(atom_name="CA", atom_type="C")
        groups.append(builder.add_group([atom], group_name=group_name))
    system = builder.build()

    observed_groups = msm.physchem.get_charge(
        system, element="group", definition="physical_pH7"
    )
    observed_system = msm.physchem.get_charge(
        system, element="system", definition="physical_pH7"
    )

    np.testing.assert_allclose(
        _values(observed_groups, "elementary_charge"),
        np.array([1.0, -1.0, 0.0]),
        rtol=0.0,
        atol=float64_kernel_atol,
    )
    np.testing.assert_allclose(
        _values(observed_system, "elementary_charge"),
        0.0,
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_collantes_indices_match_published_residue_values(float64_kernel_atol):
    """Match independently transcribed Collantes electronic charge indices."""

    builder = msm.MolSysBuilder()
    for group_name in ("ARG", "ASP", "ALA"):
        atom = builder.add_atom(atom_name="CA", atom_type="C")
        builder.add_group([atom], group_name=group_name)
    system = builder.build()

    observed_groups = msm.physchem.get_charge(
        system, element="group", definition="collantes"
    )
    observed_system = msm.physchem.get_charge(
        system, element="system", definition="collantes"
    )
    expected = np.array([1.69, 1.25, 0.05])

    np.testing.assert_allclose(
        _values(observed_groups, "elementary_charge"),
        expected,
        rtol=0.0,
        atol=float64_kernel_atol,
    )
    np.testing.assert_allclose(
        _values(observed_system, "elementary_charge"),
        expected.sum(),
        rtol=0.0,
        atol=float64_kernel_atol,
    )


def test_openmm_charges_preserve_explicit_nonbonded_parameters(float64_kernel_atol):
    """Read arbitrary charges from an independently constructed NonbondedForce."""

    openmm = pytest.importorskip("openmm")
    system = openmm.System()
    force = openmm.NonbondedForce()
    expected = np.array([0.25, -0.75, 0.125])
    for charge in expected:
        system.addParticle(1.0 * openmm.unit.dalton)
        force.addParticle(
            charge * openmm.unit.elementary_charge,
            0.3 * openmm.unit.nanometer,
            0.0 * openmm.unit.kilojoule_per_mole,
        )
    system.addForce(force)

    observed_atoms = msm.physchem.get_charge(system, element="atom", definition="OpenMM")
    observed_system = msm.physchem.get_charge(system, element="system", definition="OpenMM")

    np.testing.assert_allclose(
        _values(observed_atoms, "elementary_charge"),
        expected,
        rtol=0.0,
        atol=float64_kernel_atol,
    )
    np.testing.assert_allclose(
        _values(observed_system, "elementary_charge"),
        expected.sum(),
        rtol=0.0,
        atol=float64_kernel_atol,
    )
