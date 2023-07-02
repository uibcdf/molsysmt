from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.variables import is_all
import numpy as np
import warnings

@digest()
def get_missing_bonds(molecular_system, threshold='2 angstroms', selection='all',
                      structure_indices='all', syntax='MolSysMT', engine='MolSysMT'):
    """
    To be written soon...
    """

    output = []

    if engine=="MolSysMT":

        from molsysmt.basic import get, select
        from molsysmt.structure import get_neighbors

        atom_indices = select(molecular_system, selection=selection, syntax=syntax)

        if is_all(structure_indices):
            n_atoms = get(molecular_system, element='system', n_structures=True)
            structure_indices = np.arange(n_atoms)

        old_bonds = get(molecular_system, element='atom', selection=atom_indices, inner_bonded_atoms=True)

        for ii in range(len(old_bonds)):
            if old_bonds[ii][0]>old_bonds[ii][1]:
                old_bonds[ii][0], old_bonds[ii][1] = old_bonds[ii][1], old_bonds[ii][0]

        neighbors, distance = get_neighbors(molecular_system, selection=atom_indices,
                                            selection_2=atom_indices, threshold=threshold, output='dict')

        for atom_i, atom_j in old_bonds:
            for kk, neighbors_frame in enumerate(neighbors):
                if atom_j not in neighbors_frame[atom_i]:
                    warnings.warn(f"The bond between atoms {atom_i} and {atom_j} was observed with a length larger than the threshold: distance[kk][atom_i]")

        for ii, atom_index in enumerate(atom_indices):
            atom_i = atom_index
            for neighbors_frame in neighbors:
                for atom_j in neighbors_frame[ii]:
                    if atom_i < atom_j:
                        if [atom_i, atom_j] not in old_bonds:
                            if [atom_i, atom_j] not in output:
                                output.append([atom_i, atom_j])

    elif engine=="pytraj":

        from molsysmt.basic import convert, get
        from os import remove
        from molsysmt._private.files_and_directories import temp_filename

        old_bonds = get(molecular_system, element='atom', selection=atom_indices, inner_bonded_atoms=True)

        for ii in range(old_bonds):
            if old_bonds[ii][0]>old_bonds[ii][1]:
                old_bonds[ii][0], old_bonds[ii][1] = old_bonds[ii][1], old_bonds[ii][0]


        temp_pdb_file = temp_filename(extension='pdb')
        temp_molecular_system = convert(molecular_system, to_form=temp_pdb_file)
        temp_molecular_system = convert(temp_molecular_system, to_form="pytraj.Topology", threshold=threshold)

        new_bonds = get(molecular_system, element='atom', selection=atom_indices, inner_bonded_atoms=True)

        for ii in range(old_bonds):
            if old_bonds[ii][0]>old_bonds[ii][1]:
                old_bonds[ii][0], old_bonds[ii][1] = old_bonds[ii][1], old_bonds[ii][0]

        for bond in new_bonds:
            if bond not in old_bonds:
                output.append(bond)

    else:

        raise NotImplementedMethodError

    output = np.array(output)

    return output

