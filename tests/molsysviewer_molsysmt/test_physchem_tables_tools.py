"""Receive raw reference descriptors and native ProtOr outputs without assignment."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm

puw = msm.pyunitwizard
NAMES = (
    "get_protor_atom_type",
    "get_protor_vdw_radius",
    "get_surface_area",
    "get_volume",
    "get_area_buried",
    "get_buried_fraction",
)
FIRST = {
    "get_mass",
    "get_charge",
    "get_atomic_radius",
    "get_electronegativity",
    "get_hydrophobicity",
    "get_polarity",
    "get_transmembrane_tendency",
}
TABLES = {
    "get_surface_area": (None, {"ALA": 62.90, "LYS": 102.78, "GLU": 30.19}),
    "get_volume": (np.ndarray, {"ALA": 31.0, "LYS": 119.0, "GLU": 83.0}),
    "get_area_buried": (np.ndarray, {"ALA": 86.6, "LYS": 115.5, "GLU": 113.9}),
    "get_buried_fraction": (list, {"ALA": 11.2, "LYS": 0.5, "GLU": 1.8}),
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
                method="receiving.physchem.tables",
            )
            result.interactions.attach(analysis, name="preserve", assume_aligned=True)
            result.regions.add(selection=[0, 2, 4], tag="source")
            yield result


@pytest.fixture(scope="module")
def protein():
    with msv.demo["181L"] as result:
        yield result


def same(actual, expected):
    assert type(actual) is type(expected)
    if puw.is_quantity(actual):
        assert puw.get_unit(actual) == puw.get_unit(expected)
        np.testing.assert_array_equal(puw.get_value(actual), puw.get_value(expected))
    elif isinstance(actual, tuple):
        assert len(actual) == len(expected)
        for a, e in zip(actual, expected):
            same(a, e)
    else:
        np.testing.assert_equal(actual, expected)


@pytest.mark.parametrize("name", NAMES)
def test_signatures_help_digestion_and_no_invented_scientific_inputs(view, name):
    native = inspect.signature(getattr(msm.physchem, name))
    expected = list(native.parameters.values())[1:]
    if name == "get_volume":
        expected.append(
            inspect.Parameter(
                "skip_digestion", inspect.Parameter.KEYWORD_ONLY, default=False
            )
        )
    method = getattr(view.addons.molsysmt.physchem, name)
    assert inspect.signature(method) == native.replace(parameters=expected)
    assert method.digestion_plan is not None
    assert not hasattr(view.addons.molsysmt, name)
    assert "update_view" not in inspect.signature(method).parameters
    doc = inspect.getdoc(method)
    assert "current view.molsys" in doc and "not a scene object" in doc
    assert "\nmolecular_system :" not in doc
    if name == "get_volume":
        assert "retains ordinary validation" in doc
    if name == "get_area_buried":
        assert "syntax" not in inspect.signature(method).parameters
    assert set(dir(view.addons.molsysmt.physchem)) == FIRST | set(NAMES) | {
        "get_sasa",
        "get_hydrogen_inventory",
        "get_chemical_readiness",
        "get_aromatic_rings",
        "get_aromaticity",
        "get_charge_centers",
        "get_hydrophobic_sites",
        "get_halogen_bond_sites",
        "get_bulkiness",
        "get_secondary_structure_propensity",
        "get_tpsa",
    }


@pytest.mark.parametrize("name", TABLES)
@pytest.mark.parametrize(
    "selection", ["group_name in ['ALA', 'LYS', 'GLU']", "indices", []]
)
def test_raw_reference_values_group_axes_containers_order_and_empty(
    protein, name, selection
):
    # These literal values receive forwarding and selection, not the physical
    # unit interpretation of every published reference table.
    if selection == "indices":
        groups = msm.select(
            protein.molsys,
            element="group",
            selection="group_name in ['ALA', 'LYS', 'GLU']",
        )
        selection = [int(groups[-1]), int(groups[0]), int(groups[-1]), int(groups[2])]
    names = msm.get(
        protein.molsys, element="group", selection=selection, group_name=True
    )
    actual = getattr(protein.addons.molsysmt.physchem, name)(selection=selection)
    container, reference = TABLES[name]
    if container is None:
        assert puw.is_quantity(actual)
        values = puw.get_value(actual, to_unit="angstrom**2")
    else:
        assert type(actual) is container and not puw.is_quantity(actual)
        values = actual
    np.testing.assert_allclose(values, [reference[n] for n in names])
    same(actual, getattr(msm.physchem, name)(protein.molsys, selection=selection))


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("skip", [False, True])
def test_skip_controls_preserve_native_validation_and_outputs(view, name, skip):
    args = dict(selection="group_name=='ALA'")
    if name != "get_volume":
        args["skip_digestion"] = skip
    expected = getattr(msm.physchem, name)(view.molsys, **args)
    actual = getattr(view.addons.molsysmt.physchem, name)(
        selection="group_name=='ALA'", skip_digestion=skip
    )
    same(actual, expected)


def test_protor_alanine_backbone_sidechain_hydrogen_rules_and_radius_units(view):
    args = dict(selection="group_name=='ALA'")
    types, provenance = view.addons.molsysmt.physchem.get_protor_atom_type(**args)
    radii = view.addons.molsysmt.physchem.get_protor_vdw_radius(**args)
    names, elements = msm.get(
        view.molsys,
        element="atom",
        selection=args["selection"],
        atom_name=True,
        atom_type=True,
    )
    reference = {
        "N": ("N3H1", "protein_backbone", 0.164),
        "CA": ("C4H1", "protein_backbone", 0.188),
        "C": ("C3H0", "protein_backbone", 0.161),
        "O": ("O1H0", "protein_backbone", 0.142),
        "CB": ("C4H3", "protein_heavy", 0.188),
    }
    assert types.shape == provenance.shape == (len(names),)
    assert types.dtype == provenance.dtype == np.dtype(object)
    assert puw.get_unit(radii) == puw.unit("nm")
    for index, (name, element) in enumerate(zip(names, elements)):
        expected = (None, "ignored", 0.11) if element == "H" else reference[name]
        assert types[index] == expected[0] and provenance[index] == expected[1]
        np.testing.assert_allclose(puw.get_value(radii)[index], expected[2])
    same((types, provenance), msm.physchem.get_protor_atom_type(view.molsys, **args))
    same(
        radii,
        view.addons.molsysmt.physchem.get_atomic_radius(definition="protor", **args),
    )


@pytest.mark.parametrize("name", ["get_protor_atom_type", "get_protor_vdw_radius"])
@pytest.mark.parametrize("selection", [[7, 1, 7, 4], [], "atom_type=='H'"])
def test_protor_selection_duplicates_empty_and_hydrogen_outputs(view, name, selection):
    same(
        getattr(view.addons.molsysmt.physchem, name)(selection=selection),
        getattr(msm.physchem, name)(view.molsys, selection=selection),
    )


def test_explicit_hydrogen_removal_does_not_change_heavy_protor_types(view):
    # A separate explicit extraction, never implicit preparation by the reader.
    with msv.new_view(msm.extract(view.molsys, selection="atom_type!='H'")) as heavy:
        for name in ["get_protor_atom_type", "get_protor_vdw_radius"]:
            same(
                getattr(view.addons.molsysmt.physchem, name)(
                    selection="atom_type!='H'"
                ),
                getattr(heavy.addons.molsysmt.physchem, name)(),
            )


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
def test_context_does_not_convert_raw_descriptors_or_native_protor_unit(view, unit):
    with puw.context(
        standard_units=[unit, "ps", "radians", "dalton", "e", "dimensionless"]
    ):
        for name in TABLES:
            same(
                getattr(view.addons.molsysmt.physchem, name)(
                    selection="group_name=='ALA'"
                ),
                getattr(msm.physchem, name)(view.molsys, selection="group_name=='ALA'"),
            )
        radii = view.addons.molsysmt.physchem.get_protor_vdw_radius()
        assert puw.get_unit(radii) == puw.unit("nm")


@pytest.mark.parametrize("name", TABLES)
@pytest.mark.parametrize(
    "args", [dict(definition="missing"), dict(selection="group_name=='ACE'")]
)
def test_table_rejections_are_not_converted_to_silent_defaults(view, name, args):
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    with pytest.raises(Exception) as expected:
        getattr(msm.physchem, name)(view.molsys, **args)
    with pytest.raises(type(expected.value)):
        getattr(view.addons.molsysmt.physchem, name)(**args)
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )


@pytest.mark.parametrize("name", [n for n in NAMES if n != "get_area_buried"])
def test_alternative_syntax_matches_intended_population(view, name):
    element = "atom" if name.startswith("get_protor") else "group"
    indices = msm.select(
        view.molsys, element=element, selection="name CA", syntax="MDTraj"
    )
    expected = getattr(msm.physchem, name)(view.molsys, selection=indices)
    actual = getattr(view.addons.molsysmt.physchem, name)(
        selection="name CA", syntax="MDTraj"
    )
    same(actual, expected)
    assert (
        len(actual[0] if name == "get_protor_atom_type" else actual)
        == len(indices)
        == 5
    )


@pytest.mark.parametrize("name", NAMES)
def test_reads_preserve_molecular_owners_scene_and_analysis(view, name):
    primary, structures, topology = (
        view.molsys,
        view.molsys.structures,
        view.molsys.topology,
    )
    xyz = puw.get_value(msm.get(primary, element="atom", coordinates=True)).copy()
    analysis = primary.interactions["preserve"]
    coverage = analysis.to_dict()
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    getattr(view.addons.molsysmt.physchem, name)(selection="group_name=='ALA'")
    assert (
        view.molsys is primary
        and primary.structures is structures
        and primary.topology is topology
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(primary, element="atom", coordinates=True)), xyz
    )
    assert primary.interactions["preserve"] is analysis
    for key, value in coverage.items():
        if isinstance(value, np.ndarray):
            np.testing.assert_array_equal(analysis.to_dict()[key], value)
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )


@pytest.mark.parametrize("name", NAMES)
def test_lifetime_reserved_primary_and_replacement(view, name):
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


def test_pending_reader_does_not_synchronize_or_replay_science(view):
    tools = view.addons.molsysmt
    tools.structure.translate(
        translation="[1, 0, 0] nm", in_place=True, update_view=False
    )
    status = tools.get_sync_status()
    assert status["state"] == "pending"
    for name in NAMES:
        same(
            getattr(tools.physchem, name)(selection="group_name=='ALA'"),
            getattr(msm.physchem, name)(view.molsys, selection="group_name=='ALA'"),
        )
    assert tools.get_sync_status() == status
    tools.sync_view()


@pytest.mark.parametrize(
    "name,element",
    [
        ("get_atomic_radius", "group"),
        ("get_electronegativity", "group"),
        ("get_hydrophobicity", "atom"),
        ("get_polarity", "atom"),
        ("get_transmembrane_tendency", "atom"),
        ("get_surface_area", "atom"),
        ("get_area_buried", "atom"),
        ("get_buried_fraction", "atom"),
    ],
)
@pytest.mark.parametrize("skip", [False, True])
def test_unsupported_levels_reject_before_interpreting_invalid_selection(
    view, name, element, skip
):
    from molsysmt._private.smonitor import ArgumentChoiceError

    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    with pytest.raises(ArgumentChoiceError):
        getattr(view.addons.molsysmt.physchem, name)(
            element=element,
            selection="this is not a valid selector",
            skip_digestion=skip,
        )
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )
