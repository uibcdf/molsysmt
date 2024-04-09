from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):

    try:
        from mdtraj import Topology
        from mdtraj.core import element
    except:
        raise LibraryNotFound('mdtraj')

    tmp_item = Topology()

    list_new_atoms = []
    list_new_residues = []
    list_new_chains = []

    for chain in item.chains.itertuples(index=True):
        tmp_chain = tmp_item.add_chain(chain_id=str(chain.chain_id))
        list_new_chains.append(tmp_chain)

    group_chain_mapping = item.atoms.groupby('group_index')['chain_index'].agg('first').to_dict()

    for group in item.groups.itertuples(index=True):
        tmp_residue = tmp_item.add_residue(group.group_name, list_new_chains[group_chain_mapping[group.Index]],
                                      resSeq=str(group.group_id))
        list_new_residues.append(tmp_residue)

    for atom in item.atoms.itertuples(index=True):

        elem = element.get_by_symbol(atom.atom_type)
        tmp_atom = tmp_item.add_atom(atom.atom_name, elem, list_new_residues[atom.group_index], atom.atom_id)

        list_new_atoms.append(tmp_atom)

    for bond in item.bonds.itertuples(index=False):

        tmp_item.add_bond(list_new_atoms[bond.atom1_index], list_new_atoms[bond.atom2_index])

    del list_new_atoms, list_new_residues, list_new_chains

    return tmp_item

