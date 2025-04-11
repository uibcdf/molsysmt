from molsysmt._private.exceptions import NotSupportedFormError
from pathlib import PosixPath

# This method must not be digested
def get_form(molecular_system):
    """
    Return the form of a molecular system.

    This function returns a string identifying the form of the input molecular system,
    such as `'file:pdb'`, `'openmm.Topology'`, `'string:pdb_id'`, or any other
    supported form.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to be analyzed, in any of the :ref:`supported forms <Introduction_Forms>`.

    Returns
    -------
    str
        Name of the form of the input molecular system.

    Raises
    ------
    NotSupportedFormError
        If the input molecular system has a form that is not supported.

    Notes
    -----
    See :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>` for a full list of supported forms.

    See Also
    --------
    :func:`molsysmt.convert`
        Convert a molecular system into a different form.

    :func:`molsysmt.get_attributes`
        Get the set of available attributes in a molecular system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys_A = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'])
    >>> msm.get_form(molsys)
    'file:h5msm'
    >>> molsys_B = msm.convert(molsys_A, to_form='openmm.Topology')
    >>> msm.get_form(molsys_B)
    'openmm.Topology'

    .. admonition:: User guide

       For a tutorial on using this function, see:
       :ref:`User Guide > Tools > Basic > Get form <Tutorial_Get_form>`

    .. versionadded:: 0.1.0
    """

    # This method can check if molecular system is indeed a molecular system
    # This method is used to check that a molecular system is a molecular system

    from molsysmt.form import _dict_modules

    if isinstance(molecular_system, (list, tuple)):
        output = [get_form(ii) for ii in molecular_system]
        return output

    if isinstance(molecular_system, PosixPath):
        molecular_system = molecular_system.absolute().__str__()

    output = None

    for form, module in _dict_modules.items():
        if module.is_form(molecular_system):
            output = form
            break

    if output is None:
        raise NotSupportedFormError(type(molecular_system))

    return output

