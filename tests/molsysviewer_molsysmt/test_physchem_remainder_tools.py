"""Receive site readers, explicit template transfer and independent factories."""

import inspect
from copy import deepcopy

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError
from molsysviewer.system_edits import SystemEditPendingError
from rdkit import Chem
from rdkit.Chem import rdDepictor

import molsysmt as msm
from molsysmt.native import Structures

puw = msm.pyunitwizard
SITES = ("get_water_sites", "get_metal_coordination_sites")
TEMPLATES = ("assess_chemical_template", "apply_chemical_template")
NAMES = (
    *SITES,
    *TEMPLATES,
    "normalize_aromatic_bond_orders",
    "get_peptide_chemical_template",
)
PROVENANCE = dict(
    identity="methanol",
    version="1",
    source_uri="fixture:methanol",
    checksum="caller-declaration",
    hydrogen_policy="explicit_atoms",
)


def molecular_system(smiles):
    molsys = Chem.AddHs(Chem.MolFromSmiles(smiles))
    rdDepictor.Compute2DCoords(molsys)
    result = msm.convert(molsys)
    xyz = puw.get_value(result.structures.coordinates, to_unit="nm").copy()
    result.structures.append(
        coordinates=puw.quantity(
            np.concatenate([xyz + [1, 0, 0], xyz + [0, 1, 0]]), "nm"
        ),
        structure_id=[70, 200],
    )
    return result


def prepare_view(source):
    view = msv.new_view(source)
    view.regions.add(selection=[0], tag="source")
    view.interactions.attach(
        msm.Interactions.from_records(
            [],
            n_atoms=source.get_n_atoms(),
            n_structures=3,
            evaluated_structure_indices=[0, 1, 2],
            method="receiving.physchem.remainder",
        ),
        name="preserve",
        assume_aligned=True,
    )
    return view


@pytest.fixture
def sites_view():
    with prepare_view(molecular_system("[Zn+2].O.CO.O")) as view:
        yield view


@pytest.fixture
def template_view():
    template = molecular_system("CO")
    source = template.copy()
    state = source.chemical_states._states[0]
    state.atom_attributes = pd.DataFrame(index=range(6))
    state.bonds.drop(
        columns=[
            c
            for c in ("bond_type", "bond_order", "is_aromatic", "joins_components")
            if c in state.bonds
        ],
        inplace=True,
    )
    state.bonds["evidence"] = "inferred"
    state.connectivity_completeness = "partial"
    with prepare_view(source) as view:
        yield (
            view,
            dict(
                template=template,
                template_provenance=deepcopy(PROVENANCE),
                atom_correspondence=np.column_stack((np.arange(6), np.arange(6))),
            ),
        )


@pytest.fixture
def aromatic_view():
    source = msm.physchem.get_peptide_chemical_template(
        ["PHE"], "ammonium", "carboxylate"
    )["template"]
    state = source.chemical_states._states[0]
    aromatic = state.bonds.index[state.bonds.is_aromatic.eq(True)]
    state.bonds.loc[aromatic, "bond_order"] = [1, 2, 1, 2, 1, 2]
    state.bonds.loc[aromatic, "fractional_bond_order"] = pd.NA
    state.connectivity_completeness = "partial"
    n = source.get_n_atoms()
    source.structures = Structures()
    source.structures.append(
        coordinates=puw.quantity(np.arange(9 * n).reshape(3, n, 3) / 100, "nm")
    )
    with prepare_view(source) as view:
        yield view, np.asarray(aromatic, dtype=np.int64)


def same(actual, expected):
    if isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for key in expected:
            same(actual[key], expected[key])
    elif puw.is_quantity(expected):
        assert puw.get_unit(actual) == puw.get_unit(expected)
        np.testing.assert_equal(puw.get_value(actual), puw.get_value(expected))
    elif isinstance(expected, (list, tuple)):
        assert type(actual) is type(expected) and len(actual) == len(expected)
        for a, e in zip(actual, expected):
            same(a, e)
    else:
        np.testing.assert_equal(actual, expected)


def scientific_snapshot(view):
    primary = view.molsys
    return (
        primary,
        primary.chemical_states._states[0].atom_attributes.copy(deep=True),
        primary.chemical_states._states[0].bonds.copy(deep=True),
        puw.get_value(primary.structures.coordinates).copy(),
        deepcopy(primary.interactions["preserve"].to_dict()),
        view.export_state(),
        view.addons.molsysmt.get_sync_status(),
    )


def unchanged(view, snapshot):
    primary, attrs, bonds, xyz, interactions, scene, status = snapshot
    assert view.molsys is primary
    pd.testing.assert_frame_equal(
        primary.chemical_states._states[0].atom_attributes, attrs
    )
    pd.testing.assert_frame_equal(primary.chemical_states._states[0].bonds, bonds)
    np.testing.assert_array_equal(puw.get_value(primary.structures.coordinates), xyz)
    same(primary.interactions["preserve"].to_dict(), interactions)
    assert (
        view.export_state() == scene
        and view.addons.molsysmt.get_sync_status() == status
    )


@pytest.mark.parametrize("name", NAMES)
def test_explicit_signature_digestion_help_and_no_implicit_adoption(sites_view, name):
    method = getattr(sites_view.addons.molsysmt.physchem, name)
    native = inspect.signature(getattr(msm.physchem, name))
    parameters = list(native.parameters.values())
    if name != "get_peptide_chemical_template":
        parameters = parameters[1:]
    assert inspect.signature(method) == native.replace(parameters=parameters)
    assert method.digestion_plan is not None
    assert not hasattr(sites_view.addons.molsysmt, name)
    assert "update_view" not in inspect.signature(method).parameters
    doc = inspect.getdoc(method)
    assert "\nmolecular_system :" not in doc
    if name == "get_peptide_chemical_template":
        assert "explicit-input factory works before" in doc
    else:
        assert "current view.molsys" in doc
    with pytest.raises(UnknownArgumentError):
        method(molecular_system=sites_view.molsys)


@pytest.mark.parametrize("name", SITES)
@pytest.mark.parametrize("structures", ["all", [2, 0, 2], [1]])
@pytest.mark.parametrize("skip", [False, True])
def test_sparse_sites_explicit_structures_roles_and_native_output(
    sites_view, name, structures, skip
):
    before = scientific_snapshot(sites_view)
    kwargs = dict(structure_indices=structures, skip_digestion=skip)
    actual = getattr(sites_view.addons.molsysmt.physchem, name)(**kwargs)
    same(actual, getattr(msm.physchem, name)(sites_view.molsys, **kwargs))
    if name == "get_water_sites":
        assert actual["water_atom_indices"].tolist() == [[1, 5, 6], [4, 11, 12]]
        assert actual["water_atom_indices"].dtype == np.int64
    else:
        assert actual["metal_atom_indices"].tolist() == [0]
        assert actual["ligand_atom_indices"].tolist() == [1, 3, 4]
    unchanged(sites_view, before)


@pytest.mark.parametrize(
    "selection,expected", [([], []), ([1], []), ([6, 1, 5, 6], [[1, 5, 6]])]
)
def test_water_selection_requires_whole_participant_without_expansion(
    sites_view, selection, expected
):
    actual = sites_view.addons.molsysmt.physchem.get_water_sites(selection=selection)
    assert actual["water_atom_indices"].tolist() == expected
    assert actual["water_atom_indices"].shape == (len(expected), 3)


@pytest.mark.parametrize("name", SITES)
def test_external_selection_and_match_budget_use_full_source(sites_view, name):
    method = getattr(sites_view.addons.molsysmt.physchem, name)
    same(
        method(selection="index 1", syntax="MDTraj"),
        getattr(msm.physchem, name)(sites_view.molsys, selection=[1]),
    )
    from molsysmt._private.smonitor import UnsupportedHeavyOperationError

    with pytest.raises(UnsupportedHeavyOperationError):
        method(selection=[], max_matches=1)
    with pytest.raises(msm.ArgumentError):
        method(structure_indices=[999])


@pytest.mark.parametrize("name", SITES)
def test_assumption_is_explicit_and_never_prepares_source(sites_view, name):
    state = sites_view.molsys.chemical_states._states[0]
    state.connectivity_completeness = "partial"
    method = getattr(sites_view.addons.molsysmt.physchem, name)
    with pytest.raises(msm.StructuralInconsistencyError):
        method()
    same(
        method(assume_complete_connectivity=True),
        getattr(msm.physchem, name)(
            sites_view.molsys, assume_complete_connectivity=True
        ),
    )
    assert state.connectivity_completeness == "partial"


@pytest.mark.parametrize("name", TEMPLATES)
@pytest.mark.parametrize("skip", [False, True])
def test_explicit_template_map_preserves_source_and_independent_result(
    template_view, name, skip
):
    view, kwargs = template_view
    before = scientific_snapshot(view)
    template_before = (
        kwargs["template"].chemical_states._states[0].atom_attributes.copy(deep=True)
    )
    actual = getattr(view.addons.molsysmt.physchem, name)(**kwargs, skip_digestion=skip)
    native = getattr(msm.physchem, name)(view.molsys, **kwargs, skip_digestion=skip)
    if name == "assess_chemical_template":
        assert actual["status"] == "compatible"
        same(actual, native)
    else:
        same(actual["report"], native["report"])
        result = actual["molecular_system"]
        assert result is not view.molsys and actual["report"]["status"] == "applied"
        assert (
            result.chemical_states._states[0].atom_attributes["formal_charge"].tolist()
            == [0] * 6
        )
        assert result.chemical_states._states[0].connectivity_completeness == "complete"
        assert result.interactions["preserve"].evaluated_structure_indices.size == 0
        np.testing.assert_array_equal(
            puw.get_value(result.structures.coordinates), before[3]
        )
        actual["report"]["template_provenance"]["identity"] = "edited"
        assert kwargs["template_provenance"]["identity"] == "methanol"
    unchanged(view, before)
    pd.testing.assert_frame_equal(
        kwargs["template"].chemical_states._states[0].atom_attributes, template_before
    )


@pytest.mark.parametrize("name", TEMPLATES)
def test_template_conflicts_and_nonexhaustive_map_remain_explicit(template_view, name):
    view, kwargs = template_view
    before = scientific_snapshot(view)
    with pytest.raises(msm.ArgumentError):
        getattr(view.addons.molsysmt.physchem, name)(
            **dict(kwargs, atom_correspondence=[[0, 0]])
        )
    view.molsys.chemical_states._states[0].set_atom_attribute(
        "formal_charge", [1], atom_indices=[0]
    )
    args = dict(kwargs)
    if name == "assess_chemical_template":
        assert (
            getattr(view.addons.molsysmt.physchem, name)(**args)["status"] == "conflict"
        )
    else:
        with pytest.raises(msm.StructuralInconsistencyError) as caught:
            getattr(view.addons.molsysmt.physchem, name)(**args)
        assert caught.value.report["status"] == "conflict"
    assert view.export_state() == before[-2]


def test_selected_template_context_preserves_outside_atoms_and_boundary_roles():
    definition = msm.physchem.get_peptide_chemical_template(
        ["GLY", "GLY", "GLY"], "ammonium", "carboxylate"
    )
    source = definition["template"].copy()
    state = source.chemical_states._states[0]
    for field in state.atom_attributes:
        state.atom_attributes[field] = pd.NA
    state._normalize_atom_attribute_columns()
    state.connectivity_completeness = "partial"
    source.structures = Structures()
    source.structures.append(
        coordinates=puw.quantity(np.zeros((3, source.get_n_atoms(), 3)), "nm")
    )
    selected = msm.select(source, selection="group_index==1")
    pairs = state.bonds[["atom1_index", "atom2_index"]].to_numpy(dtype=np.int64)
    context = np.setdiff1d(pairs[np.isin(pairs, selected).any(axis=1)], selected)
    kwargs = dict(
        template=definition["template"],
        template_provenance=definition["template_provenance"],
        selection=selected,
        atom_correspondence=np.column_stack((selected, selected)),
        context_atom_correspondence=np.column_stack((context, context)),
    )
    with prepare_view(source) as view:
        before = scientific_snapshot(view)
        result = view.addons.molsysmt.physchem.apply_chemical_template(**kwargs)
        assert result["report"]["coverage"]["scope"] == "selected_with_context"
        outside = np.setdiff1d(np.arange(source.get_n_atoms()), selected)
        pd.testing.assert_frame_equal(
            result["molecular_system"]
            .chemical_states._states[0]
            .atom_attributes.iloc[outside],
            before[1].iloc[outside],
        )
        unchanged(view, before)


@pytest.mark.parametrize("skip", [False, True])
def test_normalization_has_independent_chemistry_history_and_coverage(
    aromatic_view, skip
):
    view, aromatic = aromatic_view
    before = scientific_snapshot(view)
    result = view.addons.molsysmt.physchem.normalize_aromatic_bond_orders(
        skip_digestion=skip
    )
    actual, report = result["molecular_system"], result["report"]
    same(
        report,
        msm.physchem.normalize_aromatic_bond_orders(view.molsys, skip_digestion=skip)[
            "report"
        ],
    )
    assert report["status"] == "normalized"
    np.testing.assert_array_equal(report["changed_bond_indices"], aromatic)
    assert (
        actual.chemical_states._states[0]
        .bonds.loc[aromatic, "fractional_bond_order"]
        .eq(1.5)
        .all()
    )
    assert actual.interactions["preserve"].evaluated_structure_indices.size == 0
    history = actual.chemical_states.get_preparation_history()
    assert history[-1]["report"]["status"] == "normalized"
    report["status"] = "edited"
    assert (
        actual.chemical_states.get_preparation_history()[-1]["report"]["status"]
        == "normalized"
    )
    unchanged(view, before)


@pytest.mark.parametrize("skip", [False, True])
def test_explicit_factory_works_without_primary_and_preserves_lifetime(skip):
    with msv.new_view() as view:
        factory = view.addons.molsysmt.physchem.get_peptide_chemical_template
        result = factory(["GLY", "GLY"], "ammonium", "carboxylate", skip_digestion=skip)
        assert result["template"].get_n_atoms() == 9
        assert result["report"]["n_stored_hydrogens"] == 8
        assert (
            result["template"].structures is None
            or result["template"].structures.coordinates is None
        ) and view.molsys is None
        result["template_provenance"]["identity"] = "edited"
        assert (
            factory(["GLY", "GLY"], "ammonium", "carboxylate")["template_provenance"][
                "identity"
            ]
            != "edited"
        )
    with pytest.raises(RuntimeError, match="closed view"):
        factory(["GLY"], "ammonium", "carboxylate")


def test_explicit_factory_forwards_declared_disulfides_without_geometry(sites_view):
    before = scientific_snapshot(sites_view)
    result = sites_view.addons.molsysmt.physchem.get_peptide_chemical_template(
        ["CYX", "GLY", "CYX"], "ammonium", "carboxylate", disulfide_group_pairs=[[0, 2]]
    )
    assert (
        result["template"].structures is None
        or result["template"].structures.coordinates is None
    )
    same(
        result["report"],
        msm.physchem.get_peptide_chemical_template(
            ["CYX", "GLY", "CYX"],
            "ammonium",
            "carboxylate",
            disulfide_group_pairs=[[0, 2]],
        )["report"],
    )
    unchanged(sites_view, before)


@pytest.mark.parametrize("name", (*SITES, "normalize_aromatic_bond_orders"))
def test_pending_reads_do_not_adopt_and_cached_readers_follow_replacement(
    sites_view, name
):
    method = getattr(sites_view.addons.molsysmt.physchem, name)
    sites_view.addons.molsysmt.structure.translate(
        translation=puw.quantity([1, 0, 0], "nm"), in_place=True, update_view=False
    )
    status = sites_view.addons.molsysmt.get_sync_status()
    method()
    assert (
        sites_view.addons.molsysmt.get_sync_status() == status
        and status["state"] == "pending"
    )
    with pytest.raises(SystemEditPendingError):
        sites_view.export_state()
    sites_view.addons.molsysmt.sync_view()
    sites_view.load(molecular_system("CO"), mode="replace")
    actual, native = method(), getattr(msm.physchem, name)(sites_view.molsys)
    same(
        actual["report"] if name == "normalize_aromatic_bond_orders" else actual,
        native["report"] if name == "normalize_aromatic_bond_orders" else native,
    )
    sites_view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method()
