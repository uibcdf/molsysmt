from molsysmt._private.arg_digestion import arg_digest
from smonitor import signal
from molsysmt._private.chemical_state import resolve_chemical_state

@signal(tags=['api', 'get'])
@arg_digest()
@resolve_chemical_state
def has_attribute(molecular_system, attribute, include_none=False,
                  structure_indices='all', chemical_state='reference',
                  skip_digestion=False):
    """
    Checking whether a molecular system has a specific attribute.

    This function returns `True` if the given attribute is available for the input molecular
    system, and `False` otherwise. Availability depends on the form-specific backend and the global attribute registry.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to analyze, in any of the :ref:`supported forms <Introduction_Forms>`.
    attribute : str
        Name of the attribute to check.
    include_none : bool, default False
        Whether to consider attributes currently holding `None` as **available**.
        If `True`, an attribute that exists but is `None` will return `True`.
    structure_indices : int, tuple, list, numpy.ndarray or 'all', default 'all'
        Structures used when ``chemical_state='structure'`` resolves
        state-dependent availability.
    chemical_state : {'reference', 'structure'} or int, default 'reference'
        Chemical state used to resolve state-dependent attribute availability.
        ``'structure'`` uses the unique state associated with `structure_indices`.
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
    bool
        `True` if the attribute is available in the molecular system, `False` otherwise.

    Raises
    ------
    NotSupportedFormError
        If the molecular system has a form that is not supported.
    ArgumentError
        If input arguments are invalid or inconsistent.

    Notes
    -----
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.
    - For native multi-state systems, ``chemical_state`` resolves availability
      without changing the topology's reference state.
    - Explicit integer state selection currently requires a native Topology or
      MolSys.

    See Also
    --------
    :func:`molsysmt.basic.get_attributes`
        Retrieve the list of available attributes in a molecular system.
    :func:`molsysmt.basic.get`
        Retrieve values of specific attributes from a molecular system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> molsys = msm.convert(systems['T4 lysozyme L99A']['181l.h5msm'])
    >>> msm.has_attribute(molsys, 'box')
    True
    >>> msm.has_attribute(molsys, 'forcefield')
    False

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Has_attribute`.

    .. versionadded:: 1.0.0
    """

    from molsysmt import get_form
    from molsysmt.form import _dict_modules

    forms_in = get_form(molecular_system)

    if not isinstance(forms_in, (list, tuple)):
        forms_in = [forms_in]
        molecular_system = [molecular_system]

    output = False

    for form_in, item in zip(forms_in, molecular_system):
        if _dict_modules[form_in].has_attribute(item, attribute, include_none=include_none):
            output=True
            break

    return output
