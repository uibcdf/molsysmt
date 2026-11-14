"""Check native-domain ownership in the documented client copy probe."""

import weakref

import pytest

from devtools.scripts import qualify_topomt_native_copy as probe
from devtools.scripts.benchmark_native_copy import _fixture


@pytest.mark.parametrize("deep", [False, True])
def test_client_probe_accepts_independently_owned_native_domains(deep):
    source = _fixture(4, 7)
    system = source.copy()
    copied = system.copy(deep=deep)
    probe._check_domain_ownership(source, system, copied)
    assert copied.chemical_states is not system.chemical_states
    assert not hasattr(copied.topology, "_chemical_states_domain")


@pytest.mark.parametrize("domain", ["topology", "structures", "chemical_states"])
def test_client_probe_rejects_a_copied_domain_bound_to_another_owner(domain):
    source = _fixture(4, 7)
    system = source.copy()
    copied = system.copy(deep=False)
    object.__setattr__(
        getattr(copied, domain), "_molsys_owner_ref", weakref.ref(system)
    )
    with pytest.raises(AssertionError):
        probe._check_domain_ownership(source, system, copied)


def test_client_probe_rejects_shared_source_chemistry():
    source = _fixture(4, 7)
    system = source.copy()
    copied = system.copy(deep=False)
    object.__setattr__(copied, "_chemical_states_domain", system.chemical_states)
    with pytest.raises(AssertionError):
        probe._check_domain_ownership(source, system, copied)


def test_client_probe_rejects_retired_topology_chemical_storage():
    source = _fixture(4, 7)
    system = source.copy()
    copied = system.copy(deep=False)
    object.__setattr__(
        copied.topology, "_chemical_states_domain", copied.chemical_states
    )
    with pytest.raises(AssertionError):
        probe._check_domain_ownership(source, system, copied)
