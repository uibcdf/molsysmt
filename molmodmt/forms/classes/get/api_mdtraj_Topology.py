
def get(item, atom_indices=None, **kwargs):

    if atom_indices is not None:
        tmp_item = extract_atom_indices(item,atom_indices)
    else:
        tmp_item = item

    result=[]
    for option in kwargs:
        if option=='n_atoms' and kwargs[option]==True:
            result.append(tmp_item.n_atoms)
        if option=='n_frames' and kwargs[option]==True:
            raise BadCallError(BadCallMessage)
        if option=='n_residues' and kwargs[option]==True:
            result.append(tmp_item.n_residues)
        if option=='n_chains' and kwargs[option]==True:
            result.append(tmp_item.n_chains)
        if option=='n_molecules' and kwargs[option]==True:
            result.append(len(get(tmp_item,molecules=True)))
        if option=='masses' and kwargs[option]==True:
            result.append([atom.element.mass for atom in tmp_item.atoms])
        if option=='bonded_atoms' and kwargs[option]==True:
            tmp_bonded = [[] for ii in range(item.n_atoms)]
            for bond in item.bonds:
                tmp_bonded[bond.atom1.index].append(bond.atom2.index)
                tmp_bonded[bond.atom2.index].append(bond.atom1.index)
            result.append(tmp_bonded)
        if option=='bonds' and kwargs[option]==True:
            tmp_bonds = []
            for bond in item.bonds:
                tmp_bonds.append([bond.atom1.index,bond.atom2.index])
            result.append(tmp_bonds)
        if option=='graph' and kwargs[option]==True:
            result.append(item.to_bondgraph())
        if option=='chain_name' and kwargs[option] is not None:
            raise NotImplementedError
        if option=='chain_names' and kwargs[option] is not None:
            raise NotImplementedError
        if option=='molecules' and kwargs[option]==True:
            tmp_molecules = []
            for mm in item.find_molecules():
                tmp_molecules.append([ii.index for ii in mm])
            result.append(tmp_molecules)
        if option=='molecule_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='residue_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='atom_type' and kwargs[option]==True:
            raise NotImplementedError

    del(tmp_item)

    if len(result)==1:
        return result[0]
    else:
        return result



