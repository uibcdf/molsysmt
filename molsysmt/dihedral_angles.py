

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

    from numpy import array, zeros, asfortranarray, ascontiguousarray
    from numpy import ndarray
    from molsysmt import get
    from molsysmt.utils import units as msm_units
    from .lib import geometry as libgeometry

    if type(quartets) in [list,tuple]:
        quartets = array(quartets, dtype=int)
    elif type(quartets) is ndarray:
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

    coordinates, box, box_shape = get(item, target='system', frame_indices=frame_indices, coordinates=True, box=True, box_shape=True)

    orthogonal = 0
    if box_shape is None:
        orthogonal =1
        if pbc:
            raise ValueError("The system has no PBC box. The input argument 'pbc' can not be True.")
    elif box_shape == 'cubic':
        orthogonal =1

    n_angles = quartets.shape[0]
    n_frames = coordinates.shape[0]
    n_atoms = coordinates.shape[1]

    if box is None:
        box= zeros([nframes,3,3])*msm_units.length

    box = asfortranarray(box._value, dtype='float64')
    coordinates = asfortranarray(coordinates._value, dtype='float64')

    angles = libgeometry.dihedral_angles(coordinates, box, orthogonal, int(pbc), quartets, n_angles, n_atoms, n_frames)
    angles = ascontiguousarray(angles)*msm_units.angle

    return angles

def ramachandran_angles(item, selection='all', frame_indices='all', syntaxis='MolSysMT', pbc=False,
                        plot=False):

    from numpy import vstack

    phi_covalent_chain = covalent_chains(item, chain='phi', selection=selection, syntaxis=syntaxis)
    psi_covalent_chain = covalent_chains(item, chain='psi', selection=selection, syntaxis=syntaxis)

    n_chains = phi_covalent_chain.shape[0]

    angles = dihedral_angles(item, quartets=vstack([phi_covalent_chain, psi_covalent_chain]),
                             frame_indices=frame_indices, pbc=pbc)

    return phi_covalent_chain, psi_covalent_chain, angles[:,:n_chains], angles[:,n_chains:]

