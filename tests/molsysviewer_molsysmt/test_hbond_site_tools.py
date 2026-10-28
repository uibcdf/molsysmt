"""Receive hydrogen-bond recognition and local hypotheses without scene effects."""

import inspect
from copy import deepcopy

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError
from molsysviewer.system_edits import SystemEditPendingError
from rdkit import Chem

import molsysmt as msm
from molsysmt._private.smonitor import StructuralInconsistencyError

puw = msm.pyunitwizard
LEGACY = ("get_donor_atoms", "get_acceptor_atoms")
MODERN = ("get_hbond_sites", "get_hbond_site_directions")
NAMES = LEGACY + MODERN


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
        for first, second in zip(actual, expected):
            same(first, second)
    else:
        np.testing.assert_equal(actual, expected)


def system(smiles="CC=O", coordinates=None):
    # Explicit source fixture, without embedding or preparation inside the addon.
    molecule = Chem.MolFromSmiles(smiles)
    if coordinates is None:
        coordinates = [[0, 1, 0], [0, 0, 0], [1, 0, 0]]
    conformer = Chem.Conformer(molecule.GetNumAtoms())
    for atom, position in enumerate(coordinates):
        conformer.SetAtomPosition(atom, tuple(float(value) for value in position))
    molecule.AddConformer(conformer)
    source = msm.convert(molecule)
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm")
    source.structures.append(
        coordinates=puw.quantity(
            np.concatenate([xyz + [1, 0, 0], xyz + [0, 1, 0]]), "nm"
        ),
        structure_id=[20, 70],
    )
    return source


@pytest.fixture
def view():
    with msv.new_view(system()) as result:
        result.regions.add(selection=[2], tag="oxygen")
        result.interactions.attach(
            msm.Interactions.from_records(
                [],
                n_atoms=3,
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.hbond.sites",
            ),
            name="preserve",
            assume_aligned=True,
        )
        yield result


def call(view, name, *, native=False, **kwargs):
    if native:
        return getattr(msm.interactions.hbonds, name)(view.molsys, **kwargs)
    return getattr(view.addons.molsysmt.interactions.hbonds, name)(**kwargs)


def kwargs_for(name):
    if name == "get_hbond_site_directions":
        return dict(structure_indices=[2, 0, 2], pbc=False)
    if name == "get_hbond_sites":
        return dict(structure_indices=[2, 0, 2])
    return {}


def test_hydrogen_free_custom_donor_receives_native_empty_pair_contract(view):
    before = view.export_state()
    arguments = dict(
        inclusion_rules=("atom_type=='O'",),
        default_inclusion_rules=False,
        default_exclusion_rules=False,
    )
    expected = call(view, "get_donor_atoms", native=True, **arguments)
    actual = call(view, "get_donor_atoms", **arguments)
    assert actual.shape == expected.shape == (0, 2)
    assert actual.dtype == expected.dtype == np.dtype(np.int64)
    assert view.export_state() == before


@pytest.mark.parametrize("name", NAMES)
def test_nested_explicit_signatures_help_and_no_unreceived_detectors(view, name):
    core = view.interactions
    tools = view.addons.molsysmt.interactions
    assert set(dir(tools)) == {
        "hbonds",
        "disulfides",
        "ionic",
        "hydrophobic",
        "halogen_bonds",
    }
    assert set(NAMES).issubset(dir(tools.hbonds))
    assert core is view.interactions and tools is not core
    assert not hasattr(tools, "metal_coordination")
    assert not hasattr(view.addons.molsysmt, name)
    method = getattr(tools.hbonds, name)
    signature = inspect.signature(getattr(msm.interactions.hbonds, name))
    parameters = list(signature.parameters.values())[1:]
    if name in LEGACY:
        parameters.append(
            inspect.Parameter(
                "skip_digestion", inspect.Parameter.KEYWORD_ONLY, default=False
            )
        )
        assert "receives no such keyword" in inspect.getdoc(method)
    assert inspect.signature(method) == signature.replace(parameters=parameters)
    assert method.digestion_plan is not None
    assert "current view.molsys" in inspect.getdoc(method)
    assert "not a scene object" in inspect.getdoc(method)
    for kwargs in [
        dict(molecular_system=view.molsys),
        dict(update_view=False),
        dict(prepare=True),
    ]:
        with pytest.raises(UnknownArgumentError):
            method(**kwargs)


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("skip", [False, True])
def test_native_result_and_primary_chemistry_source_scene_preserved(view, name, skip):
    primary = view.molsys
    before = view.export_state()
    atoms = primary.topology.atoms.copy(deep=True)
    state = primary.chemical_states._states[0]
    bonds = state.bonds.copy(deep=True)
    attrs = state.atom_attributes.copy(deep=True)
    xyz = puw.get_value(primary.structures.coordinates).copy()
    analysis = primary.interactions["preserve"]
    coverage = deepcopy(analysis.to_dict())
    args = kwargs_for(name)
    actual = call(view, name, **args, skip_digestion=skip)
    if name in MODERN:
        args["skip_digestion"] = skip
    same(actual, call(view, name, native=True, **args))
    assert view.molsys is primary and view.export_state() == before
    assert primary.interactions["preserve"] is analysis
    same(analysis.to_dict(), coverage)
    pd.testing.assert_frame_equal(atoms, primary.topology.atoms)
    pd.testing.assert_frame_equal(bonds, state.bonds)
    pd.testing.assert_frame_equal(attrs, state.atom_attributes)
    np.testing.assert_array_equal(xyz, puw.get_value(primary.structures.coordinates))


@pytest.mark.parametrize("name", NAMES)
def test_numeric_expression_empty_native_selection(view, name):
    for selection in [[2, 2], "atom_index==2", []]:
        args = dict(kwargs_for(name), selection=selection)
        same(call(view, name, **args), call(view, name, native=True, **args))
    result = call(view, name, **dict(kwargs_for(name), selection=[]))
    if name == "get_hbond_site_directions":
        assert result["directions"].shape == (0, 3)
        assert result["status"].shape == (3, 0)
        assert result["status"].dtype == np.uint8
        assert result["image_offsets"].tolist() == [0]
    elif name == "get_hbond_sites":
        assert result["donor_hydrogen_pairs"].shape == (0, 2)
        assert result["acceptor_atom_indices"].dtype == np.int64
    else:
        assert result.shape == ((0, 2) if name == "get_donor_atoms" else (0,))


def test_carbonyl_independent_local_angles_units_and_repeated_source_positions(view):
    method = view.addons.molsysmt.interactions.hbonds.get_hbond_site_directions
    with puw.context(standard_units=["angstrom", "ps", "e"]):
        result = method(structure_indices=[2, 0, 2], pbc=False, heavy_mode="force")
    expected = np.tile([[0.5, np.sqrt(3) / 2, 0], [0.5, -np.sqrt(3) / 2, 0]], (3, 1))
    np.testing.assert_allclose(result["directions"], expected, atol=1e-14)
    np.testing.assert_allclose(
        np.linalg.norm(result["directions"], axis=1), 1, atol=1e-14
    )
    assert result["evaluated_structure_indices"].tolist() == [2, 0, 2]
    assert result["direction_structure_indices"].tolist() == [2, 2, 0, 0, 2, 2]
    assert result["direction_structure_positions"].tolist() == [0, 0, 1, 1, 2, 2]
    assert result["direction_indices"].tolist() == [0, 1, 0, 1, 0, 1]
    assert result["status"].tolist() == [[1], [1], [1]]
    np.testing.assert_allclose(
        puw.get_value(result["origins"], to_unit="angstrom"),
        [[1, 10, 0], [1, 10, 0], [1, 0, 0], [1, 0, 0], [1, 10, 0], [1, 10, 0]],
    )
    assert result["units"]["origins"] == str(puw.get_unit(result["origins"]))
    eager = method(structure_indices=[2, 0, 2], pbc=False, heavy_mode="off")
    np.testing.assert_allclose(eager["directions"], result["directions"])


@pytest.mark.parametrize(
    "box", [np.eye(3), np.array([[1, 0, 0], [0.2, 1, 0], [0.1, 0.2, 1]])]
)
def test_periodic_support_images_reconstruct_selected_anchor_and_external_support(box):
    source = system()
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    shifts = np.array([[1, -1, 0], [0, 1, 0], [-1, 0, 0]])
    wrapped = xyz + shifts @ box
    source.structures.coordinates = puw.quantity(wrapped * 10, "angstrom")
    source.structures.box = puw.quantity(
        np.repeat(box[None], 3, axis=0) * 10, "angstrom"
    )
    with msv.new_view(source) as view:
        result = call(
            view,
            "get_hbond_site_directions",
            selection=[2],
            structure_indices=[0],
            pbc=True,
        )
        np.testing.assert_allclose(
            result["directions"],
            [[0.5, np.sqrt(3) / 2, 0], [0.5, -np.sqrt(3) / 2, 0]],
            atol=1e-13,
        )
        assert result["support_atom_indices"].tolist() == [2, 1, 0]
        images = shifts[2] - shifts[[2, 1, 0]]
        np.testing.assert_array_equal(result["image_vectors"], np.tile(images, (2, 1)))
        reconstructed = wrapped[0, [2, 1, 0]] + result["image_vectors"][:3] @ box
        np.testing.assert_allclose(
            reconstructed - reconstructed[0], xyz[0, [2, 1, 0]] - xyz[0, 2], atol=1e-13
        )


def water_system():
    # Declare complete bond chemistry explicitly in the fixture. A bare builder
    # bond table is insufficient for the modern chemical-graph contract.
    molecule = Chem.AddHs(Chem.MolFromSmiles("O"))
    conformer = Chem.Conformer(3)
    for atom, position in enumerate([[0, 0, 0], [1, 0, 0], [0, 1, 0]]):
        conformer.SetAtomPosition(atom, tuple(position))
    molecule.AddConformer(conformer)
    return msm.convert(molecule)


def test_indexed_hydrogens_and_native_legacy_selection_contract_stay_distinct():
    with msv.new_view(water_system()) as view:
        tools = view.addons.molsysmt.interactions.hbonds
        assert tools.get_donor_atoms(selection=[0]).tolist() == [[0, 1], [0, 2]]
        assert tools.get_hbond_sites(selection=[0], assume_complete_connectivity=True)[
            "donor_hydrogen_pairs"
        ].shape == (0, 2)
        sites = tools.get_hbond_sites(
            selection=[0, 1], assume_complete_connectivity=True
        )
        assert sites["donor_hydrogen_pairs"].tolist() == [[0, 1]]
        assert sites["acceptor_atom_indices"].tolist() == [0]
        # Water's acceptor direction is explicitly unsupported, not an invented axis.
        result = tools.get_hbond_site_directions(
            site_method="elemental_nitrogen_oxygen",
            pbc=False,
            assume_complete_connectivity=True,
        )
        assert result["site_roles"].tolist() == [0, 0, 1]
        assert result["status"].tolist() == [[1, 1, 0]]
        np.testing.assert_allclose(result["directions"], [[1, 0, 0], [0, 1, 0]])


@pytest.mark.parametrize(
    "method",
    [
        "elemental_nitrogen_oxygen",
        "elemental_fluorine_oxygen_nitrogen",
        "smarts_donor_acceptor",
    ],
)
def test_recognition_rules_remain_scientifically_distinct(method):
    source = system("NC(=O)N", [[-1, 0, 0], [0, 0, 0], [0, 1, 0], [1, 0, 0]])
    with msv.new_view(source) as view:
        result = call(view, "get_hbond_sites", method=method)
        same(result, call(view, "get_hbond_sites", method=method, native=True))
        assert result["acceptor_atom_indices"].tolist() == (
            [2] if method == "smarts_donor_acceptor" else [0, 2, 3]
        )
        assert result["donor_hydrogen_pairs"].shape == (0, 2)


@pytest.mark.parametrize("name", LEGACY)
def test_native_custom_tuple_rules_and_flags_are_forwarded(name):
    with msv.new_view(water_system()) as view:
        args = dict(
            inclusion_rules=("atom_type=='O'",),
            exclusion_rules=(),
            default_inclusion_rules=False,
            default_exclusion_rules=False,
        )
        actual = call(view, name, **args)
        same(actual, call(view, name, native=True, **args))
        assert (
            args["inclusion_rules"] == ("atom_type=='O'",)
            and args["exclusion_rules"] == ()
        )
        assert actual.tolist() == (
            [0] if name == "get_acceptor_atoms" else [[0, 1], [0, 2]]
        )


@pytest.mark.parametrize("name", MODERN)
def test_external_selection_numeric_equivalence_and_explicit_state_scope(view, name):
    same(
        call(
            view, name, **dict(kwargs_for(name), selection="index 2", syntax="MDTraj")
        ),
        call(view, name, **dict(kwargs_for(name), selection=[2])),
    )
    state = view.molsys.chemical_states._states[0].copy()
    view.molsys.chemical_states._append_state(state)
    msm.set(view.molsys, structure_chemical_state_index=[1, 0, 1])
    args = dict(structure_indices=[2, 0], chemical_state="structure")
    if name == "get_hbond_site_directions":
        args["pbc"] = False
    assert call(view, name, **args)["chemical_state_index"] == 1
    with pytest.raises(StructuralInconsistencyError):
        call(view, name, **dict(args, structure_indices=[0, 1]))
    assert view.molsys.chemical_states.reference_chemical_state_index == 0


@pytest.mark.parametrize("name", MODERN)
def test_missing_connectivity_rejects_without_an_implicit_assumption(view, name):
    view.molsys.chemical_states._states[0].connectivity_completeness = "partial"
    with pytest.raises(StructuralInconsistencyError):
        call(view, name, **kwargs_for(name))
    result = call(
        view, name, **dict(kwargs_for(name), assume_complete_connectivity=True)
    )
    assert result["assume_complete_connectivity"]


@pytest.mark.parametrize(
    "name,kwargs",
    [
        (name, args)
        for name in MODERN
        for args in [dict(method="unknown"), dict(max_matches=0)]
    ]
    + [
        ("get_hbond_site_directions", dict(structure_indices=frames))
        for frames in [[-1], [3]]
    ],
)
def test_native_rejection_types_and_no_scene_side_effects(view, name, kwargs):
    before = view.export_state()
    with pytest.raises(Exception) as expected:
        call(view, name, native=True, **kwargs)
    with pytest.raises(type(expected.value)):
        call(view, name, **kwargs)
    assert view.export_state() == before


@pytest.mark.parametrize("name", MODERN)
def test_returned_arrays_and_bibliography_are_independent_from_source_and_later_calls(
    view, name
):
    args = kwargs_for(name)
    baseline = call(view, name, **args)
    changed = call(view, name, **args)

    def edit(value):
        if isinstance(value, dict):
            for child in value.values():
                edit(child)
        elif isinstance(value, np.ndarray) and value.size and value.dtype.kind in "ifu":
            value.flat[0] = 0
        elif isinstance(value, list):
            for child in value:
                edit(child)
            value.append("changed")

    edit(changed)
    same(call(view, name, **args), baseline)


@pytest.mark.parametrize("name", NAMES)
def test_pending_primary_replacement_empty_closed_and_core_owner(view, name):
    method = getattr(view.addons.molsysmt.interactions.hbonds, name)
    core = view.interactions
    view.addons.molsysmt.structure.translate(
        translation="[1, 0, 0] nm", in_place=True, update_view=False
    )
    pending = view.addons.molsysmt.get_sync_status()
    method(**kwargs_for(name))
    assert (
        view.addons.molsysmt.get_sync_status() == pending
        and pending["state"] == "pending"
    )
    assert view.interactions is core
    with pytest.raises(SystemEditPendingError):
        view.export_state()
    view.addons.molsysmt.sync_view()
    view.load(system("C#N", [[0, 0, 0], [1, 0, 0]]), mode="replace")
    same(method(**kwargs_for(name)), call(view, name, native=True, **kwargs_for(name)))
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method(**kwargs_for(name))
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt.interactions.hbonds, name)()


def test_real_pentalanine_preserves_literal_covalent_hydrogen_membership():
    with msv.demo["pentalanine"] as view:
        tools = view.addons.molsysmt.interactions.hbonds
        pairs = tools.get_donor_atoms()
        assert len(pairs) > 0
        bonds = {
            frozenset(pair)
            for pair in msm.get(view.molsys, inner_bonded_atom_pairs=True)
        }
        kinds = msm.get(view.molsys, element="atom", atom_type=True)
        assert all(
            kinds[d] in {"O", "N"} and kinds[h] == "H" and frozenset([d, h]) in bonds
            for d, h in pairs
        )
        same(
            tools.get_acceptor_atoms(),
            msm.interactions.hbonds.get_acceptor_atoms(view.molsys),
        )


def test_undefined_carbonyl_geometry_has_status_without_a_fabricated_direction():
    with msv.new_view(system(coordinates=[[2, 0, 0], [0, 0, 0], [1, 0, 0]])) as view:
        result = call(view, "get_hbond_site_directions", pbc=False)
        assert result["status"].tolist() == [[2], [2], [2]]
        assert result["directions"].shape == (0, 3)
        assert result["origins"].shape == (0, 3)


def test_legacy_interleaved_pair_membership_is_not_column_sorted():
    builder = msm.MolSysBuilder()
    for name, kind in [("N1", "N"), ("H2", "H"), ("N2", "N"), ("H1", "H")]:
        builder.add_atom(atom_name=name, atom_type=kind)
    builder.add_group([0, 1, 2, 3], group_name="ALA")
    builder.add_bond(0, 3)
    builder.add_bond(2, 1)
    builder.set_coordinates(puw.quantity(np.arange(12).reshape(4, 3), "angstrom"))
    with msv.new_view(builder.build()) as view:
        assert call(view, "get_donor_atoms").tolist() == [[0, 3], [2, 1]]
