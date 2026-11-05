"""Keep source occupancies on the canonical atom and structure axes."""

import gzip
from copy import deepcopy

import numpy as np
import pytest
from mmcif.api.DataCategory import DataCategory
from mmcif.api.PdbxContainers import DataContainer
from mmcif.io import IoAdapter

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import MolecularSystemMismatchWarning
from molsysmt.native import MolSys


def _container(models, *, alternatives=False, omit_occupancy=False):
    source = DataContainer("occupancy")
    for name, attributes, rows in (
        ("chem_comp", ["id", "type"], [["LIG", "NON-POLYMER"]]),
        (
            "pdbx_entity_nonpoly",
            ["entity_id", "name", "comp_id"],
            [["1", "Ligand", "LIG"]],
        ),
        (
            "entity",
            ["id", "type", "pdbx_description"],
            [["1", "non-polymer", "Ligand"]],
        ),
        ("struct_asym", ["id", "entity_id"], [["A", "1"]]),
    ):
        source.append(DataCategory(name, attributeNameList=attributes, rowList=rows))
    attributes = [
        "group_PDB",
        "id",
        "type_symbol",
        "label_atom_id",
        "label_alt_id",
        "label_comp_id",
        "label_asym_id",
        "label_entity_id",
        "label_seq_id",
        "pdbx_PDB_ins_code",
        "Cartn_x",
        "Cartn_y",
        "Cartn_z",
        "occupancy",
        "B_iso_or_equiv",
        "pdbx_formal_charge",
        "auth_seq_id",
        "auth_comp_id",
        "auth_asym_id",
        "auth_atom_id",
        "pdbx_PDB_model_num",
    ]
    rows = []
    for model, occupancies in enumerate(models, start=1):
        names = ["C1", "C1", "O1"] if alternatives else ["C1", "O1"]
        labels = ["A", "B", "."] if alternatives else [".", "."]
        for site, (name, label, occupancy) in enumerate(
            zip(names, labels, occupancies)
        ):
            rows.append(
                [
                    "HETATM",
                    str(len(rows) + 1),
                    name[0],
                    name,
                    label,
                    "LIG",
                    "A",
                    "1",
                    "1",
                    "?",
                    str(10 * model + site),
                    "0",
                    "0",
                    str(occupancy),
                    str(20 + site),
                    "?",
                    "1",
                    "LIG",
                    "A",
                    name,
                    str(model),
                ]
            )
    if omit_occupancy:
        index = attributes.index("occupancy")
        attributes.pop(index)
        for row in rows:
            row.pop(index)
    source.append(DataCategory("atom_site", attributeNameList=attributes, rowList=rows))
    return source


def _as_file(source, tmp_path, suffix):
    filename = tmp_path / ("occupancy." + suffix.removesuffix(".gz"))
    assert IoAdapter().writeFile(
        str(filename),
        [source],
        fmt="bcif" if suffix.startswith("bcif") else "mmcif",
        applyTypes=False,
        useStringTypes=True,
        copyInputData=True,
    )
    if suffix.endswith(".gz"):
        compressed = tmp_path / ("occupancy." + suffix)
        compressed.write_bytes(gzip.compress(filename.read_bytes()))
        filename = compressed
    return filename


@pytest.mark.parametrize("form", ["container", "cif", "cif.gz", "bcif", "bcif.gz"])
def test_primary_occupancy_survives_native_conversion_and_axis_selection(
    tmp_path, form
):
    source = _container([[0.42, 1.0], [0.35, 0.7], [0.9, 0.55]])
    before = deepcopy(source.getObj("atom_site").getRowList())
    molecular_system = (
        source if form == "container" else _as_file(source, tmp_path, form)
    )
    original_bytes = None if form == "container" else molecular_system.read_bytes()
    result = msm.convert(molecular_system, to_form="molsysmt.MolSys")
    expected = np.array([[0.42, 1.0], [0.35, 0.7], [0.9, 0.55]])
    assert result.structures.occupancy.dtype.kind == "f"
    np.testing.assert_allclose(result.structures.occupancy, expected)
    selected = msm.convert(
        molecular_system,
        to_form="molsysmt.MolSys",
        selection=[1, 0],
        structure_indices=[2, 0, 2],
    )
    # Conversion follows native MolSys extraction's sorted atom order.
    np.testing.assert_allclose(selected.structures.occupancy, expected[[2, 0, 2]])
    observed = msm.get(
        molecular_system,
        element="atom",
        selection=[1, 0],
        structure_indices=[2, 0, 2],
        occupancy=True,
    )
    np.testing.assert_allclose(observed, expected[[2, 0, 2]][:, [1, 0]])
    np.testing.assert_allclose(
        puw.get_value(selected.structures.coordinates, to_unit="angstrom")[:, :, 0],
        [[30, 31], [10, 11], [30, 31]],
    )
    assert source.getObj("atom_site").getRowList() == before
    if original_bytes is not None:
        assert molecular_system.read_bytes() == original_bytes


def test_atom_subset_and_direct_getter_follow_their_declared_axes():
    source = _container([[0.0, 0.42], [0.8, 0.6], [0.3, 1.0]])
    selected = msm.convert(source, selection=[1], structure_indices=[2, 0, 2])
    assert selected.topology.atoms["atom_name"].tolist() == ["O1"]
    np.testing.assert_allclose(selected.structures.occupancy, [[1.0], [0.42], [1.0]])
    from molsysmt.form.mmcif_PdbxContainers_DataContainer import get_occupancy_from_atom

    observed = get_occupancy_from_atom(
        source, indices=[1, 0, 1], structure_indices=[2, 0, 2]
    )
    np.testing.assert_allclose(
        observed, [[1.0, 0.3, 1.0], [0.42, 0.0, 0.42], [1.0, 0.3, 1.0]]
    )


def test_primary_b_factor_query_uses_selected_structure_order():
    source = _container([[0.3, 0.7, 0.8], [0.9, 0.1, 0.6]], alternatives=True)
    observed = msm.get(
        source,
        element="atom",
        selection=[0],
        structure_indices=[1, 0, 1],
        b_factor=True,
    )
    np.testing.assert_allclose(
        puw.get_value(observed, to_unit="angstrom**2"), [[20], [21], [20]]
    )


@pytest.mark.parametrize("target", ["molsysmt.MolSys", "molsysmt.Structures"])
def test_alternate_sites_are_canonicalized_separately_in_each_structure(target):
    source = _container([[0.3, 0.7, 0.8], [0.9, 0.1, 0.6]], alternatives=True)
    before = deepcopy(source.getObj("atom_site").getRowList())
    result = msm.convert(source, to_form=target)
    structures = result.structures if target == "molsysmt.MolSys" else result
    np.testing.assert_allclose(structures.occupancy, [[0.7, 0.8], [0.9, 0.6]])
    np.testing.assert_allclose(
        puw.get_value(structures.coordinates, to_unit="angstrom")[:, :, 0],
        [[11, 12], [20, 22]],
    )
    np.testing.assert_allclose(
        puw.get_value(structures.b_factor, to_unit="angstrom**2"), [[21, 22], [20, 22]]
    )
    for index, expected in enumerate(([0.3, 0.7], [0.9, 0.1])):
        np.testing.assert_allclose(
            structures.alternate_location[index][0]["occupancy"], expected
        )
        assert structures.alternate_location[index][0]["location_id"].tolist() == [
            "A",
            "B",
        ]
    assert source.getObj("atom_site").getRowList() == before


def test_alternate_models_keep_their_explicit_chemical_graph():
    source = _container([[0.8, 0.2, 1.0], [0.3, 0.7, 0.6]], alternatives=True)
    source.append(
        DataCategory(
            "chem_comp_bond",
            attributeNameList=["comp_id", "atom_id_1", "atom_id_2", "value_order"],
            rowList=[["LIG", "C1", "O1", "DOUB"]],
        )
    )
    result = msm.convert(source)
    assert isinstance(result, MolSys)
    assert result.topology.n_groups == 1
    np.testing.assert_allclose(result.structures.occupancy, [[0.8, 1.0], [0.7, 0.6]])
    assert msm.get(result, element="bond", bonded_atom_pairs=True) == [[0, 1]]
    assert msm.get(result, element="bond", bond_order=True) == [2.0]


def test_different_model_inventories_are_still_returned_separately():
    source = _container([[0.8, 0.2, 1.0], [0.3, 0.7, 0.6]], alternatives=True)
    category = source.getObj("atom_site")
    category.setValue("N1", "label_atom_id", 5)
    category.setValue("N1", "auth_atom_id", 5)
    category.setValue("N", "type_symbol", 5)
    with pytest.warns(MolecularSystemMismatchWarning):
        results = msm.convert(source)
    assert isinstance(results, list) and len(results) == 2
    assert results[0].topology.atoms["atom_name"].tolist() == ["C1", "O1"]
    assert results[1].topology.atoms["atom_name"].tolist() == ["C1", "N1"]
    np.testing.assert_allclose(results[0].structures.occupancy, [[0.8, 1.0]])
    np.testing.assert_allclose(results[1].structures.occupancy, [[0.7, 0.6]])


@pytest.mark.parametrize(
    "fixture",
    ["hp35_cif_file", "hp35_cif_gz_file", "hp35_bcif_file", "hp35_bcif_gz_file"],
)
def test_bundled_coordinate_file_retains_its_declared_occupancies(fixture, request):
    filename = request.getfixturevalue(fixture)
    source = msm.convert(filename, to_form="mmcif.PdbxContainers.DataContainer")
    category = source.getObj("atom_site")
    columns = {name: index for index, name in enumerate(category.getAttributeList())}
    source_values = {
        str(row[columns["id"]]): float(row[columns["occupancy"]]) for row in category
    }
    result = msm.convert(filename)
    expected = [[source_values[label] for label in result.topology.atoms["atom_id"]]]
    assert result.structures.occupancy.shape == (1, 596)
    np.testing.assert_allclose(result.structures.occupancy, expected)


@pytest.mark.parametrize("unknown", ["?", "."])
def test_missing_occupancy_keeps_unknown_cells_without_inventing_full_occupancy(
    unknown,
):
    result = msm.convert(_container([[unknown, 0.42]]), to_form="molsysmt.MolSys")
    np.testing.assert_allclose(
        result.structures.occupancy, [[np.nan, 0.42]], equal_nan=True
    )


@pytest.mark.parametrize("omit_occupancy", [False, True])
def test_wholly_missing_occupancy_remains_unavailable(omit_occupancy):
    result = msm.convert(
        _container([["?", "."]], omit_occupancy=omit_occupancy),
        to_form="molsysmt.MolSys",
    )
    assert result.structures.occupancy is None


@pytest.mark.parametrize(
    "occupancies,expected_x,expected_occupancy",
    [(["?", 0.4, 1.0], 11, 0.4), (["?", ".", 1.0], 10, np.nan)],
)
def test_unknown_alternate_occupancy_retains_source_evidence(
    occupancies, expected_x, expected_occupancy
):
    result = msm.convert(
        _container([occupancies], alternatives=True), to_form="molsysmt.MolSys"
    )
    np.testing.assert_allclose(
        result.structures.occupancy, [[expected_occupancy, 1.0]], equal_nan=True
    )
    assert puw.get_value(result.structures.coordinates, to_unit="angstrom")[
        0, 0, 0
    ] == pytest.approx(expected_x)
    variants = result.structures.alternate_location[0][0]
    assert np.isnan(variants["occupancy"][0])
    assert variants["location_id"].tolist() == ["A", "B"]


def test_primary_and_alternate_occupancies_round_trip_h5msm(tmp_path):
    source = _container([[0.2, 0.8, 0.6], [0.9, 0.1, 0.5]], alternatives=True)
    result = msm.convert(source, to_form="molsysmt.MolSys")
    filename = tmp_path / "occupancies.h5msm"
    msm.convert(result, to_form=str(filename))
    restored = msm.convert(filename, to_form="molsysmt.MolSys")
    np.testing.assert_allclose(restored.structures.occupancy, [[0.8, 0.6], [0.9, 0.5]])
    for index, values in enumerate(([0.2, 0.8], [0.9, 0.1])):
        np.testing.assert_allclose(
            restored.structures.alternate_location[index][0]["occupancy"], values
        )


def test_tied_alternates_without_label_a_use_source_order():
    source = _container([[0.5, 0.5, 1.0]], alternatives=True)
    category = source.getObj("atom_site")
    category.setValue("C", "label_alt_id", 0)
    category.setValue("B", "label_alt_id", 1)
    result = msm.convert(source)
    np.testing.assert_allclose(result.structures.occupancy, [[0.5, 1.0]])
    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="angstrom")[:, :, 0],
        [[10, 12]],
    )
    assert result.structures.alternate_location[0][0]["location_id"].tolist() == [
        "C",
        "B",
    ]


def test_unknown_alternate_label_is_not_an_alternate_site():
    source = _container([[0.0, 0.42]])
    source.getObj("atom_site").setValue("?", "label_alt_id", 0)
    result = msm.convert(source)
    np.testing.assert_allclose(result.structures.occupancy, [[0.0, 0.42]])
    assert result.structures.alternate_location is None


def test_nondefault_units_keep_observations_and_geometry_aligned(tmp_path):
    source = _container([[0.3, 0.7, 0.6], [0.9, 0.1, 0.8]], alternatives=True)
    filename = tmp_path / "nondefault.h5msm"
    with puw.context(standard_units=["pm", "fs", "kJ/mol", "K"]):
        result = msm.convert(source)
        msm.convert(result, to_form=str(filename))
        restored = msm.convert(filename)
    np.testing.assert_allclose(restored.structures.occupancy, [[0.7, 0.6], [0.9, 0.8]])
    np.testing.assert_allclose(
        puw.get_value(restored.structures.coordinates, to_unit="angstrom")[:, :, 0],
        [[11, 12], [20, 22]],
    )
    np.testing.assert_allclose(
        puw.get_value(
            restored.structures.alternate_location[1][0]["coordinates"],
            to_unit="angstrom",
        )[:, 0],
        [20, 21],
    )
