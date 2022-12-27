from molsysmt._private.digestion import digest
import numpy as np
from pandas import DataFrame as df


@digest()
def info(molecular_system,
         element='system',
         indices=None,
         selection='all',
         syntax='MolSysMT',
         output_type='dataframe',
         ):
    """info(item, element='system', indices=None, selection='all', syntax='MolSysMT')

    Print out general information of a molecular model.

    Paragraph with detailed explanation.

    Parameters
    ----------

    molecular_system: molecular model
        Molecular model in any of the supported forms by MolSysMT. (See: XXX)

    element: str, default='system'
        The nature of the entities this method is going to work with: 'atom', 'group', 'chain' or
        'system'.

    indices: int, list, tuple or np.ndarray, default=None
        List of indices referring the set of elementted entities ('atom', 'group' or 'chain') this
        method is going to work with. The set of indices can be given by a list, tuple or numpy
        array of integers (0-based).


    selection: str, list, tuple or np.ndarray, default='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntax parsable by MolSysMT.

    syntax: str, default='MolSysMT'
       Selection syntax used in the argument `selection` (in case `selection` is a string). Find
       current options supported by MolSysMt in section 'Selection'.

    Returns
    -------
    None
        The method prints out a pandas dataframe with relevant information depending on the element
        and the form of the item.

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.get`, :func:`molsysmt.select`

    Notes
    -----

    """

    from . import get_form, get, convert, select
    from molsysmt.element import elements_to_string

    # Some forms should be converted to make this function faster

    form = get_form(molecular_system)

    if form in ['string:pdb_id', 'file:pdb', 'nglview.NGLWidget']:
        molecular_system = convert(molecular_system)

    if output_type == 'dataframe':

        if element == 'atom':

            atom_index, atom_id, atom_name, atom_type, \
            group_index, group_id, group_name, group_type, \
            component_index, \
            chain_index, \
            molecule_index, molecule_type, \
            entity_index, entity_name = get(molecular_system, element=element, indices=indices, selection=selection,
                                            syntax=syntax, atom_index=True, atom_id=True, atom_name=True,
                                            atom_type=True, group_index=True, group_id=True, group_name=True,
                                            group_type=True, component_index=True, chain_index=True,
                                            molecule_index=True,
                                            molecule_type=True, entity_index=True, entity_name=True,
                                            )

            return df({'index': atom_index, 'id': atom_id, 'name': atom_name, 'type': atom_type,
                       'group index': group_index, 'group id': group_id, 'group name': group_name,
                       'group type': group_type,
                       'component index': component_index,
                       'chain index': chain_index,
                       'molecule index': molecule_index, 'molecule type': molecule_type,
                       'entity index': entity_index, 'entity name': entity_name}).style.hide(axis='index')

        elif element == 'group':

            group_index, group_id, group_name, group_type, \
            n_atoms, component_index, \
            chain_index, \
            molecule_index, molecule_type, \
            entity_index, entity_name = get(molecular_system, element=element, indices=indices, selection=selection,
                                            syntax=syntax, group_index=True, group_id=True, group_name=True,
                                            group_type=True, n_atoms=True, component_index=True, chain_index=True,
                                            molecule_index=True, molecule_type=True, entity_index=True,
                                            entity_name=True)

            return df({'index': group_index, 'id': group_id, 'name': group_name, 'type': group_type,
                       'n atoms': n_atoms,
                       'component index': component_index,
                       'chain index': chain_index,
                       'molecule index': molecule_index, 'molecule type': molecule_type,
                       'entity index': entity_index, 'entity name': entity_name}).style.hide(axis='index')

        elif element == 'component':

            component_index, n_atoms, n_groups, \
            chain_index, \
            molecule_index, molecule_type, \
            entity_index, entity_name = get(molecular_system, element=element, indices=indices, selection=selection,
                                            syntax=syntax, component_index=True, n_atoms=True, n_groups=True,
                                            chain_index=True, molecule_index=True, molecule_type=True,
                                            entity_index=True, entity_name=True)

            return df({'index': component_index,
                       'n atoms': n_atoms, 'n groups': n_groups,
                       'chain index': chain_index,
                       'molecule index': molecule_index, 'molecule type': molecule_type,
                       'entity index': entity_index, 'entity name': entity_name}).style.hide(axis='index')

        elif element == 'chain':

            chain_index, chain_id, chain_name, \
            n_atoms, n_groups, n_components, \
            molecule_index, molecule_type, \
            entity_index, entity_name = get(molecular_system, element=element, indices=indices, selection=selection,
                                            syntax=syntax, chain_index=True, chain_id=True, chain_name=True,
                                            n_atoms=True, n_groups=True, n_components=True, molecule_index=True,
                                            molecule_type=True, entity_index=True, entity_name=True)

            if len(molecule_index.shape) > 1:
                n_objects = molecule_index.shape[0]
                aux_obj1_array = np.empty([n_objects], dtype='object')
                aux_obj2_array = np.empty([n_objects], dtype='object')
                for ii in range(n_objects):
                    aux_obj1_array[ii] = molecule_index[ii]
                    aux_obj2_array[ii] = molecule_type[ii]
                molecule_index = aux_obj1_array
                molecule_type = aux_obj2_array

            for ii in range(len(molecule_index)):
                if len(molecule_index[ii]) == 1:
                    molecule_index[ii] = molecule_index[ii][0]
                    molecule_type[ii] = molecule_type[ii][0]

            if len(entity_index.shape) > 1:
                n_objects = entity_index.shape[0]
                aux_obj1_array = np.empty([n_objects], dtype='object')
                aux_obj2_array = np.empty([n_objects], dtype='object')
                for ii in range(n_objects):
                    aux_obj1_array[ii] = entity_index[ii]
                    aux_obj2_array[ii] = entity_name[ii]
                entity_index = aux_obj1_array
                entity_name = aux_obj2_array

            for ii in range(len(entity_index)):
                if len(entity_index[ii]) == 1:
                    entity_index[ii] = entity_index[ii][0]
                    entity_name[ii] = entity_name[ii][0]

            return df({'index': chain_index, 'id': chain_id, 'name': chain_name,
                       'n atoms': n_atoms, 'n groups': n_groups, 'n components': n_components,
                       'molecule index': molecule_index, 'molecule type': molecule_type,
                       'entity index': entity_index, 'entity name': entity_name}).style.hide(axis='index')

        elif element == 'molecule':

            molecule_index, molecule_name, molecule_type, \
            n_atoms, n_groups, n_components, chain_index, \
            entity_index, entity_name = get(molecular_system, element=element, indices=indices, selection=selection,
                                            syntax=syntax, molecule_index=True, molecule_name=True,
                                            molecule_type=True, n_atoms=True, n_groups=True, n_components=True,
                                            chain_index=True, entity_index=True, entity_name=True)

            if len(chain_index.shape) > 1:
                n_objects = chain_index.shape[0]
                aux_obj_array = np.empty([n_objects], dtype='object')
                for ii in range(n_objects):
                    aux_obj_array[ii] = chain_index[ii]
                chain_index = aux_obj_array

            for ii in range(len(chain_index)):
                if len(chain_index[ii]) == 1:
                    chain_index[ii] = chain_index[ii][0]

            return df({'index': molecule_index, 'name': molecule_name, 'type': molecule_type,
                       'n atoms': n_atoms, 'n groups': n_groups, 'n components': n_components,
                       'chain index': chain_index,
                       'entity index': entity_index, 'entity name': entity_name}).style.hide(axis='index')

        elif element == 'entity':

            entity_index, entity_name, entity_type, \
            n_atoms, n_groups, n_components, n_chains, \
            n_molecules = get(molecular_system, element=element, indices=indices, selection=selection,
                              syntax=syntax, entity_index=True, entity_name=True, entity_type=True, n_atoms=True,
                              n_groups=True, n_components=True, n_chains=True, n_molecules=True)

            return df({'index': entity_index, 'name': entity_name, 'type': entity_type,
                       'n atoms': n_atoms, 'n groups': n_groups, 'n components': n_components,
                       'n chains': n_chains, 'n molecules': n_molecules
                       }).style.hide(axis='index')

        elif element == 'system':

            n_atoms, n_groups, n_components, n_chains, n_molecules, n_entities, n_structures, \
            n_ions, n_waters, n_small_molecules, n_peptides, n_proteins, n_dnas, \
            n_rnas, n_lipids, n_oligosaccharides = get(molecular_system, element=element, n_atoms=True, n_groups=True,
                    n_components=True, n_chains=True, n_molecules=True, n_entities=True, n_structures=True, n_ions=True,
                    n_waters=True, n_small_molecules=True, n_peptides=True, n_proteins=True, n_dnas=True,
                    n_rnas=True, n_lipids=True, n_oligosaccharides=True)

            tmp_df = df([{'form': form, 'n_atoms': n_atoms, 'n_groups': n_groups, 'n_components': n_components,
                          'n_chains': n_chains, 'n_molecules': n_molecules, 'n_entities': n_entities,
                          'n_waters': n_waters, 'n_ions': n_ions,
                          'n_small_molecules': n_small_molecules,
                          'n_peptides': n_peptides, 'n_proteins': n_proteins, 'n_dnas': n_dnas, 'n_rnas': n_rnas,
                          'n_lipids': n_lipids, 'n_oligosaccharides': n_oligosaccharides,
                          'n_structures': n_structures}], index=[0])

            if n_ions == 0 or n_ions is None:
                tmp_df.drop(columns=['n_ions'], inplace=True)

            if n_waters == 0 or n_waters is None:
                tmp_df.drop(columns=['n_waters'], inplace=True)

            if n_small_molecules == 0 or n_small_molecules is None:
                tmp_df.drop(columns=['n_small_molecules'], inplace=True)

            if n_peptides == 0 or n_peptides is None:
                tmp_df.drop(columns=['n_peptides'], inplace=True)

            if n_proteins == 0 or n_proteins is None:
                tmp_df.drop(columns=['n_proteins'], inplace=True)

            if n_dnas == 0 or n_dnas is None:
                tmp_df.drop(columns=['n_dnas'], inplace=True)

            if n_rnas == 0 or n_rnas is None:
                tmp_df.drop(columns=['n_rnas'], inplace=True)

            if n_lipids == 0 or n_lipids is None:
                tmp_df.drop(columns=['n_lipids'], inplace=True)

            if n_oligosaccharides == 0 or n_oligosaccharides is None:
                tmp_df.drop(columns=['n_oligosaccharides'], inplace=True)

            return tmp_df.style.hide(axis='index')

        else:

            raise ValueError('"element" needs one of the following strings: "atom", "group",\
                             "component", "chain", "molecule", "entity" or "system"')

    elif output_type == 'short_string':

        if indices is None and selection is not None:
            indices = select(molecular_system, selection=selection, element=element)

        string = elements_to_string(molecular_system, indices=indices, element=element)

        if len(string) == 1:
            return string[0]
        else:
            return string

    elif output_type == 'long_string':

        if element == 'atom':

            group_indices, chain_indices, molecule_indices = get(molecular_system, element=element, indices=indices,
                                                                 group_index=True, chain_index=True,
                                                                 molecule_index=True)

            atom_string = elements_to_string(molecular_system, indices=indices, element=element)
            group_string = elements_to_string(molecular_system, indices=group_indices, element='group')
            chain_string = elements_to_string(molecular_system, indices=chain_indices, element='chain')
            molecule_string = elements_to_string(molecular_system, indices=molecule_indices, element='molecule')

            string = []

            for list_strings in zip(atom_string, group_string, chain_string,
                                    molecule_string):
                string.append('/'.join(list_strings))

            if len(string) == 1:
                string = string[0]

        elif element == 'group':

            chain_indices, molecule_indices = get(molecular_system, element=element, indices=indices, chain_index=True,
                                                  molecule_index=True)

            group_string = elements_to_string(molecular_system, indices=indices, element=element)
            chain_string = elements_to_string(molecular_system, indices=chain_indices, element='chain')
            molecule_string = elements_to_string(molecular_system, indices=molecule_indices, element='molecule')

            string = []

            for list_strings in zip(group_string, chain_string,
                                    molecule_string):
                string.append('/'.join(list_strings))

            if len(string) == 1:
                string = string[0]

        elif element == 'component':

            chain_indices, molecule_indices = get(molecular_system, element=element, indices=indices, chain_index=True,
                                                  molecule_index=True)

            component_string = elements_to_string(molecular_system, indices=indices, element=element)
            chain_string = elements_to_string(molecular_system, indices=chain_indices, element='chain')
            molecule_string = elements_to_string(molecular_system, indices=molecule_indices, element='molecule')

            string = []

            for list_strings in zip(component_string, chain_string, molecule_string):
                string.append('/'.join(list_strings))

            if len(string) == 1:
                string = string[0]

        elif element == 'chain':

            chain_string = elements_to_string(molecular_system, indices=indices, element=element)
            string = chain_string

            if len(string) == 1:
                string = string[0]

        elif element == 'molecule':

            molecule_string = elements_to_string(molecular_system, indices=indices, element=element)
            string = molecule_string

            if len(string) == 1:
                string = string[0]

        elif element == 'entity':

            entity_string = elements_to_string(molecular_system, indices=indices, element=element)
            string = entity_string

            if len(string) == 1:
                string = string[0]

        else:

            raise NotImplementedError

        return string

    else:

        raise ValueError()

