"""Receive native chemical features without preparation or scene projection."""

import inspect

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError
from molsysviewer.system_edits import SystemEditPendingError
from rdkit import Chem
from rdkit.Chem import rdDepictor

import molsysmt as msm
from molsysmt._private.smonitor import UnsupportedHeavyOperationError

puw = msm.pyunitwizard
SMILES = {
    "get_charge_centers": "CC(=O)[O-].[Na+]",
    "get_hydrophobic_sites": "CCC.CSC.CF.CC.C[NH3+]",
    "get_halogen_bond_sites": "CCl.C=O.CF.[Cl-].N#C",
}
NAMES = tuple(SMILES)


def feature_system(smiles):
    # Declared graph and deterministic viewable coordinates precede the view.
    # Neither the adapter nor the scientific readers perform this preparation.
    molecule = Chem.MolFromSmiles(smiles)
    rdDepictor.Compute2DCoords(molecule)
    builder = msm.MolSysBuilder(msm.convert(molecule))
    group = builder.add_group(list(range(builder.n_atoms)), group_name="LIG")
    builder.add_chain([group], chain_id="A")
    result = builder.build()
    xyz = puw.get_value(result.structures.coordinates, to_unit="nm").copy()
    result.structures.append(
        coordinates=puw.quantity(
            np.concatenate([xyz + [1, 0, 0], xyz + [0, 1, 0]]), "nm"
        ),
        structure_id=[70, 200],
    )
    return result


@pytest.fixture(params=NAMES)
def feature_view(request):
    with msv.new_view(feature_system(SMILES[request.param])) as view:
        n_atoms = msm.get(view.molsys, n_atoms=True)
        view.interactions.attach(
            msm.Interactions.from_records(
                [],
                n_atoms=n_atoms,
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.chemical_features",
            ),
            name="preserve",
            assume_aligned=True,
        )
        view.regions.add(selection=[0], tag="source")
        yield view, request.param


def same(actual, expected):
    if isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for key in expected:
            same(actual[key], expected[key])
    elif puw.is_quantity(expected):
        assert puw.get_unit(actual) == puw.get_unit(expected)
        np.testing.assert_array_equal(puw.get_value(actual), puw.get_value(expected))
    elif isinstance(expected, (list, tuple)):
        assert type(actual) is type(expected) and len(actual) == len(expected)
        for a, e in zip(actual, expected):
            same(a, e)
    else:
        np.testing.assert_equal(actual, expected)


def test_explicit_native_signatures_help_and_reserved_primary(feature_view):
    view, name = feature_view
    method = getattr(view.addons.molsysmt.physchem, name)
    native = inspect.signature(getattr(msm.physchem, name))
    assert inspect.signature(method) == native.replace(
        parameters=list(native.parameters.values())[1:]
    )
    assert method.digestion_plan is not None
    assert not hasattr(view.addons.molsysmt, name)
    doc = inspect.getdoc(method)
    assert "current view.molsys" in doc and "not a scene object" in doc
    assert "not interaction occurrences" in doc
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


@pytest.mark.parametrize("indices", ["all", [2, 0, 2], [1]])
@pytest.mark.parametrize("skip", [False, True])
def test_nonconsecutive_structure_axes_and_native_skip_parity(
    feature_view, indices, skip
):
    view, name = feature_view
    args = dict(structure_indices=indices, skip_digestion=skip)
    result = getattr(view.addons.molsysmt.physchem, name)(**args)
    same(result, getattr(msm.physchem, name)(view.molsys, **args))
    assert result["chemical_state_index"] == 0
    assert "coordinates" not in result and "occurrences" not in result


@pytest.mark.parametrize("query", ["index >= 0", "index le 999", "name ZZZX"])
@pytest.mark.parametrize("chemical_state", [None, "reference"])
def test_external_reference_selections_match_intended_numeric_population(
    feature_view, query, chemical_state
):
    view, name = feature_view
    indices = (
        [] if query == "name ZZZX" else list(range(msm.get(view.molsys, n_atoms=True)))
    )
    actual = getattr(view.addons.molsysmt.physchem, name)(
        selection=query,
        syntax="MDTraj",
        structure_indices=[2, 0],
        chemical_state=chemical_state,
    )
    same(
        actual,
        getattr(msm.physchem, name)(
            view.molsys,
            selection=indices,
            structure_indices=[2, 0],
            chemical_state=chemical_state,
        ),
    )


def test_known_formal_centers_memberships_references_and_elementary_charge():
    with msv.new_view(feature_system(SMILES["get_charge_centers"])) as view:
        centers = view.addons.molsysmt.physchem.get_charge_centers()
        assert centers["atom_indices"].tolist() == [1, 2, 3, 4]
        assert centers["atom_offsets"].tolist() == [0, 3, 4]
        assert centers["geometry_atom_indices"].tolist() == [2, 3, 4]
        assert centers["geometry_atom_offsets"].tolist() == [0, 2, 3]
        assert centers["center_types"].tolist() == ["carboxylate", "formal_charge_atom"]
        np.testing.assert_array_equal(
            puw.get_value(centers["charges"], to_unit="e"), [-1, 1]
        )
        assert centers["charge_source"] == "chemical_states.formal_charge"
        assert centers["atom_indices"].dtype == np.int64
        with pytest.raises(msm.ArgumentError, match="cuts a compound charge center"):
            view.addons.molsysmt.physchem.get_charge_centers(selection=[2, 3])


def test_known_hydrophobic_sites_are_not_all_carbon_or_group_scale():
    with msv.new_view(feature_system(SMILES["get_hydrophobic_sites"])) as view:
        method = view.addons.molsysmt.physchem.get_hydrophobic_sites
        result = method()
        assert result["hydrophobic_atom_indices"].tolist() == [1, 4]
        assert result["hydrophobic_atom_indices"].dtype == np.int64
        assert method(selection=[0])["hydrophobic_atom_indices"].shape == (0,)
        assert result["method"] == "smarts_hydrophobic_atoms"
        assert result["scope"] == "full_source_recognition_then_selection"
        assert "rdkit" in result["software"]
        assert result["attribution"]["items"]


def test_halogen_pair_column_roles_and_complete_pair_filter():
    with msv.new_view(feature_system(SMILES["get_halogen_bond_sites"])) as view:
        method = view.addons.molsysmt.physchem.get_halogen_bond_sites
        result = method()
        assert result["donor_halogen_pairs"].tolist() == [[0, 1]]
        assert result["acceptor_reference_pairs"].tolist() == [[3, 2]]
        assert result["acceptor_reference_pairs"].dtype == np.int64
        assert method(selection=[1, 3])["donor_halogen_pairs"].shape == (0, 2)
        assert method(selection=[1, 3])["acceptor_reference_pairs"].shape == (0, 2)
        assert method(selection=[3, 2, 3])["acceptor_reference_pairs"].tolist() == [
            [3, 2]
        ]
        assert "rdkit" in result["software"]
        assert result["attribution"]["items"]


def test_empty_selection_retains_typed_native_output(feature_view):
    view, name = feature_view
    result = getattr(view.addons.molsysmt.physchem, name)(selection=[])
    same(result, getattr(msm.physchem, name)(view.molsys, selection=[]))
    if name == "get_charge_centers":
        assert result["atom_offsets"].tolist() == [0]
        assert result["geometry_atom_offsets"].tolist() == [0]
        assert result["atom_indices"].dtype == np.int64
        assert puw.get_value(result["charges"], to_unit="e").shape == (0,)
    elif name == "get_hydrophobic_sites":
        assert result["hydrophobic_atom_indices"].shape == (0,)
    else:
        assert result["donor_halogen_pairs"].shape == (0, 2)
        assert result["acceptor_reference_pairs"].shape == (0, 2)


@pytest.mark.parametrize("skip", [False, True])
def test_unknown_scientific_definitions_reject_without_scene_effects(
    feature_view, skip
):
    view, name = feature_view
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    args = {
        "definition" if name == "get_charge_centers" else "method": "guess",
        "skip_digestion": skip,
    }
    with pytest.raises(msm.ArgumentError):
        getattr(msm.physchem, name)(view.molsys, **args)
    with pytest.raises(msm.ArgumentError):
        getattr(view.addons.molsysmt.physchem, name)(**args)
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )


def test_missing_chemistry_is_not_prepared_even_for_empty_output(feature_view):
    view, name = feature_view
    state = view.molsys.chemical_states._states[0]
    state.atom_attributes.loc[0, "formal_charge"] = pd.NA
    before = state.atom_attributes.copy(deep=True)
    with pytest.raises(msm.StructuralInconsistencyError):
        getattr(view.addons.molsysmt.physchem, name)(
            selection=[], assume_complete_connectivity=True
        )
    pd.testing.assert_frame_equal(state.atom_attributes, before)


def test_completeness_assumption_is_explicit_and_does_not_change_evidence(feature_view):
    view, name = feature_view
    state = view.molsys.chemical_states._states[0]
    state.connectivity_completeness = "partial"
    method = getattr(view.addons.molsysmt.physchem, name)
    with pytest.raises(msm.StructuralInconsistencyError):
        method()
    args = dict(assume_complete_connectivity=True)
    result = method(**args)
    same(result, getattr(msm.physchem, name)(view.molsys, **args))
    assert result["evidence"]["assume_complete_connectivity"]
    assert state.connectivity_completeness == "partial"


@pytest.mark.parametrize(
    "name,smiles",
    [("get_hydrophobic_sites", "c1ccccc1"), ("get_halogen_bond_sites", "CCl.CBr.C=O")],
)
def test_match_limit_precedes_small_output_selection(name, smiles):
    with msv.new_view(feature_system(smiles)) as view:
        args = dict(selection=[], max_matches=1)
        with pytest.raises(UnsupportedHeavyOperationError):
            getattr(msm.physchem, name)(view.molsys, **args)
        with pytest.raises(UnsupportedHeavyOperationError):
            getattr(view.addons.molsysmt.physchem, name)(**args)


def test_structure_associations_and_reference_identity_remain_explicit(feature_view):
    view, name = feature_view
    primary = view.molsys
    second = primary.chemical_states._states[0].copy()
    second.state_id = "alternate"
    primary.chemical_states._append_state(second)
    msm.set(primary, structure_chemical_state_index=[0, 1, 0])
    method = getattr(view.addons.molsysmt.physchem, name)
    for indices, expected in [([2, 0, 2], 0), ([1], 1)]:
        args = dict(chemical_state="structure", structure_indices=indices)
        result = method(**args)
        same(result, getattr(msm.physchem, name)(primary, **args))
        assert result["chemical_state_index"] == expected
    with pytest.raises(msm.StructuralInconsistencyError):
        method(chemical_state="structure", structure_indices=[0, 1])
    assert primary.chemical_states.reference_chemical_state_index == 0


@pytest.mark.parametrize("chemical_state", [None, "reference"])
def test_external_reference_resolves_nonzero_reference_without_changing_associations(
    feature_view, chemical_state
):
    view, name = feature_view
    primary = view.molsys
    states = primary.chemical_states
    states._append_state(states._states[0].copy(), set_as_reference=True)
    msm.set(primary, structure_chemical_state_index=[0, 0, 0])
    result = getattr(view.addons.molsysmt.physchem, name)(
        selection="index >= 0",
        syntax="MDTraj",
        chemical_state=chemical_state,
        structure_indices=[2, 0],
    )
    assert result["chemical_state_index"] == 1
    same(
        result,
        getattr(msm.physchem, name)(
            primary,
            selection=list(range(msm.get(primary, n_atoms=True))),
            chemical_state=chemical_state,
            structure_indices=[2, 0],
        ),
    )
    assert states.reference_chemical_state_index == 1
    assert msm.get(primary, structure_chemical_state_index=True) == [0, 0, 0]


@pytest.mark.parametrize("name", ["get_hydrophobic_sites", "get_halogen_bond_sites"])
@pytest.mark.parametrize("chemical_state", [0, "structure"])
def test_smarts_reference_repair_preserves_explicit_state_syntax_restrictions(
    name, chemical_state
):
    with msv.new_view(feature_system(SMILES[name])) as view:
        args = dict(
            selection="index >= 0",
            syntax="MDTraj",
            chemical_state=chemical_state,
            structure_indices=[0],
        )
        with pytest.raises(msm.ArgumentError, match="syntax"):
            getattr(msm.physchem, name)(view.molsys, **args)
        with pytest.raises(msm.ArgumentError, match="syntax"):
            getattr(view.addons.molsysmt.physchem, name)(**args)


def test_reads_and_detached_results_preserve_domains_coverage_and_scene(feature_view):
    view, name = feature_view
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
    coverage = owners[3].to_dict()
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    expected = getattr(msm.physchem, name)(primary)
    result = getattr(view.addons.molsysmt.physchem, name)()
    same(result, expected)
    result["evidence"]["kind"] = "changed-return"
    key = {
        "get_charge_centers": "atom_indices",
        "get_hydrophobic_sites": "hydrophobic_atom_indices",
        "get_halogen_bond_sites": "acceptor_reference_pairs",
    }[name]
    result[key][:] = -1
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
    same(
        msm.convert(
            primary.chemical_states, to_form="molsysmt.ChemicalStatesDict"
        ).to_dict(),
        chemistry,
    )
    np.testing.assert_array_equal(puw.get_value(primary.structures.coordinates), xyz)
    same(owners[3].to_dict(), coverage)
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )


def test_reads_pending_primary_without_synchronizing(feature_view):
    view, name = feature_view
    tools = view.addons.molsysmt
    tools.structure.translate(
        translation=puw.quantity([1, 0, 0], "nm"), in_place=True, update_view=False
    )
    status = tools.get_sync_status()
    assert status["state"] == "pending"
    same(getattr(tools.physchem, name)(), getattr(msm.physchem, name)(view.molsys))
    assert tools.get_sync_status() == status
    with pytest.raises(SystemEditPendingError):
        view.export_state()


def test_cached_facade_tracks_replacement_and_lifetime(feature_view):
    view, name = feature_view
    method = getattr(view.addons.molsysmt.physchem, name)
    replacement = feature_system("CC")
    view.load(replacement, mode="replace")
    same(method(), getattr(msm.physchem, name)(view.molsys))
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt.physchem, name)()
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method()
