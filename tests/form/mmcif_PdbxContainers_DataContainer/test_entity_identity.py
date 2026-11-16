"""Preserve declared entity identity across revisits and category row order."""

from copy import deepcopy

import numpy as np
import pytest
from mmcif.api.DataCategory import DataCategory
from mmcif.api.PdbxContainers import DataContainer

import molsysmt as msm
from molsysmt._private.smonitor import FormatError

from .test_primary_occupancy import _as_file, _container


def source_with_entities(sites, entity_order, *, extra_entity=None):
    """Build explicit independent source labels, names and atom positions."""
    source = DataContainer("entity_identity")
    template = _container([[1.0, 1.0]]).getObj("atom_site")
    attributes = template.getAttributeList()
    columns = {name: index for index, name in enumerate(attributes)}
    rows = []
    for index, (chain, entity, group) in enumerate(sites):
        row = list(template.getRowList()[0])
        values = {
            "id": str(index + 1),
            "type_symbol": "O",
            "label_atom_id": "O",
            "auth_atom_id": "O",
            "label_comp_id": "HOH",
            "auth_comp_id": "HOH",
            "label_asym_id": chain,
            "auth_asym_id": chain,
            "label_entity_id": entity,
            "label_seq_id": str(group),
            "auth_seq_id": str(group),
            "Cartn_x": str(index * 3),
        }
        for name, value in values.items():
            row[columns[name]] = value
        rows.append(row)
    entities = list(entity_order)
    if extra_entity is not None:
        entities.append(extra_entity)
    chains = dict((chain, entity) for chain, entity, _ in sites)
    for name, attrs, data in (
        ("chem_comp", ["id", "type"], [["HOH", "NON-POLYMER"]]),
        (
            "entity",
            ["id", "type", "pdbx_description"],
            [[entity, "water", f"Declared {entity}"] for entity in entities],
        ),
        (
            "pdbx_entity_nonpoly",
            ["entity_id", "name", "comp_id"],
            [[entity, f"Declared {entity}", "HOH"] for entity in entities],
        ),
        ("struct_asym", ["id", "entity_id"], list(chains.items())),
        ("atom_site", attributes, rows),
    ):
        source.append(DataCategory(name, attributeNameList=attrs, rowList=data))
    return source


REVISIT = [("A", "10", 1), ("B", "2", 1), ("C", "10", 1), ("D", "42", 1)]


def test_repeated_entity_visit_does_not_reuse_an_existing_entity_index():
    source = source_with_entities(REVISIT, ["10", "2", "42"])
    result = msm.convert(source, get_missing_bonds=False)
    assert result.topology.entities.entity_id.tolist() == ["10", "2", "42"]
    assert list(msm.get(result, element="atom", entity_id=True)) == [
        "10",
        "2",
        "10",
        "42",
    ]


@pytest.mark.parametrize("target", ["molsysmt.MolSys", "molsysmt.Topology"])
@pytest.mark.parametrize("form", ["container", "cif", "cif.gz", "bcif", "bcif.gz"])
@pytest.mark.parametrize("reversed_metadata", [False, True])
@pytest.mark.parametrize(
    ("sites", "entities", "chains"),
    [
        (REVISIT, ["10", "2", "42"], ["A", "B", "C", "D"]),
        (
            [("A", "10", 1), ("B", "2", 1), ("A", "10", 2), ("C", "42", 1)],
            ["10", "2", "42"],
            ["A", "B", "C"],
        ),
        (
            [("A", "007", 1), ("B", "ligand", 1), ("C", "007", 1), ("D", "42", 1)],
            ["007", "ligand", "42"],
            ["A", "B", "C", "D"],
        ),
    ],
    ids=["entity-revisit", "chain-revisit", "textual-labels"],
)
def test_explicit_labels_and_metadata_survive_all_entry_routes(
    tmp_path, target, form, reversed_metadata, sites, entities, chains
):
    source = source_with_entities(
        sites, entities[::-1] if reversed_metadata else entities
    )
    before = {
        name: deepcopy(source.getObj(name).getRowList())
        for name in ["atom_site", "entity", "pdbx_entity_nonpoly", "struct_asym"]
    }
    item = source if form == "container" else _as_file(source, tmp_path, form)
    original_bytes = None if form == "container" else item.read_bytes()
    result = msm.convert(item, to_form=target, get_missing_bonds=False)
    topology = result.topology if target == "molsysmt.MolSys" else result
    assert topology.entities.entity_id.tolist() == entities
    assert topology.entities.entity_name.tolist() == [f"Declared {e}" for e in entities]
    assert topology.chains.chain_id.tolist() == chains
    assert list(msm.get(result, element="atom", entity_id=True)) == [
        s[1] for s in sites
    ]
    assert list(msm.get(result, element="atom", chain_id=True)) == [s[0] for s in sites]
    assert list(msm.get(result, element="atom", entity_name=True)) == [
        f"Declared {s[1]}" for s in sites
    ]
    assert topology.atoms.atom_id.tolist() == ["1", "2", "3", "4"]
    if target == "molsysmt.MolSys":
        assert result.structures.coordinates.shape == (1, 4, 3)
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(
                result.structures.coordinates, to_unit="angstrom"
            )[0],
            [[0, 0, 0], [3, 0, 0], [6, 0, 0], [9, 0, 0]],
        )
    for name, rows in before.items():
        assert source.getObj(name).getRowList() == rows
    if original_bytes is not None:
        assert item.read_bytes() == original_bytes


@pytest.mark.parametrize("target", ["molsysmt.MolSys", "molsysmt.Topology"])
@pytest.mark.parametrize("form", ["container", "cif", "cif.gz", "bcif", "bcif.gz"])
def test_unrepresented_entity_declarations_do_not_change_represented_axes(
    tmp_path, target, form
):
    source = source_with_entities(REVISIT, ["42", "10", "2"], extra_entity="unused")
    item = source if form == "container" else _as_file(source, tmp_path, form)
    result = msm.convert(item, to_form=target, get_missing_bonds=False)
    topology = result.topology if target == "molsysmt.MolSys" else result
    assert topology.entities.entity_id.tolist() == ["10", "2", "42"]
    assert "unused" not in topology.entities.entity_id.tolist()


@pytest.mark.parametrize("invalid", ["missing", "duplicate"])
def test_invalid_entity_declarations_fail_without_mutating_source(invalid):
    source = source_with_entities(REVISIT, ["10", "2", "42"])
    entity = source.getObj("entity")
    if invalid == "missing":
        entity.data.pop()
    else:
        entity.append(list(entity.data[0]))
    before = deepcopy(entity.getRowList())
    with pytest.raises(FormatError, match="entity"):
        msm.convert(source, get_missing_bonds=False)
    assert entity.getRowList() == before


def test_branched_entity_metadata_uses_its_chain_instead_of_the_entity_index():
    sites = [("A", "10", 1), ("B", "10", 1), ("C", "42", 1), ("D", "42", 1)]
    source = source_with_entities(sites, ["42", "10"])
    source.getObj("chem_comp").append(["NAG", "D-saccharide, beta linking"])
    entity = source.getObj("entity")
    entity.data[0][entity.getAttributeList().index("type")] = "branched"
    atoms = source.getObj("atom_site")
    for row in atoms.data[2:]:
        for name in ["label_comp_id", "auth_comp_id"]:
            row[atoms.getAttributeList().index(name)] = "NAG"
    result = msm.convert(source, get_missing_bonds=False)
    assert result.topology.entities.entity_id.tolist() == ["10", "42"]
    assert result.topology.entities.entity_type.tolist() == ["water", "monosaccharide"]
    assert list(msm.get(result, element="atom", entity_id=True)) == [
        "10",
        "10",
        "42",
        "42",
    ]
