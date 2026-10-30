"""Inherited native constructors retain their declared count contracts."""

import copy

import numpy as np
import pytest
from argdigest.core.errors import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.argdigest import arg_digest
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
        else result
        if isinstance(result, ChemicalStates)
        else None
    )
    if states is None:
        assert not hasattr(result, "_chemical_states_domain")
    else:
        assert states.n_atoms == expected
        assert states.n_chemical_states == (
            0 if isinstance(result, ChemicalStates) else 1
        )
    if isinstance(result, MolSys):
        assert result.topology._molsys_owner_ref() is result
        assert result.chemical_states._molsys_owner_ref() is result
        assert result.chemical_states._molsys_owner_ref() is result
        assert result.structures.n_structures == 0


@pytest.mark.parametrize("cls", [ExtendedTopology, ExtendedMolSys])
@pytest.mark.parametrize("count", COUNTS)
def test_every_inherited_hierarchy_count_uses_the_native_contract(cls, count):
    if issubclass(cls, Topology) and count in {"n_components", "n_bonds"}:
        with pytest.raises(UnknownArgumentError):
            cls(**{count: 2})
        return
    result = cls(**{count: 2})
    domain = result.topology if isinstance(result, MolSys) else result
    assert (
        result.get(**{count: True})
        if count in {"n_components", "n_bonds"}
        else getattr(domain, count)
    ) == 2


@pytest.mark.parametrize("cls", CLASSES)
@pytest.mark.parametrize("value", [None, "2", 2.5, [2]])
def test_inherited_constructor_still_rejects_invalid_atom_counts(cls, value):
    with pytest.raises(ArgumentError) as refusal:
        cls(n_atoms=value)
    assert refusal.value.extra["argument"] == "n_atoms"


@pytest.mark.parametrize("cls", [ExtendedTopology, ExtendedMolSys])
@pytest.mark.parametrize("count", COUNTS)
def test_every_inherited_hierarchy_count_rejects_noninteger_values(cls, count):
    if issubclass(cls, Topology) and count in {"n_components", "n_bonds"}:
        with pytest.raises(UnknownArgumentError):
            cls(**{count: 2.5})
        return
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
    if issubclass(cls, Topology) and count in {"n_components", "n_bonds"}:
        with pytest.raises(UnknownArgumentError):
            cls(**{count: True})
        return
    result = cls(**{count: True})
    domain = result.topology if isinstance(result, MolSys) else result
    assert (
        result.get(**{count: True})
        if count in {"n_components", "n_bonds"}
        else getattr(domain, count)
    ) == 1


class _ExternalQueryMixin:
    def selected_atom_indices(self):
        return self.get(element="atom", selection=[1, 0], atom_indices=True)


class MixedMolSys(_ExternalQueryMixin, MolSys):
    pass


class OverriddenMolSys(MolSys):
    @arg_digest(native_constructor="molsysmt.native.molsys.__init__")
    def __init__(self, n_atoms=0, skip_digestion=False):
        super().__init__(n_atoms=n_atoms, skip_digestion=True)


@pytest.mark.parametrize("cls", [MixedMolSys, OverriddenMolSys])
def test_external_mixin_and_decorated_override_preserve_native_queries(cls):
    source = cls(n_atoms=2)
    assert source.topology.n_atoms == 2
    assert source.get(n_atoms=True) == 2
    np.testing.assert_array_equal(source.get(element="atom", atom_indices=True), [0, 1])
    np.testing.assert_array_equal(
        source.get(element="atom", selection=[1, 0], atom_index=True), [1, 0]
    )
    if isinstance(source, MixedMolSys):
        np.testing.assert_array_equal(source.selected_atom_indices(), [1, 0])
    with pytest.raises(ArgumentError):
        source.get(n_atoms=2)
    with pytest.raises(UnknownArgumentError):
        source.get(atom_indeces=True)


@pytest.mark.parametrize("cls", [MixedMolSys, OverriddenMolSys])
@pytest.mark.parametrize("value", [None, "2", 2.5, [2]])
def test_external_mixin_and_decorated_override_validate_before_construction(cls, value):
    with pytest.raises(ArgumentError) as refusal:
        cls(n_atoms=value)
    assert refusal.value.extra["argument"] == "n_atoms"


@pytest.mark.parametrize("cls", [MixedMolSys, OverriddenMolSys])
def test_external_mixin_and_decorated_override_refuse_unknown_keywords(cls):
    with pytest.raises(UnknownArgumentError):
        cls(n_atom=2)
