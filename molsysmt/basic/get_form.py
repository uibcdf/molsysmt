from molsysmt._private.smonitor import NotSupportedFormError
from molsysmt._private.form_tier import check_form_tier
from pathlib import PosixPath


def _is_detector_available(module):
    """Return whether a form detector can run in the current environment."""

    from depdigest import is_installed
    from molsysmt._depdigest import LIBRARIES, MAPPING

    plugin_name = module.__name__.rsplit('.', maxsplit=1)[-1]
    library = MAPPING.get(plugin_name)
    if library is None:
        return True

    library_info = LIBRARIES.get(library, {})
    if library_info.get('type') != 'soft':
        return True

    return is_installed(library)


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
        if not _is_detector_available(module):
            continue
        if module.is_form(molecular_system):
            output = form
            break

    if output is None:
        raise NotSupportedFormError(
            form=type(molecular_system),
            caller='molsysmt.basic.get_form'
        )

    check_form_tier(output)

    return output
