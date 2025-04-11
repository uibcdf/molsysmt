from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest()
def extract(molecular_system, selection='all', structure_indices='all', to_form=None, copy_if_all=True,
            syntax='MolSysMT', skip_digestion=False):
    """
    Extract a subset of atoms and/or structures from a molecular system.

    This function creates a new molecular system containing only the elements and structures
    specified by the `selection` and `structure_indices` arguments. Optionally, the result can be
    returned in a different form using `to_form`.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to extract from, in any of the :ref:`supported forms <Introduction_Forms>`.

    selection : str, tuple, list, or numpy.ndarray, default 'all'
        Subset of atoms to extract. Can be given as:
        - A list, tuple, or array of 0-based atom indices.
        - A string using a supported selection syntax.
        The default 'all' selects all atoms.

    structure_indices : int, tuple, list, or numpy.ndarray, default 'all'
        Indices of structures (0-based) to extract. The default 'all' includes all structures.

    to_form : str or None, default None
        Form of the output system. If None, the form is the same as the input system.
        See :ref:`Supported conversions <Introduction_Supported>`.

    copy_if_all : bool, default True
        If both `selection` and `structure_indices` are set to 'all':
        - `True`: return an independent copy of the system.
        - `False`: return a view or reference to the original data, if supported.

    syntax : str, default 'MolSysMT'
        Selection syntax used to interpret the `selection` string.
        See :ref:`Introduction_Selection` for supported options.

    skip_digestion : bool, default False
        If True, skip input validation and digestion. For advanced use only.

    Returns
    -------
    molecular_system : molecular system
        A new molecular system containing only the selected atoms and structures.

    Raises
    ------
    NotSupportedFormError
        If the input or output form is not supported.

    ArgumentError
        If input arguments are invalid or inconsistent.

    Notes
    -----
    For supported molecular system forms, see:
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.

    See Also
    --------
    :func:`molsysmt.basic.select`
        Select elements from a molecular system without extracting them.

    :func:`molsysmt.basic.copy`
        Create a full independent copy of a molecular system.

    :func:`molsysmt.basic.convert`
        Convert a molecular system into a different form.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.systems import demo
    >>> molsys_A = msm.convert(demo['T4 lysozyme L99A']['181l.mmtf'])
    >>> molsys_B = msm.extract(molsys_A, selection='molecule_type=="protein"')
    >>> msm.contains(molsys_A, waters=True)
    True
    >>> msm.contains(molsys_B, waters=True)
    False

    .. admonition:: User guide

       For a tutorial on using this function, see:
       :ref:`User Guide > Tools > Basic > Extract <Tutorial_Extract>`

    .. versionadded:: 1.0.0
    """

    from . import get_form, select, convert
    from molsysmt.form import _dict_modules

    if to_form is not None:

        return convert(molecular_system, to_form=to_form, selection=selection, structure_indices=structure_indices,
                       syntax=syntax, skip_digestion=True)

    forms_in = get_form(molecular_system)

    if not is_all(selection):
        atom_indices = select(molecular_system, selection=selection, syntax=syntax, skip_digestion=True)
    else:
        atom_indices = 'all'

    if not isinstance(get_form, (list, tuple)):
        forms_in = [forms_in]
        molecular_system = [molecular_system]

    output = []

    for form_in, item in zip(forms_in, molecular_system):
        output_item = _dict_modules[form_in].extract(item, atom_indices=atom_indices,
                                                     structure_indices=structure_indices, copy_if_all=copy_if_all,
                                                     skip_digestion=True)
        output.append(output_item)

    if len(output)==1:
        output=output[0]

    return output

