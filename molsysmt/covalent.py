import numpy as _np

def covalent_dihedral_quartets(item, dihedral_angle=None, with_blocks=False, selection='all',
                               syntaxis='MolSysMT'):

    if dihedral_angle is not None:
        if dihedral_angle=='phi':
            chain=['C', 'N', 'CA', 'C']
        elif dihedral_angle=='psi':
            chain=['N', 'CA', 'C', 'N']
        elif dihedral_angle=='omega':
            chain=[['CA', 'CH3'], 'C', 'N', ['CA', 'CH3']]
        elif dihedral_angle=='chi1':
            chain=['N','CA','CB', ['CG', 'CG1', 'OG', 'OG1', 'SG']] # flexible but PRO
        elif dihedral_angle=='chi2':
            chain=['CA','CB', ['CG', 'CG1'], ['CD', 'CD1', 'SD', 'OD1', 'ND1']] # flexible but PRO
        elif dihedral_angle=='chi3':
            chain=['CB', 'CG', ['CD', 'SD'], ['NE', 'OE1', 'CE']]
        elif dihedral_angle=='chi4':
            chain=['CG', 'CD', ['NE', 'CE'], ['CZ', 'NZ']]
        elif dihedral_angle=='chi5':
            chain=['CD', 'NE', 'CZ', 'NH1']
        elif dihedral_angle=='all':
            tmp_phi = covalent_dihedral_quartets(item, dihedral_angle='phi', with_blocks=with_blocks, selection=selection, syntaxis=syntaxis)
            tmp_psi = covalent_dihedral_quartets(item, dihedral_angle='psi', with_blocks=with_blocks, selection=selection, syntaxis=syntaxis)
            tmp_omega = covalent_dihedral_quartets(item, dihedral_angle='omega', with_blocks=with_blocks, selection=selection, syntaxis=syntaxis)
            tmp_chi1 = covalent_dihedral_quartets(item, dihedral_angle='chi1', with_blocks=with_blocks, selection=selection, syntaxis=syntaxis)
            tmp_chi2 = covalent_dihedral_quartets(item, dihedral_angle='chi2', with_blocks=with_blocks, selection=selection, syntaxis=syntaxis)
            tmp_chi3 = covalent_dihedral_quartets(item, dihedral_angle='chi3', with_blocks=with_blocks, selection=selection, syntaxis=syntaxis)
            tmp_chi4 = covalent_dihedral_quartets(item, dihedral_angle='chi4', with_blocks=with_blocks, selection=selection, syntaxis=syntaxis)
            tmp_chi5 = covalent_dihedral_quartets(item, dihedral_angle='chi5', with_blocks=with_blocks, selection=selection, syntaxis=syntaxis)
            if not with_blocks:
                tmp_angs = [ii for ii in [tmp_phi, tmp_psi, tmp_omega, tmp_chi1, tmp_chi2, tmp_chi3, tmp_chi4, tmp_chi5] if ii.shape[0]>0]
                tmp_angs = _np.vstack(tmp_angs)
                return tmp_angs
            else:
                tmp_angs = [ii for ii in [tmp_phi[0], tmp_psi[0], tmp_omega[0], tmp_chi1[0],
                                          tmp_chi2[0], tmp_chi3[0], tmp_chi4[0], tmp_chi5[0]] if ii.shape[0]>0]
                tmp_angs = _np.vstack(tmp_angs)
                tmp_blocks = [ii for ii in [tmp_phi[1], tmp_psi[1], tmp_omega[1], tmp_chi1[1],
                                          tmp_chi2[1], tmp_chi3[1], tmp_chi4[1], tmp_chi5[1]] if ii.shape[0]>0]
                tmp_blocks = _np.vstack(tmp_blocks)
                return tmp_angs, tmp_blocks
        else:
            raise ValueError

    quartets = covalent_chains(item, chain=chain, selection=selection, syntaxis=syntaxis)

    if with_blocks:

        from molsysmt import get

        n_quartets = quartets.shape[0]

        blocks = []

        for quartet_index in range(n_quartets):

            quartet = quartets[quartet_index]
            component_index = get(item, target='atom', indices=quartet[1], component_index=True)[0]
            component_atom_indices = get(item, target='component', indices=component_index, atom_index=True)[0]
            tmp_blocks = covalent_blocks(item, remove_bonds=[quartet[1], quartet[2]], output_form='sets')
            blocks_in_component = []
            for block in tmp_blocks:
                if block.issubset(component_atom_indices):
                    blocks_in_component.append(block)
            blocks.append(blocks_in_component)

        return quartets, _np.array(blocks)

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

    return _np.array(blocks)

