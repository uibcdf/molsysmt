
def get(item, atom_indices=None, **kwargs):

    if atom_indices is not None:
        tmp_item = extract(item,atom_indices)
    else:
        tmp_item = item

    result=[]
    for option in kwargs:
        if option=='n_atoms' and kwargs[option]==True:
            result.append(tmp_item.n_atoms)
        if option=='n_frames' and kwargs[option]==True:
            result.append(tmp_item.n_frames)
        if option=='n_residues' and kwargs[option]==True:
            result.append(tmp_item.n_residues)
        if option=='n_molecules' and kwargs[option]==True:
            result.append(len(get_molecules(tmp_item)))
        if option=='masses' and kwargs[option]==True:
            result.append([atom.element.mass for atom in tmp_item.topology.atoms])
        if option=='bonded_atoms' and kwargs[option]==True:
            from .api_mdtraj_Topology import get as _get
            result.append(_get(item.topology,bonded_atoms=True))
        if option=='bonds' and kwargs[option]==True:
            from .api_mdtraj_Topology import get as _get
            result.append(_get(item.topology,bonds=True))
        if option=='graph' and kwargs[option]==True:
            from .api_mdtraj_Topology import get as _get
            result.append(_get(item.topology,graph=True))
        if option=='molecules' and kwargs[option]==True:
            from .api_mdtraj_Topology import get as _get
            result.append(_get(item.topology,molecules=True))
        if option=='molecule_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='residue_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='atom_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='coordinates' and kwargs[option]==True:
            result.append(item.xyz)


    del(tmp_item)

    if len(result)==1:
        return result[0]
    else:
        return result

