"""Testing the complete topology-and-structures contract of MolSysBuilder."""

import numpy as np

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.form import _dict_modules


def _declared_attributes(form):
    return {
        attribute
        for attribute, available in _dict_modules[form].attributes.items()
        if available
    }


def test_builder_declares_exactly_its_two_stored_native_components():
    expected = _declared_attributes("molsysmt.Topology") | _declared_attributes(
        "molsysmt.Structures"
    )
    observed = _declared_attributes("molsysmt.MolSysBuilder")

    assert len(expected) == 96
    assert observed == expected
    assert "partial_charge" not in observed
    assert "structure_chemical_state_index" not in observed


def test_every_declared_builder_attribute_has_a_direct_getter():
    module = _dict_modules["molsysmt.MolSysBuilder"]

    for attribute in _declared_attributes("molsysmt.MolSysBuilder"):
        prefix = f"get_{attribute}_"
        assert any(
            name.startswith(prefix) and callable(getattr(module, name))
            for name in vars(module)
        ), attribute


def test_builder_composes_native_instance_presence(molsys_builder_complete):
    builder = molsys_builder_complete

    assert not msm.has_attribute(builder, "formal_charge")
    assert not msm.has_attribute(builder, "velocities")
    assert not msm.has_attribute(builder, "temperature")
    assert msm.has_attribute(builder, "formal_charge", include_none=True)
    assert msm.has_attribute(builder, "velocities", include_none=True)

    builder.topology._set_chemical_state_atom_attribute(
        "formal_charge",
        [0, 1, 0],
    )
    builder.structures.velocities = puw.quantity(
        np.ones((1, 3, 3)),
        "nm/ps",
    )
    builder.structures.temperature = puw.quantity([300.0], "K")

    assert msm.has_attribute(builder, "formal_charge")
    assert msm.has_attribute(builder, "velocities")
    assert msm.has_attribute(builder, "temperature")


def test_get_reads_rich_builder_state_without_materializing_molsys(
    molsys_builder_complete,
):
    builder = molsys_builder_complete

    def fail_if_materialized(*args, **kwargs):
        raise AssertionError("Direct builder getters must not call build().")

    builder.build = fail_if_materialized
    builder.topology._set_chemical_state_atom_attribute(
        "formal_charge",
        [0, 1, 0],
    )
    builder.topology._set_component_indices([0, 0, 1])
    builder.topology.reset_components(n_components=2)
    builder.structures.velocities = puw.quantity(
        np.ones((1, 3, 3)),
        "nm/ps",
    )
    builder.structures.occupancy = np.array([[1.0, 0.5, 1.0]])
    builder.structures.temperature = puw.quantity([300.0], "K")
    builder.structures.potential_energy = puw.quantity([-2.0], "kJ/mol")
    builder.structures.kinetic_energy = puw.quantity([1.0], "kJ/mol")

    assert msm.get(builder, formal_charge=True) == [0, 1, 0]
    assert msm.get(builder, element="atom", component_index=True) == [0, 0, 1]
    assert msm.get(builder, element="bond", bond_order=True) == [None]
    assert msm.get(builder, structure_index=True) == [0]
    assert np.allclose(msm.get(builder, occupancy=True), [[1.0, 0.5, 1.0]])
    assert np.allclose(
        puw.get_value(msm.get(builder, velocities=True), to_unit="nm/ps"),
        np.ones((1, 3, 3)),
    )
    assert np.allclose(
        puw.get_value(msm.get(builder, temperature=True), to_unit="K"),
        [300.0],
    )
    assert np.allclose(
        puw.get_value(msm.get(builder, total_energy=True), to_unit="kJ/mol"),
        [-1.0],
    )
