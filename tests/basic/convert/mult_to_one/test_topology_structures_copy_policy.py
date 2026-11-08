"""Protect explicit two-domain copy requests and original full-axis admission."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys, Structures, Topology


def domains(owned):
    topology = Topology(n_atoms=4)
    topology.atoms.atom_name = ["A", "B", "C", "D"]
    structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.arange(36.0).reshape(3, 4, 3), "nm")
    )
    owner = None
    if owned:
        owner = MolSys._from_partial_domains(topology=topology, structures=structures)
    return topology, structures, owner


@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("owned", [False, True])
@pytest.mark.parametrize("copy_policy", ["default", False, True])
def test_explicit_copy_policy_keeps_native_domain_ownership(
    reverse, owned, copy_policy
):
    topology, structures, owner = domains(owned)
    inputs = [topology, structures][::-1] if reverse else [topology, structures]
    before = msm.pyunitwizard.get_value(structures.coordinates).copy()
    options = {} if copy_policy == "default" else dict(copy_if_all=copy_policy)
    result = msm.convert(inputs, **options)
    assert result.topology is not topology
    assert result.topology._molsys_owner_ref() is result
    if copy_policy is False and not owned:
        assert result.structures is structures
    else:
        assert result.structures is not structures
    assert result.structures._molsys_owner_ref() is result
    assert result.chemical_states is None  # Inventory cannot recreate chemical state.
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(structures.coordinates), before
    )
    result.topology.atoms.loc[0, "atom_name"] = "changed"
    assert topology.atoms.atom_name[0] == "A"
    if owned:
        assert topology._molsys_owner_ref() is owner
        assert structures._molsys_owner_ref() is owner
        assert owner.structures is structures and owner.topology is topology
    msm.set(result, coordinates=msm.pyunitwizard.quantity(before + 1, "nm"))
    expected = before + 1 if copy_policy is False and not owned else before
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(structures.coordinates), expected
    )


@pytest.mark.parametrize("copy_policy", ["default", False, True])
@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("selection", [[3, 0], [3, 1, 0, 2], []])
def test_subset_is_independent_even_when_full_axis_copy_is_disabled(
    reverse, copy_policy, selection
):
    topology, structures, _ = domains(False)
    inputs = [topology, structures][::-1] if reverse else [topology, structures]
    options = {} if copy_policy == "default" else dict(copy_if_all=copy_policy)
    result = msm.convert(
        inputs, selection=selection, structure_indices=[2, 0, 2], **options
    )
    selected = sorted(selection)
    assert result.topology.atoms.atom_name.tolist() == [
        "ABCD"[index] for index in selected
    ]
    assert result.structures is not structures
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(result.structures.coordinates),
        np.arange(36.0).reshape(3, 4, 3)[[2, 0, 2]][:, selected],
    )
    assert topology.n_atoms == structures.n_atoms == 4
    assert structures.n_structures == 3


@pytest.mark.parametrize("reverse", [False, True])
def test_atom_selection_cannot_hide_conflicting_original_domains(reverse):
    topology, structures, _ = domains(False)
    structures = structures.extract(atom_indices=[0, 1, 2])
    inputs = [topology, structures][::-1] if reverse else [structures, topology]
    with pytest.raises(StructuralInconsistencyError):
        msm.convert(inputs, selection=[0, 1])
    assert getattr(topology, "_molsys_owner_ref", None) is None
    assert getattr(structures, "_molsys_owner_ref", None) is None


@pytest.mark.parametrize("copy_policy", [None, 1, "false", np.bool_(False)])
def test_copy_policy_requires_a_plain_boolean(copy_policy):
    topology, structures, _ = domains(False)
    with pytest.raises(ArgumentError):
        msm.convert([topology, structures], copy_if_all=copy_policy)


def test_structural_observables_without_an_atom_axis_remain_composable():
    topology = Topology(n_atoms=4)
    structures = Structures(time=msm.pyunitwizard.quantity([0.0, 1.0], "ps"))
    result = msm.convert([topology, structures], copy_if_all=False)
    assert result.topology.n_atoms == 4 and result.structures.n_structures == 2
    assert result.structures.coordinates is None
