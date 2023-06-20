from molsysmt._private.digestion import digest
import numpy as np

@digest()
def is_composed_of(molecular_system, selection='all', syntax='MolSysMT', **kwargs):
    """
    Checking if a molecular system is composed of specific elements.

    The function returns True or False depending on whether or not the system is entirely composed
    of the elements required.


    Parameters
    ----------

    molecular_system : molecular system
        The molecular system in any of :ref:`the supported forms
        <Introduction_Forms>` to be analysed by the function.

    selection : tuple, list, numpy.ndarray or str, default 'all'
        Selection of elements of the molecular system to be checked by the function. The selection can be
        given by a list, tuple or numpy array of atom indices (0-based
        integers); or by means of a string following any of :ref:`the selection
        syntaxes parsable by MolSysMT <Introduction_Selection>`.

    syntax : str, default 'MolSysMT'
        :ref:`Supported syntax <Introduction_Selection>` used in the `selection` argument (in case
        it is a string).

    **kwargs : {{keyword : str,  value : (bool, int)}, default None}
        The elements to be checked in the molecular system are introduced as
        additional keywords with value either 'True', 'False', or by means of an integer to
        indicate to amount of specific elements the system is composed of.


    Returns
    -------

    bool
        A boolean value is returned reporting if the molecular system is composed of the elements required.


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


    .. versionadded:: 0.5.0

    Notes
    -----

    The list of supported molecular systems' forms is detailed in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.

    The list of supported selection syntaxes can be checked in the documentation section
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`.


    See Also
    --------

    :func:`molsysmt.basic.select`
        Selecting elements of a molecular system.

    :func:`molsysmt.basic.contains`
        Checking if a molecular system contains certain elements or attributes.

    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> molecular_system = msm.systems.demo['T4 lysozyme L99A']['181l.mmtf']
    >>> msm.basic.is_composed_of(molecular_system, waters=True, ions=True)
    False
    >>> msm.basic.is_composed_of(molecular_system, waters=True, ions=True, small_molecules=2,
    >>>                          proteins=1)
    True
    >>> msm.basic.is_composed_of(molecular_system, n_chains=6)
    True


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Is composed of <Tutorial_Is_composed_of>`.


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
