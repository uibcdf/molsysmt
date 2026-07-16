from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='molsysmt.Topology')
@dep_digest('mdtraj')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):

    import pandas as pd
    from mdtraj import Topology, Single, Double, Triple, Aromatic
    from mdtraj.core import element
    from .extract import extract

    item = extract(
        item,
        atom_indices=atom_indices,
        copy_if_all=False,
        skip_digestion=True,
    )

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

    formal_charges = item._get_chemical_state_atom_attribute('formal_charge')
    for atom in item.atoms.itertuples(index=True):

        elem = element.get_by_symbol(atom.atom_type)
        formal_charge = None
        if formal_charges is not None and not pd.isna(formal_charges.iloc[atom.Index]):
            formal_charge = int(formal_charges.iloc[atom.Index])
        tmp_atom = tmp_item.add_atom(
            atom.atom_name, elem, list_new_residues[atom.group_index],
            atom.atom_id, formal_charge=formal_charge,
        )

        list_new_atoms.append(tmp_atom)

    bonds = item._get_chemical_state_bonds()
    type_by_order = {1: Single, 2: Double, 3: Triple}
    for bond in bonds.itertuples(index=False):
        order = None
        bond_type = None
        if hasattr(bond, 'bond_order') and not pd.isna(bond.bond_order):
            order = int(bond.bond_order)
            bond_type = type_by_order.get(order)
        if hasattr(bond, 'is_aromatic') and not pd.isna(bond.is_aromatic) and bond.is_aromatic:
            bond_type = Aromatic
        tmp_item.add_bond(
            list_new_atoms[bond.atom1_index], list_new_atoms[bond.atom2_index],
            type=bond_type, order=order,
        )

    del list_new_atoms, list_new_residues, list_new_chains

    return tmp_item
