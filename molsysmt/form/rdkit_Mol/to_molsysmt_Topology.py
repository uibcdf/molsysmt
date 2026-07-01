from molsysmt._private.arg_digestion import arg_digest


def _rdkit_bond_metadata(bond):
    bond_type = str(bond.GetBondType()).lower()
    if bond.GetIsAromatic():
        return "aromatic", "aromatic"
    order = {
        "single": "1",
        "double": "2",
        "triple": "3",
        "quadruple": "4",
        "oneandahalf": "1.5",
        "twoandahalf": "2.5",
        "threeandahalf": "3.5",
        "dative": "dative",
        "zero": "0",
        "unspecified": None,
    }.get(bond_type, bond_type or None)
    return order, bond_type or None


@arg_digest(form='rdkit.Mol')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.native import Topology
    from molsysmt._private.variables import is_all

    n_atoms = item.GetNumAtoms()
    n_bonds = item.GetNumBonds()

    tmp_item = Topology(n_atoms=n_atoms)

    atom_id = []
    atom_name = []
    atom_type = []

    for atom in item.GetAtoms():
        atom_id.append(str(atom.GetIdx()))

        info = atom.GetPDBResidueInfo()
        if info:
            atom_name.append(info.GetName().strip())
            atom_type.append(atom.GetSymbol())
        else:
            atom_name.append(atom.GetSymbol() + str(atom.GetIdx()))
            atom_type.append(atom.GetSymbol())

    tmp_item.atoms['atom_id'] = atom_id
    tmp_item.atoms['atom_name'] = atom_name
    tmp_item.atoms['atom_type'] = atom_type

    if n_bonds > 0:
        bonded_atoms = []
        metadata_by_pair = {}
        for bond in item.GetBonds():
            atom_i = bond.GetBeginAtomIdx()
            atom_j = bond.GetEndAtomIdx()
            bonded_atoms.append([atom_i, atom_j])
            metadata_by_pair[tuple(sorted((atom_i, atom_j)))] = _rdkit_bond_metadata(bond)
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
