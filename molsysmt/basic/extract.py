from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from smonitor import signal

@signal(tags=['api', 'extract'])
@arg_digest()
def extract(molecular_system, selection='all', structure_indices='all', to_form=None, output_filename=None,
            copy_if_all=True, syntax='MolSysMT', skip_digestion=False):
    """
    Extracting a subset of atoms and/or structures from a molecular system.

    This function creates a new molecular system containing only the elements and structures
    specified by `selection` and `structure_indices`. Composite inputs are materialized as a
    native `molsysmt.MolSys` before extraction so topology and structural data remain aligned.
    Optionally, the result can be returned in another form using `to_form`.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    to_form : str, list of str, or None, default=None
        Target molecular-system form; `None` preserves or infers the input form.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    copy_if_all : bool, default=True
        Whether an unrestricted extraction returns a copy instead of the original object.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molecular system
        A new molecular system containing only the selected atoms and structures, in `to_form`
        if provided. Otherwise, the result uses the singular input form or `molsysmt.MolSys`
        for a composite input.


    Raises
    ------
    NotSupportedFormError
        If the input or requested output form is not supported.
    ArgumentError
        If input arguments are invalid or inconsistent, including an
        out-of-range structure index.


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

    from ._index_validation import validate_structure_indices

    structure_indices = validate_structure_indices(
        molecular_system, structure_indices, 'molsysmt.extract'
    )

    forms_in = get_form(molecular_system)

    if isinstance(forms_in, (list, tuple)):
        native_system = convert(
            molecular_system,
            to_form='molsysmt.MolSys',
            skip_digestion=True,
        )
        return extract(
            native_system,
            selection=selection,
            structure_indices=structure_indices,
            to_form=to_form,
            copy_if_all=copy_if_all,
            syntax=syntax,
            skip_digestion=True,
        )

    if to_form is not None:

        return convert(molecular_system, to_form=to_form, selection=selection, structure_indices=structure_indices,
                       syntax=syntax, skip_digestion=True)

    if not is_all(selection):
        atom_indices = select(molecular_system, selection=selection, syntax=syntax, skip_digestion=True)
    else:
        atom_indices = 'all'

    if not isinstance(forms_in, (list, tuple)):
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
