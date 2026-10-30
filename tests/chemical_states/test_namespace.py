"""Protect the accepted graph namespace and absence of a Topology facade."""

import molsysmt as msm


def test_canonical_graph_namespace_has_no_topology_facade():
    expected = {
        "get_atom_correspondences",
        "get_bondgraph",
        "get_covalent_blocks",
        "get_covalent_paths",
        "get_dihedral_quartets",
        "get_rigid_fragments",
        "get_rings",
        "get_rotatable_bonds",
        "get_substructure_matches",
    }
    observed = {name for name in vars(msm.chemical_states) if name.startswith("get_")}
    assert observed == expected
    for name in expected:
        function = getattr(msm.chemical_states, name)
        assert callable(function)
        assert function.__module__ == "molsysmt.chemical_states." + name
        assert not hasattr(msm.topology, name)
    assert callable(msm.topology.get_sequence_alignment)
    assert callable(msm.topology.get_sequence_identity)
