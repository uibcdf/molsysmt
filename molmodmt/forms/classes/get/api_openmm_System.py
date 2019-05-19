
def get(item, atom_indices=None, **kwargs):

    if atom_indices is not None:
        tmp_item = extract(item,atom_indices)
    else:
        tmp_item = item

    result=[]
    for option in kwargs:
        if option=='n_atoms' and kwargs[option]==True:
            result.append(item.topology.getNumAtoms())
        if option=='n_frames' and kwargs[option]==True:
            raise NotImplementedError
        if option=='n_residues' and kwargs[option]==True:
            result.append(item.topology.getNumResidues())
        if option=='n_chains' and kwargs[option]==True:
            result.append(item.topology.getNumChains())
        if option=='n_molecules' and kwargs[option]==True:
            raise NotImplementedError
        if option=='masses' and kwargs[option]==True:
            raise NotImplementedError
        if option=='charge' and kwargs[option]==True:
            from molmodmt.utils.openmm import get_net_charge
            result.append(get_net_charge(item, atom_indices))
        if option=='bonded_atoms' and kwargs[option]==True:
            raise NotImplementedError
        if option=='bonds' and kwargs[option]==True:
            raise NotImplementedError
        if option=='graph' and kwargs[option]==True:
            raise NotImplementedError
        if option=='molecules' and kwargs[option]==True:
            raise NotImplementedError
        if option=='molecule_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='residue_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='atom_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='coordinates' and kwargs[option]==True:
            result.append(item.getPositions())

    del(tmp_item)

    if len(result)==1:
        return result[0]
    else:
        return result

