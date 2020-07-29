import numpy as _np

def covalent_dihedral_quartets(item, dihedral_angles=None, with_blocks=False, selection='all',
                               syntaxis='MolSysMT'):

    if dihedral_angles is not None:
        if dihedral_angles=='phi':
            chain=['C', 'N', 'CA', 'C']
        elif dihedral_angles=='psi':
            chain=['N', 'CA', 'C', 'N']
        elif dihedral_angles=='omega':
            chain=[['CA', 'CH3'], 'C', 'N', ['CA', 'CH3']]
        elif dihedral_angles=='chi1':
            chain=['N','CA','CB', ['CG', 'CG1', 'OG', 'OG1', 'SG']] # flexible but PRO
        elif dihedral_angles=='chi2':
            chain=['CA','CB', ['CG', 'CG1'], ['CD', 'CD1', 'SD', 'OD1', 'ND1']] # flexible but PRO
        elif dihedral_angles=='chi3':
            chain=['CB', 'CG', ['CD', 'SD'], ['NE', 'OE1', 'CE']]
        elif dihedral_angles=='chi4':
            chain=['CG', 'CD', ['NE', 'CE'], ['CZ', 'NZ']]
        elif dihedral_angles=='chi5':
            chain=['CD', 'NE', 'CZ', 'NH1']
        else:
            raise ValueError

    quartets = covalent_chains(item, chain=chain, selection=selection, syntaxis=syntaxis)

    if with_blocks:

        from molsysmt import get

        n_atoms = get(item, target='system', n_atoms=True)
        n_quartets = quartets.shape[0]

        blocks = _np.zeros([n_quartets, n_atoms], dtype=int)

        for quartet_index in range(n_quartets):

            quartet = quartets[quartet_index]
            blocks[quartet_index,:] = covalent_blocks(item, remove_bonds=[quartet[1], quartet[2]], output_form='array')

        return quartets, blocks

    else:

        return quartets


def covalent_chains(item, chain=None, selection='all', syntaxis='MolSysMT'):

    from molsysmt import select, bondgraph
    from numpy import sort, concatenate, unique, array

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

def covalent_blocks(item, remove_bonds=None, output_form='sets'):

    from molsysmt import get, bondgraph
    from networkx import connected_components

    G = bondgraph(item, nodes_name='atom_index')

    if remove_bonds is not None:

        if type(remove_bonds) in [list,tuple]:
            remove_bonds = _np.array(remove_bonds)

        if len(remove_bonds.shape)==1:
            if remove_bonds.shape[0]==2:
                remove_bonds=remove_bonds.reshape([1,2])
            else:
                raise ValueError("Input argument bonded_atoms with wrong shape")
        elif len(remove_bonds.shape)==2:
            if remove_bonds.shape[1]!=2:
                raise ValueError("Input argument bonded_atoms with wrong shape")
        else:
            raise ValueError("Input argument bonded_atoms with wrong shape")

        for atom_pair in remove_bonds:
            G.remove_edge(atom_pair[0], atom_pair[1])

    components = connected_components(G)

    del(G)

    if output_form=='sets':

        blocks = list(components)

    elif output_form=='array':

        n_atoms = get(item, target='system', n_atoms=True)
        blocks = -_np.ones([n_atoms], dtype=int)
        component_index = 0
        for component in components:
            blocks[list(component)]=component_index
            component_index += 1

    else:

        raise ValueError('Input argument "output" must be "sets" or "array"')

    return blocks

