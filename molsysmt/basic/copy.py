from molsysmt._private.argdigest import arg_digest
from smonitor import signal

@signal(tags=['api', 'copy'])
@arg_digest()
def copy(molecular_system, output_filename=None, skip_digestion=False):
    """
    Creating an independent copy of a molecular system.

    This function returns a deep copy of the input molecular system, fully detached from
    the original. If the input is in a file-based form and `output_filename` is provided,
    the copy is written to a new file using the corresponding form handler.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
     molecular system or list of molecular systems
        A new molecular system (or list of systems if the input is a sequence), independent
        of the original and in the same form as the input.
        When `output_filename` is given for a file-based form, the returned object follows
        the form-specific handler’s semantics (typically the path or a file-form handle).


    Raises
    ------
    NotSupportedFormError
        If the input molecular system has an unsupported form.
    ArgumentError
        If input arguments are invalid or inconsistent.


    Notes
    -----
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.


    See Also
    --------
    :func:`molsysmt.basic.convert`
        Convert a molecular system into another form.


    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys_A = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'])
    >>> molsys_B = msm.copy(molsys_A)
    >>> msm.compare(molsys_A, molsys_B, rule='equal')
    True
    >>> id(molsys_A) == id(molsys_B)
    False


    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Copy`.

    .. versionadded:: 1.0.0
    """

    from . import get_form
    from molsysmt.form import is_file, _dict_modules

    form_in = get_form(molecular_system)

    if output_filename is None:

        if not isinstance(form_in, (list, tuple)):
            form_in = [form_in]
            molecular_system = [molecular_system]

        output = []

        for item_form, item in zip(form_in, molecular_system):
            output_item = _dict_modules[item_form].copy(item)
            output.append(output_item)

        if len(output)==1:
            output=output[0]

    else:

        output = _dict_modules[form_in].copy(molecular_system, output_filename=output_filename)

    return output

