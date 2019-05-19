def get(item, atom_indices=None, **kwargs):

    if atom_indices is not None:
        tmp_topology = extract_atom_indices(item,atom_indices)
    else:
        tmp_topology = item

    result=[]
    for option in kwargs:
        if option=='n_atoms' and kwargs[option]==True:
            result.append(len(item.atoms))
        if option=='n_frames' and kwargs[option]==True:
            raise BadCallError
        if option=='n_residues' and kwargs[option]==True:
            result.append(len(item.residues))
        if option=='n_molecules' and kwargs[option]==True:
            raise BadCallError
        if option=='masses' and kwargs[option]==True:
            tmp_masses=[atom.mass for atom in item.atoms]
            result.append(tmp_masses)
        if option=='bonded_atoms' and kwargs[option]==True:
            tmp_bonded = [[] for ii in range(len(st.atoms))]
            for bond in st.bonds:
                tmp_bonded[bond.atom1.idx].append(bond.atom2.idx)
                tmp_bonded[bond.atom2.idx].append(bond.atom1.idx)
            result.append(tmp_bonded)
        if option=='bonds' and kwargs[option]==True:
            tmp_bonds = []
            for bond in item.bonds:
                tmp_bonds.append([bond.atom1.idx,bond.atom2.idx])
            result.append(tmp_bonds)
        if option=='graph' and kwargs[option]==True:
            from networkx import Graph as _Graph
            tmp_graph = _Graph(get(item,bonds=True))
            for atom in item.atoms:
                if len(atom.bonds)==0:
                    tmp_graph.add_node(atom.idx)
            result.append(tmp_graph)
        if option=='molecules' and kwargs[option]==True:
            from networkx import connected_components as _connected_components
            tmp_graph = get(item, graph=True)
            result.append([list(ii) for ii in _connected_components(tmp_graph)])
        if option=='molecule_type' and kwargs[option]==True:
            from molmodmt.utils.types import residue2molecule_types
            tmp_molecules = get(item,molecules=True)
            tmp_types = []
            for molecule in tmp_molecules:
                tmp_types.append(residue2molecule_types(item.atoms[molecule[0]].residue.name))
            if len(tmp_types)==1:
                tmp_types=tmp_types[0]
            result.append(tmp_types)
        if option=='residue_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='atom_type' and kwargs[option]==True:
            raise NotImplementedError

    if len(result)==1:
        return result[0]
    else:
        return result

