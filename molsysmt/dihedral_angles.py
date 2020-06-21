def covalent_chains(item, chain=None, selection='all', syntaxis='MolSysMT'):

    from molsysmt import select

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

    return chain_atom_indices

def dihedral_angles(item, angle=None , quartets={'phi':['C', 'N', 'CA', 'C'], 'psi':['N', 'CA', 'C', 'N'], 'omega': [['CA', 'CH3'], 'C', 'N', ['CA', 'CH3']]},
                    selection='all', frame_indices='all', syntaxis='MolSysMT'):

    # angle in ['phi', 'psi', 'omega', 'xi1']
    # phi = ['C', 'N', 'CA', 'C']
    # psi = ['N', 'CA', 'C', 'N']
    # omega = [['CA', 'CH3'], 'C', 'N', ['CA', 'CH3']]
    # xi1 = ['N','CA','CB','CG']

    pass

def ramachandran_map(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):



    pass

