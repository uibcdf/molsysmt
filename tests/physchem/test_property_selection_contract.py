"""Resolve advertised syntax and element axes against independently named populations."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentChoiceError, UnknownGroupInTableError

# Literal controls distinguish both atom types and group labels. These test the
# selected tabulated assignment, not chemical validation of a complete peptide.
TOOLS = [
    ("get_atomic_radius", "atom", "vdw", [0.155, 0.170, 0.152] * 3, "nm", "quantity"),
    (
        "get_atomic_radius",
        "atom",
        "protor",
        [0.164, 0.188, 0.142] * 3,
        "nm",
        "quantity",
    ),
    (
        "get_electronegativity",
        "atom",
        "pauling",
        [3.04, 2.55, 3.44] * 3,
        "dimensionless",
        "quantity",
    ),
    ("get_hydrophobicity", "group", "eisenberg", [-1.5, 0.62, -0.74], None, "array"),
    ("get_charge", "group", "physical_pH7", [1.0, 0.0, -1.0], "e", "quantity"),
    ("get_charge", "group", "collantes", [0.53, 0.05, 1.31], "e", "quantity"),
    ("get_polarity", "group", "grantham", [11.3, 8.1, 12.3], None, "list"),
    ("get_transmembrane_tendency", "group", "zhao", [-3.46, 0.38, -2.9], None, "list"),
    ("get_volume", "group", "grantham", [119.0, 31.0, 83.0], None, "array"),
    ("get_surface_area", "group", "collantes", [102.78, 62.9, 30.19], None, "list"),
    ("get_area_buried", "group", "rose", [115.5, 86.6, 113.9], None, "array"),
    ("get_buried_fraction", "group", "janin", [0.5, 11.2, 1.8], None, "list"),
]


def system(form):
    builder = msm.MolSysBuilder()
    for group in ["LYS", "ALA", "GLU"]:
        atoms = [
            builder.add_atom(atom_name=name, atom_type=element)
            for name, element in [("N", "N"), ("CA", "C"), ("O", "O")]
        ]
        builder.add_group(atoms, group_name=group)
        builder.add_bond(atoms[0], atoms[1])
        builder.add_bond(atoms[1], atoms[2])
    builder.set_coordinates(
        puw.quantity(np.arange(27, dtype=float).reshape(1, 9, 3) / 10, "nm")
    )
    molsys = builder.build()
    return molsys if form == "molsys" else molsys.topology


def topology(source):
    return source.topology if msm.get_form(source) == "molsysmt.MolSys" else source


def snapshot(source):
    t = topology(source)
    return t.atoms.copy(deep=True), t.groups.copy(deep=True), t.bonds.copy(deep=True)


def unchanged(source, before):
    t = topology(source)
    for current, previous in zip([t.atoms, t.groups, t.bonds], before):
        pd.testing.assert_frame_equal(current, previous)


def population(element, mode):
    size = 9 if element == "atom" else 3
    if mode == "default":
        return {}, list(range(size))
    if mode == "all":
        return {"selection": "all"}, list(range(size))
    if mode == "empty":
        return {"selection": []}, []
    if mode == "indices":
        axis = [8, 0, 4, 8] if element == "atom" else [2, 0, 2]
        return {"selection": axis}, axis
    if element == "atom":
        indices = [1, 2, 4, 5, 7, 8]
        expression = (
            "name CA or name O"
            if mode == "mdtraj"
            else 'atom_name=="CA" or atom_name=="O"'
        )
    else:
        indices = [0, 2]
        expression = (
            "resname LYS or resname GLU"
            if mode == "mdtraj"
            else 'group_name=="LYS" or group_name=="GLU"'
        )
    return {
        "selection": expression,
        "syntax": "MDTraj" if mode == "mdtraj" else "MolSysMT",
    }, indices


@pytest.mark.parametrize(
    "tool,element,definition,table,unit,container,mode",
    [
        (*tool, mode)
        for tool in TOOLS
        for mode in ["default", "all", "empty", "indices", "molsysmt", "mdtraj"]
        if not (tool[0] == "get_area_buried" and mode == "mdtraj")
    ],
)
@pytest.mark.parametrize("form", ["molsys", "topology"])
@pytest.mark.parametrize("length_unit", ["nm", "pm"])
def test_property_uses_exact_selected_axis_and_retains_container_units(
    tool, element, definition, table, unit, container, form, mode, length_unit
):
    if mode == "mdtraj":
        pytest.importorskip("mdtraj")
    source = system(form)
    before = snapshot(source)
    kwargs, indices = population(element, mode)
    # These explicit indices are the fixture's intended population, independently
    # checked against the public selector before invoking the property reader.
    actual_indices = msm.select(source, element=element, **kwargs)
    np.testing.assert_array_equal(actual_indices, indices)
    with puw.context(standard_units=[length_unit, "fs", "coulomb"]):
        arguments = dict(definition=definition, **kwargs)
        if tool != "get_volume":
            arguments["element"] = element
        if tool == "get_area_buried":
            # This API has no syntax parameter. Default MolSysMT strings and
            # explicit group indices remain its declared contract.
            assert arguments.pop("syntax", "MolSysMT") == "MolSysMT"
        result = getattr(msm.physchem, tool)(source, **arguments)
    if container == "quantity":
        assert puw.is_quantity(result)
        assert puw.are_compatible(result, unit)
        observed = puw.get_value(result, to_unit=unit)
    else:
        assert type(result) is (list if container == "list" else np.ndarray)
        observed = np.asarray(result)
    assert np.shape(observed) == (len(indices),)
    np.testing.assert_allclose(observed, np.asarray(table)[indices], rtol=0, atol=1e-12)
    unchanged(source, before)


@pytest.mark.parametrize(
    "tool,definition,requested",
    [
        (tool, definition, requested)
        for tool, supported, definition, *_ in TOOLS
        if tool not in {"get_charge", "get_volume"}
        for requested in [
            "atom",
            "group",
            "component",
            "molecule",
            "chain",
            "entity",
            "system",
            "bond",
        ]
        if requested != supported
    ],
)
@pytest.mark.parametrize("selection", [[1], "deliberately invalid selector"])
def test_unsupported_property_scope_is_rejected_before_population_lookup(
    tool, definition, requested, selection
):
    source = system("molsys")
    before = snapshot(source)
    with pytest.raises(ArgumentChoiceError, match="element"):
        getattr(msm.physchem, tool)(
            source, element=requested, definition=definition, selection=selection
        )
    unchanged(source, before)


@pytest.mark.parametrize(
    "tool,definition",
    [
        ("get_hydrophobicity", "eisenberg"),
        ("get_polarity", "grantham"),
        ("get_transmembrane_tendency", "zhao"),
        ("get_charge", "physical_pH7"),
        ("get_charge", "collantes"),
        ("get_volume", "grantham"),
        ("get_surface_area", "collantes"),
        ("get_buried_fraction", "janin"),
    ],
)
@pytest.mark.parametrize("syntax", ["MolSysMT", "MDTraj"])
def test_unknown_group_still_raises_the_public_table_diagnostic(
    tool, definition, syntax
):
    if syntax == "MDTraj":
        pytest.importorskip("mdtraj")
    source = system("molsys")
    source.topology.groups.loc[1, "group_name"] = "UNK"
    before = snapshot(source)
    expression = "resname UNK" if syntax == "MDTraj" else 'group_name=="UNK"'
    with pytest.raises(UnknownGroupInTableError):
        getattr(msm.physchem, tool)(
            source, selection=expression, syntax=syntax, definition=definition
        )
    unchanged(source, before)


def test_direct_protor_tools_resolve_the_same_explicit_selector():
    pytest.importorskip("mdtraj")
    source = system("topology")
    kinds, provenance = msm.physchem.get_protor_atom_type(
        source, selection="name CA or name O", syntax="MDTraj"
    )
    assert kinds.tolist() == ["C4H1", "O1H0"] * 3
    assert provenance.tolist() == ["protein_backbone"] * 6
    radii = msm.physchem.get_protor_vdw_radius(
        source, selection="name CA or name O", syntax="MDTraj"
    )
    np.testing.assert_allclose(puw.get_value(radii, to_unit="nm"), [0.188, 0.142] * 3)


@pytest.mark.parametrize(
    "definition,table",
    [("physical_pH7", [1.0, 0.0, -1.0]), ("collantes", [0.53, 0.05, 1.31])],
)
@pytest.mark.parametrize(
    "selection,syntax,indices",
    [
        ([2, 0, 2], "MolSysMT", [2, 0, 2]),
        ("resname LYS or resname GLU", "MDTraj", [0, 2]),
    ],
)
def test_tabulated_charge_retains_component_selection_and_aggregation(
    definition, table, selection, syntax, indices
):
    if syntax == "MDTraj":
        pytest.importorskip("mdtraj")
    source = system("molsys")
    observed = msm.physchem.get_charge(
        source,
        element="component",
        selection=selection,
        syntax=syntax,
        definition=definition,
    )
    np.testing.assert_allclose(
        puw.get_value(observed, to_unit="e"), np.array(table)[indices]
    )


def test_area_buried_unknown_group_preserves_its_default_selection_contract():
    source = system("molsys")
    source.topology.groups.loc[1, "group_name"] = "UNK"
    with pytest.raises(UnknownGroupInTableError):
        msm.physchem.get_area_buried(source, selection='group_name=="UNK"')


@pytest.mark.parametrize("definition", ["physical_pH7", "collantes", "OpenMM"])
def test_charge_rejects_an_unsupported_bond_population_before_calculation(definition):
    with pytest.raises(ArgumentChoiceError, match="element"):
        msm.physchem.get_charge(
            system("molsys"),
            element="bond",
            selection="deliberately invalid selector",
            definition=definition,
        )
