"""Preserving explicit naming declarations without changing molecular chemistry."""

import copy
import pickle

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentError,
    ArgumentLengthError,
    StructuralInconsistencyError,
)
from molsysmt.native import MolSys, Topology


def topology_with_schemes(*, atoms=True):
    topology = Topology(
        n_atoms=4 if atoms else 0, n_groups=3, n_chains=1, n_molecules=1, n_entities=1
    )
    topology.groups["group_name"] = ["HIP", "CYX", "GLH"]
    topology.groups["group_id"] = ["a", "b", "c"]
    topology.groups["molecule_index"] = pd.array([0, 0, 0], dtype="Int64")
    topology.molecules["entity_index"] = pd.array([0], dtype="Int64")
    topology.chains["chain_id"] = ["A"]
    if atoms:
        topology.atoms["atom_id"] = ["10", "11", "12", "13"]
        topology.atoms["group_index"] = pd.array([2, 0, 2, 1], dtype="Int64")
        topology.atoms["chain_index"] = pd.array([0, 0, 0, 0], dtype="Int64")
    else:
        topology.set_chain_groups([[0, 1, 2]])
    topology.set_group_naming_schemes(["amber", None, "ccd"])
    return topology


def test_unknown_is_not_inferred_and_known_storage_costs_one_byte_per_group():
    topology = Topology(n_groups=100_000)
    assert topology._group_naming_codes is None
    topology.set_group_naming_schemes("amber")
    assert topology._group_naming_codes.dtype == np.dtype("uint8")
    assert topology._group_naming_codes.nbytes == 100_000
    assert not topology._group_naming_codes.flags.writeable
    topology.set_group_naming_schemes(None)
    assert topology._group_naming_codes is None


def test_partial_assignment_preserves_order_inputs_names_and_absent_domains():
    topology = topology_with_schemes()
    source = MolSys._from_partial_domains(topology=topology)
    names = topology.groups.copy(deep=True)
    schemes = np.array(["legacy", "amber"], dtype=object)
    indices = np.array([2, 1], dtype=np.int64)
    schemes.flags.writeable = indices.flags.writeable = False
    topology.set_group_naming_schemes(schemes, group_indices=indices)
    assert topology.group_naming_schemes == ("amber", "amber", "legacy")
    pd.testing.assert_frame_equal(names, topology.groups, check_frame_type=False)
    assert source.chemical_states is source.structures is None
    np.testing.assert_array_equal(schemes, ["legacy", "amber"])
    np.testing.assert_array_equal(indices, [2, 1])
    topology.set_group_naming_schemes(None, group_indices=1)
    assert topology.group_naming_schemes == ("amber", None, "legacy")


@pytest.mark.parametrize(
    "bad",
    [
        "AMBER",
        "unknown",
        "",
        1,
        False,
        ["amber", "ccd"],
        [None, "amber", 4],
        [["amber"]],
        np.ma.array(["amber"] * 3),
    ],
)
def test_invalid_scheme_assignment_is_atomic_and_diagnostic(bad):
    topology = topology_with_schemes()
    before = topology.group_naming_schemes
    with pytest.raises((ArgumentError, ArgumentLengthError)) as error:
        topology.set_group_naming_schemes(bad)
    assert error.value.extra["argument"] == "naming_schemes"
    assert error.value.extra["caller"].endswith(".set_group_naming_schemes")
    assert topology.group_naming_schemes == before


@pytest.mark.parametrize(
    "bad",
    [
        [0, 0],
        [-1],
        [3],
        [True],
        [0.0],
        [[0]],
        None,
        "group_id=='a'",
        np.ma.array([0]),
        [2**64],
    ],
)
def test_invalid_group_axis_is_atomic(bad):
    topology = topology_with_schemes()
    with pytest.raises(ArgumentError) as error:
        topology.set_group_naming_schemes("legacy", group_indices=bad)
    assert error.value.extra["argument"] == "group_indices"
    assert topology.group_naming_schemes == ("amber", None, "ccd")


def test_empty_axes_remain_unknown_and_invalid_scalar_still_rejects():
    topology = Topology()
    topology.set_group_naming_schemes([])
    assert topology.group_naming_schemes == ()
    with pytest.raises(ArgumentError):
        topology.set_group_naming_schemes("unreviewed")


@pytest.mark.parametrize(
    "copier",
    [
        copy.copy,
        copy.deepcopy,
        lambda item: item.copy(),
        lambda item: pickle.loads(pickle.dumps(item)),
    ],
)
def test_copy_and_pickle_declarations_are_independent(copier):
    source = topology_with_schemes()
    result = copier(source)
    result.set_group_naming_schemes("legacy", group_indices=0)
    assert source.group_naming_schemes == ("amber", None, "ccd")
    assert result.group_naming_schemes == ("legacy", None, "ccd")
    assert not np.shares_memory(source._group_naming_codes, result._group_naming_codes)


def test_older_pickle_state_without_declaration_retains_unknown_context():
    source = topology_with_schemes()
    state = source.__getstate__()
    state.pop("_group_naming_codes")
    restored = object.__new__(Topology)
    restored.__setstate__(state)
    assert restored.group_naming_schemes == (None, None, None)


def test_atom_subset_follows_actual_group_map_and_keeps_source():
    source = topology_with_schemes()
    result = source.extract(atom_indices=[0, 3])
    assert result.groups.group_name.tolist() == ["GLH", "CYX"]
    assert result.group_naming_schemes == ("ccd", None)
    assert source.group_naming_schemes == ("amber", None, "ccd")


def test_atom_free_reordering_and_deletion_preserve_each_group_context():
    source = topology_with_schemes(atoms=False)
    result = msm.extract(source, element="group", selection=[2, 0])
    assert result.groups.group_name.tolist() == ["GLH", "HIP"]
    assert result.group_naming_schemes == ("ccd", "amber")
    assert result.n_atoms == 0
    assert source.group_naming_schemes == ("amber", None, "ccd")


@pytest.mark.parametrize("known_left", [False, True])
def test_native_add_keeps_unknown_and_mixed_scheme_groups(known_left):
    known = topology_with_schemes(atoms=False)
    unknown = Topology(n_groups=2)
    left, right = (known, unknown) if known_left else (unknown, known)
    left.add(right)
    expected = (
        ("amber", None, "ccd", None, None)
        if known_left
        else (None, None, "amber", None, "ccd")
    )
    assert left.group_naming_schemes == expected


def test_atom_permutation_keeps_stable_group_axis_and_declarations():
    source = MolSys._from_partial_domains(topology=topology_with_schemes())
    result = msm.permute_atoms(source, [3, 0, 2, 1])
    assert result.topology.atoms.atom_id.tolist() == ["13", "10", "12", "11"]
    assert result.topology.group_naming_schemes == ("amber", None, "ccd")


def test_builder_appends_unknown_group_and_retains_source_declarations():
    source = MolSys._from_partial_domains(topology=topology_with_schemes(atoms=False))
    builder = msm.MolSysBuilder(source)
    builder.add_group([], group_name="LIG", group_type="small molecule")
    result = builder.build()
    assert result.topology.group_naming_schemes == ("amber", None, "ccd", None)
    assert source.topology.group_naming_schemes == ("amber", None, "ccd")
    assert result.chemical_states is None


def test_group_table_reset_clears_context_and_raw_axis_changes_reject():
    source = topology_with_schemes()
    source.groups.loc[3] = source.groups.iloc[0]
    with pytest.raises(StructuralInconsistencyError, match="aligned"):
        _ = source.group_naming_schemes
    with pytest.raises(StructuralInconsistencyError):
        source.set_group_naming_schemes("amber")
    source.reset_groups(2)
    assert source.group_naming_schemes == (None, None)


@pytest.mark.parametrize("failure", [False, True])
def test_attached_declaration_change_invalidates_atomically_without_geometry_copy(
    monkeypatch, failure
):
    from molsysmt.native import Structures

    topology = topology_with_schemes()
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=4,
        n_structures=2,
        evaluated_structure_indices=[0, 1],
        method="fixture",
    )
    source = MolSys._from_partial_domains(
        topology=topology,
        structures=Structures(
            coordinates=msm.pyunitwizard.quantity(np.zeros((2, 4, 3)), "nm")
        ),
        interactions={"empty": analysis},
    )
    geometry = source.structures._coordinates
    snapshot = source.interactions["empty"]
    source.topology.set_group_naming_schemes(["amber", None, "ccd"])
    assert source.interactions["empty"] is snapshot
    if failure:

        def refuse(*args, **kwargs):
            raise MemoryError("invalidation allocation refused")

        monkeypatch.setattr(source, "_invalidating_interaction_frames", refuse)
        with pytest.raises(MemoryError):
            source.topology.set_group_naming_schemes("legacy", group_indices=0)
        assert source.topology.group_naming_schemes == ("amber", None, "ccd")
        assert source.interactions["empty"] is snapshot
    else:
        source.topology.set_group_naming_schemes("legacy", group_indices=0)
        assert source.interactions["empty"].evaluated_structure_indices.tolist() == []
        assert snapshot.evaluated_structure_indices.tolist() == [0, 1]
    assert source.structures._coordinates is geometry


def test_builder_fallback_groups_start_unknown():
    source = MolSys._from_partial_domains(topology=topology_with_schemes())
    builder = msm.MolSysBuilder(source)
    builder.add_atom(atom_name="Ar", atom_type="Ar")
    result = builder.build()
    assert result.topology.group_naming_schemes == ("amber", None, "ccd", None)


def test_public_merge_preserves_mixed_atom_free_context():
    first = topology_with_schemes(atoms=False)
    second = Topology(n_groups=1)
    result = msm.merge([first, second])
    assert result.group_naming_schemes == ("amber", None, "ccd", None)
    assert first.group_naming_schemes == ("amber", None, "ccd")


def test_inserted_caps_start_unknown_and_existing_groups_keep_context():
    source = msm.build.build_peptide("AlaValPro", engine="MolSysMT")
    source.topology.set_group_naming_schemes(["amber", "legacy", "ccd"])
    result = msm.build.add_missing_terminal_cappings(
        source, N_terminal="ACE", C_terminal="NME", engine="MolSysMT"
    )
    assert result.topology.groups.group_name.tolist() == [
        "ACE",
        "ALA",
        "VAL",
        "PRO",
        "NME",
    ]
    assert result.topology.group_naming_schemes == (
        None,
        "amber",
        "legacy",
        "ccd",
        None,
    )


def test_trusted_scalar_assignment_keeps_broadcast_contract():
    source = Topology(n_groups=3)
    source.set_group_naming_schemes("amber", skip_digestion=True)
    assert source.group_naming_schemes == ("amber",) * 3


def test_appending_chemistry_requires_matching_naming_declarations():
    from molsysmt.native import Structures

    chemistry = msm.ChemicalStates(n_atoms=4)
    chemistry.append_state()
    first = MolSys._from_partial_domains(
        topology=topology_with_schemes(),
        chemical_states=chemistry,
        structures=Structures(
            coordinates=msm.pyunitwizard.quantity(np.zeros((1, 4, 3)), "nm")
        ),
    )
    second = first.copy()
    second.topology.set_group_naming_schemes("legacy", group_indices=0)
    with pytest.raises(StructuralInconsistencyError, match="inventory alignment"):
        first.append_structures(second)
    assert first.structures.n_structures == 1
    assert first.topology.group_naming_schemes == ("amber", None, "ccd")
