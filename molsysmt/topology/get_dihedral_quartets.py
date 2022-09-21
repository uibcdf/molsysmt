from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_dihedral_quartets(molecular_system, with_blocks=False, selection='all',
                               syntax='MolSysMT', **kwargs):

    # phi, psi, omega, chi1, chi2, chi3, chi4, chi5

    from molsysmt.basic import get
    from . import get_covalent_blocks, get_covalent_chains

    dihedral_angles = []
    for key in kwargs.keys():
        if kwargs[key]:
            dihedral_angles.append(key)

    all_quartets = []
    all_blocks = []

    for dihedral_angle in dihedral_angles:

        if dihedral_angle=='phi':
            chain=['atom_name=="C"', 'atom_name=="N"', 'atom_name=="CA"', 'atom_name=="C"']
        elif dihedral_angle=='psi':
            chain=['atom_name=="N"', 'atom_name=="CA"', 'atom_name=="C"', 'atom_name=="N"']
        elif dihedral_angle=='omega':
            chain=['atom_name==["CA","CH3"]', 'atom_name=="C"', 'atom_name=="N"', 'atom_name==["CA","CH3"]']
        elif dihedral_angle=='chi1':
            chain=['atom_name=="N"','atom_name=="CA"','atom_name=="CB"', 'atom_name==["CG","CG1","OG","OG1","SG"]'] # flexible but PRO
        elif dihedral_angle=='chi2':
            chain=['atom_name=="CA"','atom_name=="CB"', 'atom_name==["CG","CG1"]', 'atom_name==["CD","CD1","SD","OD1","ND1"]'] # flexible but PRO
        elif dihedral_angle=='chi3':
            chain=['atom_name=="CB"', 'atom_name=="CG"', 'atom_name==["CD","SD"]','atom_name==["NE","OE1","CE"]']
        elif dihedral_angle=='chi4':
            chain=['atom_name=="CG"', 'atom_name=="CD"', 'atom_name==["NE","CE"]', 'atom_name==["CZ","NZ"]']
        elif dihedral_angle=='chi5':
            chain=['atom_name=="CD"', 'atom_name=="NE"', 'atom_name=="CZ"', 'atom_name=="NH1"']

        quartets = get_covalent_chains(molecular_system, chain=chain, selection=selection, syntax=syntax)

        all_quartets.append(quartets)

        if with_blocks:

            n_quartets = quartets.shape[0]

            blocks = []

            for quartet_index in range(n_quartets):

                quartet = quartets[quartet_index]
                component_index = get(molecular_system, element='atom', indices=quartet[1], component_index=True)[0]
                component_atom_indices = get(molecular_system, element='component', indices=component_index,
                                             atom_index=True)[0]
                tmp_blocks = get_covalent_blocks(molecular_system, remove_bonds=[quartet[1],
                    quartet[2]], output='sets')
                blocks_in_component = []
                for block in tmp_blocks:
                    if block.issubset(component_atom_indices):
                        blocks_in_component.append(block)
                blocks.append(blocks_in_component)
            
            all_blocks.append(np.array(blocks))

    
    if len(dihedral_angles)==1:
        all_quartets = all_quartets[0]
        if with_blocks:
            all_blocks = all_blocks[0]
    elif len(dihedral_angles)==0:
        all_quartets = None
        all_blocks = None

    if with_blocks:
        return all_quartets, all_blocks
    else:
        return all_quartets

