"""Native metadata reads retain labelled inventories and unknown memberships."""

import pandas as pd
import pytest

import molsysmt as msm


def _snapshot(topology):
    return {
        name: getattr(topology, name).copy(deep=True)
        for name in ["atoms", "groups", "molecules", "entities", "chains"]
    }, (topology._molecules_dirty, topology._entities_dirty)


def _assert_unchanged(topology, snapshot):
    tables, flags = snapshot
    for name, expected in tables.items():
        pd.testing.assert_frame_equal(getattr(topology, name), expected)
    assert (topology._molecules_dirty, topology._entities_dirty) == flags


@pytest.mark.parametrize("native", [False, True])
@pytest.mark.parametrize("topology_only", [False, True])
@pytest.mark.parametrize("summary", [False, True])
@pytest.mark.parametrize("mode", ["missing", "dirty", "atom_free"])
def test_counts_and_summaries_preserve_the_complete_declared_inventory(
    partial_declared_inventory_molsys, native, topology_only, summary, mode
):
    molsys = partial_declared_inventory_molsys
    topology = molsys.topology
    if mode == "dirty":
        topology.groups["molecule_index"] = pd.array([0, 2], dtype="Int64")
        topology.molecules["entity_index"] = pd.array([0, 2, 3], dtype="Int64")
        topology._molecules_dirty = topology._entities_dirty = True
    elif mode == "atom_free":
        # Keep declared parent rows even when there are no represented atoms.
        from molsysmt.native import MolSys

        molsys = MolSys(n_molecules=3, n_entities=4)
        topology = molsys.topology
    source = topology if topology_only else molsys
    before = _snapshot(topology)
    if summary:
        result = (
            source.info(output_type="dictionary")
            if native
            else msm.info(source, output_type="dictionary")
        )[0]
    else:
        options = dict(n_molecules=True, n_entities=True, output_type="dictionary")
        result = source.get(**options) if native else msm.get(source, **options)
    assert result["n_molecules"] == 3
    assert result["n_entities"] == 4
    _assert_unchanged(topology, before)


@pytest.mark.parametrize("topology_only", [False, True])
@pytest.mark.parametrize("element,index", [("molecule", 2), ("entity", 3)])
def test_public_selection_preflight_does_not_reconstruct_parents(
    partial_declared_inventory_molsys, topology_only, element, index
):
    molsys = partial_declared_inventory_molsys
    topology = molsys.topology
    source = topology if topology_only else molsys
    before = _snapshot(topology)
    assert msm.select(source, element=element, selection=[index, 0, index]) == [
        index,
        0,
        index,
    ]
    _assert_unchanged(topology, before)


@pytest.mark.parametrize("topology_only", [False, True])
@pytest.mark.parametrize("element,index", [("molecule", 2), ("entity", 3)])
def test_public_label_edit_uses_existing_positions_without_reconstruction(
    partial_declared_inventory_molsys, topology_only, element, index
):
    molsys = partial_declared_inventory_molsys
    topology = molsys.topology
    source = topology if topology_only else molsys
    before = _snapshot(topology)
    msm.set(
        source, element=element, selection=[index], **{element + "_name": "new-label"}
    )
    # Only the explicitly addressed label changes; inventory and correspondence stay fixed.
    table = "molecules" if element == "molecule" else "entities"
    before[0][table].loc[index, element + "_name"] = "new-label"
    _assert_unchanged(topology, before)


@pytest.mark.parametrize("molecules,entities", [(0, 0), (1, 2), (5, 6)])
def test_parent_counts_follow_current_stored_rows(molecules, entities):
    from molsysmt.native import Topology

    topology = Topology(
        n_atoms=2, n_groups=1, n_molecules=molecules, n_entities=entities
    )
    before = _snapshot(topology)
    assert topology.get(n_molecules=True, n_entities=True) == [molecules, entities]
    _assert_unchanged(topology, before)
    topology.reset_molecules(n_molecules=molecules + 1)
    topology.reset_entities(n_entities=entities + 1)
    before = _snapshot(topology)
    assert msm.get(topology, n_molecules=True, n_entities=True) == [
        molecules + 1,
        entities + 1,
    ]
    _assert_unchanged(topology, before)


@pytest.mark.parametrize("native", [False, True])
@pytest.mark.parametrize("topology_only", [False, True])
@pytest.mark.parametrize(
    "element,parent,selection,expected",
    [
        ("atom", "molecule", [3, 0, 1], [None, 1, None]),
        ("atom", "entity", [3, 0, 1], [None, 0, None]),
        ("group", "molecule", [1, 0, 1], [None, 1, None]),
        ("group", "entity", [1, 0, 1], [None, 0, None]),
        ("molecule", "entity", [1, 2, 0, 1], [None, 0, 2, None]),
    ],
)
def test_nullable_parent_reads_preserve_order_and_unknown_correspondence(
    partial_declared_inventory_molsys,
    native,
    topology_only,
    element,
    parent,
    selection,
    expected,
):
    molsys = partial_declared_inventory_molsys
    topology = molsys.topology
    for name, plural, types in [
        ("molecule", "molecules", ["small molecule", "protein", "ion"]),
        ("entity", "entities", ["small molecule", "protein", "ion", "water"]),
    ]:
        table = getattr(topology, plural)
        table[name + "_name"] = pd.array(
            [f"{name}-name-{i}" for i in range(len(table))], dtype="string"
        )
        table[name + "_type"] = pd.array(types, dtype="string")
    if parent == "entity" and element != "molecule":
        topology.groups.loc[0, "molecule_index"] = 2
    source = topology if topology_only else molsys
    before = _snapshot(topology)
    options = dict(
        element=element,
        selection=selection,
        output_type="dictionary",
        **{parent + "_" + field: True for field in ["index", "id", "name", "type"]},
    )
    result = source.get(**options) if native else msm.get(source, **options)
    assert result[parent + "_index"] == expected
    assert result[parent + "_id"] == [
        None if i is None else f"declared-{parent}-{i}" for i in expected
    ]
    assert result[parent + "_name"] == [
        None if i is None else f"{parent}-name-{i}" for i in expected
    ]
    types = ["small molecule", "protein", "ion", "water"]
    assert result[parent + "_type"] == [
        None if i is None else types[i] for i in expected
    ]
    _assert_unchanged(topology, before)


@pytest.mark.parametrize("native", [False, True])
def test_unknown_parents_do_not_create_inventory_and_empty_selections_stay_empty(
    partial_declared_inventory_molsys, native
):
    molsys = partial_declared_inventory_molsys
    topology = molsys.topology
    topology.groups["molecule_index"] = pd.array([None, None], dtype="Int64")
    topology.reset_molecules(n_molecules=0)
    topology.reset_entities(n_entities=0)
    before = _snapshot(topology)
    for element, indices in [("atom", [3, 0, 3]), ("group", [1, 0, 1])]:
        options = dict(
            element=element, selection=indices, molecule_id=True, entity_id=True
        )
        result = molsys.get(**options) if native else msm.get(molsys, **options)
        assert result == [[None] * 3, [None] * 3]
        options["selection"] = []
        result = molsys.get(**options) if native else msm.get(molsys, **options)
        assert result == [[], []]
    _assert_unchanged(topology, before)
