from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.variables import is_all
import numpy as np
import warnings

_sorted=sorted

# Protein:
# Enlace C-N: aproximadamente 1.33 Å
# Enlace C-C: aproximadamente 1.54 Å
# Enlace C-S: aproximadamente 1.82 Å
# Small molecule:
# Enlace C-H: aproximadamente 1.09 Å
# Enlace C-C: aproximadamente 1.54 Å
# Enlace C-O: aproximadamente 1.43 Å
# Enlace C-N: aproximadamente 1.47 Å
# Water molecule:
# Enlace O-H: aproximadamente 0.96 Å
# Lipid:
# Enlace C-H: aproximadamente 1.09 Å
# Enlace C-C: aproximadamente 1.54 Å
# Enlace P-O: aproximadamente 1.61 Å


@digest()
def get_missing_bonds(molecular_system, threshold='2 angstroms', selection='all',
                      structure_indices=0, syntax='MolSysMT', engine='MolSysMT',
                      sorted=True, skip_digestion=False):
    """
    To be written soon...
    """

    bonds = []

    if engine=="MolSysMT":

        from molsysmt import select, get
        from molsysmt.structure import get_contacts
        from molsysmt.element.group.water import get_bonded_atom_pairs as _bonds_in_water
        from molsysmt.element.group.ion import get_bonded_atom_pairs as _bonds_in_ion
        from molsysmt.element.group.amino_acid import get_bonded_atom_pairs as _bonds_in_amino_acid
        from molsysmt.element.group.terminal_capping import get_bonded_atom_pairs as _bonds_in_terminal_capping
        from molsysmt.element.group.small_molecule import get_bonded_atom_pairs as _bonds_in_small_molecule
        from molsysmt.element.group.terminal_capping import is_n_terminal_capping, is_c_terminal_capping

        aux_lists = get(molecular_system, element='group', selection=selection, group_name=True,
                        group_type=True, atom_index=True, atom_name=True,
                        skip_digestion=True)

        group_index = -1
        groups_undone = []
        atoms_undone = []

        aux_peptidic_bonds_C={}
        aux_peptidic_bonds_N={}

        for group_name, group_type, atom_indices, atom_names in zip(*aux_lists):

            group_index += 1

            match group_type:

                case 'water':

                    aux_bonds = _bonds_in_water(atom_names, atom_indices, sorted=False)
                    bonds += aux_bonds

                case 'ion':

                    aux_bonds = _bonds_in_ion(group_name, atom_names, atom_indices, sorted=False)
                    bonds += aux_bonds

                case 'amino acid':

                    aux_bonds = _bonds_in_amino_acid(group_name, atom_names, atom_indices, sorted=False)
                    bonds += aux_bonds

                    aux_peptidic_bonds_C[group_index]=atom_indices[atom_names.index('C')]
                    aux_peptidic_bonds_N[group_index]=atom_indices[atom_names.index('N')]

                case 'terminal capping':

                    aux_bonds = _bonds_in_terminal_capping(group_name, atom_names, atom_indices, sorted=False)
                    bonds += aux_bonds

                    if is_c_terminal_capping(group_name):
                        aux_peptidic_bonds_C[group_index]=atom_indices[atom_names.index('C')]
                    elif is_n_terminal_capping(group_name):
                        aux_peptidic_bonds_N[group_index]=atom_indices[atom_names.index('N')]
                    else:
                        raise ValueError("terminal capping not recognized as C- or N-")

                case 'small molecule':

                    aux_bonds = _bonds_in_small_molecule(group_name, atom_names, atom_indices, sorted=False)
                    bonds += aux_bonds

                case 'saccharide':

                    raise NotImplementedError('Group type "saccharide" not implemented')

                case 'oligosaccharide':

                    raise NotImplementedError('Group type "oligosaccharide" not implemented')

                case 'lipid':

                    raise NotImplementedError('Group type "lipid" not implemented')

                case 'nucleotide':

                    raise NotImplementedError('Group type "nucleotide" not implemented')

                case _:

                    groups_undone.append(group_index)

        # peptidic bonds

        aux_C = []
        aux_N = []

        for group_index in aux_peptidic_bonds_C.keys():
            if group_index+1 in aux_peptidic_bonds_N:
                aux_C.append(aux_peptidic_bonds_C[group_index])
                aux_N.append(aux_peptidic_bonds_N[group_index+1])

        if len(aux_C):
            peptidic_bonds = get_contacts(molecular_system, selection=aux_C, selection_2=aux_N,
                                          threshold=threshold, pairs=True, output_type='pairs',
                                          output_indices='atom', pbc=True, skip_digestion=True)[0]

            bonds += peptidic_bonds

        del(aux_lists, group_name, group_type, atom_indices, atom_names)
        del(aux_peptidic_bonds_C, aux_peptidic_bonds_N, aux_C, aux_N)
        
        if len(groups_undone):
            raise NotImplementedError('Some groups not defined with templates')
        if len(atoms_undone):
            raise NotImplementedError('Some atoms not defined with templates')

        if not is_all(selection):
            mask =  select(molecular_system, element='atom', selection=selection)
            tmp_bonds = []
            for bond in bonds:
                if (bond[0] in mask) and (bond[1] in mask):
                    tmp_bonds += bond
            bonds = tmp_bonds

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

        bonds = output

    else:

        raise NotImplementedMethodError

    #if sorted:
    #    bonds = _sorted(bonds)

    return bonds


