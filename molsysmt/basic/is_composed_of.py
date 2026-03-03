from molsysmt._private.arg_digestion import arg_digest
import numpy as np
from smonitor import signal


@signal(tags=['api', 'get'])
@arg_digest()
def is_composed_of(molecular_system, selection='all', syntax='MolSysMT', skip_digestion=False, **kwargs):
    """
    Checking whether a molecular system is composed exclusively of specific elements.

    This function returns `True` if the selected portion of the molecular system is entirely
    composed of the requested element types and counts provided via keyword conditions in
    `**kwargs`; otherwise it returns `False`.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to analyze, provided in any of the
        :ref:`supported forms <Introduction_Forms>`.
    selection : int, tuple, list, numpy.ndarray or str, default 'all'
        Subset of the molecular system to check. It can be a 0-based index collection or
        a selection string following :ref:`Introduction_Selection`. If 'all', the entire
        molecular system is considered.
    syntax : str, default 'MolSysMT'
        Selection syntax used when `selection` is a string. See :ref:`Introduction_Selection`.
    skip_digestion : bool, default False
        Whether to skip MolSysMT’s internal argument digestion mechanism.

        MolSysMT includes a built-in digestion system that validates and normalizes
        function arguments. This process checks types, shapes, and values, and automatically
        adjusts them when possible to meet expected formats.

        Setting `skip_digestion=True` disables this process, which may improve performance
        in workflows where inputs are already validated. Use with caution: only set this to
        `True` if you are certain all input arguments are correct and consistent.
    **kwargs
        Composition conditions as ``name=value`` pairs. Accepted names include type
        counters (`n_ions`, `n_waters`, `n_small_molecules`, `n_peptides`, `n_proteins`,
        `n_dnas`, `n_rnas`, `n_lipids`, `n_polysaccharides`, `n_saccharides`, ...) and element
        counters (`n_atoms`, `n_groups`, `n_components`, `n_molecules`, `n_chains`, `n_entities`, ...).
        Values are interpreted as:
        - `True`  → the count must be **> 0** (presence required)
        - `False` → the count must be **== 0** (absence required)
        - `int`   → the count must be **exactly** that integer

    Returns
    -------
    bool
        `True` if all provided conditions are satisfied by the selection; `False` otherwise.

    Raises
    ------
    NotSupportedFormError
        If the molecular system has an unsupported form.
    ArgumentError
        If any argument is invalid or inconsistent.

    Notes
    -----
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.

    See Also
    --------
    :func:`molsysmt.basic.select`
        Select specific elements from a molecular system.
    :func:`molsysmt.basic.contains`
        Check whether certain elements or attributes are present in a molecular system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> molsys = systems['T4 lysozyme L99A']['181l.h5msm']
    >>> msm.basic.is_composed_of(molsys, waters=True, ions=True)
    False
    >>> msm.basic.is_composed_of(molsys, waters=True, ions=True, small_molecules=2, proteins=1)
    True
    >>> msm.basic.is_composed_of(molsys, n_chains=6)
    True

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Is_composed_of`.

    .. versionadded:: 1.0.0
    """

    from . import get

    if len(kwargs):

        # molecules in kwargs
        set_molecules = {'n_ions', 'n_waters', 'n_small_molecules', 'n_peptides', 'n_proteins',
                'n_dnas', 'n_rnas', 'n_lipids', 'n_polysaccharides', 'n_saccharides'}

        if set_molecules & set(kwargs.keys()):

            aux_dictionary = get(molecular_system, element="atom", selection=selection, syntax=syntax,
                    output_type='dictionary',
                    n_ions=True, n_waters=True, n_small_molecules=True, n_peptides=True, n_proteins=True,
                    n_dnas=True, n_rnas=True, n_lipids=True, n_polysaccharides=True, n_saccharides=True)

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
