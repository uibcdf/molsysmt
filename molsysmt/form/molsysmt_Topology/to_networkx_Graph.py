from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
import networkx as nx
import pandas as pd


_ATOM_STATE_NAMES = {
    'formal_charge': 'formal_charge',
    'is_aromatic': 'atom_is_aromatic',
    'n_unpaired_electrons': 'n_unpaired_electrons',
    'n_implicit_hydrogens': 'n_implicit_hydrogens',
    'allows_implicit_hydrogens': 'allows_implicit_hydrogens',
    'stereochemistry': 'atom_stereochemistry',
}
_BOND_NAMES = {
    'bond_id': 'bond_id',
    'bond_order': 'bond_order',
    'fractional_bond_order': 'fractional_bond_order',
    'bond_type': 'bond_type',
    'is_aromatic': 'bond_is_aromatic',
    'is_conjugated': 'bond_is_conjugated',
    'stereochemistry': 'bond_stereochemistry',
    'donor_atom_index': 'bond_donor_atom_index',
    'acceptor_atom_index': 'bond_acceptor_atom_index',
    'joins_components': 'bond_joins_components',
    'evidence': 'bond_evidence',
}


def _plain_value(value):
    """Return a NetworkX-safe scalar or ``None`` for missing data."""

    if pd.isna(value):
        return None
    return value.item() if hasattr(value, 'item') else value


@arg_digest(form='molsysmt.Topology')
def to_networkx_Graph(item, atom_indices='all', skip_digestion=False):

    if not is_all(atom_indices):
        from molsysmt.form.molsysmt_Topology.extract import extract

        item = extract(item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)

    state = item._resolve_chemical_state()
    g = nx.Graph(
        molsysmt_contract='canonical_attribute_graph_v1',
        connectivity_completeness=state.connectivity_completeness,
        component_completeness=state.component_completeness,
        component_evidence=state.component_evidence,
    )

    for atom_index, atom in item.atoms.iterrows():
        node_attributes = {
            name: _plain_value(value)
            for name, value in atom.items()
            if not pd.isna(value)
        }
        component_index = state.component_indices.iloc[atom_index]
        if not pd.isna(component_index):
            node_attributes['component_index'] = _plain_value(component_index)
        for storage_name, public_name in _ATOM_STATE_NAMES.items():
            if storage_name in state.atom_attributes:
                value = state.atom_attributes.iloc[atom_index][storage_name]
                if not pd.isna(value):
                    node_attributes[public_name] = _plain_value(value)
        g.add_node(int(atom_index), **node_attributes)

    for _, bond in state.bonds.iterrows():
        edge_attributes = {}
        for storage_name, public_name in _BOND_NAMES.items():
            if storage_name in bond.index and not pd.isna(bond[storage_name]):
                edge_attributes[public_name] = _plain_value(bond[storage_name])
        if (
            'stereo_atom1_index' in bond.index
            and 'stereo_atom2_index' in bond.index
            and not pd.isna(bond['stereo_atom1_index'])
            and not pd.isna(bond['stereo_atom2_index'])
        ):
            edge_attributes['bond_stereo_atom_indices'] = (
                _plain_value(bond['stereo_atom1_index']),
                _plain_value(bond['stereo_atom2_index']),
            )
        g.add_edge(
            int(bond['atom1_index']),
            int(bond['atom2_index']),
            **edge_attributes,
        )

    return g
