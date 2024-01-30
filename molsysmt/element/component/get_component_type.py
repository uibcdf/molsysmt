from molsysmt._private.digestion import digest
import numpy as np


@digest()
def get_component_type(molecular_system, element='atom', selection='all', redefine_indices=False,
                       redefine_types=False, syntax='MolSysMT', skip_digestion=False):

    from molsysmt.basic import get

    if redefine_indices or redefine_types:

        from molsysmt.basic import select
        from .get_component_index import get_component_index

        if redefine_indices:

            atom_indices = select(molecular_system, element=element, selection=selection,
                                  syntax=syntax, skip_digestion=True)

            if element!='atom':
                aux_atom_indices = []
                for aux in atom_indices:
                    aux_atom_indices += aux
                atom_indices = aux_atom_indices

            component_indices = get_component_index(molecular_system, element='atom',
                                                    selection='all', redefine_indices=True,
                                                    skip_digestion=True)

            unique_component_indices, first_atoms, n_atoms = np.unique(component_indices, return_index=True,
                                                                      return_count=True)

            component_types={}

            for component_index, first_atom, aux_n_atoms in zip(unique_component_indices, first_atoms, n_atoms):

                atom_indices_component = list(arange(aux_n_atoms))+first_atom
                aux_group_names, aux_group_types = get(molecular_system, element='group',
                                                       selection='atom_indices in @atom_indices_component',
                                                       syntax='molsysmt.MolSys', skip_digestion=True)

                component_type = _get_component_type_from_group_names_and_types(aux_group_names, aux_group_types)

                component_types[component_index]=component_type

            if element == 'atom':

                output = [component_type[component_indices[ii]] for ii in atom_indices]

            elif element == 'group':

                output = []
                group_indices = get(molecular_system, element='atom',
                                        selection=atom_indices, group_indices=True, skip_digestion=True)
                former_index = -1
                for ii,jj,kk in zip(group_indices, atom_indices, component_indices):
                    if ii!=former_index:
                        output.append(component_types[kk])

                del(group_indices)

            elif element == 'component':

                output = list(component_types.values())

            else:

                raise NotImplementedError

            del atom_indices, component_types, component_indices 

        else:

            pass

    else:

        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     component_type=True, skip_digestion=True)

    return output


def _get_component_type_from_group_names_and_types(group_names, group_types):

    from molsysmt.config import min_length_protein

    n_groups = len(group_types)
    first_group_type = group_types[0]
    last_group_type = group_types[-1]
    first_group_name = group_names[0]

    if first_group_type in ['water', 'ion', 'small molecule', 'lipid']:
        tmp_type = first_group_type
    elif (first_group_type == 'amino acid') or (first_group_type == 'terminal capping'):
        if first_group_type == 'terminal capping':
            n_groups -= 1
        if last_group_type == 'terminal capping':
            n_groups -= 1
        if n_groups >= min_length_protein:
            tmp_type = 'protein'
        else:
            tmp_type = 'peptide'
    elif first_group_type == 'nucleotide':
        if first_group_name in rna_names:
            tmp_type = 'rna'
        elif first_group_name in dna_names:
            tmp_type = 'dna'
    else:
        tmp_type = 'unknown'

    return tmp_type

