"""Receive stored-chemistry reports without preparation or scene publication."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError
from molsysviewer.system_edits import SystemEditPendingError

import molsysmt as msm

puw = msm.pyunitwizard
NAMES = ("get_hydrogen_inventory", "get_chemical_readiness")


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as original:
        with msv.new_view(original.molsys, structure_indices=[0, 8, 3]) as result:
            result.interactions.attach(
                msm.Interactions.from_records(
                    [],
                    n_atoms=result.molsys.get_n_atoms(),
                    n_structures=3,
                    evaluated_structure_indices=[0, 1, 2],
                    method="receiving.chemistry",
                ),
                name="preserve",
                assume_aligned=True,
            )
            result.regions.add(selection=[0, 2, 4], tag="source")
            yield result


@pytest.fixture
def ligand():
    # A real bundled SDF with declared connectivity and ten indexed hydrogens.
    with msv.new_view(msm.systems["caffeine"]["caffeine.sdf"]) as result:
        yield result


def same(actual, expected):
    assert type(actual) is type(expected)
    np.testing.assert_equal(actual, expected)


@pytest.mark.parametrize("name", NAMES)
def test_signature_help_digestion_and_reserved_controls(view, name):
    method = getattr(view.addons.molsysmt.physchem, name)
    native = inspect.signature(getattr(msm.physchem, name))
    assert inspect.signature(method) == native.replace(
        parameters=list(native.parameters.values())[1:]
    )
    assert method.digestion_plan is not None
    assert not hasattr(view.addons.molsysmt, name)
    assert "update_view" not in inspect.signature(method).parameters
    doc = inspect.getdoc(method)
    assert "current view.molsys" in doc and "detached stored-chemistry report" in doc
    assert "not a scene object" in doc and "does not substitute" in doc
    assert "\nmolecular_system :" not in doc
    for kwargs in [
        dict(molecular_system=view.molsys),
        dict(update_view=False),
        dict(prepare=True),
    ]:
        with pytest.raises(UnknownArgumentError):
            method(**kwargs)
        with pytest.raises(TypeError):
            method(**kwargs, skip_digestion=True)


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("structures", [[2], [0, 0], [1]])
@pytest.mark.parametrize(
    "selection,syntax",
    [
        ([7, 1, 7, 4], "MolSysMT"),
        ([], "MolSysMT"),
        ("atom_name=='CA'", "MolSysMT"),
    ],
)
def test_native_selection_deduplication_structure_scope_and_syntax(
    view, name, structures, selection, syntax
):
    args = dict(selection=selection, syntax=syntax, structure_indices=structures)
    actual = getattr(view.addons.molsysmt.physchem, name)(**args)
    same(actual, getattr(msm.physchem, name)(view.molsys, **args))
    expected = np.unique(msm.select(view.molsys, selection=selection, syntax=syntax))
    np.testing.assert_array_equal(actual["atom_indices"], expected)
    assert actual["atom_indices"].dtype == np.int64
    assert actual["structure_index"] == structures[0]
    if not len(expected):
        key = (
            "parent_hydrogen_pairs"
            if name == "get_hydrogen_inventory"
            else "bonded_atom_pairs"
        )
        assert actual[key].shape == (0, 2) and actual[key].dtype == np.int64
        if name == "get_hydrogen_inventory":
            assert actual["status"] == "empty"
        else:
            assert all(
                field["status"] == "empty" for field in actual["fields"].values()
            )


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "args",
    [
        dict(),
        dict(structure_indices=[2, 0]),
        dict(structure_indices=[]),
        dict(structure_indices=[999]),
        dict(chemical_state=999),
        dict(selection=[-1]),
    ],
)
def test_native_rejection_is_not_hidden_by_current_frame_or_skip(
    view, name, skip, args
):
    parameters = dict(structure_indices=[1], skip_digestion=skip)
    parameters.update(args)
    # The bare default deliberately requests all three structures and must fail.
    if not args:
        parameters.pop("structure_indices")
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    with pytest.raises(Exception) as expected:
        getattr(msm.physchem, name)(view.molsys, **parameters)
    with pytest.raises(type(expected.value)):
        getattr(view.addons.molsysmt.physchem, name)(**parameters)
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )


def test_caffeine_unknown_counts_are_not_filled_or_certified(ligand):
    inventory = ligand.addons.molsysmt.physchem.get_hydrogen_inventory()
    assert inventory["schema"] == "molsysmt.hydrogen_inventory@1"
    assert inventory["status"] == "unassessed"
    assert inventory["indexed_hydrogen_counts"].sum() == 10
    np.testing.assert_array_equal(
        inventory["explicit_hydrogen_atom_indices"], np.arange(14, 24)
    )
    for key in ["missing_hydrogen_counts", "total_hydrogen_counts"]:
        assert inventory[key].dtype == np.int64 and np.all(inventory[key] == -1)
    assert {"valence", "protonation"} <= set(inventory["unassessed_checks"])
    readiness = ligand.addons.molsysmt.physchem.get_chemical_readiness()
    assert (
        readiness["schema"] == "molsysmt.chemical_readiness@1"
        and "ready" not in readiness
    )
    assert readiness["chemical_state_status"] == "resolved"
    assert readiness["fields"]["formal_charge"]["status"] == "present"
    assert readiness["fields"]["n_implicit_hydrogens"]["status"] == "missing"
    assert readiness["fields"]["coordinates"]["unit"] == "nm"
    assert readiness["fields"]["formal_charge"]["unit"] == "elementary_charge"
    assert readiness["fields"]["coordinates"]["values"].tolist() == [True] * 24
    assert "docking_readiness" in readiness["unassessed_checks"]


def test_declared_zero_virtual_inventory_and_external_hydrogen_parent_pairs(ligand):
    primary = ligand.molsys
    msm.set(primary, element="atom", n_implicit_hydrogens=0, n_explicit_hydrogens=0)
    symbols = np.asarray(msm.get(primary, element="atom", atom_type=True))
    bonds = primary.topology.bonds[["atom1_index", "atom2_index"]].to_numpy(
        dtype=np.int64
    )
    pairs = []
    for a, b in bonds:
        if (symbols[a] == "H") != (symbols[b] == "H"):
            pairs.append((int(b), int(a)) if symbols[a] == "H" else (int(a), int(b)))
    expected = np.asarray(pairs, dtype=np.int64).reshape(-1, 2)
    counts = np.bincount(expected[:, 0], minlength=len(symbols))
    all_atoms = ligand.addons.molsysmt.physchem.get_hydrogen_inventory()
    assert all_atoms["status"] == "available"
    np.testing.assert_array_equal(all_atoms["parent_hydrogen_pairs"], expected)
    np.testing.assert_array_equal(all_atoms["indexed_hydrogen_counts"], counts)
    np.testing.assert_array_equal(all_atoms["total_hydrogen_counts"], counts)
    parent = int(counts.argmax())
    selected = ligand.addons.molsysmt.physchem.get_hydrogen_inventory(
        selection=[parent]
    )
    np.testing.assert_array_equal(
        selected["parent_hydrogen_pairs"], expected[expected[:, 0] == parent]
    )
    assert selected["indexed_hydrogen_counts"].tolist() == [3]
    assert selected["explicit_hydrogen_atom_indices"].size == 0
    # Virtual H annotations are additional, not a substitute for indexed neighbors.
    msm.set(
        primary,
        element="atom",
        selection=[parent],
        n_implicit_hydrogens=2,
        n_explicit_hydrogens=1,
    )
    selected = ligand.addons.molsysmt.physchem.get_hydrogen_inventory(
        selection=[parent]
    )
    assert selected["missing_hydrogen_counts"].tolist() == [3]
    assert selected["total_hydrogen_counts"].tolist() == [6]
    assert "protonation" in selected["unassessed_checks"]


def test_readiness_incident_crossing_bonds_preserve_source_indices(ligand):
    pairs = ligand.molsys.topology.bonds[["atom1_index", "atom2_index"]].to_numpy(
        dtype=np.int64
    )
    selected = np.array([0, 2], dtype=np.int64)
    incident = np.isin(pairs, selected).any(axis=1)
    boundary = incident & ~np.isin(pairs, selected).all(axis=1)
    actual = ligand.addons.molsysmt.physchem.get_chemical_readiness(selection=[2, 0, 2])
    np.testing.assert_array_equal(actual["atom_indices"], selected)
    np.testing.assert_array_equal(actual["bond_indices"], np.flatnonzero(incident))
    np.testing.assert_array_equal(actual["bonded_atom_pairs"], pairs[incident])
    np.testing.assert_array_equal(
        actual["connectivity"]["crossing_bond_indices"], np.flatnonzero(boundary)
    )
    assert boundary.any()


@pytest.mark.parametrize("name", NAMES)
def test_reports_are_detached_and_source_scene_domains_and_analysis_are_preserved(
    view, name
):
    primary = view.molsys
    owners = (
        primary.topology,
        primary.structures,
        primary.chemical_states,
        primary.interactions["preserve"],
    )
    chemical = msm.convert(
        primary.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    ).to_dict()
    coordinates = puw.get_value(msm.get(primary, coordinates=True)).copy()
    coverage = owners[3].to_dict()
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    actual = getattr(view.addons.molsysmt.physchem, name)(structure_indices=[1])
    expected = getattr(msm.physchem, name)(primary, structure_indices=[1])
    same(actual, expected)
    actual["atom_indices"][:] = -1
    actual["unassessed_checks"].append("modified_detached_result")
    if name == "get_chemical_readiness":
        actual["fields"]["coordinates"]["values"][:] = False
        actual["bonded_atom_pairs"][:] = -1
    else:
        actual["total_hydrogen_counts"][:] = 999
        actual["parent_hydrogen_pairs"][:] = -1
        actual["issues"].clear()
    same(getattr(view.addons.molsysmt.physchem, name)(structure_indices=[1]), expected)
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
        chemical,
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(primary, coordinates=True)), coordinates
    )
    np.testing.assert_equal(owners[3].to_dict(), coverage)
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("skip", [False, True])
def test_explicit_state_and_structure_associations_remain_native(view, name, skip):
    primary = view.molsys
    primary.chemical_states.append_state()
    msm.set(
        primary,
        element="atom",
        chemical_state=1,
        formal_charge=0,
        n_implicit_hydrogens=0,
        n_explicit_hydrogens=0,
    )
    msm.set(primary, element="system", structure_chemical_state_index=[0, 1, None])
    args = dict(
        structure_indices=[1, 1], chemical_state="structure", skip_digestion=skip
    )
    actual = getattr(view.addons.molsysmt.physchem, name)(**args)
    same(actual, getattr(msm.physchem, name)(primary, **args))
    assert actual["chemical_state_index"] == 1 and actual["structure_index"] == 1
    if name == "get_chemical_readiness":
        assert actual["fields"]["formal_charge"]["values"].tolist() == [0] * 62
    unresolved = getattr(view.addons.molsysmt.physchem, name)(
        structure_indices=[2], chemical_state="structure", skip_digestion=skip
    )
    assert unresolved["chemical_state_index"] is None
    if name == "get_chemical_readiness":
        assert unresolved["chemical_state_status"] == "unassociated"
    primary.chemical_states._set_reference_index(None)
    ambiguous = getattr(view.addons.molsysmt.physchem, name)(
        structure_indices=[0], skip_digestion=skip
    )
    assert ambiguous["chemical_state_index"] is None
    explicit = getattr(view.addons.molsysmt.physchem, name)(
        structure_indices=[0], chemical_state=1, skip_digestion=skip
    )
    assert explicit["chemical_state_index"] == 1
    assert primary.chemical_states.reference_chemical_state_index is None


@pytest.mark.parametrize("name", NAMES)
def test_pending_primary_is_read_without_projecting_or_clearing_pending(view, name):
    tools = view.addons.molsysmt
    tools.structure.translate(
        translation=puw.quantity([1, 0, 0], "nm"), in_place=True, update_view=False
    )
    status = tools.get_sync_status()
    assert status["state"] == "pending"
    with pytest.raises(SystemEditPendingError):
        view.export_state()
    args = dict(structure_indices=[2], selection=[7, 1, 7])
    same(
        getattr(tools.physchem, name)(**args),
        getattr(msm.physchem, name)(view.molsys, **args),
    )
    assert tools.get_sync_status() == status
    with pytest.raises(SystemEditPendingError):
        view.export_state()


@pytest.mark.parametrize("name", NAMES)
def test_cached_facade_replacement_empty_and_closed_lifetime(view, name):
    facade = view.addons.molsysmt.physchem
    with msv.demo["dialanine"] as replacement:
        view.load(replacement.molsys, mode="replace")
        same(
            getattr(facade, name)(structure_indices=[0]),
            getattr(msm.physchem, name)(view.molsys, structure_indices=[0]),
        )
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt.physchem, name)()
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        getattr(facade, name)()


@pytest.mark.parametrize("structure", [0, 1, 2])
def test_inventory_external_syntax_reports_intended_population(view, structure):
    args = dict(selection="name CA", syntax="MDTraj", structure_indices=[structure])
    actual = view.addons.molsysmt.physchem.get_hydrogen_inventory(**args)
    indices = msm.select(view.molsys, selection="atom_name=='CA'")
    expected = msm.physchem.get_hydrogen_inventory(
        view.molsys, selection=indices, structure_indices=[structure]
    )
    same(actual, expected)
    assert len(actual["atom_indices"]) == 5


def test_native_readiness_external_syntax_limitation_is_forwarded(view):
    # Native reference resolution currently turns reference into integer 0,
    # which the common selector rejects with external syntax. Do not repair it
    # in the wrapper; uibcdf/molsysmt#480 and its receiving remain separate work.
    args = dict(selection="name CA", syntax="MDTraj", structure_indices=[2])
    with pytest.raises(msm.ArgumentError) as expected:
        msm.physchem.get_chemical_readiness(view.molsys, **args)
    with pytest.raises(type(expected.value)):
        view.addons.molsysmt.physchem.get_chemical_readiness(**args)


@pytest.mark.parametrize("length_unit", ["nm", "angstrom", "pm"])
def test_coordinate_coverage_units_are_explicit_and_not_raw_positions(
    ligand, length_unit
):
    with puw.context(
        standard_units=[length_unit, "ps", "radians", "dalton", "e", "dimensionless"]
    ):
        result = ligand.addons.molsysmt.physchem.get_chemical_readiness()
    assert result["fields"]["coordinates"]["unit"] == "nm"
    assert result["fields"]["coordinates"]["values"].tolist() == [True] * 24
    assert result["fields"]["formal_charge"]["unit"] == "elementary_charge"


def test_nonfinite_position_is_reported_without_repair_or_scene_update(view):
    primary = view.molsys
    coordinates = puw.get_value(primary.structures.coordinates, to_unit="nm").copy()
    coordinates[1, 2, 0] = np.nan
    # Deliberately edit the native array outside managed publication, then audit.
    # The reader does not observe arbitrary edits or publish a repaired scene.
    primary.structures.coordinates = puw.quantity(coordinates, "nm")
    status = view.addons.molsysmt.get_sync_status()
    result = view.addons.molsysmt.physchem.get_chemical_readiness(
        selection=[2], structure_indices=[1]
    )
    assert result["fields"]["coordinates"]["status"] == "conflict"
    assert result["fields"]["coordinates"]["conflict_indices"].tolist() == [2]
    assert result["fields"]["coordinates"]["values"].tolist() == [False]
    assert np.isnan(puw.get_value(primary.structures.coordinates)[1, 2, 0])
    assert view.addons.molsysmt.get_sync_status() == status


def test_parent_selection_does_not_mask_global_indexed_hydrogen_conflict(ligand):
    msm.set(
        ligand.molsys, element="atom", n_implicit_hydrogens=0, n_explicit_hydrogens=0
    )
    msm.set(ligand.molsys, element="atom", selection=[14], n_explicit_hydrogens=1)
    result = ligand.addons.molsysmt.physchem.get_hydrogen_inventory(selection=[0])
    assert result["status"] == "conflict"
    assert any(
        issue["reason_code"] == "invalid_indexed_hydrogen" and issue["atom_index"] == 14
        for issue in result["issues"]
    )
    assert result["atom_indices"].tolist() == [0]
