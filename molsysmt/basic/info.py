from molsysmt._private.digestion import digest
import numpy as np
from pandas import DataFrame as df


@digest()
def info(molecular_system,
         element='system',
         selection='all',
         syntax='MolSysMT',
         ):
    """
    Printing out summary information of a molecular system

    This function returns a Pandas DataFrame with a summary of the elements selection or of the
    entiry system.

    Parameters
    ----------

    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms
        <Introduction_Forms>` to be analysed by this function.

    element: {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'}, default 'system'
        The summary information is obtained for the elements of the system specified by this argument.

    selection : index, tuple, list, numpy.ndarray or str, default 'all'
        Selection of elements of the molecular system to build the summary information table. The
        selection can be given by a list, tuple or numpy array of element indices (0-based
        integers) -up to the value of the ``element`` input argument-; or by means of a query
        string following any of :ref:`the selection syntaxes parsable by MolSysMT
        <Introduction_Selection>`.

    syntax : str, default 'MolSysMT'
        :ref:`Supported syntax <Introduction_Selection>` used in the `selection` argument (in case
        it is a string).


    Returns
    -------
    pandas.DataFrame
        The method returns a pandas dataframe with relevant information depending on the element
        and the form of the item.


    Raises
    ------

    NotSupportedFormError
        The function raises a NotSupportedFormError in case a molecular system
        is introduced with a not supported form.

    ArgumentError
        The function raises an ArgumentError in case an input argument value
        does not meet the required conditions.

    SyntaxError
        The function raises a SyntaxError in case the syntax argument takes a not supported value. 


    .. versionadded:: 0.1.0



    Notes
    -----

    The list of supported molecular systems' forms is detailed in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.

    The list of supported selection syntaxes can be checked in the documentation section
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`.


    See Also
    --------

    :func:`molsysmt.basic.select`
        Selecting elements of a molecular system


    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> from molsysmt.systems import demo
    >>> molecular_system = msm.basic.convert(demo['T4 lysozyme L99A']['181l.mmtf'])
    >>> info_df = msm.basic.info(molecular_system, element='entity')
    >>> print(info_df.to_string())
    index name type n atoms n groups n components n chains n molecules
    0 T4 lysozyme protein 1291 164 3 3 3
    1 2-hydroxyethyl disulfide small molecule 8 1 1 1 1
    2 Benzene small molecule 6 1 1 1 1
    3 water water 136 136 136 1 136

    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Info <Tutorial_Info>`.


    """

    from . import get_form, get, convert, select
    from molsysmt.form import _dict_modules

    form = get_form(molecular_system)

    if isinstance(form, (list, tuple)):
        attributes_filter = _dict_modules[form[0]].attributes.copy()
        for aux_form in form[1:]:
            for aux_attribute, aux_bool in _dict_modules[aux_form].attributes.items():
                if aux_bool:
                    attributes_filter[aux_attribute]=True
    else:
        attributes_filter = _dict_modules[form].attributes

    if not isinstance(molecular_system, (list, tuple)):
        molecular_system = [molecular_system]

    if element == 'atom':

        atom_index, atom_id, atom_name, atom_type, \
        group_index, group_id, group_name, group_type, \
        component_index, \
        chain_index, \
        molecule_index, molecule_type, \
        entity_index, entity_name = get(molecular_system, element=element, selection=selection,
                                        syntax=syntax, skip_digestion=True, atom_index=True, atom_id=True,
                                        atom_name=True, atom_type=True, group_index=True, group_id=True,
                                        group_name=True, group_type=True, component_index=True,
                                        chain_index=True, molecule_index=True, molecule_type=True,
                                        entity_index=True, entity_name=True,
                                        )

        if not attributes_filter['atom_index']: atom_index=None
        if not attributes_filter['atom_id']: atom_id=None
        if not attributes_filter['atom_name']: atom_name=None
        if not attributes_filter['atom_type']: atom_type=None
        if not attributes_filter['group_index']: group_index=None
        if not attributes_filter['group_id']: group_id=None
        if not attributes_filter['group_name']: group_name=None
        if not attributes_filter['group_type']: group_type=None
        if not attributes_filter['component_index']: component_index=None
        if not attributes_filter['chain_index']: chain_index=None
        if not attributes_filter['molecule_index']: molecule_index=None
        if not attributes_filter['molecule_type']: molecule_type=None
        if not attributes_filter['entity_index']: entity_index=None
        if not attributes_filter['entity_name']: entity_name=None

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
        entity_index, entity_name = get(molecular_system, element=element, selection=selection,
                                        syntax=syntax, skip_digestion=True, group_index=True, group_id=True,
                                        group_name=True, group_type=True, n_atoms=True, component_index=True,
                                        chain_index=True, molecule_index=True, molecule_type=True, entity_index=True,
                                        entity_name=True)

        if not attributes_filter['group_index']: group_index=None
        if not attributes_filter['group_id']: group_id=None
        if not attributes_filter['group_name']: group_name=None
        if not attributes_filter['group_type']: group_type=None
        if not attributes_filter['n_atoms']: n_atoms=None
        if not attributes_filter['component_index']: component_index=None
        if not attributes_filter['chain_index']: chain_index=None
        if not attributes_filter['molecule_index']: molecule_index=None
        if not attributes_filter['molecule_type']: molecule_type=None
        if not attributes_filter['entity_index']: entity_index=None
        if not attributes_filter['entity_name']: entity_name=None

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
        entity_index, entity_name = get(molecular_system, element=element, selection=selection,
                                        syntax=syntax, skip_digestion=True, component_index=True,
                                        n_atoms=True, n_groups=True, chain_index=True, molecule_index=True,
                                        molecule_type=True, entity_index=True, entity_name=True)

        if not attributes_filter['component_index']: component_index=None
        if not attributes_filter['n_atoms']: n_atoms=None
        if not attributes_filter['n_groups']: n_groups=None
        if not attributes_filter['chain_index']: chain_index=None
        if not attributes_filter['molecule_index']: molecule_index=None
        if not attributes_filter['molecule_type']: molecule_type=None
        if not attributes_filter['entity_index']: entity_index=None
        if not attributes_filter['entity_name']: entity_name=None

        return df({'index': component_index,
                   'n atoms': n_atoms, 'n groups': n_groups,
                   'chain index': chain_index,
                   'molecule index': molecule_index, 'molecule type': molecule_type,
                   'entity index': entity_index, 'entity name': entity_name}).style.hide(axis='index')

    elif element == 'chain':

        chain_index, chain_id, chain_name, \
        n_atoms, n_groups, n_components, \
        molecule_index, molecule_type, \
        entity_index, entity_name = get(molecular_system, element=element, selection=selection,
                                        syntax=syntax, skip_digestion=True, chain_index=True, chain_id=True,
                                        chain_name=True, n_atoms=True, n_groups=True, n_components=True,
                                        molecule_index=True, molecule_type=True, entity_index=True, entity_name=True)

        if not attributes_filter['chain_index']: chain_index=None
        if not attributes_filter['chain_id']: chain_id=None
        if not attributes_filter['chain_name']: chain_name=None
        if not attributes_filter['n_atoms']: n_atoms=None
        if not attributes_filter['n_groups']: n_groups=None
        if not attributes_filter['n_components']: n_components=None
        if not attributes_filter['molecule_index']: molecule_index=None
        if not attributes_filter['molecule_type']: molecule_type=None
        if not attributes_filter['entity_index']: entity_index=None
        if not attributes_filter['entity_name']: entity_name=None

        return df({'index': chain_index, 'id': chain_id, 'name': chain_name,
                   'n atoms': n_atoms, 'n groups': n_groups, 'n components': n_components,
                   'molecule index': molecule_index, 'molecule type': molecule_type,
                   'entity index': entity_index, 'entity name': entity_name}).style.hide(axis='index')

    elif element == 'molecule':

        molecule_index, molecule_name, molecule_type, \
        n_atoms, n_groups, n_components, chain_index, \
        entity_index, entity_name = get(molecular_system, element=element, selection=selection,
                                        syntax=syntax, skip_digestion=True, molecule_index=True, molecule_name=True,
                                        molecule_type=True, n_atoms=True, n_groups=True, n_components=True,
                                        chain_index=True, entity_index=True, entity_name=True)

        if not attributes_filter['molecule_index']: molecule_index=None
        if not attributes_filter['molecule_name']: molecule_name=None
        if not attributes_filter['molecule_type']: molecule_type=None
        if not attributes_filter['n_atoms']: n_atoms=None
        if not attributes_filter['n_groups']: n_groups=None
        if not attributes_filter['n_components']: n_components=None
        if not attributes_filter['chain_index']: chain_index=None
        if not attributes_filter['entity_index']: entity_index=None
        if not attributes_filter['entity_name']: entity_name=None

        return df({'index': molecule_index, 'name': molecule_name, 'type': molecule_type,
                   'n atoms': n_atoms, 'n groups': n_groups, 'n components': n_components,
                   'chain index': chain_index,
                   'entity index': entity_index, 'entity name': entity_name}).style.hide(axis='index')

    elif element == 'entity':

        entity_index, entity_name, entity_type, \
        n_atoms, n_groups, n_components, n_chains, \
        n_molecules = get(molecular_system, element=element, selection=selection,
                          syntax=syntax, skip_digestion=True, entity_index=True, entity_name=True,
                          entity_type=True, n_atoms=True, n_groups=True, n_components=True, n_chains=True,
                          n_molecules=True)

        if not attributes_filter['entity_index']: entity_index=None
        if not attributes_filter['entity_name']: entity_name=None
        if not attributes_filter['entity_type']: entity_type=None
        if not attributes_filter['n_atoms']: n_atoms=None
        if not attributes_filter['n_groups']: n_groups=None
        if not attributes_filter['n_components']: n_components=None
        if not attributes_filter['n_chains']: n_chains=None
        if not attributes_filter['n_molecules']: n_molecules=None

        return df({'index': entity_index, 'name': entity_name, 'type': entity_type,
                   'n atoms': n_atoms, 'n groups': n_groups, 'n components': n_components,
                   'n chains': n_chains, 'n molecules': n_molecules
                   }).style.hide(axis='index')

    elif element == 'system':

        n_atoms, n_groups, n_components, n_chains, n_molecules, n_entities, n_structures, \
        n_ions, n_waters, n_small_molecules, n_peptides, n_proteins, n_dnas, \
        n_rnas, n_lipids, n_oligosaccharides, n_saccharides = get(molecular_system, element=element, skip_digestion=True,
                n_atoms=True, n_groups=True,
                n_components=True, n_chains=True, n_molecules=True, n_entities=True, n_structures=True, n_ions=True,
                n_waters=True, n_small_molecules=True, n_peptides=True, n_proteins=True, n_dnas=True,
                n_rnas=True, n_lipids=True, n_oligosaccharides=True, n_saccharides=True)

        if not attributes_filter['n_atoms']: n_atoms=None
        if not attributes_filter['n_groups']: n_groups=None
        if not attributes_filter['n_components']: n_components=None
        if not attributes_filter['n_chains']: n_chains=None
        if not attributes_filter['n_molecules']: n_molecules=None
        if not attributes_filter['n_entities']: n_entities=None
        if not attributes_filter['n_structures']: n_structures=None
        if not attributes_filter['n_ions']: n_ions=None
        if not attributes_filter['n_waters']: n_waters=None
        if not attributes_filter['n_small_molecules']: n_small_molecules=None
        if not attributes_filter['n_peptides']: n_peptides=None
        if not attributes_filter['n_proteins']: n_proteins=None
        if not attributes_filter['n_dnas']: n_dnas=None
        if not attributes_filter['n_rnas']: n_rnas=None
        if not attributes_filter['n_lipids']: n_lipids=None
        if not attributes_filter['n_oligosaccharides']: n_oligosaccharides=None
        if not attributes_filter['n_saccharides']: n_saccharides=None

        tmp_df = df([{'form': form, 'n_atoms': n_atoms, 'n_groups': n_groups, 'n_components': n_components,
                      'n_chains': n_chains, 'n_molecules': n_molecules, 'n_entities': n_entities,
                      'n_waters': n_waters, 'n_ions': n_ions,
                      'n_small_molecules': n_small_molecules,
                      'n_peptides': n_peptides, 'n_proteins': n_proteins, 'n_dnas': n_dnas, 'n_rnas': n_rnas,
                      'n_lipids': n_lipids, 'n_oligosaccharides': n_oligosaccharides, 'n_saccharides': n_saccharides,
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

        if n_saccharides == 0 or n_saccharides is None:
            tmp_df.drop(columns=['n_saccharides'], inplace=True)

        return tmp_df.style.hide(axis='index')

    else:

        raise ValueError('"element" needs one of the following strings: "atom", "group",\
                          "component", "chain", "molecule", "entity" or "system"')


