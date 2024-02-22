from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.variables import is_all
import numpy as np
import warnings
from molsysmt.element.group.amino_acid import get_bonded_atom_pairs as _bonds_in_amino_acid

@digest()
def get_missing_bonds(molecular_system, threshold='2 angstroms', selection='all',
                      structure_indices=0, syntax='MolSysMT', engine='MolSysMT',
                      with_templates=True, skip_digestion=False):
    """
    To be written soon...
    """

    if engine=="MolSysMT":

        from molsysmt.basic import get, select, get_form
        from molsysmt.structure import get_neighbors

        if is_all(selection):

            bonds = []
            bonds_templates = []
            bonds_distances = []

            if with_templates:

                aux_peptidic_bonds={'C':[], 'N':[]}

                form = get_form(molecular_system)

                if form=='molsysmt.Topology':

                    raise ValueError('The molecular system needs to have coordinates')

                if form=='molsysmt.MolSys':

                    aux_output = [np.arange(molecular_system.topology.groups.shape[0]).tolist(),
                                  molecular_system.topology.groups.group_name.tolist(),
                                  molecular_system.topology.groups.group_type.tolist()]

                    former_group_index = -1

                    atom_indices = []
                    atom_names = []
                    atom_types = []

                    aux_atom_indices = []
                    aux_atom_names = []
                    aux_atom_types = []

                    for atom in molecular_system.topology.atoms.itertuples():
                        if former_group_index != atom.group_index:
                            if former_group_index != -1:
                                atom_indices.append(aux_atom_indices)
                                atom_names.append(aux_atom_names)
                                atom_types.append(aux_atom_types)
                                aux_atom_indices = []
                                aux_atom_names = []
                                aux_atom_types = []
                            former_group_index = atom.group_index
                        aux_atom_indices.append(atom.Index)
                        aux_atom_names.append(atom.atom_name)
                        aux_atom_types.append(atom.atom_type)

                    aux_output += [atom_indices, atom_names, atom_types]

                    del atom_indices, atom_names, atom_types, aux_atom_indices, aux_atom_names, aux_atom_types

                else:

                    aux_output = get(molecular_system, element='group', group_index=True, group_name=True,
                                     group_type=True, atom_index=True, atom_name=True, atom_type=True,
                                     skip_digestion=True)

                for group_index, group_name, group_type, atom_indices, atom_names, atom_types in zip(*aux_output):

                    if group_type=='water':
                        aux_bonds = _bonds_in_water(atom_indices, atom_names, atom_types)
                        bonds_templates += aux_bonds
                    elif group_type=='ion':
                        aux_bonds = _bonds_in_ion(group_name, atom_indices, atom_names)
                        bonds_templates += aux_bonds
                    elif group_type=='amino acid':
                        aux_bonds, unk_atom_indices = _bonds_in_amino_acid(group_name, atom_indices, atom_names)
                        bonds_templates += aux_bonds
                        aux_peptidic_bonds['C'].append(atom_indices[atom_names.index('C')])
                        aux_peptidic_bonds['N'].append(atom_indices[atom_names.index('N')])

                        if len(unk_atom_indices):
                            iii=[]
                            for ii in unk_atom_indices:
                                iii.append(atom_names[atom_indices.index(ii)])
                            print('>>',group_name,unk_atom_indices,iii)
                            print('')
                        if len(unk_atom_indices):
                            aux_bonds_unk_atoms = []
                            neighbors, _ = get_neighbors(molecular_system, selection=unk_atom_indices,
                                                         selection_2=atom_indices, structure_indices=structure_indices,
                                                         threshold=threshold, skip_digestion=True)
                            for ii, nn in zip(unk_atom_indices, neighbors[0]):
                                mm = atom_indices.index(ii)
                                ii_type = atom_types[mm]
                                if ii_type == 'H':
                                    for jj in nn:
                                        if ii!=atom_indices[jj] and atom_types[jj]!='H':
                                            iii = ii
                                            jjj = atom_indices[jj]
                                            if iii<jjj:
                                                aux_bonds_unk_atoms.append([iii,jjj])
                                            else:
                                                aux_bonds_unk_atoms.append([jjj,iii])
                                else:
                                    for jj in nn:
                                        if ii!=atom_indices[jj]:
                                            iii = ii
                                            jjj = atom_indices[jj]
                                            if iii<jjj:
                                                aux_bonds_unk_atoms.append([iii,jjj])
                                            else:
                                                aux_bonds_unk_atoms.append([jjj,iii])
                            bonds_distances += aux_bonds_unk_atoms
                            print(aux_bonds_unk_atoms)
                            print(' ')

                    elif group_type=='small molecule':
                        raise NotImplementedError
                    elif group_type=='terminal capping':
                        raise NotImplementedError
                    elif group_type=='saccharide':
                        raise NotImplementedError
                    elif group_type=='oligosaccharide':
                        raise NotImplementedError
                    elif group_type=='lipid':
                        raise NotImplementedError
                    elif group_type=='nucleotide':
                        raise NotImplementedError
                    else:
                        indices_with_distance += atom_indices

                if len(aux_peptidic_bonds['C']) and len(aux_peptidic_bonds['N']):
                    aux_bonds = []
                    neighbors, _ = get_neighbors(molecular_system, selection=aux_peptidic_bonds['C'],
                                                 selection_2=aux_peptidic_bonds['N'],
                                                 structure_indices=structure_indices,
                                                 threshold=threshold)
                    for iii, nn in zip(aux_peptidic_bonds['C'], neighbors[0]):
                        for jj in nn:
                            jjj = aux_peptidic_bonds['N'][jj]
                            if iii<jjj:
                                aux_bonds.append([iii,jjj])
                            else:
                                aux_bonds.append([jjj,iii])
                    bonds_distances += aux_bonds
                    
                bonds += bonds_templates
                bonds += bonds_distances

            else:

                raise NotImplementedError

            #neighbors, _ = get_neighbors(molecular_system, selection=indices_with_distance, threshold=threshold)

            #if is_all(indices_with_distance):
            #    for atom_i, neighbors_frame in enumerate(neighbors):
            #        for atom_j in neighbors_frame[ii]:
            #            if atom_i < atom_j:
            #                bonds_with_distance.append([atom_i, atom_j])
            #else:
            #    for atom_i, neighbors_frame in enumerate(neighbors):
            #        for atom_j in neighbors_frame[ii]:
            #            if atom_i < atom_j:
            #                bonds_with_distance.append([atom_i, atom_j])



            output = sorted(bonds)

        else:

            raise NotImplementedError


        #neighbors, distance = get_neighbors(molecular_system, selection=atom_indices,
        #                                    selection_2=atom_indices, threshold=threshold, output='dict')

        #for atom_i, atom_j in old_bonds:
        #    for kk, neighbors_frame in enumerate(neighbors):
        #        if atom_j not in neighbors_frame[atom_i]:
        #            warnings.warn(f"The bond between atoms {atom_i} and {atom_j} was observed with a length larger than the threshold: distance[kk][atom_i]")

        #for ii, atom_index in enumerate(atom_indices):
        #    atom_i = atom_index
        #    for neighbors_frame in neighbors:
        #        for atom_j in neighbors_frame[ii]:
        #            if atom_i < atom_j:
        #                if [atom_i, atom_j] not in old_bonds:
        #                    if [atom_i, atom_j] not in output:
        #                        output.append([atom_i, atom_j])

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

    return output

def _bonds_in_water(atom_indices, atom_names, atom_type):

    if len(atom_indices)>=3:

        O = None
        Hs = []

        for ii,jj in zip(atom_indices, atom_type):
            if jj=='O':
                O=ii
            else:
                Hs.append(ii)

        return  [[O,Hs[0]], [O,Hs[1]]]

    else:

        return []

def _bonds_in_ion(group_name, atom_indices, atom_names):

    n_atoms=len(atom_indices)

    if n_atoms==1:

        return []

    elif n_atoms==2:

        return [atom_indices]
    
    else:

        raise NotImplementedError

