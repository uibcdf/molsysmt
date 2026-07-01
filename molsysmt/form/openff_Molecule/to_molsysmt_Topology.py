from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all


def _openff_bond_metadata(bond):
    order = getattr(bond, "bond_order", None)
    aromatic = bool(getattr(bond, "is_aromatic", False))
    if aromatic:
        return "aromatic", "aromatic"
    if order is None:
        return None, None
    try:
        if float(order).is_integer():
            order_value = str(int(order))
        else:
            order_value = str(order)
    except Exception:
        order_value = str(order)
    return order_value, order_value


@arg_digest(form='openff.Molecule')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.native import Topology

    n_atoms = item.n_atoms
    n_bonds = item.n_bonds

    tmp_item = Topology(n_atoms=n_atoms)

    atom_id = []
    atom_name = []
    atom_type = []

    for atom in item.atoms:
        idx = atom.molecule_atom_index
        symbol = atom.symbol
        name = atom.name if atom.name else symbol + str(idx)
        atom_id.append(str(idx))
        atom_name.append(name)
        atom_type.append(symbol)

    tmp_item.atoms['atom_id'] = atom_id
    tmp_item.atoms['atom_name'] = atom_name
    tmp_item.atoms['atom_type'] = atom_type

    if n_bonds > 0:
        bonded_atoms = []
        metadata_by_pair = {}
        for bond in item.bonds:
            atom_i = bond.atom1_index
            atom_j = bond.atom2_index
            bonded_atoms.append([atom_i, atom_j])
            metadata_by_pair[tuple(sorted((atom_i, atom_j)))] = _openff_bond_metadata(bond)
        tmp_item.add_bonds(bonded_atoms, skip_digestion=True)
        bond_orders = []
        bond_types = []
        for _, row in tmp_item.bonds.iterrows():
            key = tuple(sorted((int(row['atom1_index']), int(row['atom2_index']))))
            order, bond_type = metadata_by_pair.get(key, (None, None))
            bond_orders.append(order)
            bond_types.append(bond_type)
        tmp_item.bonds['order'] = bond_orders
        tmp_item.bonds['type'] = bond_types

    tmp_item.rebuild_components()
    tmp_item.rebuild_molecules()
    tmp_item.rebuild_entities()

    if not is_all(atom_indices):
        from molsysmt.form.molsysmt_Topology.extract import extract
        tmp_item = extract(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
