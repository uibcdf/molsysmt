"""Keeping native elementary-charge values consumable during composition."""

import numpy as np

import molsysmt as msm
from tests.build.test_merge_nonpolar_hydrogens import declared_methanol


def test_native_charge_getter_returns_numeric_values_for_public_setters():
    source = declared_methanol()
    values = msm.get(source.molecular_mechanics, element="atom", partial_charge=True)
    assert values.dtype == np.dtype("float64")
    np.testing.assert_allclose(values, [-0.4, -0.5, 0.1, 0.2, 0.3, 0.3])
    output = source.copy()
    msm.set(output, partial_charge=values)
    np.testing.assert_allclose(msm.get(output, partial_charge=True), values)


def test_native_topology_structures_mechanics_compose_with_nondefault_charge_policy():
    source = declared_methanol()
    with msm.pyunitwizard.context(standard_units=["pm", "coulomb"]):
        result = msm.convert(
            [source.topology, source.structures, source.molecular_mechanics],
            to_form="molsysmt.MolSys",
        )
    np.testing.assert_allclose(
        msm.get(result, partial_charge=True), msm.get(source, partial_charge=True)
    )
    assert (
        result.molecular_mechanics.atom_ff_type.tolist()
        == source.molecular_mechanics.atom_ff_type.tolist()
    )
    assert result.chemical_states._states[0].connectivity_completeness == "complete"
