"""Round-trip optional native domains through the explicitly versioned schema."""

import json
import pickle

import numpy as np
import pytest

import molsysmt as msm
from tests.native import test_chemical_domain_separation as fixtures
from tests.native.test_chemical_state_edits import _analysis

states = fixtures.states
system = fixtures.system


def test_full_schema_preserves_states_associations_stable_membership_and_analysis(
    system,
):
    system.topology.reset_molecules(1)
    system.topology.set_atom_molecules([0, 0, 0])
    _analysis(system)
    wire = msm.convert(system, to_form="molsysmt.MolSysDict")
    assert wire.data["version"] == "0.2"
    assert "bonds" not in wire.data["topology"]
    restored = msm.convert(
        msm.MolSysDict(json.loads(json.dumps(wire.data, allow_nan=False))),
        to_form="molsysmt.MolSys",
    )
    assert restored.get(n_chemical_states=True) == 2
    assert restored.get(chemical_state=1, formal_charge=True) == [1, -1, 0]
    assert restored.get(structure_chemical_state_index=True) == [0, 1, 0, 1]
    assert restored.get(element="atom", molecule_index=True) == [0, 0, 0]
    assert restored.interactions["control"].evaluated_structure_indices.tolist() == [
        0,
        2,
    ]
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(restored.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(system.structures.coordinates, to_unit="nm"),
    )


@pytest.mark.parametrize(
    "mode", ["topology", "structures", "states", "zero_states", "interactions"]
)
def test_partial_domains_do_not_become_synthetic_chemistry(mode, states):
    from molsysmt.native import MolSys, Structures, Topology

    if mode == "topology":
        source = MolSys._from_partial_domains(topology=Topology(n_atoms=3))
    elif mode == "structures":
        source = MolSys._from_partial_domains(
            structures=Structures(
                coordinates=msm.pyunitwizard.quantity(np.zeros((2, 3, 3)), "angstrom")
            )
        )
    elif mode in {"states", "zero_states"}:
        source = MolSys._from_partial_domains(
            chemical_states=states
            if mode == "states"
            else msm.ChemicalStates(n_atoms=3)
        )
    else:
        analysis = msm.Interactions.from_records(
            [],
            n_atoms=3,
            n_structures=4,
            evaluated_structure_indices=[2],
            method="dictionary_fixture",
        )
        source = MolSys._from_partial_domains(interactions={"empty": analysis})
    wire = msm.convert(source, to_form="molsysmt.MolSysDict")
    restored = msm.convert(
        msm.MolSysDict(json.loads(json.dumps(wire.data, allow_nan=False))),
        to_form="molsysmt.MolSys",
    )
    assert (restored.topology is None) == (source.topology is None)
    assert (restored.structures is None) == (source.structures is None)
    assert (restored.chemical_states is None) == (source.chemical_states is None)
    if mode == "zero_states":
        assert restored.chemical_states.n_chemical_states == 0
    if mode == "interactions":
        assert restored.interactions["empty"].evaluated_structure_indices.tolist() == [
            2
        ]


def test_current_pickle_retains_independent_domains_and_owner_links(system):
    restored = pickle.loads(pickle.dumps(system))
    assert not hasattr(restored.topology, "bonds")
    assert restored.chemical_states._molsys_owner_ref() is restored
    assert restored.topology._molsys_owner_ref() is restored
    assert restored.get(chemical_state=1, formal_charge=True) == [1, -1, 0]


@pytest.mark.parametrize("entry", ["basic", "native"])
def test_explicit_dictionary_state_queries_preserve_reference(system, entry):
    payload = msm.convert(system, to_form="molsysmt.MolSysDict")
    query = (
        msm.convert(payload, to_form="molsysmt.MolSys").get
        if entry == "native"
        else lambda **kw: msm.get(payload, **kw)
    )
    assert query(chemical_state=1, formal_charge=True, n_bonds=True) == [[1, -1, 0], 1]
    assert query(
        chemical_state="structure", structure_indices=[3, 1], formal_charge=True
    ) == [1, -1, 0]
    assert query(formal_charge=True) == [0, 0, 0]


@pytest.mark.parametrize("damage", ["root", "row", "metadata", "nested_metadata"])
def test_schema_02_rejects_unsupported_fields_instead_of_dropping_them(system, damage):
    payload = msm.convert(system, to_form="molsysmt.MolSysDict")
    if damage == "root":
        payload.data["topology"]["bonds"] = [{"atom1_index": 0, "atom2_index": 1}]
    elif damage == "row":
        payload.data["topology"]["atoms"][0]["formal_charge"] = 7
    elif damage == "metadata":
        payload.data["metadata"]["important"] = "not represented"
    else:
        payload.data["topology"]["metadata"]["important"] = "not represented"
    with pytest.raises(ValueError, match="Unsupported|Invalid"):
        msm.convert(payload, to_form="molsysmt.MolSys")


@pytest.mark.parametrize("domain", ["system", "topology", "structures", "states"])
@pytest.mark.parametrize("extension", ["attribute", "slot"])
def test_dictionary_export_rejects_untyped_native_extensions(system, domain, extension):
    target = {
        "system": system,
        "topology": system.topology,
        "structures": system.structures,
        "states": system.chemical_states,
    }[domain]
    if extension == "slot":

        class Extended(type(target)):
            __slots__ = ("custom_payload",)

        replacement = object.__new__(Extended)
        replacement.__dict__.update(vars(target))
        if domain == "system":
            system = replacement
        elif domain == "topology":
            system._topology = replacement
        elif domain == "structures":
            system._structures = replacement
        else:
            system._chemical_states_domain = replacement
        target = replacement
    target.custom_payload = {"important": [1, 2]}
    from molsysmt.form._native_dict import encode_molsys

    with pytest.raises(ValueError, match="extension"):
        encode_molsys(system)
