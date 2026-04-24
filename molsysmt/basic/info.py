from molsysmt._private.arg_digestion import arg_digest
import numpy as np
from pandas import DataFrame as df
from smonitor import signal


def _to_python(col):
    """Convert a list of values to native Python types, stripping numpy scalars."""
    if col is None:
        return None
    return [v.item() if hasattr(v, 'item') else v for v in col]


@signal(tags=['api', 'get'])
@arg_digest()
def info(molecular_system,
         element='system',
         selection='all',
         structure_indices='all',
         syntax='MolSysMT',
         output_type='styler',
         skip_digestion=False
         ):
    """
    Display a summary table of a molecular system or selected elements.

    This function produces a formatted summary table (as a Pandas *Styler*, *DataFrame*, or *Dictionary*)
    with key attributes of a molecular system, either for the whole system or for a given `element`
    level and `selection`. The columns returned depend on the chosen `element` and on the attributes
    available in the underlying form(s).

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to analyze, in any of the :ref:`supported forms <Introduction_Forms>`.
    element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'}, default 'system'
        Hierarchical level for which the summary is generated.
    selection : int, tuple, list, numpy.ndarray or str, default 'all'
        Selection of elements at the specified level. It can be a 0-based index collection or
        a selection string parsed according to :ref:`Introduction_Selection`.
    structure_indices : int, list, tuple, numpy.ndarray or str, default 'all'
        Indices of the structures to be considered if the system summary is requested.
    syntax : str, default 'MolSysMT'
        Selection syntax used when `selection` is a string. See :ref:`Introduction_Selection`.
    output_type : {'styler', 'dataframe', 'dictionary'}, default 'styler'
        The type of the output object. 'styler' returns a Pandas Styler (best for notebooks),
        'dataframe' returns a raw Pandas DataFrame, and 'dictionary' returns a Python dict.
    skip_digestion : bool, default False
        Whether to skip MolSysMT’s internal argument digestion mechanism.

        MolSysMT includes a built-in digestion system that validates and normalizes
        function arguments. This process checks types, shapes, and values, and automatically
        adjusts them when possible to meet expected formats.

        Setting `skip_digestion=True` disables this process, which may improve performance
        in workflows where inputs are already validated. Use with caution: only set this to
        `True` if you are certain all input arguments are correct and consistent.

    Returns
    -------
    pandas.io.formats.style.Styler
        A Pandas *Styler* wrapping a DataFrame with the summary. The exact columns depend on
        `element` and on the attributes exposed by the input form(s).

    Raises
    ------
    NotSupportedFormError
        If the molecular system has an unsupported form.
    ArgumentError
        If any input argument is invalid or inconsistent.

    Notes
    -----
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.
    - The function hides the row index for readability using Pandas’ Styler API; you can access
      the underlying DataFrame via the `.data` attribute (depending on your Pandas version) or
      by rebuilding it from the original values if needed.

    See Also
    --------
    :func:`molsysmt.basic.select`
        Select elements from a molecular system.
    :func:`molsysmt.basic.get`
        Retrieve values of attributes from a molecular system.
    :func:`molsysmt.basic.get_form`
        Retrieve the form of a molecular system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> molsys = msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'])
    >>> print(msm.info(molsys, element='entity').to_string()) # doctest: +NORMALIZE_WHITESPACE
    index  name                       type     n atoms  n groups  n components  n chains  n molecules
    0      T4 LYSOZYME                protein  1289     162       1             1         1
    1      CHLORIDE ION               ion      2        2         2             2         2
    2      2-HYDROXYETHYL DISULFIDE   small molecule    8        1         1         1         1
    3      BENZENE                    small molecule    6        1         1         1         1
    4      water                      water    136      136       136           1         136
    >>> # If you are working in a Jupyter notebook, you can simply run:
    >>> # msm.info(molsys, element='entity')
    >>> # And the table will be displayed in a nicely formatted style by Pandas.

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Info`.

    .. versionadded:: 1.0.0
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

        tmp_df = df({'index': _to_python(atom_index), 'id': _to_python(atom_id),
                      'name': _to_python(atom_name), 'type': _to_python(atom_type),
                      'group index': _to_python(group_index), 'group id': _to_python(group_id),
                      'group name': _to_python(group_name), 'group type': _to_python(group_type),
                      'component index': _to_python(component_index),
                      'chain index': _to_python(chain_index),
                      'molecule index': _to_python(molecule_index), 'molecule type': _to_python(molecule_type),
                      'entity index': _to_python(entity_index), 'entity name': _to_python(entity_name)})

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

        tmp_df = df({'index': _to_python(group_index), 'id': _to_python(group_id),
                      'name': _to_python(group_name), 'type': _to_python(group_type),
                      'n atoms': _to_python(n_atoms),
                      'component index': _to_python(component_index),
                      'chain index': _to_python(chain_index),
                      'molecule index': _to_python(molecule_index), 'molecule type': _to_python(molecule_type),
                      'entity index': _to_python(entity_index), 'entity name': _to_python(entity_name)})

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

        tmp_df = df({'index': _to_python(component_index),
                      'n atoms': _to_python(n_atoms), 'n groups': _to_python(n_groups),
                      'chain index': _to_python(chain_index),
                      'molecule index': _to_python(molecule_index), 'molecule type': _to_python(molecule_type),
                      'entity index': _to_python(entity_index), 'entity name': _to_python(entity_name)})

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

        tmp_df = df({'index': _to_python(chain_index), 'id': _to_python(chain_id),
                      'name': _to_python(chain_name),
                      'n atoms': _to_python(n_atoms), 'n groups': _to_python(n_groups),
                      'n components': _to_python(n_components),
                      'molecule index': _to_python(molecule_index), 'molecule type': _to_python(molecule_type),
                      'entity index': _to_python(entity_index), 'entity name': _to_python(entity_name)})

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

        tmp_df = df({'index': _to_python(molecule_index), 'name': _to_python(molecule_name),
                      'type': _to_python(molecule_type),
                      'n atoms': _to_python(n_atoms), 'n groups': _to_python(n_groups),
                      'n components': _to_python(n_components),
                      'chain index': _to_python(chain_index),
                      'entity index': _to_python(entity_index), 'entity name': _to_python(entity_name)})

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

        tmp_df = df({'index': _to_python(entity_index), 'name': _to_python(entity_name),
                      'type': _to_python(entity_type),
                      'n atoms': _to_python(n_atoms), 'n groups': _to_python(n_groups),
                      'n components': _to_python(n_components),
                      'n chains': _to_python(n_chains), 'n molecules': _to_python(n_molecules)
                      })

    elif element == 'system':

        if selection == 'all':
            n_atoms, n_groups, n_components, n_chains, n_molecules, n_entities, n_structures, \
            n_ions, n_waters, n_small_molecules, n_peptides, n_proteins, n_dnas, \
            n_rnas, n_lipids, n_polysaccharides, n_saccharides = get(molecular_system, element=element, skip_digestion=True,
                    n_atoms=True, n_groups=True,
                    n_components=True, n_chains=True, n_molecules=True, n_entities=True, n_structures=True, n_ions=True,
                    n_waters=True, n_small_molecules=True, n_peptides=True, n_proteins=True, n_dnas=True,
                    n_rnas=True, n_lipids=True, n_polysaccharides=True, n_saccharides=True)
        else:
            atom_indices_resolved = select(molecular_system, selection=selection, syntax=syntax, skip_digestion=True)
            n_atoms, n_groups, n_components, n_chains, n_molecules, n_entities, \
            n_ions, n_waters, n_small_molecules, n_peptides, n_proteins, n_dnas, \
            n_rnas, n_lipids, n_polysaccharides, n_saccharides = get(molecular_system, element='atom',
                    selection=atom_indices_resolved, skip_digestion=True,
                    n_atoms=True, n_groups=True, n_components=True, n_chains=True,
                    n_molecules=True, n_entities=True,
                    n_ions=True, n_waters=True, n_small_molecules=True, n_peptides=True,
                    n_proteins=True, n_dnas=True, n_rnas=True, n_lipids=True,
                    n_polysaccharides=True, n_saccharides=True)
            n_structures = get(molecular_system, element='system', n_structures=True, skip_digestion=True)

        if structure_indices != 'all' and structure_indices is not None:
            n_structures = len(structure_indices)

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
        if not attributes_filter['n_polysaccharides']: n_polysaccharides=None
        if not attributes_filter['n_saccharides']: n_saccharides=None

        tmp_df = df([{'form': form, 'n_atoms': n_atoms, 'n_groups': n_groups, 'n_components': n_components,
                      'n_chains': n_chains, 'n_molecules': n_molecules, 'n_entities': n_entities,
                      'n_waters': n_waters, 'n_ions': n_ions,
                      'n_small_molecules': n_small_molecules,
                      'n_peptides': n_peptides, 'n_proteins': n_proteins, 'n_dnas': n_dnas, 'n_rnas': n_rnas,
                      'n_lipids': n_lipids, 'n_polysaccharides': n_polysaccharides, 'n_saccharides': n_saccharides,
                      'n_structures': n_structures}], index=[0])

        if n_ions == 0 or n_ions is None:
            if 'n_ions' in tmp_df.columns:
                tmp_df.drop(columns=['n_ions'], inplace=True)

        if n_waters == 0 or n_waters is None:
            if 'n_waters' in tmp_df.columns:
                tmp_df.drop(columns=['n_waters'], inplace=True)

        if n_small_molecules == 0 or n_small_molecules is None:
            if 'n_small_molecules' in tmp_df.columns:
                tmp_df.drop(columns=['n_small_molecules'], inplace=True)

        if n_peptides == 0 or n_peptides is None:
            if 'n_peptides' in tmp_df.columns:
                tmp_df.drop(columns=['n_peptides'], inplace=True)

        if n_proteins == 0 or n_proteins is None:
            if 'n_proteins' in tmp_df.columns:
                tmp_df.drop(columns=['n_proteins'], inplace=True)

        if n_dnas == 0 or n_dnas is None:
            if 'n_dnas' in tmp_df.columns:
                tmp_df.drop(columns=['n_dnas'], inplace=True)

        if n_rnas == 0 or n_rnas is None:
            if 'n_rnas' in tmp_df.columns:
                tmp_df.drop(columns=['n_rnas'], inplace=True)

        if n_lipids == 0 or n_lipids is None:
            if 'n_lipids' in tmp_df.columns:
                tmp_df.drop(columns=['n_lipids'], inplace=True)

        if n_polysaccharides == 0 or n_polysaccharides is None:
            if 'n_polysaccharides' in tmp_df.columns:
                tmp_df.drop(columns=['n_polysaccharides'], inplace=True)

        if n_saccharides == 0 or n_saccharides is None:
            if 'n_saccharides' in tmp_df.columns:
                tmp_df.drop(columns=['n_saccharides'], inplace=True)

    else:
        from molsysmt._private.smonitor import ArgumentChoiceError
        raise ArgumentChoiceError(
            argument="element",
            value=element,
            choices=["atom", "group", "component", "chain", "molecule", "entity", "system"],
            caller="molsysmt.basic.info",
        )

    if output_type == 'styler':
        return tmp_df.style.hide(axis='index')
    elif output_type == 'dataframe':
        return tmp_df
    elif output_type == 'dictionary':
        return tmp_df.to_dict(orient='records')
    else:
        from molsysmt._private.smonitor import ArgumentChoiceError
        raise ArgumentChoiceError(
            argument="output_type",
            value=output_type,
            choices=["styler", "dataframe", "dictionary"],
            caller="molsysmt.basic.info",
        )


