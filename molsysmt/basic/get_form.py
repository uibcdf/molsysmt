from molsysmt._private.exceptions import NotSupportedFormError
from pathlib import PosixPath

# This method must not be digested
def get_form(molecular_system):
    """
    Getting the form of a molecular system.

    The function returns the name of the form of the molecular system introduced as input argument.

    Parameters
    ----------

    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms
        <Introduction_Forms>` to be analysed by the function.


    Returns
    -------
    str
        Name of the form of the input molecular system.


    Raises
    ------

    NotSupportedFormError
        The function raises a NotSupportedFormError in case a molecular system
        is introduced with a not supported form.


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
    >>> molecular_system = msm.basic.convert(demo['T4 lysozyme L99A']['181l.mmtf'])
    >>> msm.basic.get_form(molecular_system)
    'file:mmtf'
    >>> molecular_system_2 = msm.basic.convert(molecular_system, to_form='openmm.Topology')
    >>> msm.basic.get_form(molecular_system_2)
    'openmm.Topology'


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Get form <Tutorial_Get_form>`.


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

