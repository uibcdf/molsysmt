"""Assess opt-in ownership without changing the production digestion policy."""

import inspect
from dataclasses import fields, replace

import numpy as np
import pytest
from argdigest import DigestConfig, UnknownArgumentError, arg_digest

import molsysmt as msm
from molsysmt import _argdigest as configuration
from molsysmt._private.smonitor import ArgumentError
from molsysmt.native import ChemicalStates, MolSys, Topology

pytestmark = pytest.mark.skipif(
    "contract_owner" not in {field.name for field in fields(DigestConfig)},
    reason="The optional ownership study requires ArgDigest >=0.17.0.",
)


def _config(owner):
    # Read the consumer configuration rather than introducing a second registry.
    options = {
        field.name: getattr(configuration, field.name.upper())
        for field in fields(DigestConfig)
        if hasattr(configuration, field.name.upper())
    }
    return replace(DigestConfig(**options), contract_owner=owner)


@pytest.mark.parametrize("base", [MolSys, Topology, ChemicalStates])
@pytest.mark.parametrize("policy", [None, "definition", "exact"])
def test_context_free_constructor_candidate_needs_an_explicit_owner(base, policy):
    original = inspect.unwrap(base.__init__)
    owner = f"{original.__module__}.__init__" if policy == "exact" else policy
    candidate = arg_digest(config=_config(owner))(original)
    child = type("Candidate", (base,), {"__init__": candidate})
    if policy is None:
        # Removing native_constructor alone revives the external-count refusal.
        with pytest.raises(ArgumentError):
            child(n_atoms=2)
        return
    assert child().get(n_atoms=True) == 0
    assert child(n_atoms=2).get(n_atoms=True) == 2
    with pytest.raises(ArgumentError):
        child(n_atoms=2.5)
    with pytest.raises(UnknownArgumentError) as refusal:
        child(n_atom=2)
    assert "Candidate.__init__" in str(refusal.value)


@pytest.mark.parametrize("policy", ["definition", "exact"])
def test_ownership_preserves_aliases_standardizer_domain_and_value_checks(policy):
    key = "molsysmt.basic.get.get"
    owner = key if policy == "exact" else policy
    seen = []

    def standardize(caller, arguments):
        seen.append((caller, dict(arguments)))
        return arguments

    config = replace(_config(owner), standardizer=standardize)
    query = arg_digest(config=config)(inspect.unwrap(msm.get))
    source = MolSys(n_atoms=2)
    result = query(source, element="atom", atom_indices=True)
    np.testing.assert_array_equal(result, [0, 1])
    assert seen[-1][0] == key
    assert seen[-1][1]["atom_index"] is True
    assert "atom_indices" not in seen[-1][1]
    assert query(source, n_atoms=True) == 2
    with pytest.raises(ArgumentError):
        query(source, n_atoms=2)
    with pytest.raises(UnknownArgumentError):
        query(source, atom_indeces=True)


@pytest.mark.parametrize("policy", ["definition", "exact"])
def test_separately_decorated_override_needs_its_own_logical_contract(policy):
    owner = "molsysmt.native.molsys.__init__" if policy == "exact" else policy

    class Override(MolSys):
        @arg_digest(config=_config(owner))
        def __init__(self, n_atoms=0, skip_digestion=False):
            super().__init__(n_atoms=n_atoms, skip_digestion=True)

    if policy == "definition":
        # Definition mode selects this test module, not the inherited base owner.
        with pytest.raises(ArgumentError):
            Override(n_atoms=2)
    else:
        assert Override(n_atoms=2).topology.n_atoms == 2
        with pytest.raises(ArgumentError):
            Override(n_atoms=2.5)


class _CountMixin:
    def get(self, n_atoms=True):
        return n_atoms


def test_mixin_runtime_and_definition_ownership_select_distinct_contracts():
    # An attribute-query mixin may deliberately select the assembled runtime
    # module's count semantics. A definition-owned method would change them.
    runtime = arg_digest(config=_config(None))(_CountMixin.get)
    assembled = type(
        "Assembled", (), {"__module__": "molsysmt.basic.get", "get": runtime}
    )
    assert assembled().get(n_atoms=True) is True
    with pytest.raises(ArgumentError):
        assembled().get(n_atoms=2)
    fixed = arg_digest(config=_config("definition"))(_CountMixin.get)
    with pytest.raises(ArgumentError):
        fixed(assembled(), n_atoms=True)
