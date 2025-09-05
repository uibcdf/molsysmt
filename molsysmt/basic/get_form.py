from molsysmt._private.exceptions import NotSupportedFormError
from pathlib import PosixPath

# This method must not be digested
def get_form(molecular_system):
    """
    Retrieving the form of a molecular system.

    This function returns a string that identifies the form of the input molecular system,
    such as ``'file:pdb'``, ``'openmm.Topology'``, ``'string:pdb_id'``, or any other
    supported form.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to analyze, in any of the :ref:`supported forms <Introduction_Forms>`.

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
    - See :ref:`Introduction_Forms` for a full list of supported forms.

    See Also
    --------
    :func:`molsysmt.convert`
        Convert a molecular system into a different form.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> molsys_A = systems['T4 lysozyme L99A']['181l.h5msm']
    >>> msm.get_form(molsys_A)
    'file:h5msm'
    >>> molsys_B = msm.convert(molsys_A, to_form='molsysmt.MolSys')
    >>> msm.get_form(molsys_B)
    'molsysmt.MolSys'
    >>> molsys_C = msm.convert(molsys_B, to_form='openmm.Topology')
    >>> msm.get_form(molsys_C)
    'openmm.Topology'

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Get_form`.

    .. versionadded:: 1.0.0
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

