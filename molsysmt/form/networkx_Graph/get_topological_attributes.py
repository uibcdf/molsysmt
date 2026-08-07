from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import types

form = 'networkx.Graph'


@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):
    if indices is None:
        return None
    if is_all(indices):
        return list(item.nodes)
    return list(indices)


@arg_digest(form=form)
def get_bond_index_from_atom(item, indices='all', skip_digestion=False):
    if indices is None:
        return None
    selected_atoms = list(item.nodes if is_all(indices) else indices)
    output = []
    for atom_index in selected_atoms:
        output.append([
            bond_index
            for bond_index, edge in enumerate(item.edges)
            if atom_index in edge
        ])
    return output


@arg_digest(form=form)
def get_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):
    if indices is None:
        return None
    selected_atoms = item.nodes if is_all(indices) else indices
    return [list(item.neighbors(atom_index)) for atom_index in selected_atoms]


@arg_digest(form=form)
def get_bond_index_from_bond(item, indices='all', skip_digestion=False):
    if indices is None:
        return None
    if is_all(indices):
        return list(range(item.number_of_edges()))
    return list(indices)


@arg_digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all', skip_digestion=False):
    if indices is None:
        return None
    edges = list(item.edges)
    if not is_all(indices):
        edges = [edges[index] for index in indices]
    return sorted({atom_index for edge in edges for atom_index in edge})


@arg_digest(form=form)
def get_bond_index_from_system(item, skip_digestion=False):
    return get_bond_index_from_bond(item, skip_digestion=True)


@arg_digest(form=form)
def get_bonded_atoms_from_system(item, skip_digestion=False):
    return get_bonded_atoms_from_bond(item, skip_digestion=True)


def _node_values(item, indices, attribute):
    selected = list(item.nodes if is_all(indices) else indices)
    values = [item.nodes[index].get(attribute) for index in selected]
    return None if values and all(value is None for value in values) else values


def _edge_values(item, indices, attribute):
    edges = list(item.edges(data=True))
    if not is_all(indices):
        edges = [edges[index] for index in indices]
    values = [data.get(attribute) for _, _, data in edges]
    return None if values and all(value is None for value in values) else values


def _make_node_getter(attribute):
    @arg_digest(form=form)
    def getter(item, indices='all', skip_digestion=False):
        return _node_values(item, indices, attribute)

    getter.__name__ = f'get_{attribute}_from_atom'
    return getter


def _make_edge_getter(attribute):
    @arg_digest(form=form)
    def getter(item, indices='all', skip_digestion=False):
        return _edge_values(item, indices, attribute)

    getter.__name__ = f'get_{attribute}_from_bond'
    return getter


for _attribute in (
    'atom_id', 'atom_name', 'atom_type', 'isotope', 'group_index', 'chain_index',
    'component_index', 'formal_charge', 'atom_is_aromatic', 'n_unpaired_electrons',
    'n_implicit_hydrogens', 'allows_implicit_hydrogens', 'atom_stereochemistry',
):
    globals()[f'get_{_attribute}_from_atom'] = _make_node_getter(_attribute)

for _attribute in (
    'bond_id', 'bond_order', 'fractional_bond_order', 'bond_type',
    'bond_is_aromatic', 'bond_is_conjugated', 'bond_stereochemistry',
    'bond_stereo_atom_indices', 'bond_donor_atom_index', 'bond_acceptor_atom_index',
    'bond_joins_components', 'bond_evidence',
):
    globals()[f'get_{_attribute}_from_bond'] = _make_edge_getter(_attribute)


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    return item.number_of_nodes()


@arg_digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):
    return item.number_of_edges()


def _make_graph_getter(attribute):
    @arg_digest(form=form)
    def getter(item, skip_digestion=False):
        return item.graph.get(attribute)

    getter.__name__ = f'get_{attribute}_from_system'
    return getter


for _attribute in (
    'connectivity_completeness', 'component_completeness', 'component_evidence',
):
    globals()[f'get_{_attribute}_from_system'] = _make_graph_getter(_attribute)


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
