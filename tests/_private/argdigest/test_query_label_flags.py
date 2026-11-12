"""Reject label values in Boolean contexts without changing real label inputs."""

import importlib

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt.native import Topology

NAMES = [
    "atom_ff_type",
    "atom_name",
    "atom_type",
    "group_name",
    "group_type",
    "component_name",
    "component_type",
    "chain_name",
    "chain_type",
    "molecule_name",
    "molecule_type",
    "entity_name",
    "entity_type",
]


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("bad", ["CA", ["CA"], ("CA",), np.array(["CA"]), None, 7])
@pytest.mark.parametrize(
    "caller",
    [
        "molsysmt.basic.get.get",
        "molsysmt.basic.compare.compare",
        "molsysmt.basic.iterator.__init__",
    ],
)
def test_query_flag_digesters_reject_nonboolean_label_values(name, bad, caller):
    module = importlib.import_module("molsysmt._private.argdigest.argument." + name)
    with pytest.raises(ArgumentError):
        getattr(module, "digest_" + name)(bad, caller=caller)


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("flag", [False, True])
@pytest.mark.parametrize(
    "caller",
    [
        "molsysmt.basic.get.get",
        "molsysmt.basic.compare.compare",
        "molsysmt.basic.iterator.__init__",
    ],
)
def test_query_flag_digesters_keep_real_boolean_values(name, flag, caller):
    module = importlib.import_module("molsysmt._private.argdigest.argument." + name)
    assert getattr(module, "digest_" + name)(flag, caller=caller) is flag


@pytest.mark.parametrize("route", ["native", "get", "compare"])
def test_public_atom_name_queries_refuse_string_flags(route):
    topology = Topology(n_atoms=2)
    with pytest.raises(ArgumentError):
        if route == "native":
            topology.get(element="atom", atom_name="CA")
        elif route == "get":
            msm.get(topology, element="atom", atom_name="CA")
        else:
            msm.compare(topology, topology, atom_name="CA")


@pytest.mark.parametrize(
    "element,attribute,expected",
    [
        ("atom", "atom_type", ["N", "C", "O", "H"]),
        ("group", "group_type", ["amino acid", "water"]),
        ("molecule", "molecule_type", ["peptide", "water"]),
        ("entity", "entity_type", ["peptide", "water"]),
    ],
)
def test_public_type_flags_work_for_get_compare_and_inventory_iteration(
    element, attribute, expected
):
    from tests.native.test_topology_operations import build_minimal_topology

    topology = build_minimal_topology()
    assert msm.get(topology, element=element, **{attribute: True}) == expected
    assert msm.compare(topology, topology, **{attribute: True})
    chunks = list(
        msm.Iterator(
            topology,
            element=element,
            chunk=1,
            output_type="values",
            **{attribute: True},
        )
    )
    assert [value for chunk in chunks for value in chunk] == expected
