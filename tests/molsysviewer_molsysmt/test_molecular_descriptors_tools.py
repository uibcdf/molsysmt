"""Receiving complete-context TPSA and lipophilicity outputs through a live view."""

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
from molsysmt.native.topology import Chains_DataFrame, Groups_DataFrame

puw = msm.pyunitwizard
DESCRIPTORS = ("tpsa", "lipophilicity")
LEVELS = ("atom", "group", "component", "molecule", "chain", "entity", "system")
ATOMIC = {
    "tpsa": np.array([0.0, 0.0, 20.23]),
    "lipophilicity": np.array([0.5131, 0.0425, -0.5570]),
}


def molecular_system(smiles="CCO", *, hierarchy=None, indexed_h=False):
    # Declared fixture chemistry, H presentation and coordinates precede the view.
    # No scientific wrapper creates hierarchy or prepares the molecular graph.
    molecule = Chem.MolFromSmiles(smiles)
    if indexed_h:
        molecule = Chem.AddHs(molecule)
    rdDepictor.Compute2DCoords(molecule)
    source = msm.convert(molecule)
    if hierarchy is not None:
        assert smiles == "CCO" and not indexed_h
        top = source.topology
        top.groups = Groups_DataFrame(n_groups=2)
        top.groups["group_id"] = ["1", "2"]
        top.groups["group_name"] = (
            ["POLAR", "ALKYL"] if hierarchy == "reversed" else ["ALKYL", "POLAR"]
        )
        top.groups["group_type"] = ["small molecule", "small molecule"]
        top.groups["molecule_index"] = [0, 0]
        mapping = [1, 0, 0] if hierarchy == "reversed" else [0, 0, 1]
        top.atoms["group_index"] = mapping
        top.chains = Chains_DataFrame(n_chains=2)
        top.chains["chain_id"] = ["A", "B"]
        top.atoms["chain_index"] = mapping
        top._molecules_dirty = False
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    source.structures.append(
        coordinates=puw.quantity(
            np.concatenate([xyz + [1, 0, 0], xyz + [0, 1, 0]]), "nm"
        ),
        structure_id=[70, 200],
    )
    return source


@pytest.fixture(params=DESCRIPTORS)
def descriptor(request):
    return request.param


@pytest.fixture
def view():
    with msv.new_view(molecular_system(hierarchy="reversed")) as result:
        result.regions.add(selection=[2], tag="oxygen")
        result.interactions.attach(
            msm.Interactions.from_records(
                [],
                n_atoms=3,
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.descriptors",
            ),
            name="preserve",
            assume_aligned=True,
        )
        yield result


def bound(view, descriptor, **kwargs):
    return getattr(view.addons.molsysmt.physchem, "get_" + descriptor)(**kwargs)


def native(view, descriptor, **kwargs):
    return getattr(msm.physchem, "get_" + descriptor)(view.molsys, **kwargs)


def values(result, descriptor):
    if isinstance(result, dict):
        result = result[descriptor]
    if descriptor == "tpsa":
        assert puw.is_quantity(result)
        return puw.get_value(result, to_unit="angstrom**2")
    assert not puw.is_quantity(result)
    assert np.asarray(result).dtype == np.float64
    return result


def same(actual, expected):
    if isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for key in expected:
            same(actual[key], expected[key])
    elif puw.is_quantity(expected):
        assert puw.get_unit(actual) == puw.get_unit(expected)
        np.testing.assert_array_equal(puw.get_value(actual), puw.get_value(expected))
    else:
        np.testing.assert_equal(actual, expected)


def test_exact_signature_help_digestion_and_no_invented_controls(view, descriptor):
    name = "get_" + descriptor
    method = getattr(view.addons.molsysmt.physchem, name)
    sig = inspect.signature(getattr(msm.physchem, name))
    assert inspect.signature(method) == sig.replace(
        parameters=list(sig.parameters.values())[1:]
    )
    assert method.digestion_plan is not None
    assert not hasattr(view.addons.molsysmt, name)
    doc = inspect.getdoc(method)
    assert "current view.molsys" in doc and "not a scene object" in doc
    assert "complete molecular context" in doc and "Output element maps" in doc
    assert "\nmolecular_system :" not in doc
    for args in [
        dict(molecular_system=view.molsys),
        dict(update_view=False),
        dict(prepare=True),
        dict(aggregate=True),
        dict(engine="rdkit"),
    ]:
        with pytest.raises(UnknownArgumentError):
            method(**args)
        with pytest.raises(TypeError):
            method(**args, skip_digestion=True)


@pytest.mark.parametrize(
    "element,selection,members",
    [
        ("atom", "all", [[0], [1], [2]]),
        ("atom", [2, 0, 2], [[2], [0], [2]]),
        ("group", "all", [[1, 2], [0]]),
        ("group", [1, 0, 1], [[0], [1, 2], [0]]),
        ("group", "atom_index==0", [[0]]),
        ("chain", "all", [[1, 2], [0]]),
        ("chain", [1, 0, 1], [[0], [1, 2], [0]]),
        ("component", "all", [[0, 1, 2]]),
        ("entity", "all", [[0, 1, 2]]),
        ("molecule", [0, 0], [[0, 1, 2], [0, 1, 2]]),
        ("system", [2, 0, 2], [[2, 0, 2]]),
    ],
)
@pytest.mark.parametrize("skip", [False, True])
def test_complete_context_reference_contributions_and_output_membership(
    view, descriptor, element, selection, members, skip
):
    args = dict(
        element=element,
        selection=selection,
        structure_indices=[2, 0, 2],
        return_report=True,
        skip_digestion=skip,
    )
    result = bound(view, descriptor, **args)
    same(result, native(view, descriptor, **args))
    expected = [sum(ATOMIC[descriptor][atoms]) for atoms in members]
    observed = values(result, descriptor)
    assert np.shape(observed) == (() if element == "system" else (len(members),))
    np.testing.assert_allclose(
        observed, expected[0] if element == "system" else expected, atol=1e-12, rtol=0
    )
    report = result["report"]
    assert report["element"] == element
    assert report["element_atom_indices"].tolist() == [
        atom for atoms in members for atom in atoms
    ]
    assert (
        report["element_atom_offsets"].tolist()
        == [0] + np.cumsum([len(atoms) for atoms in members]).tolist()
    )
    assert report["element_atom_indices"].dtype == np.int64
    assert report["output_kind"] == (
        "molecular_descriptor" if element == "molecule" else "atomic_contribution_sum"
    )
    if element != "molecule":
        assert report["molecule_indices"].tolist() == [0]
        assert report["atom_indices"].tolist() == [0, 1, 2]
        assert (
            report["parameters"]["contribution_context"] == "complete_source_molecules"
        )


@pytest.mark.parametrize("element", LEVELS)
def test_empty_selections_preserve_scalar_or_empty_axis_and_context(
    view, descriptor, element
):
    result = bound(view, descriptor, element=element, selection=[], return_report=True)
    observed = values(result, descriptor)
    assert np.shape(observed) == (() if element == "system" else (0,))
    if element == "system":
        assert observed == 0
    report = result["report"]
    assert report["element_atom_indices"].shape == (0,)
    assert report["element_atom_offsets"].tolist() == (
        [0, 0] if element == "system" else [0]
    )
    assert report["molecule_indices"].shape == (0,)
    assert report["attribution"]["items"]
    same(
        result,
        native(view, descriptor, element=element, selection=[], return_report=True),
    )


@pytest.mark.parametrize("element", LEVELS[:-1])
def test_scalar_index_keeps_element_axis(view, descriptor, element):
    result = bound(view, descriptor, element=element, selection=0)
    assert np.shape(values(result, descriptor)) == (1,)
    same(result, native(view, descriptor, element=element, selection=0))


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("element", ["atom", "group", "system"])
def test_units_follow_physical_dimension_without_rescaling_scores(
    view, descriptor, unit, element
):
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = bound(view, descriptor, element=element)
        if descriptor == "tpsa":
            assert puw.get_unit(result) == puw.unit(unit) ** 2
        else:
            assert not puw.is_quantity(result)
    if descriptor == "lipophilicity":
        same(result, native(view, descriptor, element=element))
    expected = (
        ATOMIC[descriptor]
        if element == "atom"
        else [sum(ATOMIC[descriptor][[1, 2]]), ATOMIC[descriptor][0]]
        if element == "group"
        else sum(ATOMIC[descriptor])
    )
    np.testing.assert_allclose(values(result, descriptor), expected, atol=1e-12, rtol=0)


@pytest.mark.parametrize(
    "element,indices",
    [("atom", [2]), ("group", [1]), ("molecule", [0]), ("system", [2])],
)
def test_positive_external_selection_on_explicit_hierarchy(
    descriptor, element, indices
):
    with msv.new_view(molecular_system(hierarchy="ordered")) as result:
        actual = bound(
            result,
            descriptor,
            element=element,
            selection="index 2",
            syntax="MDTraj",
            return_report=True,
        )
        expected = native(
            result, descriptor, element=element, selection=indices, return_report=True
        )
        same(actual, expected)


def test_declared_chemical_states_and_nonconsecutive_structures_remain_explicit(
    descriptor,
):
    source = molecular_system("CC(=O)O")
    state = source.chemical_states._states[0].copy()
    state.state_id = "acetate"
    state.atom_attributes.loc[3, "formal_charge"] = -1
    state.atom_attributes.loc[3, "n_implicit_hydrogens"] = 0
    source.chemical_states._append_state(state)
    msm.set(source, structure_chemical_state_index=[0, 1, 0])
    with msv.new_view(source) as result:
        baseline = bound(result, descriptor, element="atom", return_report=True)
        same(
            baseline,
            bound(
                result,
                descriptor,
                element="atom",
                chemical_state="structure",
                structure_indices=[2, 0, 2],
                return_report=True,
            ),
        )
        alternate = bound(
            result,
            descriptor,
            element="atom",
            chemical_state="structure",
            structure_indices=[1],
            return_report=True,
        )
        assert alternate["report"]["chemical_state_index"] == 1
        assert alternate["report"]["chemical_state_id"] == "acetate"
        assert not np.array_equal(
            values(baseline, descriptor), values(alternate, descriptor)
        )
        with pytest.raises(msm.StructuralInconsistencyError):
            bound(
                result,
                descriptor,
                element="atom",
                chemical_state="structure",
                structure_indices=[0, 1],
            )
        assert result.molsys.chemical_states.reference_chemical_state_index == 0


def test_hydrogen_presentation_changes_rows_not_complete_contribution_sum(descriptor):
    implicit = molecular_system()
    expanded = molecular_system(indexed_h=True)
    with msv.new_view(implicit) as small, msv.new_view(expanded) as large:
        first = values(bound(small, descriptor, element="atom"), descriptor)
        second = values(bound(large, descriptor, element="atom"), descriptor)
        assert first.shape == (3,) and second.shape == (9,)
        rdkit = msm.convert(large.molsys, to_form="rdkit.Mol")
        folded = second[:3].copy()
        for atom in rdkit.GetAtoms():
            if atom.GetIdx() >= 3:
                folded[atom.GetNeighbors()[0].GetIdx()] += second[atom.GetIdx()]
        np.testing.assert_allclose(first, folded, atol=1e-12, rtol=0)
        np.testing.assert_allclose(sum(first), sum(second), atol=1e-12, rtol=0)
        assert msm.get(small.molsys, n_atoms=True) == 3
        assert msm.get(large.molsys, n_atoms=True) == 9


def test_lipophilicity_retains_charged_sites_even_for_net_neutral_graphs():
    with msv.new_view(molecular_system("CCO.CC[NH3+].[NH3+]CC(=O)[O-]")) as result:
        charges_before = result.molsys.chemical_states._states[0].atom_attributes.copy(
            deep=True
        )
        received = bound(
            result, "lipophilicity", selection=[2, 1, 0, 2], return_report=True
        )
        same(
            received,
            native(result, "lipophilicity", selection=[2, 1, 0, 2], return_report=True),
        )
        report = received["report"]
        assert report["formal_charges"].tolist() == [0, 1, 0, 0]
        assert np.diff(report["charged_atom_offsets"]).tolist() == [2, 1, 0, 2]
        np.testing.assert_allclose(
            received["lipophilicity"][[1, 2]], [-0.7518, -0.0014], atol=1e-12, rtol=0
        )
        assert report["parameters"]["chemical_preparation"] == "none"
        assert report["value_kind"] == "wildman_crippen_model_score"
        assert report["value_unit"] == "dimensionless"
        pd.testing.assert_frame_equal(
            result.molsys.chemical_states._states[0].atom_attributes, charges_before
        )


def test_selected_atom_cannot_hide_incomplete_parent_chemistry(view, descriptor):
    attrs = view.molsys.chemical_states._states[0].atom_attributes
    attrs.loc[0, "n_implicit_hydrogens"] = None
    before, scene = attrs.copy(deep=True), view.export_state()
    with pytest.raises(msm.StructuralInconsistencyError):
        bound(view, descriptor, element="atom", selection=[2])
    pd.testing.assert_frame_equal(before, attrs)
    assert view.export_state() == scene


def test_reports_values_source_domains_and_scene_remain_independent(view, descriptor):
    primary = view.molsys
    owners = (
        primary.topology,
        primary.structures,
        primary.chemical_states,
        primary.interactions["preserve"],
    )
    attrs = primary.chemical_states._states[0].atom_attributes.copy(deep=True)
    bonds = primary.chemical_states._states[0].bonds.copy(deep=True)
    coordinates = puw.get_value(primary.structures.coordinates).copy()
    coverage = deepcopy(owners[3].to_dict())
    scene, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    received = bound(
        view, descriptor, element="group", selection=[1, 0, 1], return_report=True
    )
    received[descriptor][:] *= 2
    received["report"]["element_indices"][:] = -1
    received["report"]["element_atom_indices"][:] = -1
    received["report"]["parameters"]["contribution_context"] = "edited"
    article = next(
        x
        for x in received["report"]["attribution"]["items"]
        if x["id"].startswith("doi:")
    )
    article["authors"].append("edited")
    fresh = bound(
        view, descriptor, element="group", selection=[1, 0, 1], return_report=True
    )
    same(
        fresh,
        native(
            view, descriptor, element="group", selection=[1, 0, 1], return_report=True
        ),
    )
    assert all(
        "edited" not in item.get("authors", [])
        for item in fresh["report"]["attribution"]["items"]
    )
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
    pd.testing.assert_frame_equal(
        primary.chemical_states._states[0].atom_attributes, attrs
    )
    pd.testing.assert_frame_equal(primary.chemical_states._states[0].bonds, bonds)
    np.testing.assert_array_equal(
        puw.get_value(primary.structures.coordinates), coordinates
    )
    same(primary.interactions["preserve"].to_dict(), coverage)
    assert (
        view.export_state() == scene
        and view.addons.molsysmt.get_sync_status() == status
    )


def test_pending_read_cached_replacement_and_lifetime(view, descriptor):
    method = getattr(view.addons.molsysmt.physchem, "get_" + descriptor)
    view.addons.molsysmt.structure.translate(
        translation=puw.quantity([1, 0, 0], "nm"), in_place=True, update_view=False
    )
    status = view.addons.molsysmt.get_sync_status()
    method(element="atom")
    assert (
        view.addons.molsysmt.get_sync_status() == status
        and status["state"] == "pending"
    )
    with pytest.raises(SystemEditPendingError):
        view.export_state()
    view.addons.molsysmt.sync_view()
    view.load(molecular_system("c1ccccc1"), mode="replace")
    expected = [0.0] * 6 if descriptor == "tpsa" else [0.2811] * 6
    np.testing.assert_allclose(
        values(method(element="atom"), descriptor), expected, atol=1e-12, rtol=0
    )
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method()
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt.physchem, "get_" + descriptor)(selection=[])


@pytest.mark.parametrize(
    "args",
    [
        dict(element="bond"),
        dict(method="guess"),
        dict(selection=[999]),
        dict(structure_indices=[999]),
        dict(return_report="yes"),
    ],
)
def test_native_rejections_preserve_scene(view, descriptor, args):
    scene = view.export_state()
    with pytest.raises(Exception) as expected:
        native(view, descriptor, **args)
    with pytest.raises(type(expected.value)):
        bound(view, descriptor, **args)
    assert view.export_state() == scene


def test_real_bundled_caffeine_no_input_or_scene_assignment(descriptor):
    molecule = Chem.SDMolSupplier(
        msm.systems["caffeine"]["caffeine.sdf"], removeHs=False
    )[0]
    assert molecule is not None
    with msv.new_view(molecule) as result:
        before = result.export_state()
        received = bound(result, descriptor, element="atom", return_report=True)
        assert np.shape(values(received, descriptor)) == (24,)
        same(received, native(result, descriptor, element="atom", return_report=True))
        assert result.export_state() == before


def test_optional_attribution_keeps_native_scope_for_empty_and_contribution_calls(view):
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("bound molecular descriptors"):
        with ackredit.scope("consumer.bound_descriptors"):
            for descriptor in DESCRIPTORS:
                bound(view, descriptor, element="group", return_report=True)
                empty = bound(
                    view, descriptor, element="system", selection=[], return_report=True
                )
                assert np.shape(values(empty, descriptor)) == ()
        assert {"doi:10.1021/jm000942e", "doi:10.1021/ci990307l"} <= set(
            ackredit.get_used_items()
        )
        children = ackredit.current_session().usage_tree["consumer.bound_descriptors"][
            "children"
        ]
        assert {
            "molsysmt.physchem.get_tpsa",
            "molsysmt.physchem.get_lipophilicity",
        } <= set(children)
