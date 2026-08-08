from molsysmt._private.smonitor import NotSupportedFormError
from molsysmt._private.form_tier import check_form_tier
import depdigest
from pathlib import PosixPath


#: Resolved once. `get_form` asks `_is_detector_available` for every form module on every
#: call, so the `import` statements that used to sit inside it ran ~73 times per call.
_dependency_tables = None


def _is_detector_available(module):
    """Return whether a form detector can run in the current environment."""

    global _dependency_tables

    if _dependency_tables is None:
        from molsysmt._depdigest import LIBRARIES, MAPPING
        _dependency_tables = (LIBRARIES, MAPPING)
    LIBRARIES, MAPPING = _dependency_tables

    # Reached through the module rather than bound at import time, so that a test which
    # simulates an absent soft dependency by patching `depdigest.is_installed` is obeyed.
    is_installed = depdigest.is_installed

    plugin_name = module.__name__.rsplit('.', maxsplit=1)[-1]
    library = MAPPING.get(plugin_name)
    if library is None:
        return True

    library_info = LIBRARIES.get(library, {})
    if library_info.get('type') != 'soft':
        return True

    return is_installed(library)



def _asks(form, molecular_system):
    """Put the question to the one form that claims this shape, if it can answer."""

    from molsysmt.form import catalogue

    module = catalogue.module_of(form)
    if module is None or not _is_detector_available(module):
        return False
    return bool(module.is_form(molecular_system))


def _sweep(molecular_system, *form_types):
    """Ask the detectors of the given categories, in catalogue order."""

    from molsysmt.form import catalogue

    for form in catalogue.forms_of_type(*form_types):
        if _asks(form, molecular_system):
            return form
    return None


def _detect(molecular_system):
    """The form of an item, or None.

    The catalogue knows which class each form holds and which extension each file form
    uses, and it knows it *without importing anything* -- the comparison is between the
    strings a class carries and the strings a form declared. So the common cases are a
    dictionary lookup followed by importing the single plugin that will answer, instead of
    importing all 89 to ask each in turn.

    A candidate is still confirmed by the form's own `is_form`. The index says which
    detector is worth asking; the detector decides.
    """

    candidate = catalogue_form_of_class(molecular_system)
    if candidate is not None and _asks(candidate, molecular_system):
        return candidate

    if isinstance(molecular_system, str):
        from molsysmt.form import catalogue

        candidate = catalogue.form_of_extension(molecular_system)
        if candidate is not None and _asks(candidate, molecular_system):
            return candidate
        # A string is a file path or content. It is never an instance of a class form.
        return _sweep(molecular_system, 'string', 'file')

    # Anything else can only be an instance: a file form is named by a path and a string
    # form carries its content in a string, and both were handled above.
    return _sweep(molecular_system, 'class')


def catalogue_form_of_class(molecular_system):
    from molsysmt.form import catalogue

    return catalogue.form_of_class(molecular_system)


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

    if isinstance(molecular_system, (list, tuple)):
        output = [get_form(ii) for ii in molecular_system]
        return output

    if isinstance(molecular_system, PosixPath):
        molecular_system = molecular_system.absolute().__str__()

    output = _detect(molecular_system)

    if output is None:
        raise NotSupportedFormError(
            form=type(molecular_system),
            caller='molsysmt.basic.get_form'
        )

    check_form_tier(output)

    return output
