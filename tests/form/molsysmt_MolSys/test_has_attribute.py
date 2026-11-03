"""Testing composed instance-aware presence for native MolSys."""

import numpy as np

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.form import _dict_modules
from molsysmt.native import MolSys


def test_molsys_declares_the_complete_native_component_union():
    expected = {
        attribute
        for form in (
            "molsysmt.Topology",
            "molsysmt.ChemicalStates",
            "molsysmt.Structures",
            "molsysmt.MolecularMechanics",
        )
        for attribute, available in _dict_modules[form].attributes.items()
        if available
    }
    # Inner-edge queries require the composed selection context in MolSys.
    expected.update(
        {
            "structure_chemical_state_index",
            "inner_bond_index",
            "inner_bonded_atoms",
            "n_inner_bonds",
        }
    )
    observed = {
        attribute
        for attribute, available in _dict_modules["molsysmt.MolSys"].attributes.items()
        if available
    }

    assert observed == expected


def test_molsys_composes_topology_structures_and_mechanics_presence():
    molsys = MolSys(n_atoms=2)

    assert not msm.has_attribute(molsys, "formal_charge")
    assert not msm.has_attribute(molsys, "occupancy")
    assert not msm.has_attribute(molsys, "partial_charge")
    assert not msm.has_attribute(molsys, "structure_chemical_state_index")

    msm.set(molsys, element="atom", formal_charge=[0, 1])
    molsys.structures.coordinates = puw.quantity(np.zeros((1, 2, 3)), "nm")
    molsys.structures.occupancy = np.ones((1, 2))
    molsys.molecular_mechanics.partial_charge = [0.1, -0.1]

    assert msm.has_attribute(molsys, "formal_charge")
    assert msm.has_attribute(molsys, "occupancy")
    assert msm.has_attribute(molsys, "partial_charge")
    assert msm.has_attribute(molsys, "structure_chemical_state_index")


def test_non_bonded_method_presence_uses_mechanics_not_bond_name():
    molsys = MolSys(n_atoms=2)
    assert not msm.has_attribute(molsys, "non_bonded_method")
    assert msm.has_attribute(molsys, "non_bonded_method", include_none=True)
    molsys.molecular_mechanics.non_bonded_method = "NoCutoff"
    assert msm.has_attribute(molsys, "non_bonded_method")
    partial = MolSys._from_partial_domains(topology=molsys.topology.copy())
    partial.molecular_mechanics.non_bonded_method = "NoCutoff"
    assert partial.chemical_states is None
    assert msm.has_attribute(partial, "non_bonded_method")


def test_bond_relations_and_counts_are_chemical_catalogue_attributes():
    from molsysmt.attribute import attributes

    for name in (
        "bonded_atoms",
        "bonded_atom_pairs",
        "inner_bonded_atoms",
        "inner_bonded_atom_pairs",
        "inner_bond_index",
        "n_components",
        "n_bonds",
        "n_inner_bonds",
    ):
        assert attributes[name]["chemical_state"]
        assert not msm.has_attribute(
            MolSys(n_atoms=2).topology, name, include_none=True
        )
