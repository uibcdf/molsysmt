"""Receive chemical ring participants and detached provider aromatic flags."""

import inspect

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError
from molsysviewer.system_edits import SystemEditPendingError

import molsysmt as msm

puw = msm.pyunitwizard
NAMES = ("get_aromatic_rings", "get_aromaticity")
CAFFEINE_RINGS = {(1, 2, 3, 4, 5), (4, 5, 6, 8, 9, 11)}
CAFFEINE_AROMATIC = [1, 2, 3, 4, 5, 6, 8, 9, 11]


def caffeine_system(declared=True):
    # Explicit fixture preparation, before a view exists. Supply hierarchy and
    # optional declared flags; the bound readers never perform these edits.
    builder = msm.MolSysBuilder(msm.convert(msm.systems["caffeine"]["caffeine.sdf"]))
    group = builder.add_group(
        list(range(builder.n_atoms)), group_name="CAF", group_id="1"
    )
    builder.add_chain([group], chain_id="A")
    result = builder.build()
    if declared:
        molecule = msm.convert(result, to_form="rdkit.Mol")
        msm.set(
            result,
            element="atom",
            atom_is_aromatic=[a.GetIsAromatic() for a in molecule.GetAtoms()],
        )
        pairs = (
            result.chemical_states._resolve_chemical_state()
            .bonds[["atom1_index", "atom2_index"]]
            .to_numpy()
        )
        msm.set(
            result,
            element="bond",
            bond_is_aromatic=[
                molecule.GetBondBetweenAtoms(int(a), int(b)).GetIsAromatic()
                for a, b in pairs
            ],
        )
    xyz = puw.get_value(result.structures.coordinates, to_unit="nm").copy()
    result.structures.append(
        coordinates=puw.quantity(
            np.concatenate([xyz + [1, 0, 0], xyz + [0, 1, 0]]), "nm"
        ),
        structure_id=[70, 200],
    )
    return result


@pytest.fixture
def view():
    with msv.new_view(caffeine_system()) as result:
        result.interactions.attach(
            msm.Interactions.from_records(
                [],
                n_atoms=24,
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.aromatic",
            ),
            name="preserve",
            assume_aligned=True,
        )
        result.regions.add(selection=[0, 2, 4], tag="source")
        yield result


def memberships(result):
    return {
        tuple(result["atom_indices"][a:b])
        for a, b in zip(result["atom_offsets"][:-1], result["atom_offsets"][1:])
    }


def same(actual, expected):
    assert type(actual) is type(expected)
    np.testing.assert_equal(actual, expected)


@pytest.mark.parametrize("name", NAMES)
def test_native_signature_help_digestion_and_reserved_controls(view, name):
    method = getattr(view.addons.molsysmt.physchem, name)
    native = inspect.signature(getattr(msm.physchem, name))
    assert inspect.signature(method) == native.replace(
        parameters=list(native.parameters.values())[1:]
    )
    assert method.digestion_plan is not None
    assert not hasattr(view.addons.molsysmt, name)
    assert "update_view" not in inspect.signature(method).parameters
    doc = inspect.getdoc(method)
    assert "current view.molsys" in doc and "not a scene object" in doc
    assert "not geometry" in doc and "No aromatic flags" in doc
    assert "\nmolecular_system :" not in doc
    for args in [
        dict(molecular_system=view.molsys),
        dict(update_view=False),
        dict(prepare=True),
    ]:
        with pytest.raises(UnknownArgumentError):
            method(**args)
        with pytest.raises(TypeError):
            method(**args, skip_digestion=True)


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("structures", ["all", [2, 0, 2], [1]])
@pytest.mark.parametrize("skip", [False, True])
def test_reference_state_results_with_nonconsecutive_structures_and_skip(
    view, name, structures, skip
):
    args = dict(structure_indices=structures, skip_digestion=skip)
    actual = getattr(view.addons.molsysmt.physchem, name)(**args)
    same(actual, getattr(msm.physchem, name)(view.molsys, **args))
    assert actual["chemical_state_index"] == 0
    assert actual["atom_indices"].dtype == np.int64
    assert "coordinates" not in actual and "occurrences" not in actual


def test_caffeine_sparse_memberships_have_known_source_sets_and_not_traversals(view):
    result = view.addons.molsysmt.physchem.get_aromatic_rings()
    assert memberships(result) == CAFFEINE_RINGS
    assert result["atom_offsets"].tolist() == [0, 5, 11]
    assert result["atom_offsets"].dtype == np.int64
    assert (
        len(result["atom_indices"]) == 11
        and len(np.unique(result["atom_indices"])) == 9
    )
    assert result["source_atom_indices"].tolist() == list(range(24))
    assert result["examined_atom_indices"].tolist() == list(range(24))
    assert result["evidence"]["kind"] == "chemical_states.is_aromatic"
    assert result["max_cyclic_block_size"] == 256
    assert result["software"]["networkx"]
    for ring in memberships(result):
        assert list(ring) == sorted(ring)


def test_caffeine_perception_has_known_counts_and_explicit_attribution(view):
    result = view.addons.molsysmt.physchem.get_aromaticity()
    np.testing.assert_array_equal(
        result["atom_indices"][result["atom_is_aromatic"]], CAFFEINE_AROMATIC
    )
    assert (
        result["atom_is_aromatic"].dtype == result["bond_is_aromatic"].dtype == np.bool_
    )
    assert result["bond_is_aromatic"].sum() == 10
    assert result["evaluated_atom_indices"].tolist() == list(range(24))
    assert result["implementation"] == "rdkit.AROMATICITY_RDKIT"
    assert result["software"]["rdkit"]
    assert result["attribution"]["target"] == "molsysmt.physchem.get_aromaticity"
    assert result["references"][0]["id"] == "rdkit-aromaticity-model"


@pytest.mark.parametrize("selection", [[], [11, 1, 11, 4], "atom_type=='O'"])
def test_perception_filters_atom_flags_and_internal_bonds_after_full_graph(
    view, selection
):
    result = view.addons.molsysmt.physchem.get_aromaticity(selection=selection)
    expected = msm.physchem.get_aromaticity(view.molsys)
    indices = np.unique(
        np.asarray(msm.select(view.molsys, selection=selection), dtype=np.int64)
    )
    np.testing.assert_array_equal(result["atom_indices"], indices)
    np.testing.assert_array_equal(
        result["atom_is_aromatic"], expected["atom_is_aromatic"][indices]
    )
    internal = np.isin(expected["bonded_atom_pairs"], indices).all(axis=1)
    np.testing.assert_array_equal(
        result["bond_indices"], expected["bond_indices"][internal]
    )
    np.testing.assert_array_equal(
        result["bonded_atom_pairs"], expected["bonded_atom_pairs"][internal]
    )
    np.testing.assert_array_equal(
        result["bond_is_aromatic"], expected["bond_is_aromatic"][internal]
    )
    assert result["evaluated_atom_indices"].tolist() == list(range(24))
    if not len(indices):
        assert result["bonded_atom_pairs"].shape == (0, 2)


@pytest.mark.parametrize(
    "selection", [[], [0, 7, 10, 12, 13], CAFFEINE_AROMATIC[::-1] + [1]]
)
def test_ring_whole_membership_filtering_and_typed_empties(view, selection):
    result = view.addons.molsysmt.physchem.get_aromatic_rings(selection=selection)
    assert memberships(result) == (CAFFEINE_RINGS if 1 in selection else set())
    np.testing.assert_array_equal(
        result["selection_atom_indices"], np.unique(selection)
    )
    if not len(result["atom_indices"]):
        assert result["atom_indices"].dtype == np.int64 and result[
            "atom_offsets"
        ].tolist() == [0]


@pytest.mark.parametrize("selection", [[1], [1, 2, 3, 4, 5]])
def test_cutting_a_ring_or_its_fused_neighbor_is_not_silently_completed(
    view, selection
):
    args = dict(selection=selection)
    with pytest.raises(msm.ArgumentError) as expected:
        msm.physchem.get_aromatic_rings(view.molsys, **args)
    with pytest.raises(type(expected.value), match="cuts"):
        view.addons.molsysmt.physchem.get_aromatic_rings(**args)


def test_fusion_bond_flags_define_the_stored_basis_not_endpoint_aromaticity(view):
    state = view.molsys.chemical_states._states[0]
    pairs = state.bonds[["atom1_index", "atom2_index"]].to_numpy(dtype=np.int64)
    index = int(np.flatnonzero(np.all(np.sort(pairs, axis=1) == [4, 5], axis=1))[0])
    msm.set(view.molsys, element="bond", selection=[index], bond_is_aromatic=False)
    rings = view.addons.molsysmt.physchem.get_aromatic_rings()
    assert memberships(rings) == {tuple(CAFFEINE_AROMATIC)}
    assert state.bonds.loc[index, "is_aromatic"] == False  # noqa: E712
    # The declared-bond graph remains distinct from provider aromaticity.
    with pytest.raises(msm.StructuralInconsistencyError, match="conflicts"):
        view.addons.molsysmt.physchem.get_aromaticity()


def test_explicit_completeness_assumption_and_cyclic_block_guard(view):
    native = view.molsys.chemical_states._states[0]
    native.connectivity_completeness = "partial"
    with pytest.raises(msm.StructuralInconsistencyError):
        view.addons.molsysmt.physchem.get_aromatic_rings()
    rings = view.addons.molsysmt.physchem.get_aromatic_rings(
        assume_complete_connectivity=True, max_cyclic_block_size=9
    )
    assert memberships(rings) == CAFFEINE_RINGS
    assert rings["evidence"]["assume_complete_connectivity"] is True
    assert native.connectivity_completeness == "partial"
    args = dict(assume_complete_connectivity=True, max_cyclic_block_size=8)
    with pytest.raises(Exception) as expected:
        msm.physchem.get_aromatic_rings(view.molsys, **args)
    with pytest.raises(type(expected.value)):
        view.addons.molsysmt.physchem.get_aromatic_rings(**args)


@pytest.mark.parametrize(
    "name,args",
    [
        ("get_aromatic_rings", dict(method="guess")),
        ("get_aromatic_rings", dict(definition="geometry")),
        ("get_aromatic_rings", dict(max_cyclic_block_size=0)),
        ("get_aromaticity", dict(method="guess")),
        ("get_aromaticity", dict(structure_indices=[999])),
        ("get_aromaticity", dict(selection=[-1])),
    ],
)
@pytest.mark.parametrize("skip", [False, True])
def test_native_rejections_preserve_scientific_error_and_scene(view, name, args, skip):
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    parameters = dict(args, skip_digestion=skip)
    with pytest.raises(Exception) as expected:
        getattr(msm.physchem, name)(view.molsys, **parameters)
    with pytest.raises(type(expected.value)):
        getattr(view.addons.molsysmt.physchem, name)(**parameters)
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )


def test_perception_does_not_attach_flags_or_prepare_ring_input():
    with msv.new_view(caffeine_system(declared=False)) as result:
        attrs = result.molsys.chemical_states._states[0].atom_attributes.copy(deep=True)
        flags = result.addons.molsysmt.physchem.get_aromaticity()
        assert flags["atom_is_aromatic"].sum() == 9
        pd.testing.assert_frame_equal(
            result.molsys.chemical_states._states[0].atom_attributes, attrs
        )
        with pytest.raises(msm.StructuralInconsistencyError):
            result.addons.molsysmt.physchem.get_aromatic_rings()


@pytest.mark.parametrize("name", NAMES)
def test_full_graph_validation_precedes_empty_output_selection(view, name):
    native = view.molsys.chemical_states._states[0]
    if name == "get_aromatic_rings":
        native.atom_attributes.loc[0, "is_aromatic"] = pd.NA
    else:
        native.atom_attributes.loc[0, "formal_charge"] = pd.NA
    with pytest.raises(msm.StructuralInconsistencyError):
        getattr(view.addons.molsysmt.physchem, name)(selection=[])


@pytest.mark.parametrize("name", NAMES)
def test_explicit_structure_state_resolution_and_mixed_state_rejection(view, name):
    primary = view.molsys
    second = primary.chemical_states._states[0].copy()
    second.state_id = "alternate"
    primary.chemical_states._append_state(second)
    msm.set(primary, structure_chemical_state_index=[0, 1, 0])
    method = getattr(view.addons.molsysmt.physchem, name)
    assert (
        method(chemical_state="structure", structure_indices=[2, 0, 2])[
            "chemical_state_index"
        ]
        == 0
    )
    actual = method(chemical_state="structure", structure_indices=[1])
    assert actual["chemical_state_index"] == 1
    if name == "get_aromaticity":
        assert actual["chemical_state_id"] == "alternate"
    with pytest.raises(Exception) as expected:
        getattr(msm.physchem, name)(
            primary, chemical_state="structure", structure_indices=[0, 1]
        )
    with pytest.raises(type(expected.value)):
        method(chemical_state="structure", structure_indices=[0, 1])
    assert primary.chemical_states.reference_chemical_state_index == 0


@pytest.mark.parametrize("name", NAMES)
def test_detached_results_preserve_all_primary_domains_scene_and_coverage(view, name):
    primary = view.molsys
    owners = (
        primary.topology,
        primary.structures,
        primary.chemical_states,
        primary.interactions["preserve"],
    )
    chemistry = msm.convert(
        primary.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    ).to_dict()
    xyz = puw.get_value(primary.structures.coordinates).copy()
    state, status, coverage = (
        view.export_state(),
        view.addons.molsysmt.get_sync_status(),
        owners[3].to_dict(),
    )
    actual = getattr(view.addons.molsysmt.physchem, name)()
    expected = getattr(msm.physchem, name)(primary)
    same(actual, expected)
    actual["atom_indices"][:] = -1
    if name == "get_aromaticity":
        actual["atom_is_aromatic"][:] = False
        actual["bonded_atom_pairs"][:] = -1
        actual["attribution"]["items"].clear()
    else:
        actual["atom_offsets"][:] = 0
        actual["evidence"]["kind"] = "modified-detached-result"
    same(getattr(view.addons.molsysmt.physchem, name)(), expected)
    assert view.molsys is primary
    assert all(
        a is b
        for a, b in zip(
            owners,
            (
                primary.topology,
                primary.structures,
                primary.chemical_states,
                primary.interactions["preserve"],
            ),
        )
    )
    np.testing.assert_equal(
        msm.convert(
            primary.chemical_states, to_form="molsysmt.ChemicalStatesDict"
        ).to_dict(),
        chemistry,
    )
    np.testing.assert_array_equal(puw.get_value(primary.structures.coordinates), xyz)
    np.testing.assert_equal(owners[3].to_dict(), coverage)
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )


@pytest.mark.parametrize("name", NAMES)
def test_reads_current_pending_primary_without_sync(view, name):
    tools = view.addons.molsysmt
    tools.structure.translate(
        translation=puw.quantity([1, 0, 0], "nm"), in_place=True, update_view=False
    )
    status = tools.get_sync_status()
    assert status["state"] == "pending"
    args = dict(structure_indices=[2, 0])
    same(
        getattr(tools.physchem, name)(**args),
        getattr(msm.physchem, name)(view.molsys, **args),
    )
    assert tools.get_sync_status() == status
    with pytest.raises(SystemEditPendingError):
        view.export_state()


@pytest.mark.parametrize("name", NAMES)
def test_facade_follows_replacement_and_preserves_lifetime_guards(view, name):
    method = getattr(view.addons.molsysmt.physchem, name)
    with msv.demo["dialanine"] as replacement:
        view.load(replacement.molsys, mode="replace")
        with pytest.raises(Exception) as expected:
            getattr(msm.physchem, name)(view.molsys)
        with pytest.raises(type(expected.value)):
            method()
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt.physchem, name)()
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method()


@pytest.mark.parametrize("selection", ["all", [5, 6]])
def test_perceived_nonaromatic_bridge_between_aromatic_atoms_is_preserved(selection):
    from rdkit import Chem
    from rdkit.Chem import rdDepictor

    # Explicit biphenyl graph: two six-member aromatic rings joined by one
    # nonaromatic bond. Coordinates only make a viewable fixture, not evidence.
    molecule = Chem.MolFromSmiles("c1ccccc1-c2ccccc2")
    rdDepictor.Compute2DCoords(molecule)
    builder = msm.MolSysBuilder(msm.convert(molecule))
    group = builder.add_group(list(range(builder.n_atoms)), group_name="BPH")
    builder.add_chain([group], chain_id="A")
    with msv.new_view(builder.build()) as result:
        flags = result.addons.molsysmt.physchem.get_aromaticity(selection=selection)
        assert flags["atom_is_aromatic"].all()
        if isinstance(selection, str):
            assert len(flags["atom_indices"]) == 12
            assert flags["bond_is_aromatic"].sum() == 12
        else:
            assert flags["atom_indices"].tolist() == [5, 6]
        pairs = np.sort(flags["bonded_atom_pairs"], axis=1)
        bridge = np.flatnonzero(np.all(pairs == [5, 6], axis=1))
        assert len(bridge) == 1 and not flags["bond_is_aromatic"][bridge[0]]
        same(flags, msm.physchem.get_aromaticity(result.molsys, selection=selection))


ROUTES = [
    "physchem.get_aromatic_rings",
    "physchem.get_aromaticity",
    "chemical_states.get_rings",
]


def readers(view, route):
    module, name = route.split(".")
    return getattr(getattr(view.addons.molsysmt, module), name), getattr(
        getattr(msm, module), name
    )


@pytest.mark.parametrize("route", ROUTES)
@pytest.mark.parametrize("query", ["all and all", "name ZZZX"])
@pytest.mark.parametrize("skip", [False, True])
def test_received_reference_syntax_matches_direct_numeric_population(
    view, route, query, skip
):
    bound, native = readers(view, route)
    indices = msm.select(view.molsys, selection=query, syntax="MDTraj")
    args = dict(structure_indices=[2, 0, 2], skip_digestion=skip)
    actual = bound(selection=query, syntax="MDTraj", **args)
    same(actual, native(view.molsys, selection=indices, **args))
    key = (
        "atom_indices"
        if route.endswith("get_aromaticity")
        else "selection_atom_indices"
    )
    np.testing.assert_array_equal(actual[key], indices)
    assert actual[key].dtype == np.int64


@pytest.mark.parametrize("route", ROUTES)
@pytest.mark.parametrize("indices", [[999], [-1], [70], [0, 999]])
@pytest.mark.parametrize("skip", [False, True])
def test_received_frame_validation_rejects_invalid_positions_including_structure_ids(
    view, route, indices, skip
):
    bound, native = readers(view, route)
    args = dict(structure_indices=indices, skip_digestion=skip)
    with pytest.raises(msm.ArgumentError) as expected:
        native(view.molsys, **args)
    with pytest.raises(type(expected.value)):
        bound(**args)


@pytest.mark.parametrize("route", ROUTES)
@pytest.mark.parametrize("state", [0, "structure"])
def test_reference_syntax_repair_preserves_explicit_state_restriction(
    view, route, state
):
    bound, native = readers(view, route)
    args = dict(
        selection="all and all",
        syntax="MDTraj",
        chemical_state=state,
        structure_indices=[0],
    )
    with pytest.raises(msm.ArgumentError) as expected:
        native(view.molsys, **args)
    with pytest.raises(type(expected.value)):
        bound(**args)
    assert view.molsys.chemical_states.reference_chemical_state_index == 0
