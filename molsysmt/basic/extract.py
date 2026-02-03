from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest()
def extract(molecular_system, selection='all', structure_indices='all', to_form=None, output_filename=None,
            copy_if_all=True, syntax='MolSysMT', skip_digestion=False):
    """
    Extracting a subset of atoms and/or structures from a molecular system.

    This function creates a new molecular system containing only the elements and structures
    specified by `selection` and `structure_indices`. Optionally, the result can be returned
    in another form using `to_form`.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to extract from, in any of the :ref:`supported forms <Introduction_Forms>`.
    selection : str, tuple, list or numpy.ndarray, default 'all'
        Subset of atoms to extract. Either a 0-based index collection or a selection string
        parsed according to :ref:`Introduction_Selection`. The default 'all' selects all atoms.
    structure_indices : int, tuple, list, numpy.ndarray or 'all', default 'all'
        0-based indices of the structures to extract. The default 'all' includes all structures.
    to_form : str or None, default None
        Target form of the output system. If `None`, the output form matches the input system.
        See :ref:`Supported conversions <Introduction_Supported>`.
    output_filename : str or None, optional
        Optional output target used by certain form handlers. When applicable, the underlying
        conversion/extraction backend may write to this location.
    copy_if_all : bool, default True
        If both `selection` and `structure_indices` equal `'all'`:
        * `True`: return an independent copy of the system.
        * `False`: return a view/reference to the original data, if the backend supports it.
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

    Returns
    -------
    molecular system
        A new molecular system containing only the selected atoms and structures, in `to_form` if provided, otherwise in
        the input form.

    Raises
    ------
    NotSupportedFormError
        If the input or requested output form is not supported.
    ArgumentError
        If input arguments are invalid or inconsistent.

    Notes
    -----
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.

    See Also
    --------
    :func:`molsysmt.basic.select`
        Select elements from a molecular system without extracting them.
    :func:`molsysmt.basic.copy`
        Create an independent copy of a molecular system.
    :func:`molsysmt.basic.convert`
        Convert a molecular system into a different form.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> molsys_A = msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'])
    >>> molsys_B = msm.extract(molsys_A, selection='molecule_type=="protein"')
    >>> msm.contains(molsys_A, waters=True)
    True
    >>> msm.contains(molsys_B, waters=True)
    False

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Extract`.

    .. versionadded:: 1.0.0
    """

    from . import get_form, select, convert
    from molsysmt.form import _dict_modules

    if output_filename is not None:
        to_form=output_filename

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

