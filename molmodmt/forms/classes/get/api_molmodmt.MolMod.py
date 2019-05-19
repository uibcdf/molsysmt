
def get(item, atom_indices=None, **kwargs):

    from .api_mdtraj_Topology import get as _get

    if atom_indices is not None:
        from .api_mdtraj_Topology import extract_atom_indices as _mdtraj_extract
        tmp_topology = _mdtraj_extract(item.topology,atom_indices)
    else:
        tmp_topology = item.topology

    result=[]
    for option in kwargs:
        if option=='n_atoms' and kwargs[option]==True:
            result.append(tmp_topology.n_atoms)
        if option=='n_frames' and kwargs[option]==True:
            result.append(item.trajectory.n_frames)
        if option=='n_residues' and kwargs[option]==True:
            result.append(_get(tmp_topology,n_residues=True))
        if option=='n_chains' and kwargs[option]==True:
            result.append(_get(tmp_topology,n_chains=True))
        if option=='n_molecules' and kwargs[option]==True:
            result.append(_get(tmp_topology,n_molecules=True))
        if option=='masses' and kwargs[option]==True:
            result.append(_get(tmp_topology,masses=True))
        if option=='bonded_atoms' and kwargs[option]==True:
            result.append(_get(tmp_topology,bonded_atoms=True))
        if option=='bonds' and kwargs[option]==True:
            result.append(_get(tmp_topology,bonds=True))
        if option=='graph' and kwargs[option]==True:
            result.append(_get(tmp_topology,graph=True))
        if option=='chain_name' and kwargs[option] is not None:
            result.append(_get(tmp_topology, chain_names=kwargs[option]))
        if option=='chain_names' and kwargs[option] is not True:
            result.append(_get(tmp_topology, chain_names=kwargs[option]))
        if option=='molecules' and kwargs[option]==True:
            result.append(_get(tmp_topology,molecules=True))
        if option=='molecule_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='residue_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='atom_type' and kwargs[option]==True:
            raise NotImplementedError
        if option=='box' and kwargs[option]==True:
            result.append(item.trajectory.box)
        if option=='cell' and kwargs[option]==True:
            result.append(item.trajectory.cell)

    if len(result)==1:
        return result[0]
    else:
        return result

