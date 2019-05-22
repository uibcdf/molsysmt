
def getting(item, atom_indices='all', **kwargs):

    tmp_item = extract_atom_indices(item,atom_indices)

    result=[]
    for option in kwargs:
        if option=='n_atoms' and kwargs[option]==True:
            result.append(tmp_item.topology.getNumAtoms())
        if option=='n_frames' and kwargs[option]==True:
            raise NotImplementedError
        if option=='n_residues' and kwargs[option]==True:
            result.append(tmp_item.topology.getNumResidues())
        if option=='n_chains' and kwargs[option]==True:
            result.append(tmp_item.topology.getNumChains())
        if option=='n_molecules' and kwargs[option]==True:
            raise NotImplementedError
        if option=='n_aminoacids' and kwargs[option]==True:
            from molmodmt.topology import is_aminoacid
            n_aminoacids=0
            for residue in tmp_item.topology.residues():
                if is_aminoacid(residue.name): n_aminoacids+=1
            result.append(n_aminoacids)
        if option=='n_nucleotides' and kwargs[option]==True:
            from molmodmt.topology import is_nucleotide
            n_nucleotides=0
            for residue in tmp_item.topology.residues():
                if is_nucleotide(residue.name): n_nucleotides+=1
            result.append(n_nucleotides)
        if option=='n_waters' and kwargs[option]==True:
            from molmodmt.topology import is_water
            n_waters=0
            for residue in tmp_item.topology.residues():
                if is_water(residue.name): n_water+=1
            result.append(n_waters)
        if option=='n_ions' and kwargs[option]==True:
            from molmodmt.topology import is_ion
            n_ions=0
            for residue in tmp_item.topology.residues():
                if is_ion(residue.name): n_ions+=1
            result.append(n_ions)
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

