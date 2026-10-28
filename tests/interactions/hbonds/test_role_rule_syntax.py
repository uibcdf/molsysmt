"""Keep built-in role chemistry native while honoring the user's query language."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError


@pytest.mark.parametrize("role", ["donor", "acceptor"])
@pytest.mark.parametrize(
    "include_defaults,exclude_defaults",
    [(False, False), (True, False), (False, True), (True, True)],
)
@pytest.mark.parametrize("external_mask", ["index 0 2 4 6 8 10", [0, 2, 4, 6, 8, 10]])
def test_custom_and_default_rules_keep_their_own_languages(
    role_system, role, include_defaults, exclude_defaults, external_mask
):
    pytest.importorskip("mdtraj")
    method = getattr(msm.interactions.hbonds, f"get_{role}_atoms")
    args = dict(
        default_inclusion_rules=include_defaults,
        default_exclusion_rules=exclude_defaults,
    )
    native = method(
        role_system,
        selection=[0, 2, 4, 6, 8, 10],
        inclusion_rules="atom_index==2",
        exclusion_rules="atom_index==0",
        **args,
    )
    external = method(
        role_system,
        selection=external_mask,
        inclusion_rules="index 2",
        exclusion_rules="index 0",
        syntax="MDTraj",
        **args,
    )
    if role == "donor":
        expected = [[2, 1], [6, 7], [8, 9]] if include_defaults else [[2, 1]]
    elif not include_defaults:
        expected = [2]
    else:
        expected = [2, 4, 10] if exclude_defaults else [2, 4, 6, 8, 10]
    np.testing.assert_array_equal(native, expected)
    np.testing.assert_array_equal(external, expected)


@pytest.mark.parametrize("role", ["donor", "acceptor"])
def test_pure_default_rules_accept_external_selection(role_system, role):
    pytest.importorskip("mdtraj")
    actual = getattr(msm.interactions.hbonds, f"get_{role}_atoms")(
        role_system, selection="index 0 2 4 6 8 10", syntax="MDTraj"
    )
    expected = [[0, 3], [2, 1], [6, 7], [8, 9]] if role == "donor" else [0, 2, 4, 10]
    np.testing.assert_array_equal(actual, expected)


@pytest.mark.parametrize("role", ["donor", "acceptor"])
@pytest.mark.parametrize("selection", [[], "index 11"])
def test_no_roles_preserve_typed_empty_result(role_system, role, selection):
    pytest.importorskip("mdtraj")
    result = getattr(msm.interactions.hbonds, f"get_{role}_atoms")(
        role_system, selection=selection, syntax="MDTraj"
    )
    assert result.shape == ((0, 2) if role == "donor" else (0,))
    assert result.dtype == np.dtype(np.int64)


def test_custom_hydrogen_free_donor_keeps_native_pair_scope(role_system):
    pytest.importorskip("mdtraj")
    result = msm.interactions.hbonds.get_donor_atoms(
        role_system,
        selection="index 4",
        inclusion_rules="element O",
        default_inclusion_rules=False,
        default_exclusion_rules=False,
        syntax="MDTraj",
    )
    assert result.shape == (0, 2)
    assert result.dtype == np.dtype(np.int64)


@pytest.mark.parametrize("role", ["donor", "acceptor"])
@pytest.mark.parametrize(
    "arguments",
    [
        {"syntax": "unknown-syntax"},
        {"syntax": "MolSysMT", "inclusion_rules": "atom_type==="},
        {"syntax": "MDTraj", "inclusion_rules": "atom_type=='N'"},
        {"syntax": "MDTraj", "exclusion_rules": "not a valid query"},
    ],
)
def test_bad_syntax_or_rule_is_not_silently_translated(role_system, role, arguments):
    if arguments["syntax"] == "MDTraj":
        pytest.importorskip("mdtraj")
    with pytest.raises(ArgumentError):
        getattr(msm.interactions.hbonds, f"get_{role}_atoms")(role_system, **arguments)


@pytest.mark.parametrize("role", ["donor", "acceptor"])
@pytest.mark.parametrize("form", ["molsysmt.Topology", "file:h5msm"])
def test_external_rules_work_with_other_supported_chemical_sources(
    role_system, role, form, tmp_path
):
    pytest.importorskip("mdtraj")
    target = str(tmp_path / "roles.h5msm") if form == "file:h5msm" else form
    source = msm.convert(role_system, to_form=target)
    actual = getattr(msm.interactions.hbonds, f"get_{role}_atoms")(
        source, selection="index 2", syntax="MDTraj"
    )
    np.testing.assert_array_equal(actual, [[2, 1]] if role == "donor" else [2])
