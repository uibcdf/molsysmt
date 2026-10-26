"""Receive native property tables without molecular preparation or scene edits."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm

puw = msm.pyunitwizard
NAMES = (
    "get_mass",
    "get_charge",
    "get_atomic_radius",
    "get_electronegativity",
    "get_hydrophobicity",
    "get_polarity",
    "get_transmembrane_tendency",
)
HYDROPHOBICITY = (
    "eisenberg",
    "rao",
    "sweet",
    "kyte",
    "abraham",
    "bull",
    "guy",
    "miyazawa",
    "roseman",
    "wolfenden",
    "chothia",
    "hopp",
    "manavalan",
    "black",
    "fauchere",
)
ATOMIC = {
    "get_mass": ("dalton", {"H": 1.008, "C": 12.011, "N": 14.007, "O": 15.999}),
    "get_atomic_radius": ("nm", {"H": 0.110, "C": 0.170, "N": 0.155, "O": 0.152}),
    "get_electronegativity": (
        "dimensionless",
        {"H": 2.20, "C": 2.55, "N": 3.04, "O": 3.44},
    ),
}


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as original:
        with msv.new_view(original.molsys, structure_indices=[0, 8, 3]) as result:
            analysis = msm.Interactions.from_records(
                [],
                n_atoms=result.molsys.get_n_atoms(),
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.physchem",
            )
            result.interactions.attach(analysis, name="preserve", assume_aligned=True)
            result.regions.add(selection=[0, 2, 4], tag="source")
            yield result


@pytest.fixture(scope="module")
def protein():
    # A real diverse protein: all group scales must be checked beyond polyalanine.
    with msv.demo["181L"] as result:
        yield result


def same(actual, expected):
    assert type(actual) is type(expected)
    if puw.is_quantity(actual):
        assert puw.get_unit(actual) == puw.get_unit(expected)
        np.testing.assert_allclose(
            puw.get_value(actual), puw.get_value(expected), equal_nan=True
        )
    else:
        np.testing.assert_equal(actual, expected)


@pytest.mark.parametrize("name", NAMES)
def test_signatures_digestion_help_and_no_unreviewed_alias(view, name):
    native = inspect.signature(getattr(msm.physchem, name))
    method = getattr(view.addons.molsysmt.physchem, name)
    assert inspect.signature(method) == native.replace(
        parameters=list(native.parameters.values())[1:]
    )
    assert method.digestion_plan is not None
    assert not hasattr(view.addons.molsysmt, name)
    assert "update_view" not in inspect.signature(method).parameters
    doc = inspect.getdoc(method)
    assert "current view.molsys" in doc and "not a scene object" in doc
    assert "\nmolecular_system :" not in doc
    assert "physchem" in dir(view.addons.molsysmt)
    assert set(NAMES) <= set(dir(view.addons.molsysmt.physchem))


@pytest.mark.parametrize("name", ATOMIC)
@pytest.mark.parametrize("selection", [[7, 1, 7, 4], "atom_type=='O'", []])
def test_atomic_values_selected_order_repeats_empty_and_units(view, name, selection):
    # Independent published constants, with native selection mapping retained.
    atom_types = msm.get(
        view.molsys, element="atom", selection=selection, atom_type=True
    )
    unit, reference = ATOMIC[name]
    actual = getattr(view.addons.molsysmt.physchem, name)(
        element="atom", selection=selection
    )
    assert puw.get_unit(actual).is_compatible_with(puw.unit(unit))
    np.testing.assert_allclose(
        puw.get_value(actual, to_unit=unit), [reference[t] for t in atom_types]
    )
    same(
        actual,
        getattr(msm.physchem, name)(view.molsys, element="atom", selection=selection),
    )


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
def test_native_unit_policy_is_not_replaced_by_addon_normalization(view, unit):
    with puw.context(
        standard_units=[unit, "ps", "radians", "dalton", "e", "dimensionless"]
    ):
        for name in ATOMIC:
            actual = getattr(view.addons.molsysmt.physchem, name)(
                element="atom", selection=[0, 3]
            )
            same(
                actual,
                getattr(msm.physchem, name)(
                    view.molsys, element="atom", selection=[0, 3]
                ),
            )
        # Atomic radius retains its native nm table unit under these contexts.
        assert puw.get_unit(
            view.addons.molsysmt.physchem.get_atomic_radius(selection=[0])
        ) == puw.unit("nm")


@pytest.mark.parametrize(
    "element", ["group", "component", "molecule", "chain", "entity", "system"]
)
def test_mass_hierarchy_sums_actual_atom_composition(view, element):
    groups = msm.get(
        view.molsys, element="atom" if element == "system" else element, atom_type=True
    )
    masses = ATOMIC["get_mass"][1]
    expected = (
        sum(masses[t] for t in groups)
        if element == "system"
        else [sum(masses[t] for t in ts) for ts in groups]
    )
    actual = view.addons.molsysmt.physchem.get_mass(element=element)
    np.testing.assert_allclose(puw.get_value(actual, to_unit="dalton"), expected)
    same(actual, msm.physchem.get_mass(view.molsys, element=element))


@pytest.mark.parametrize("definition", HYDROPHOBICITY)
def test_all_received_hydrophobicity_tables_preserve_native_values_and_container(
    protein, definition
):
    args = dict(
        selection="group_name in ['ALA', 'LYS', 'GLU', 'LEU']", definition=definition
    )
    actual = protein.addons.molsysmt.physchem.get_hydrophobicity(**args)
    same(actual, msm.physchem.get_hydrophobicity(protein.molsys, **args))
    assert type(actual) is np.ndarray and actual.size > 0


@pytest.mark.parametrize(
    "name,definition,reference",
    [
        ("get_hydrophobicity", "kyte", {"ALA": 1.8, "LYS": -3.9, "GLU": -3.5}),
        ("get_polarity", "grantham", {"ALA": 8.1, "LYS": 11.3, "GLU": 12.3}),
        ("get_polarity", "zimmerman", {"ALA": 0.0, "LYS": 49.5, "GLU": 49.9}),
        (
            "get_transmembrane_tendency",
            "zhao",
            {"ALA": 0.38, "LYS": -3.46, "GLU": -2.90},
        ),
        (
            "get_transmembrane_tendency",
            "senes",
            {
                "ALA": [-0.29, 10.22, 4.67],
                "LYS": [1.66, 11.11, 2.09],
                "GLU": [1.3, 14.66, 4.16],
            },
        ),
        ("get_charge", "physical_pH7", {"ALA": 0.0, "LYS": 1.0, "GLU": -1.0}),
    ],
)
def test_diverse_group_references_order_duplicates_and_native_shapes(
    protein, name, definition, reference
):
    indices = msm.select(
        protein.molsys, element="group", selection="group_name in ['ALA', 'LYS', 'GLU']"
    )
    assert (
        len(
            set(
                msm.get(
                    protein.molsys, element="group", selection=indices, group_name=True
                )
            )
        )
        == 3
    )
    selection = [int(indices[-1]), int(indices[0]), int(indices[-1]), int(indices[2])]
    names = msm.get(
        protein.molsys, element="group", selection=selection, group_name=True
    )
    args = dict(selection=selection, definition=definition)
    actual = getattr(protein.addons.molsysmt.physchem, name)(**args)
    expected = [reference[n] for n in names]
    values = puw.get_value(actual, to_unit="e") if name == "get_charge" else actual
    np.testing.assert_allclose(values, expected)
    same(actual, getattr(msm.physchem, name)(protein.molsys, **args))
    if name in {"get_polarity", "get_transmembrane_tendency"}:
        assert type(actual) is list


@pytest.mark.parametrize(
    "element", ["group", "component", "molecule", "chain", "entity", "system"]
)
@pytest.mark.parametrize("definition", ["physical_pH7", "collantes"])
def test_tabulated_charge_hierarchy_and_units(view, element, definition):
    # Collantes has no ACE/NME entries. Use a real extracted amino-acid system,
    # rather than silently inventing charge values for its terminal caps.
    with msv.new_view(
        msm.extract(view.molsys, selection="group_name=='ALA'")
    ) as selected:
        args = dict(element=element, definition=definition)
        actual = selected.addons.molsysmt.physchem.get_charge(**args)
        same(actual, msm.physchem.get_charge(selected.molsys, **args))
        assert puw.get_unit(actual).is_compatible_with(puw.unit("e"))
        if definition == "physical_pH7":
            np.testing.assert_equal(
                puw.get_value(actual), np.zeros_like(puw.get_value(actual))
            )


def test_protor_radius_delegates_native_without_hydrogen_preparation(view):
    args = dict(selection="atom_type!='H'", definition="protor")
    same(
        view.addons.molsysmt.physchem.get_atomic_radius(**args),
        msm.physchem.get_atomic_radius(view.molsys, **args),
    )


@pytest.mark.parametrize("name", NAMES)
def test_property_reads_preserve_primary_coordinates_scene_and_named_coverage(
    view, name
):
    primary = view.molsys
    structures, topology = primary.structures, primary.topology
    xyz = puw.get_value(msm.get(primary, element="atom", coordinates=True)).copy()
    analysis = primary.interactions["preserve"]
    coverage = analysis.to_dict()
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    args = dict(selection="group_name=='ALA'")
    actual = getattr(view.addons.molsysmt.physchem, name)(**args)
    same(actual, getattr(msm.physchem, name)(primary, **args))
    assert (
        view.molsys is primary
        and primary.structures is structures
        and primary.topology is topology
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(primary, element="atom", coordinates=True)), xyz
    )
    assert primary.interactions["preserve"] is analysis
    assert analysis.to_dict().keys() == coverage.keys()
    for key, value in coverage.items():
        if isinstance(value, np.ndarray):
            np.testing.assert_array_equal(analysis.to_dict()[key], value)
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )


@pytest.mark.parametrize(
    "name,args",
    [
        ("get_charge", dict(element="atom")),
        ("get_mass", dict(definition="OpenMM")),
        ("get_atomic_radius", dict(definition="missing")),
        ("get_electronegativity", dict(definition="missing")),
        ("get_hydrophobicity", dict(element="atom")),
        ("get_polarity", dict(definition="missing")),
        ("get_transmembrane_tendency", dict(definition="missing")),
        ("get_hydrophobicity", dict(selection="group_name=='ACE'")),
        ("get_polarity", dict(selection="group_name=='ACE'")),
        ("get_transmembrane_tendency", dict(selection="group_name=='ACE'")),
    ],
)
def test_native_rejections_are_not_silently_repaired(view, name, args):
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    with pytest.raises(Exception) as expected:
        getattr(msm.physchem, name)(view.molsys, **args)
    with pytest.raises(type(expected.value)):
        getattr(view.addons.molsysmt.physchem, name)(**args)
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )


@pytest.mark.parametrize("name", NAMES)
def test_reserved_primary_controls_empty_lifetime_and_replacement(view, name):
    facade = view.addons.molsysmt.physchem
    with pytest.raises(UnknownArgumentError):
        getattr(facade, name)(molecular_system=view.molsys)
    with pytest.raises(TypeError):
        getattr(facade, name)(molecular_system=view.molsys, skip_digestion=True)
    with msv.demo["dialanine"] as replacement:
        view.load(replacement.molsys, mode="replace")
        same(
            getattr(facade, name)(selection="group_name=='ALA'"),
            getattr(msm.physchem, name)(view.molsys, selection="group_name=='ALA'"),
        )
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt.physchem, name)()
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        getattr(facade, name)()


def test_readers_use_pending_scientific_primary_without_synchronizing(view):
    tools = view.addons.molsysmt
    tools.structure.translate(
        translation=puw.quantity([1, 0, 0], "nm"), in_place=True, update_view=False
    )
    pending = tools.get_sync_status()
    assert pending["state"] == "pending"
    for name in NAMES:
        args = dict(selection="group_name=='ALA'")
        same(
            getattr(tools.physchem, name)(**args),
            getattr(msm.physchem, name)(view.molsys, **args),
        )
    assert tools.get_sync_status() == pending
    tools.sync_view()


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("skip", [False, True])
def test_declared_skip_flag_and_explicit_selection_are_forwarded(view, name, skip):
    args = dict(selection="group_name=='ALA'", skip_digestion=skip)
    same(
        getattr(view.addons.molsysmt.physchem, name)(**args),
        getattr(msm.physchem, name)(view.molsys, **args),
    )


@pytest.mark.parametrize("name", NAMES)
def test_alternative_selection_syntax_keeps_native_result_or_rejection(view, name):
    args = dict(selection="name CA", syntax="MDTraj")
    try:
        expected = getattr(msm.physchem, name)(view.molsys, **args)
    except Exception as error:
        # Several native readers currently drop syntax internally. Preserve and
        # report that owner limitation rather than translating selectors here.
        with pytest.raises(type(error)):
            getattr(view.addons.molsysmt.physchem, name)(**args)
    else:
        same(getattr(view.addons.molsysmt.physchem, name)(**args), expected)


@pytest.mark.parametrize("element", ["atom", "group", "system"])
def test_explicit_openmm_charge_definition_has_independent_parameterized_output(
    view, element
):
    pytest.importorskip("openmm")
    # The native OpenMM converter requires a single-frame periodic box.
    # Extract explicitly; the addon never picks a frame on the user's behalf.
    with msv.new_view(msm.extract(view.molsys, structure_indices=[0])) as selected:
        state, status = (
            selected.export_state(),
            selected.addons.molsysmt.get_sync_status(),
        )
        args = dict(definition="OpenMM", forcefield="AMBER14", element=element)
        actual = selected.addons.molsysmt.physchem.get_charge(**args)
        same(actual, msm.physchem.get_charge(selected.molsys, **args))
        np.testing.assert_allclose(
            np.sum(puw.get_value(actual, to_unit="e")), 0.0, atol=1e-4
        )
        assert (
            selected.export_state() == state
            and selected.addons.molsysmt.get_sync_status() == status
        )


def test_multiframe_openmm_conversion_limit_is_not_hidden_by_frame_selection(view):
    pytest.importorskip("openmm")
    args = dict(definition="OpenMM", forcefield="AMBER14", element="atom")
    state = view.export_state()
    with pytest.raises(Exception) as expected:
        msm.physchem.get_charge(view.molsys, **args)
    with pytest.raises(type(expected.value)):
        view.addons.molsysmt.physchem.get_charge(**args)
    assert view.export_state() == state
