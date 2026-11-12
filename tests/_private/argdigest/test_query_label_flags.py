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
def test_query_flag_digesters_reject_nonboolean_label_values(name, bad):
    module = importlib.import_module("molsysmt._private.argdigest.argument." + name)
    with pytest.raises(ArgumentError):
        getattr(module, "digest_" + name)(bad, caller="molsysmt.basic.get.get")


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("flag", [False, True])
def test_query_flag_digesters_keep_real_boolean_values(name, flag):
    module = importlib.import_module("molsysmt._private.argdigest.argument." + name)
    assert (
        getattr(module, "digest_" + name)(flag, caller="molsysmt.basic.get.get") is flag
    )


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
