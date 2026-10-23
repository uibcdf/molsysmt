"""Receiving native topology results without changing chemistry or the scene."""

import inspect

import molsysviewer as msv
import networkx as nx
import numpy as np
import pytest

import molsysmt as msm

pytest.importorskip("molsysviewer.system_edits")

PATH = ['atom_name=="C"', 'atom_name=="N"', 'atom_name=="CA"', 'atom_name=="C"']
NAMES = (
    "get_bondgraph",
    "get_covalent_blocks",
    "get_covalent_paths",
    "get_dihedral_quartets",
)


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as result:
            analysis = msm.Interactions.from_records(
                [],
                n_atoms=result.molsys.get_n_atoms(),
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.topology",
            )
            result.interactions.attach(analysis, name="preserve", assume_aligned=True)
            result.regions.add(selection=[0, 2, 4], tag="source")
            yield result


@pytest.mark.parametrize("name", NAMES)
def test_topology_signatures_help_and_digestion_are_native(view, name):
    native = inspect.signature(getattr(msm.topology, name))
    expected = list(native.parameters.values())[1:]
    if "skip_digestion" not in native.parameters:
        index = next(
            (
                i
                for i, p in enumerate(expected)
                if p.kind is inspect.Parameter.VAR_KEYWORD
            ),
            len(expected),
        )
        expected.insert(
            index,
            inspect.Parameter(
                "skip_digestion", inspect.Parameter.KEYWORD_ONLY, default=False
            ),
        )
    bound = getattr(view.addons.molsysmt.topology, name)
    assert list(inspect.signature(bound).parameters.values()) == expected
    assert bound.digestion_plan is not None
    assert "current view.molsys" in inspect.getdoc(bound)
    assert "not a scene object" in inspect.getdoc(bound)
    assert "\nmolecular_system :" not in inspect.getdoc(bound)
    if "skip_digestion" not in native.parameters:
        assert "flag is not added to scientific **kwargs" in inspect.getdoc(bound)


def test_namespace_is_explicit_without_invented_root_aliases(view):
    tools = view.addons.molsysmt
    assert "topology" in dir(tools)
    assert set(NAMES) <= set(dir(tools.topology))
    assert not hasattr(tools.topology, "unreviewed_tool")
    assert not hasattr(tools, "get_bondgraph")
    assert tools.get == tools.basic.get


@pytest.mark.parametrize("selection", ["all", [4, 0, 2, 0], []])
def test_bondgraph_preserves_source_indices_scopes_and_native_result(view, selection):
    arguments = dict(
        selection=selection, chemical_state="reference", structure_indices=[2, 0]
    )
    expected = msm.topology.get_bondgraph(view.molsys, **arguments)
    state = view.export_state()
    analysis = view.molsys.interactions["preserve"]
    graph = view.addons.molsysmt.topology.get_bondgraph(**arguments)
    assert type(graph) is type(expected)
    assert list(graph.nodes) == list(expected.nodes)
    assert list(graph.edges) == list(expected.edges)
    assert view.export_state() == state
    assert view.molsys.interactions["preserve"] is analysis
    graph.add_node(1000000)
    assert 1000000 not in msm.topology.get_bondgraph(view.molsys)


@pytest.mark.parametrize("output_type", ["sets", "numpy.ndarray"])
def test_hypothetical_bond_cut_does_not_remove_native_bonds(view, output_type):
    graph = msm.topology.get_bondgraph(view.molsys)
    cut = next(nx.bridges(graph))
    bonds = msm.get(view.molsys, element="atom", bonded_atom_pairs=True).copy()
    state = view.export_state()
    args = dict(
        remove_bonds=list(cut), output_type=output_type, structure_indices=[2, 0]
    )
    expected = msm.topology.get_covalent_blocks(view.molsys, **args)
    actual = view.addons.molsysmt.topology.get_covalent_blocks(**args)
    assert type(actual) is type(expected)
    assert actual.dtype == expected.dtype
    np.testing.assert_equal(actual, expected)
    if output_type == "sets":
        assert len(actual) == nx.number_connected_components(graph) + 1
        actual[0].add(1000000)
    else:
        assert actual.shape == (view.molsys.get_n_atoms(),)
        actual[:] = -100
    np.testing.assert_array_equal(
        msm.get(view.molsys, element="atom", bonded_atom_pairs=True), bonds
    )
    assert view.export_state() == state


@pytest.mark.parametrize("selection", ["all", 'atom_type!="H"'])
def test_covalent_path_patterns_and_addon_only_trusted_flag(view, selection):
    args = dict(path=PATH, selection=selection)
    expected = msm.topology.get_covalent_paths(view.molsys, **args)
    actual = view.addons.molsysmt.topology.get_covalent_paths(
        **args, skip_digestion=True
    )
    assert type(actual) is type(expected)
    np.testing.assert_array_equal(actual, expected)
    assert len(actual) > 0 and actual.shape[1] == 4


@pytest.mark.parametrize("flags", [{"phi": True}, {"phi": True, "psi": True}])
@pytest.mark.parametrize("with_blocks", [False, True])
def test_dihedral_flags_and_ragged_blocks_remain_native(view, flags, with_blocks):
    state = view.export_state()
    expected = msm.topology.get_dihedral_quartets(
        view.molsys, with_blocks=with_blocks, **flags
    )
    actual = view.addons.molsysmt.topology.get_dihedral_quartets(
        with_blocks=with_blocks, skip_digestion=True, **flags
    )
    assert type(actual) is type(expected)
    assert actual == expected
    if with_blocks:
        _, blocks = actual
        assert isinstance(blocks, list)
        nested = blocks if len(flags) == 1 else blocks[0]
        assert all(isinstance(block, set) for group in nested for block in group)
    assert view.export_state() == state


@pytest.mark.parametrize(
    "name, arguments",
    [
        ("get_bondgraph", {"nodes_name": "atom_name"}),
        ("get_bondgraph", {"to_form": "not-a-form"}),
        ("get_bondgraph", {"chemical_state": "not-a-state"}),
        ("get_covalent_blocks", {"remove_bonds": [0, 1, 2]}),
        ("get_covalent_blocks", {"output_type": "not-a-form"}),
        ("get_covalent_paths", {"path": ["not a selection"]}),
        ("get_dihedral_quartets", {"phi": True, "with_blocks": "yes"}),
    ],
)
def test_native_scientific_errors_are_not_hidden(view, name, arguments):
    with pytest.raises(Exception) as native:
        getattr(msm.topology, name)(view.molsys, **arguments)
    before = view.addons.molsysmt.get_sync_status()
    with pytest.raises(type(native.value)):
        getattr(view.addons.molsysmt.topology, name)(**arguments)
    assert view.addons.molsysmt.get_sync_status() == before


@pytest.mark.parametrize("name", ["get_covalent_paths", "get_dihedral_quartets"])
def test_unspecified_pattern_keeps_native_outcome_without_requiring_a_provider_bug(
    view, name
):
    try:
        expected = getattr(msm.topology, name)(view.molsys)
    except Exception as error:
        with pytest.raises(type(error)):
            getattr(view.addons.molsysmt.topology, name)()
    else:
        np.testing.assert_equal(
            getattr(view.addons.molsysmt.topology, name)(), expected
        )


@pytest.mark.parametrize("name", NAMES)
def test_invalid_addon_digest_control(view, name):
    with pytest.raises(msm.ArgumentError):
        getattr(view.addons.molsysmt.topology, name)(skip_digestion="yes")


def test_closed_signature_and_keyword_path_cannot_override_primary(view):
    topology = view.addons.molsysmt.topology
    target = view.molsys
    for name, arguments in [
        ("get_bondgraph", {}),
        ("get_covalent_blocks", {}),
        ("get_covalent_paths", {"path": PATH}),
        ("get_dihedral_quartets", {"phi": True}),
    ]:
        with pytest.raises(Exception):
            getattr(topology, name)(molecular_system=target, **arguments)
    assert view.molsys is target


def test_pending_topology_queries_do_not_project_the_scene_or_invalidate_analyses(view):
    tools = view.addons.molsysmt
    tools.remove(
        selection=[view.molsys.get_n_atoms() - 1], in_place=True, update_view=False
    )
    before = tools.get_sync_status()
    analysis = view.molsys.interactions["preserve"]
    graph = tools.topology.get_bondgraph()
    assert graph.number_of_nodes() == view.molsys.get_n_atoms()
    assert tools.topology.get_dihedral_quartets(
        phi=True
    ) == msm.topology.get_dihedral_quartets(view.molsys, phi=True)
    assert tools.get_sync_status() == before
    assert before["state"] == "pending"
    assert view.molsys.interactions["preserve"] is analysis


def test_cached_topology_follows_current_view_and_rejects_empty_or_closed_owners(view):
    topology = view.addons.molsysmt.topology
    graph = topology.get_bondgraph
    original_count = graph().number_of_nodes()
    with msv.demo["dialanine"] as other:
        view.load(other.molsys, mode="replace")
    assert graph().number_of_nodes() == view.molsys.get_n_atoms() != original_count
    view.addons.manager.disable("molsysmt")
    assert graph().number_of_nodes() == view.molsys.get_n_atoms()
    view.close()
    for name, args in [
        ("get_bondgraph", {}),
        ("get_covalent_blocks", {}),
        ("get_covalent_paths", {"path": PATH}),
        ("get_dihedral_quartets", {"phi": True}),
    ]:
        with pytest.raises(RuntimeError, match="closed view"):
            getattr(topology, name)(**args, skip_digestion=True)
    with msv.MolSysView() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.topology.get_bondgraph()
