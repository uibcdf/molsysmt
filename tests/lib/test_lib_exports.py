from molsysmt import lib


def test_lib_package_exports_core_namespaces():
    assert hasattr(lib, 'math')
    assert hasattr(lib, 'series')
    assert hasattr(lib, 'pbc')
    assert hasattr(lib, 'structure')
    assert hasattr(lib, 'topology')
    assert hasattr(lib.pbc, 'wrap_to_mic')
    assert hasattr(lib.structure, 'get_rmsd')
    assert hasattr(lib.topology, 'get_component_index_from_bonded_atom_pairs')
