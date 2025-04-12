from molsysmt._private.digestion import digest
import numpy as np

@digest()
def is_composed_of(molecular_system, selection='all', syntax='MolSysMT', skip_digestion=False, **kwargs):
    """
    Check whether a molecular system is composed exclusively of specific elements.

    This function returns `True` if the selected portion of the molecular system is entirely
    composed of the specified types of elements. Otherwise, it returns `False`.

    Parameters
    ----------
    molecular_system : molecular system
        The molecular system to be analyzed, provided in any of the
        :ref:`supported forms <Introduction_Forms>`.

    selection : tuple, list, numpy.ndarray or str, default 'all'
        Selection of elements (typically atoms) to check. This can be a list, tuple, or array of
        0-based indices, or a selection string using one of the
        :ref:`supported syntaxes <Introduction_Selection>`.

    syntax : str, default 'MolSysMT'
        The syntax used to interpret the `selection` string (if applicable). See:
        :ref:`Introduction_Selection`.

    **kwargs : dict of {str: bool or int}
        A set of keyword arguments defining the expected composition. Values can be:
        - `True`: require presence of that element type
        - `False`: require absence
        - integer: require an exact number

    Returns
    -------
    bool
        `True` if the selection is composed only of the specified element types and counts.
        Otherwise, `False`.

    Raises
    ------
    NotSupportedFormError
        If the molecular system has an unsupported form.

    ArgumentError
        If any argument is invalid or inconsistent.

    Notes
    -----
    For an element to be considered part of the composition, it must fully match the specified
    criteria within the given selection. To apply looser checks, use
    :func:`molsysmt.basic.contains`.

    For more information, see:
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`  
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`

    See Also
    --------
    :func:`molsysmt.basic.select`
        Select specific elements from a molecular system.

    :func:`molsysmt.basic.contains`
        Check whether certain elements or attributes are present in a molecular system.

    Examples
    --------
    The following examples illustrate the use of the function:

    >>> import molsysmt as msm
    >>> molsys = msm.systems['T4 lysozyme L99A']['181l.mmtf']
    >>> msm.basic.is_composed_of(molsys, waters=True, ions=True)
    False
    >>> msm.basic.is_composed_of(molsys, waters=True, ions=True, small_molecules=2, proteins=1)
    True
    >>> msm.basic.is_composed_of(molsys, n_chains=6)
    True

    .. admonition:: User guide

       For a tutorial on how to use this function, see:
       :ref:`User Guide > Tools > Basic > Is composed of <Tutorial_Is_composed_of>`

    .. versionadded:: 1.0.0
    """

    from . import get

    if len(kwargs):

        # molecules in kwargs
        set_molecules = {'n_ions', 'n_waters', 'n_small_molecules', 'n_peptides', 'n_proteins',
                'n_dnas', 'n_rnas', 'n_lipids', 'n_oligosaccharides', 'n_saccharides'}

        if set_molecules & set(kwargs.keys()):

            aux_dictionary = get(molecular_system, element="atom", selection=selection, syntax=syntax,
                    output_type='dictionary',
                    n_ions=True, n_waters=True, n_small_molecules=True, n_peptides=True, n_proteins=True,
                    n_dnas=True, n_rnas=True, n_lipids=True, n_oligosaccharides=True, n_saccharides=True)

            for key, value in aux_dictionary.items():
                if value:
                    if key in kwargs:
                        if isinstance(kwargs[key], bool):
                            if not kwargs[key]:
                                return False
                        elif isinstance(kwargs[key], (int, np.int64)):
                            if not kwargs[key]==value:
                                return False
                    else:
                        return False

        # n_elements in kwargs

        set_n_elements = {'n_atoms', 'n_groups', 'n_components', 'n_molecules', 'n_chains',
                          'n_entities'}

        if set_n_elements & set(kwargs.keys()):

            aux_dictionary = get(molecular_system, element="atom", selection=selection, syntax=syntax,
                    output_type='dictionary',
                    n_atoms=True, n_groups=True, n_components=True, n_molecules=True, n_chains=True,
                    n_entities=True)

            for key, value in kwargs.items():
                if key in set_n_elements:
                    if isinstance(value, bool):
                        if value:
                            if aux_dictionary[key]==0:
                                return False
                        else:
                            if aux_dictionary[key]>0:
                                return False
                    elif isinstance(value, (int, np.int64)):
                        if value!=aux_dictionary[key]:
                            return False

    else:

        n_atoms_selection = get(molecular_system, element='atom', selection=selection,
                syntax=syntax, n_atoms=True)

        n_atoms = get(molecular_system, element='atom', selection=selection,
                syntax=syntax, n_atoms=True)

        if n_atoms!=n_atoms_selection:
            return False

    return True
