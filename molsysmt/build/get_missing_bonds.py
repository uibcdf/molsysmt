from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.variables import is_all
from molsysmt._private.lists import sorted_list_of_pairs
from molsysmt.element.bond import max_expected_bond_length, bond_length_tolerance
import numpy as np
import warnings

@digest()
def get_missing_bonds(molecular_system, selection='all', structure_index=0, max_bond_distance='2 angstroms',
                      disulfide_bonds=False, disulfide_group_names=['CYS'], pbc=True,
                      syntax='MolSysMT', engine='MolSysMT', sorted=True, skip_digestion=False):

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
        from molsysmt.element.group.saccharide import get_bonded_atom_pairs as _bonds_in_saccharide
        from molsysmt.element.group.terminal_capping import is_n_terminal_capping, is_c_terminal_capping

        old_bonds = get(molecular_system, selection=selection, inner_bonded_atom_pairs=True)

        aux_lists = get(molecular_system, element='group', selection=selection, group_name=True,
                        group_type=True, atom_index=True, atom_name=True, atom_type=True,
                        skip_digestion=True)

        group_index = -1
        groups_undone = []
        atoms_undone = []

        aux_peptidic_bonds_C={}
        aux_peptidic_bonds_N={}

        bonds = []

        for group_name, group_type, atom_indices, atom_names, atom_types in zip(*aux_lists):

            group_index += 1

            aux_bonds = None

            match group_type:
                case "water":
                    aux_bonds = _bonds_in_water(atom_names, atom_indices, sorted=False)
                case "ion":
                    aux_bonds = _bonds_in_ion(group_name, atom_names, atom_indices, sorted=False)
                case "amino acid":
                    aux_bonds = _bonds_in_amino_acid(group_name, atom_names, atom_indices, sorted=False)
                    if 'C' in atom_names:
                        aux_peptidic_bonds_C[group_index]=atom_indices[atom_names.index('C')]
                    if 'N' in atom_names:
                        aux_peptidic_bonds_N[group_index]=atom_indices[atom_names.index('N')]
                case "terminal capping":
                    aux_bonds = _bonds_in_terminal_capping(group_name, atom_names, atom_indices, sorted=False)
                    if is_c_terminal_capping(group_name):
                        aux_peptidic_bonds_C[group_index]=atom_indices[atom_names.index('C')]
                    elif is_n_terminal_capping(group_name):
                        aux_peptidic_bonds_N[group_index]=atom_indices[atom_names.index('N')]
                    else:
                        raise ValueError("terminal capping not recognized as C- or N-")
                case "small molecule":
                    aux_bonds = _bonds_in_small_molecule(group_name, atom_names, atom_indices, sorted=False)
                case "saccharide":
                    aux_bonds = _bonds_in_saccharide(group_name, atom_names, atom_indices, sorted=False)
                case "oligosaccharide":
                    aux_bonds = None
                case "lipid":
                    aux_bonds = None
                case "nucleotide":
                    aux_bonds = None
                case _:
                    aux_bonds = None

            if aux_bonds is None:
                aux_bonds = _bonds_in_group_without_template(molecular_system, atom_indices, atom_names, atom_types,
                                                             group_name, group_type,
                                                             structure_index=structure_index, max_bond_distance=max_bond_distance,
                                                             sorted=False)

            bonds += aux_bonds

        # peptidic bonds

        aux_bonds = _get_peptidic_bonds(molecular_system, aux_peptidic_bonds_C, aux_peptidic_bonds_N, structure_index=structure_index,
                                        max_bond_distance=max_bond_distance, pbc=pbc, sorted=False)

        bonds += aux_bonds

        # disulfide bonds

        if disulfide_bonds:

            from .get_disulfide_bonds import get_disulfide_bonds

            aux_bonds = get_disulfide_bonds(molecular_system, selection=selection, structure_index=structure_index,
                                            max_bond_distance=None, group_names=disulfide_group_names, pbc=pbc,
                                            sorted=False, skip_digestion=True)

            bonds += aux_bonds

        # mask with selection

        if not is_all(selection):
            mask =  select(molecular_system, element='atom', selection=selection)
            tmp_bonds = []
            for bond in bonds:
                if (bond[0] in mask) and (bond[1] in mask):
                    tmp_bonds += bond
            bonds = tmp_bonds

        # remove old bonds

        if old_bonds:

            tmp_bonds = []
            for ii in bonds:
                if ii not in old_bonds:
                    tmp_bonds.append(ii)
            bonds = tmp_bonds

    elif engine=="pytraj":

        from molsysmt.basic import convert, get
        from os import remove
        from molsysmt._private.files_and_directories import temp_filename

        old_bonds = get(molecular_system, element='atom', selection=selection, inner_bonded_atoms=True)

        for ii in range(len(old_bonds)):
            if old_bonds[ii][0]>old_bonds[ii][1]:
                old_bonds[ii][0], old_bonds[ii][1] = old_bonds[ii][1], old_bonds[ii][0]


        temp_pdb_file = temp_filename(extension='pdb')
        temp_molecular_system = convert(molecular_system, to_form=temp_pdb_file)
        temp_molecular_system = convert(temp_molecular_system, to_form="pytraj.Topology", max_bond_distance=max_bond_distance)

        new_bonds = get(temp_molecular_system, element='atom', selection=selection, inner_bonded_atoms=True)

        for ii in range(len(new_bonds)):
            if new_bonds[ii][0]>new_bonds[ii][1]:
                new_bonds[ii][0], new_bonds[ii][1] = new_bonds[ii][1], new_bonds[ii][0]

        output = []
        for bond in new_bonds:
            if bond not in old_bonds:
                output.append(bond)

        bonds = output

    else:

        raise NotImplementedMethodError

    if sorted:

        bonds = sorted_list_of_pairs(bonds)

    return bonds

def _bonds_in_group_without_template(molecular_system, atom_indices, atom_names, atom_types, group_name, group_type,
                            structure_index=0, max_bond_distance='2 angstroms', pbc=True, sorted=True):

    from molsysmt.structure import get_neighbors

    bonds = []

    pairs, dists = get_neighbors(molecular_system, selection=atom_indices, structure_indices = structure_index,
                                 threshold=max_bond_distance, output_type='pairs', output_indices='selection',
                                 sorted=False, pbc=pbc, skip_digestion=True)

    n_bonds_hs = {}

    for pair, dist in zip(pairs[0], dists[0]):

        atom_type_1 = atom_types[pair[0]]
        atom_type_2 = atom_types[pair[1]]

        atom_index_1 = atom_indices[pair[0]]
        atom_index_2 = atom_indices[pair[1]]

        add_bond = False

        try:
            aux_bond_distance = max_expected_bond_length[group_type][atom_type_1][atom_type_2]
            if aux_bond_distance is not None:
                if dist<=aux_bond_distance+bond_length_tolerance:
                    add_bond = True
        except:
            message = (f"No max bond length defined between atom types {atom_type_1} and {atom_type_2} "
                       f"in group type {group_type}. The bond between atoms {pair} was defined "
                       f"by max_bond_distance={round(max_bond_distance,4)}.")
            print("Warning: "+message)
            add_bond = True

        if add_bond:
            bonds.append([atom_index_1, atom_index_2])
            if atom_type_1=='H':
                if atom_index_1 in n_bonds_hs:
                    n_bonds_hs[atom_index_1] += 1
                else:
                    n_bonds_hs[atom_index_1] = 1
            if atom_type_2=='H':
                if atom_index_2 in n_bonds_hs:
                    n_bonds_hs[atom_index_2] += 1
                else:
                    n_bonds_hs[atom_index_2] = 1

    for ii in n_bonds_hs.keys():
        if n_bonds_hs[ii]>1:
            print(f"Warning: H atom {ii} in group {group_name} has {n_bonds_hs[ii]} bonds")

    if sorted:
        bonds = sorted_list_of_pairs(bonds)

    return bonds

def _get_peptidic_bonds(molecular_system, aux_peptidic_bonds_C, aux_peptidic_bonds_N,
                        selection='all', structure_index=0, max_bond_distance='2 angstroms', pbc=True, sorted=True):

    from molsysmt.structure import get_neighbors

    bonds = []

    aux_C = []
    aux_N = []

    for group_index in aux_peptidic_bonds_C.keys():
        if group_index+1 in aux_peptidic_bonds_N:
            aux_C.append(aux_peptidic_bonds_C[group_index])
            aux_N.append(aux_peptidic_bonds_N[group_index+1])

    if len(aux_C):


        pairs, dists = get_neighbors(molecular_system, selection=aux_C, selection_2=aux_N,
                       structure_indices = structure_index, threshold=max_bond_distance, output_type='pairs',
                       output_indices = 'atom', pbc=pbc, sorted=False, skip_digestion=True)
        for pair, dist in zip(pairs[0], dists[0]):
            if dist <= max_expected_bond_length['protein']['C']['N']+bond_length_tolerance:
                bonds.append(pair)

    if sorted:
        bonds = sorted_list_of_pairs(bonds)

    return bonds

