from .lib.geometry import dihedral_angles as _dihedral_angles

def covalent_chains(item, chain=None, selection='all', syntaxis='MolSysMT'):

    from molsysmt import select, bondgraph
    from numpy import sort, concatenate, unique, array

    if type(chain) is str:
        if chain=='phi':
            chain=['C', 'N', 'CA', 'C']
        elif chain=='psi':
            chain=['N', 'CA', 'C', 'N']
        elif chain=='omega':
            chain=[['CA', 'CH3'], 'C', 'N', ['CA', 'CH3']]
        elif chain=='chi1':
            chain=['N','CA','CB','CG']
        else:
            raise ValueError

    for ii in range(len(chain)):
        if type(chain[ii]) is not list:
            chain[ii]=[chain[ii]]

    if selection is 'all':
        mask = None
    else:
        mask = select(item, selection=selection, syntaxis=syntaxis)

    chain_atom_indices = []

    for atom_names in chain:
        atom_indices = select(item, selection="atom_name==@atom_names", mask=mask)
        chain_atom_indices.append(atom_indices)

    atom_indices = sort(unique(concatenate(chain_atom_indices)))

    graph = bondgraph(item, selection=atom_indices, nodes_name='atom_index')

    n_slaves = len(chain_atom_indices)

    output = [[ii] for ii in chain_atom_indices[0]]
    for slave_index in range(n_slaves):
        chain_atom_indices[slave_index] = set(chain_atom_indices[slave_index])

    for slave_index in range(1,n_slaves):
        slave_preindex=slave_index-1
        tmp_output=output.copy()
        output=[]
        for chain in tmp_output:
            for ii in graph.neighbors(chain[slave_preindex]):
                if ii in chain_atom_indices[slave_index]:
                    new_chain = chain.copy()
                    new_chain.append(ii)
                    output.append(new_chain)
    del(graph)

    return array(output, dtype=int)

def dihedral_angles(item, quartets=None, frame_indices='all', pbc=False):

    from numpy import array
    from molsysmt import get

    if type(quartets) is str:
        if quartets in ['phi', 'psi', 'omega', 'chi1']:
            quartets = covalent_chains(item, chain=quartets)
        else:
            raise ValueError
    elif type(quartets) in [list,tuple]:
        quartets = array(quartets, dtype=int)
    elif type(quartes) is ndarray:
        pass
    else:
        raise ValueError

    shape = quartets.shape

    if len(shape)==1:
        if shape[0]==4:
            quartets=quartets.reshape([1,4])
        else:
            raise ValueError
    elif len(shape)==2:
        if shape[1]!=4:
            raise ValueError
    else:
        raise ValueError

    coordinates, box, box_shape = get(item, frame_indices=frame_indices, coordinates=True, box=True, box_shape=True)

    n_angles = quartets.shape[0]
    n_frames = coordinates.shape[0]
    n_atoms = coordinates.shape[1]

    angles = _dihedral_angles(coordinates, box, orthogonal, int(pbc), quartets, n_angles, n_atoms, n_frames)

    return angles

def ramachandran_map(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):


    pass

