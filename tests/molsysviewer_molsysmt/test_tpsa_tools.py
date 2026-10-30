"""Receiving molecular TPSA without preparing chemistry or projecting a scene."""

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
from molsysmt._private.smonitor import ArgumentChoiceError

puw = msm.pyunitwizard


def molecular_system(smiles="CCO.COC.CS(C)(=O)=O"):
    # Declared chemistry and deterministic coordinates precede the view.
    # Retain the supported group-free source and its complete molecule axis.
    molecule = Chem.MolFromSmiles(smiles)
    rdDepictor.Compute2DCoords(molecule)
    source = msm.convert(molecule)
    coordinates = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    source.structures.append(
        coordinates=puw.quantity(
            np.concatenate([coordinates + [1, 0, 0], coordinates + [0, 1, 0]]),
            "nm",
        ),
        structure_id=[70, 200],
    )
    return source


@pytest.fixture
def view():
    with msv.new_view(molecular_system()) as result:
        result.interactions.attach(
            msm.Interactions.from_records(
                [],
                n_atoms=msm.get(result.molsys, n_atoms=True),
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.tpsa",
            ),
            name="preserve",
            assume_aligned=True,
        )
        result.regions.add(selection=[0], tag="source")
        yield result


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


def test_native_signature_help_validation_and_no_invented_controls(view):
    method = view.addons.molsysmt.physchem.get_tpsa
    signature = inspect.signature(msm.physchem.get_tpsa)
    assert inspect.signature(method) == signature.replace(
        parameters=list(signature.parameters.values())[1:]
    )
    assert method.digestion_plan is not None
    assert not hasattr(view.addons.molsysmt, "get_tpsa")
    doc = inspect.getdoc(method)
    assert "current view.molsys" in doc and "not a scene object" in doc
    assert "Molecule indices address the source molecule axis" in doc
    assert "\nmolecular_system :" not in doc
    for kwargs in [
        dict(molecular_system=view.molsys),
        dict(update_view=False),
        dict(prepare=True),
        dict(engine="rdkit"),
        dict(aggregate=True),
    ]:
        with pytest.raises(UnknownArgumentError):
            method(**kwargs)
        with pytest.raises(TypeError):
            method(**kwargs, skip_digestion=True)


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize(
    "selection,expected,indices,atoms",
    [
        ("all", [20.23, 9.23, 34.14], [0, 1, 2], list(range(11))),
        ([1, 0, 1], [9.23, 20.23, 9.23], [1, 0, 1], [3, 4, 5, 0, 1, 2, 3, 4, 5]),
        (0, [20.23], [0], [0, 1, 2]),
        ([], [], [], []),
        ("atom_index==0", [20.23], [0], [0, 1, 2]),
    ],
)
@pytest.mark.parametrize("skip", [False, True])
def test_molecule_population_order_repetitions_units_and_empty_maps(
    view, unit, selection, expected, indices, atoms, skip
):
    assert msm.get(view.molsys, n_molecules=True) == 3
    args = dict(
        selection=selection,
        structure_indices=[2, 0, 2],
        return_report=True,
        skip_digestion=skip,
    )
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = view.addons.molsysmt.physchem.get_tpsa(**args)
        assert puw.get_unit(result["tpsa"]) == puw.unit(unit) ** 2
        same(result, msm.physchem.get_tpsa(view.molsys, **args))
    assert result["tpsa"].shape == (len(expected),)
    np.testing.assert_allclose(
        puw.get_value(result["tpsa"], to_unit="angstrom**2"), expected, atol=1e-12
    )
    report = result["report"]
    assert report["molecule_indices"].tolist() == indices
    assert report["atom_indices"].tolist() == atoms
    assert report["atom_offsets"].shape == (len(expected) + 1,)
    assert report["molecule_indices"].dtype == np.int64
    assert report["atom_indices"].dtype == np.int64
    assert report["schema"] == "molsysmt.tpsa@1"
    assert report["chemical_state_index"] == 0
    assert report["parameters"]["hydrogen_treatment"] == "preserve_declared_inventory"


def test_quantity_default_and_explicit_sulfur_phosphorus_variant(view):
    method = view.addons.molsysmt.physchem.get_tpsa
    for enabled, expected in [(False, 34.14), (True, 42.52)]:
        result = method(selection=[2], include_sulfur_phosphorus=enabled)
        assert puw.is_quantity(result) and result.shape == (1,)
        np.testing.assert_allclose(
            puw.get_value(result, to_unit="angstrom**2"), [expected], atol=1e-12
        )


@pytest.mark.parametrize("selection", ["index >= 0", "index 0", "name ZZZX"])
def test_external_selectors_receive_group_free_native_support(view, selection):
    # Native #495 supplies target-only MDTraj hierarchy. The consumer must
    # receive a real successful result, without translating the selection.
    args = dict(selection=selection, syntax="MDTraj", return_report=True)
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    expected = msm.physchem.get_tpsa(view.molsys, **args)
    result = view.addons.molsysmt.physchem.get_tpsa(**args)
    same(result, expected)
    indices = (
        [] if selection == "name ZZZX" else [0] if selection == "index 0" else [0, 1, 2]
    )
    assert result["report"]["molecule_indices"].tolist() == indices
    if selection == "index 0":
        assert result["report"]["atom_indices"].tolist() == [0, 1, 2]

    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status() == status
    assert view.molsys.topology.n_groups == 0


def test_real_bundled_caffeine_reference_area():
    molecule = Chem.SDMolSupplier(
        msm.systems["caffeine"]["caffeine.sdf"], removeHs=False
    )[0]
    assert molecule is not None and molecule.GetNumAtoms() == 24
    with msv.new_view(molecule) as result:
        area = result.addons.molsysmt.physchem.get_tpsa()
        # Independent Ertl N/O fragment sum for the unchanged caffeine graph.
        np.testing.assert_allclose(
            puw.get_value(area, to_unit="angstrom**2"), [61.82], atol=1e-12
        )


@pytest.mark.parametrize("structures", ["all", [2, 0, 2], [1]])
def test_graph_descriptor_does_not_add_a_structure_axis(view, structures):
    result = view.addons.molsysmt.physchem.get_tpsa(structure_indices=structures)
    assert result.shape == (3,)
    np.testing.assert_allclose(
        puw.get_value(result, to_unit="angstrom**2"), [20.23, 9.23, 34.14], atol=1e-12
    )


def test_explicit_and_structure_associated_states_are_not_the_visible_frame():
    source = molecular_system("CC(=O)O")
    alternate = source.chemical_states._states[0].copy()
    alternate.state_id = "acetate"
    alternate.atom_attributes.loc[3, "formal_charge"] = -1
    alternate.atom_attributes.loc[3, "n_implicit_hydrogens"] = 0
    source.chemical_states._append_state(alternate)
    msm.set(source, structure_chemical_state_index=[0, 1, 0])
    with msv.new_view(source) as result:
        method = result.addons.molsysmt.physchem.get_tpsa
        for args, expected in [
            (dict(), 37.30),
            (dict(chemical_state=1), 40.13),
            (dict(chemical_state="structure", structure_indices=[2, 0, 2]), 37.30),
            (dict(chemical_state="structure", structure_indices=[1]), 40.13),
        ]:
            actual = method(**args, return_report=True)
            same(
                actual, msm.physchem.get_tpsa(result.molsys, **args, return_report=True)
            )
            np.testing.assert_allclose(
                puw.get_value(actual["tpsa"], to_unit="angstrom**2"),
                [expected],
                atol=1e-12,
            )
        with pytest.raises(msm.StructuralInconsistencyError):
            method(chemical_state="structure", structure_indices=[0, 1])
        assert result.molsys.chemical_states.reference_chemical_state_index == 0


@pytest.mark.parametrize(
    "args",
    [
        dict(element="bond"),
        dict(method="rdkit"),
        dict(selection=[999]),
        dict(structure_indices=[999]),
        dict(include_sulfur_phosphorus=1),
        dict(return_report="yes"),
    ],
)
def test_native_argument_rejection_preserves_scene(view, args):
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    with pytest.raises((msm.ArgumentError, ArgumentChoiceError)) as expected:
        msm.physchem.get_tpsa(view.molsys, **args)
    with pytest.raises(type(expected.value)):
        view.addons.molsysmt.physchem.get_tpsa(**args)
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status() == status


@pytest.mark.parametrize(
    "field", ["formal_charge", "n_implicit_hydrogens", "n_explicit_hydrogens"]
)
def test_missing_evidence_is_not_prepared_or_guessed(view, field):
    attrs = view.molsys.chemical_states._states[0].atom_attributes
    attrs[field] = None
    before, scene = attrs.copy(deep=True), view.export_state()
    with pytest.raises(msm.StructuralInconsistencyError):
        view.addons.molsysmt.physchem.get_tpsa()
    pd.testing.assert_frame_equal(attrs, before)
    assert view.export_state() == scene


def test_detached_report_values_and_metadata_preserve_source_and_scene(view):
    primary = view.molsys
    owners = (
        primary.topology,
        primary.structures,
        primary.chemical_states,
        primary.interactions["preserve"],
    )
    snapshots = [
        primary.topology.copy().atoms,
        primary.chemical_states._states[0].atom_attributes.copy(deep=True),
        primary.chemical_states._states[0].bonds.copy(deep=True),
    ]
    coordinates = puw.get_value(primary.structures.coordinates).copy()
    coverage, scene = deepcopy(owners[3].to_dict()), view.export_state()
    method = view.addons.molsysmt.physchem.get_tpsa
    first = method(return_report=True)
    first["tpsa"][:] *= 2
    first["report"]["molecule_indices"][:] = -1
    first["report"]["parameters"]["include_sulfur_phosphorus"] = "edited"
    next(
        x
        for x in first["report"]["attribution"]["items"]
        if x["id"] == "doi:10.1021/jm000942e"
    )["authors"].append("edited")
    second = method(return_report=True)
    assert second["report"]["molecule_indices"].tolist() == [0, 1, 2]
    assert second["report"]["parameters"]["include_sulfur_phosphorus"] is False
    assert (
        "edited"
        not in next(
            x
            for x in second["report"]["attribution"]["items"]
            if x["id"] == "doi:10.1021/jm000942e"
        )["authors"]
    )
    np.testing.assert_allclose(
        puw.get_value(second["tpsa"], to_unit="angstrom**2"),
        [20.23, 9.23, 34.14],
        atol=1e-12,
    )
    for old, current in zip(
        snapshots,
        [
            primary.topology.atoms,
            primary.chemical_states._states[0].atom_attributes,
            primary.chemical_states._states[0].bonds,
        ],
    ):
        pd.testing.assert_frame_equal(current, old)
    assert view.molsys is primary and all(
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
    np.testing.assert_array_equal(
        puw.get_value(primary.structures.coordinates), coordinates
    )
    same(primary.interactions["preserve"].to_dict(), coverage)
    assert view.export_state() == scene


def test_pending_read_no_implicit_sync_and_cached_method_follows_replacement(view):
    method = view.addons.molsysmt.physchem.get_tpsa
    view.addons.molsysmt.structure.translate(
        translation=puw.quantity([1, 0, 0], "nm"), in_place=True, update_view=False
    )
    status = view.addons.molsysmt.get_sync_status()
    method()
    assert (
        view.addons.molsysmt.get_sync_status() == status
        and status["state"] == "pending"
    )
    with pytest.raises(SystemEditPendingError):
        view.export_state()
    view.addons.molsysmt.sync_view()
    view.load(molecular_system("COC"), mode="replace")
    np.testing.assert_allclose(
        puw.get_value(method(), to_unit="angstrom**2"), [9.23], atol=1e-12
    )
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method()
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.physchem.get_tpsa(selection=[])


def test_real_optional_attribution_including_evaluated_empty_output(view):
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("bound TPSA"):
        with ackredit.scope("consumer.bound_tpsa"):
            result = view.addons.molsysmt.physchem.get_tpsa(return_report=True)
            empty = view.addons.molsysmt.physchem.get_tpsa(
                selection=[], return_report=True
            )
        assert "doi:10.1021/jm000942e" in ackredit.get_used_items()
        assert empty["tpsa"].shape == (0,)
        assert empty["report"]["atom_offsets"].tolist() == [0]
        assert "doi:10.1021/jm000942e" in {
            x["id"] for x in empty["report"]["attribution"]["items"]
        }
        assert (
            "molsysmt.physchem.get_tpsa"
            in ackredit.current_session().usage_tree["consumer.bound_tpsa"]["children"]
        )
        assert result["report"]["method"] == "ertl_rohde_selzer"


@pytest.mark.parametrize(
    "element", ["atom", "group", "component", "molecule", "chain", "entity", "system"]
)
def test_native_contribution_levels_are_forwarded_without_scene_changes(view, element):
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    kwargs = dict(element=element, return_report=True)
    native = msm.physchem.get_tpsa(view.molsys, **kwargs)
    received = view.addons.molsysmt.physchem.get_tpsa(**kwargs)
    same(received, native)
    assert received["report"]["element"] == element
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status() == status
