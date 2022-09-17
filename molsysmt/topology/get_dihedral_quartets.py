from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_dihedral_quartets(molecular_system, dihedral_angle=None, with_blocks=False, selection='all',
                               syntax='MolSysMT'):

    from molsysmt.basic import get
    from . import get_covalent_blocks, get_covalent_chains

    if dihedral_angle is not None:
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
        elif dihedral_angle=='phi-psi':
            tmp_phi = get_dihedral_quartets(molecular_system, dihedral_angle='phi',
                    with_blocks=with_blocks, selection=selection, syntax=syntax)
            tmp_psi = get_dihedral_quartets(molecular_system, dihedral_angle='psi',
                    with_blocks=with_blocks, selection=selection, syntax=syntax)
            if not with_blocks:
                tmp_angs = [ii for ii in [tmp_phi, tmp_psi] if ii.shape[0]>0]
                tmp_angs = np.vstack(tmp_angs)
                return tmp_angs
            else:
                tmp_angs = [ii for ii in [tmp_phi[0], tmp_psi[0]] if ii.shape[0]>0]
                tmp_angs = np.vstack(tmp_angs)
                tmp_blocks = [ii for ii in [tmp_phi[1], tmp_psi[1]] if ii.shape[0]>0]
                tmp_blocks = np.vstack(tmp_blocks)
                return tmp_angs, tmp_blocks
        elif dihedral_angle=='phi-psi-omega':
            tmp_phi = get_dihedral_quartets(molecular_system, dihedral_angle='phi',
                    with_blocks=with_blocks, selection=selection, syntax=syntax)
            tmp_psi = get_dihedral_quartets(molecular_system, dihedral_angle='psi',
                    with_blocks=with_blocks, selection=selection, syntax=syntax)
            tmp_omega = get_dihedral_quartets(molecular_system, dihedral_angle='omega',
                    with_blocks=with_blocks, selection=selection, syntax=syntax)
            if not with_blocks:
                tmp_angs = [ii for ii in [tmp_phi, tmp_psi, tmp_omega] if ii.shape[0]>0]
                tmp_angs = np.vstack(tmp_angs)
                return tmp_angs
            else:
                tmp_angs = [ii for ii in [tmp_phi[0], tmp_psi[0], tmp_omega[0]] if ii.shape[0]>0]
                tmp_angs = np.vstack(tmp_angs)
                tmp_blocks = [ii for ii in [tmp_phi[1], tmp_psi[1], tmp_omega[1]] if ii.shape[0]>0]
                tmp_blocks = np.vstack(tmp_blocks)
                return tmp_angs, tmp_blocks
        elif dihedral_angle=='all':
            tmp_phi = get_dihedral_quartets(molecular_system, dihedral_angle='phi',
                    with_blocks=with_blocks, selection=selection, syntax=syntax)
            tmp_psi = get_dihedral_quartets(molecular_system, dihedral_angle='psi',
                    with_blocks=with_blocks, selection=selection, syntax=syntax)
            tmp_omega = get_dihedral_quartets(molecular_system, dihedral_angle='omega',
                    with_blocks=with_blocks, selection=selection, syntax=syntax)
            tmp_chi1 = get_dihedral_quartets(molecular_system, dihedral_angle='chi1',
                    with_blocks=with_blocks, selection=selection, syntax=syntax)
            tmp_chi2 = get_dihedral_quartets(molecular_system, dihedral_angle='chi2',
                    with_blocks=with_blocks, selection=selection, syntax=syntax)
            tmp_chi3 = get_dihedral_quartets(molecular_system, dihedral_angle='chi3',
                    with_blocks=with_blocks, selection=selection, syntax=syntax)
            tmp_chi4 = get_dihedral_quartets(molecular_system, dihedral_angle='chi4',
                    with_blocks=with_blocks, selection=selection, syntax=syntax)
            tmp_chi5 = get_dihedral_quartets(molecular_system, dihedral_angle='chi5',
                    with_blocks=with_blocks, selection=selection, syntax=syntax)
            if not with_blocks:
                tmp_angs = [ii for ii in [tmp_phi, tmp_psi, tmp_omega, tmp_chi1, tmp_chi2, tmp_chi3, tmp_chi4, tmp_chi5] if ii.shape[0]>0]
                tmp_angs = np.vstack(tmp_angs)
                return tmp_angs
            else:
                tmp_angs = [ii for ii in [tmp_phi[0], tmp_psi[0], tmp_omega[0], tmp_chi1[0],
                                          tmp_chi2[0], tmp_chi3[0], tmp_chi4[0], tmp_chi5[0]] if ii.shape[0]>0]
                tmp_angs = np.vstack(tmp_angs)
                tmp_blocks = [ii for ii in [tmp_phi[1], tmp_psi[1], tmp_omega[1], tmp_chi1[1],
                                          tmp_chi2[1], tmp_chi3[1], tmp_chi4[1], tmp_chi5[1]] if ii.shape[0]>0]
                tmp_blocks = np.vstack(tmp_blocks)
                return tmp_angs, tmp_blocks
        else:
            raise ValueError

    quartets = get_covalent_chains(molecular_system, chain=chain, selection=selection,
            syntax=syntax)

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

        return quartets, np.array(blocks)

    else:

        return quartets

