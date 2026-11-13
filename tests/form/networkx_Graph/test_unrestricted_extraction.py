"""Preserve graph inventory when unrestricted reuse is requested."""

import pytest

import molsysmt as msm


@pytest.mark.parametrize("route", ["extract", "convert"])
def test_unrestricted_graph_reuse_preserves_all_nodes_and_edges(
    builder_pdb_molsys, route
):
    graph = msm.convert(builder_pdb_molsys, to_form="networkx.Graph")
    nodes = list(graph.nodes(data=True))
    edges = list(graph.edges(data=True))
    assert len(nodes) == 4
    assert len(edges) == 2
    if route == "extract":
        result = msm.extract(graph, copy_if_all=False)
    else:
        result = msm.convert(graph, to_form="networkx.Graph", copy_if_all=False)
    assert result.number_of_nodes() == 4
    assert result.number_of_edges() == 2
    assert list(result.nodes(data=True)) == nodes
    assert list(result.edges(data=True)) == edges
    assert list(graph.nodes(data=True)) == nodes
    assert list(graph.edges(data=True)) == edges


@pytest.mark.parametrize(
    "kwargs", [{"atom_indices": [0, 1]}, {"structure_indices": [0]}]
)
def test_unimplemented_graph_selection_refuses_without_modifying_source(
    builder_pdb_molsys, kwargs
):
    from molsysmt._private.smonitor import NotImplementedMethodError
    from molsysmt.form.networkx_Graph.extract import extract

    graph = msm.convert(builder_pdb_molsys, to_form="networkx.Graph")
    nodes = list(graph.nodes(data=True))
    edges = list(graph.edges(data=True))
    with pytest.raises(NotImplementedMethodError):
        extract(graph, **kwargs)
    assert list(graph.nodes(data=True)) == nodes
    assert list(graph.edges(data=True)) == edges


def test_whole_graph_copy_owns_supported_attribute_dictionaries(builder_pdb_molsys):
    graph = msm.convert(builder_pdb_molsys, to_form="networkx.Graph")
    result = msm.extract(graph)
    assert result is not graph
    original = graph.nodes[0]["atom_name"]
    result.nodes[0]["atom_name"] = "changed"
    assert graph.nodes[0]["atom_name"] == original
    assert result.number_of_nodes() == 4
    assert result.number_of_edges() == 2
