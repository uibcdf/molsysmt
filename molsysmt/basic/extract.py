from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest()
def extract(molecular_system, selection='all', structure_indices='all', to_form=None, syntax='MolSysMT',
            copy_if_all=True):

    """
    Extract a portion of a molecular model.

    The function extracts a subsystem from a molecular system according to the
    required selection of elements and structures given by the input arguments
    ``selection`` and ``structure_indices``.


    Parameters
    ----------

    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms
        <Introduction_Forms>` to be duplicated by the function.

    selection : tuple, list, numpy.ndarray or str, default 'all'
        Selection of elements of the molecular system to be extracted by the function. The selection can be
        given by a list, tuple or numpy array of atom indices (0-based
        integers); or by means of a string following any of :ref:`the selection
        syntaxes parsable by MolSysMT <Introduction_Selection>`.

    structure_indices : tuple, list, numpy.ndarray or 'all', default 'all'
        Indices of structures (0-based integers) to be extracted from the molecular system.

    to_form: str, default=None
        The form of the resultant molecular system (see :ref:`the supported
        conversions <Introduction_Supported>`). If default value None is
        kept, the output system has the same form as the input.

    syntax : str, default 'MolSysMT'
        :ref:`Supported syntax <Introduction_Selection>` used in the `selection` argument (in case
        it is a string).

    copy_if_all : bool, default True
        If ``selection`` and ``structure_indices`` are 'all', the output can be
        an independent copy of the input, with ``copy_if_all=True`` (default), or just a view.


    Returns
    -------
    Molecular system
        Molecular system extracted from the molecular system introduced as input argument.


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

    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> from molsysmt.systems import demo
    >>> molecular_system_1 = msm.basic.convert(demo['T4 lysozyme L99A']['181l.mmtf'])
    >>> molecular_system_2 = msm.basic.extract(molecular_system_1, selection='molecule_type=="protein"')
    >>> msm.basic.contains(molecular_system_1, waters=True)
    True
    >>> msm.basic.contains(molecular_system_2, waters=True)
    False


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Extract <Tutorial_Extract>`.

    """

    from . import get_form, select, convert
    from molsysmt.form import _dict_modules

    if to_form is not None:

        return convert(molecular_system, to_form=to_form, selection=selection, structure_indices=structure_indices,
                       syntax=syntax)

    forms_in = get_form(molecular_system)

    if not is_all(selection):
        atom_indices = select(molecular_system, selection=selection, syntax=syntax)
    else:
        atom_indices = 'all'

    if not isinstance(get_form, (list, tuple)):
        forms_in = [forms_in]
        molecular_system = [molecular_system]

    output = []

    for form_in, item in zip(forms_in, molecular_system):
        output_item = _dict_modules[form_in].extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all)
        output.append(output_item)

    if len(output)==1:
        output=output[0]

    return output

