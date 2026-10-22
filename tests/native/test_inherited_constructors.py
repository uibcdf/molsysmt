"""Inherited native constructors retain their declared count contracts."""

import copy

import pytest
from argdigest.core.errors import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt.native import ChemicalStates, MolSys, Topology


class ExtendedStates(ChemicalStates):
    __slots__ = ("extra",)


class ExtendedTopology(Topology):
    __slots__ = ("extra",)


class ExtendedMolSys(MolSys):
    __slots__ = ("extra",)


class IndirectMolSys(ExtendedMolSys):
    pass


CLASSES = (ExtendedStates, ExtendedTopology, ExtendedMolSys, IndirectMolSys)
COUNTS = (
    "n_atoms",
    "n_groups",
    "n_components",
    "n_molecules",
    "n_entities",
    "n_chains",
    "n_bonds",
)


@pytest.mark.parametrize("cls", CLASSES)
@pytest.mark.parametrize("style", ["default", "positional", "keyword"])
def test_inherited_constructor_accepts_default_and_explicit_atom_counts(cls, style):
    if style == "default":
        result = cls()
        expected = 0
    elif style == "positional":
        result = cls(2)
        expected = 2
    else:
        result = cls(n_atoms=2)
        expected = 2
    domain = result.topology if isinstance(result, MolSys) else result
    assert type(result) is cls
    assert domain.n_atoms == expected
    states = (
        result.chemical_states
        if isinstance(result, MolSys)
        else (
            result._chemical_states_domain if isinstance(result, Topology) else result
        )
    )
    assert states.n_atoms == expected
    assert states.n_chemical_states == (0 if isinstance(result, ChemicalStates) else 1)
    if isinstance(result, MolSys):
        assert result.topology._molsys_owner_ref() is result
        assert result.chemical_states is result.topology._chemical_states_domain
        assert result.chemical_states._molsys_owner_ref() is result
        assert result.structures.n_structures == 0


@pytest.mark.parametrize("cls", [ExtendedTopology, ExtendedMolSys])
@pytest.mark.parametrize("count", COUNTS)
def test_every_inherited_hierarchy_count_uses_the_native_contract(cls, count):
    result = cls(**{count: 2})
    domain = result.topology if isinstance(result, MolSys) else result
    assert getattr(domain, count) == 2


@pytest.mark.parametrize("cls", CLASSES)
@pytest.mark.parametrize("value", [None, "2", 2.5, [2]])
def test_inherited_constructor_still_rejects_invalid_atom_counts(cls, value):
    with pytest.raises(ArgumentError) as refusal:
        cls(n_atoms=value)
    assert refusal.value.extra["argument"] == "n_atoms"


@pytest.mark.parametrize("cls", [ExtendedTopology, ExtendedMolSys])
@pytest.mark.parametrize("count", COUNTS)
def test_every_inherited_hierarchy_count_rejects_noninteger_values(cls, count):
    with pytest.raises(ArgumentError) as refusal:
        cls(**{count: 2.5})
    assert refusal.value.extra["argument"] == count


def test_chemical_state_boolean_count_remains_invalid():
    with pytest.raises(ArgumentError):
        ExtendedStates(n_atoms=True)


@pytest.mark.parametrize("cls", CLASSES)
def test_internal_context_is_not_an_admitted_public_argument(cls):
    with pytest.raises(UnknownArgumentError):
        cls(n_atoms=2, native_constructor="molsysmt.native.molsys.__init__")


@pytest.mark.parametrize("cls", CLASSES)
@pytest.mark.parametrize(
    "copier", [copy.copy, copy.deepcopy, lambda value: value.copy()]
)
def test_constructed_subclasses_copy_slots_cycles_and_mutable_data(cls, copier):
    source = cls(n_atoms=2)
    source.extra = {"owner": source, "values": [1]}
    duplicate = copier(source)
    assert type(duplicate) is cls
    assert duplicate.extra["owner"] is duplicate
    duplicate.extra["values"].append(2)
    assert source.extra["values"] == [1]


def test_count_queries_keep_boolean_semantics():
    source = MolSys(n_atoms=2)
    assert msm.get(source, n_atoms=True) == 2
    with pytest.raises(ArgumentError):
        msm.get(source, n_atoms=2)


@pytest.mark.parametrize("cls", [ExtendedTopology, ExtendedMolSys])
@pytest.mark.parametrize("count", COUNTS)
def test_existing_hierarchy_boolean_count_acceptance_is_unchanged(cls, count):
    result = cls(**{count: True})
    domain = result.topology if isinstance(result, MolSys) else result
    assert getattr(domain, count) == 1
