"""Keep custom rule containers and exported defaults independent of role queries."""

import importlib
from copy import deepcopy

import numpy as np
import pytest

import molsysmt as msm


@pytest.mark.parametrize("role", ["donor", "acceptor"])
@pytest.mark.parametrize("container", [type(None), str, tuple, list])
@pytest.mark.parametrize(
    "include_defaults,exclude_defaults",
    [(False, False), (True, False), (False, True), (True, True)],
)
def test_repeated_role_calls_preserve_supplied_rules(
    role_system, role, container, include_defaults, exclude_defaults
):
    include = "atom_index==2"
    exclude = "atom_index==0"
    if container is type(None):
        include = exclude = None
    elif container is not str:
        include, exclude = container([include]), container([exclude])
    before = deepcopy((include, exclude))
    method = getattr(msm.interactions.hbonds, f"get_{role}_atoms")
    first = method(
        role_system,
        inclusion_rules=include,
        exclusion_rules=exclude,
        default_inclusion_rules=include_defaults,
        default_exclusion_rules=exclude_defaults,
    )
    second = method(
        role_system,
        inclusion_rules=include,
        exclusion_rules=exclude,
        default_inclusion_rules=include_defaults,
        default_exclusion_rules=exclude_defaults,
    )
    assert (include, exclude) == before
    np.testing.assert_array_equal(first, second)
    assert not np.shares_memory(first, second)
    if first.size:
        first[...] = -1
        assert np.all(second >= 0)


def test_rule_lists_can_be_shared_between_both_roles(role_system):
    include, exclude = ["atom_index==2"], ["atom_index==0"]
    for name, expected in [
        ("get_donor_atoms", [[2, 1], [6, 7], [8, 9]]),
        ("get_acceptor_atoms", [2, 4, 5, 10]),
        ("get_donor_atoms", [[2, 1], [6, 7], [8, 9]]),
    ]:
        actual = getattr(msm.interactions.hbonds, name)(
            role_system, inclusion_rules=include, exclusion_rules=exclude
        )
        np.testing.assert_array_equal(actual, expected)
        assert include == ["atom_index==2"]
        assert exclude == ["atom_index==0"]


@pytest.mark.parametrize("role", ["donor", "acceptor"])
def test_same_list_for_inclusion_and_exclusion_does_not_merge_default_roles(
    role_system, role
):
    shared = ["atom_index==4"]
    actual = getattr(msm.interactions.hbonds, f"get_{role}_atoms")(
        role_system, inclusion_rules=shared, exclusion_rules=shared
    )
    expected = [[0, 3], [2, 1], [6, 7], [8, 9]] if role == "donor" else [0, 2, 5, 10]
    np.testing.assert_array_equal(actual, expected)
    assert shared == ["atom_index==4"]


@pytest.mark.parametrize("role", ["donor", "acceptor"])
def test_exported_default_rules_are_not_modified_when_passed_as_input(
    role_system, role
):
    module = importlib.import_module(f"molsysmt.interactions.hbonds.get_{role}_atoms")
    include = getattr(module, f"{role}_inclusion_rules")
    exclude = getattr(module, f"{role}_exclusion_rules")
    saved_include, saved_exclude = include.copy(), exclude.copy()
    try:
        getattr(module, f"get_{role}_atoms")(
            role_system, inclusion_rules=include, exclusion_rules=exclude
        )
        assert include == saved_include
        assert exclude == saved_exclude
    finally:
        include[:] = saved_include
        exclude[:] = saved_exclude
