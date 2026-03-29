from molsysmt._private.arg_digestion import arg_digest
from molsysmt.element.group import get_group_type_from_group_name
import numpy as np

@arg_digest(form='MDAnalysis.Topology')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.native import Topology
    from molsysmt.form.molsysmt_Topology.extract import extract as extract_molsysmt_Topology
    from molsysmt._private.variables import is_all

    n_atoms = item.n_atoms
    n_groups = item.n_residues
    n_chains = item.n_segments

    tmp_item = Topology(n_atoms=n_atoms, n_groups=n_groups, n_chains=n_chains)

    # Atoms
    atom_name = list(item.names.values) if hasattr(item, 'names') else [str(i) for i in range(n_atoms)]
    atom_id = list(item.ids.values.astype(str)) if hasattr(item, 'ids') else [str(i) for i in range(n_atoms)]
    atom_type = list(item.types.values) if hasattr(item, 'types') else ['' for _ in range(n_atoms)]
    group_index_of_atoms = list(item.tt.atoms2residues(np.arange(n_atoms)))

    tmp_item.atoms['atom_id'] = atom_id
    tmp_item.atoms['atom_name'] = atom_name
    tmp_item.atoms['atom_type'] = atom_type
    tmp_item.atoms['group_index'] = group_index_of_atoms

    # Groups
    group_name = list(item.resnames.values) if hasattr(item, 'resnames') else ['' for _ in range(n_groups)]
    group_id = list(item.resids.values.astype(str)) if hasattr(item, 'resids') else [str(i) for i in range(n_groups)]
    group_type = [get_group_type_from_group_name(name) for name in group_name]
    chain_index_of_groups = list(item.tt.residues2segments(np.arange(n_groups)))

    tmp_item.groups['group_id'] = group_id
    tmp_item.groups['group_name'] = group_name
    tmp_item.groups['group_type'] = group_type
    # chain_index lives on atoms only
    _ci_grp = np.array(chain_index_of_groups, dtype=int)
    _gi_atom = np.array(group_index_of_atoms, dtype=int)
    tmp_item.atoms['chain_index'] = _ci_grp[_gi_atom]

    # Chains
    segids = list(item.segids.values) if hasattr(item, 'segids') else [str(i) for i in range(n_chains)]
    tmp_item.chains['chain_id'] = segids
    tmp_item.chains['chain_name'] = segids

    # Bonds
    if hasattr(item, 'bonds'):
        bond_values = item.bonds.values
        if len(bond_values) > 0:
            tmp_item.add_bonds(bond_values.tolist(), skip_digestion=True)

    # Rebuild remaining hierarchy
    tmp_item.rebuild_components()
    tmp_item.rebuild_molecules()
    tmp_item.rebuild_entities()

    if not is_all(atom_indices):
        tmp_item = extract_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
