from molsysmt._private.digestion import digest
import numpy as np
import warnings

@digest()
def get_missing_bonds(molecular_system, max_bond_length='2 angstroms', selection='all',
                      structure_indices='all', syntaxis='MolSysMT', engine='MolSysMT', check=True):

    output = []

    if engine=="MolSysMT":

        from molsysmt.basic import get, select
        from molsysmt.structure import get_neighbors

        atom_indices = select(molecular_system, selection=selection, syntaxis=syntaxis)

        if structure_indices is 'all':
            n_atoms = get(molecular_system, element='system', n_structures=True, check=False)
            structure_indices = np.arange(n_atoms)

        old_bonds = get(molecular_system, element='atom', selection=atom_indices, inner_bonded_atoms=True, check=False)

        for ii in range(old_bonds):
            if old_bonds[ii][0]>old_bonds[ii][1]:
                old_bonds[ii][0], old_bonds[ii][1] = old_bonds[ii][1], old_bonds[ii][0]

        neighbors, distance = get_neighbors(molecular_system, selection=atom_indices,
                                            selection_2=atom_indices, threshold=max_bond_length,
                                            output_forms='dicts')

        for atom_i, atom_j in old_bonds:
            for neighbors_frame in neighbors:
                if atom_j not in neighbors_frame[atom_i]:
                    warnings.warn(f"The bond between atoms {atom_i} and {atom_j} was observed with a length larger than the max_bond_length threshold.")

        for atom_i in neighbors[0]:
            for atom_j in neighbors[0][atom_i]:
                if atom_i < atom_j:
                    always=True
                    for neighbors_frame in neighbors:
                        if atom_j not in neighbors_frame[atom_i]:
                            always=False
                            break
                    if always:
                        if [atom_i, atom_j] not in old_bonds:
                            output.append[atom_i, atom_j]

    elif engine=="ParmEd":

        raise NotImplementedError

    elif engine=="pytraj":

        from molsysmt.basic import convert, get
        from os import remove
        from molsysmt._private.files_and_directories import temp_filename

        old_bonds = get(molecular_system, element='atom', selection=atom_indices, inner_bonded_atoms=True, check=False)

        for ii in range(old_bonds):
            if old_bonds[ii][0]>old_bonds[ii][1]:
                old_bonds[ii][0], old_bonds[ii][1] = old_bonds[ii][1], old_bonds[ii][0]


        temp_pdb_file = temp_filename(extension='pdb')
        temp_molecular_system = convert(molecular_system, to_form=temp_pdb_file, check=False)
        temp_molecular_system = convert(temp_molecular_system, to_form="pytraj.Topology", max_bond_length=max_bond_length, check=False)

        new_bonds = get(molecular_system, element='atom', selection=atom_indices, inner_bonded_atoms=True, check=False)

        for ii in range(old_bonds):
            if old_bonds[ii][0]>old_bonds[ii][1]:
                old_bonds[ii][0], old_bonds[ii][1] = old_bonds[ii][1], old_bonds[ii][0]

        for bond in new_bonds:
            if bond not in old_bonds:
                output.append(bond)

    else:

        raise NotImplementedError

    output = np.array(output)

    return output

