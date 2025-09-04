from molsysmt._private.digestion import digest
import numpy as np

def _evaluation(condition, value):

    output = True

    if condition is not None:
        if isinstance(condition, bool):
            if condition==True:
                if value is None:
                    output = False
                elif isinstance(value, (int, np.int64)):
                    if value==0:
                        output = False
            else:
                if isinstance(value, (int, np.int64)):
                    if value>0:
                        output = False
                elif isinstance(value, (np.ndarray, list, tuple)):
                        output = False
        elif isinstance(condition, int):
            if isinstance(value, int):
                if condition>value:
                    output = False

    return output

@digest()
def contains(molecular_system, selection='all', syntax='MolSysMT', **kwargs):
    """Check whether a molecular system satisfies given conditions.

    This routine queries attributes from a molecular system and evaluates them
    against user‑provided conditions. The evaluation can be restricted to a
    subset of atoms through ``selection``. If no conditions are supplied, the
    function simply checks whether the selection contains at least one atom.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to analyse, in any of the :ref:`supported forms
        <Introduction_Forms>`.
    selection : str, list, tuple or numpy.ndarray, default='all'
        Atoms defining the portion of the system to evaluate. It may be given as
        a list/array of 0-based atom indices or as a string following one of the
        :ref:`supported selection syntaxes <Introduction_Selection>`.
    syntax : str, default='MolSysMT'
        Selection syntax used when ``selection`` is a string.
    **kwargs : dict
        Attribute–value pairs defining the conditions to test. Each key must be
        an attribute name accepted by :func:`molsysmt.basic.get`. The associated
        value can be:

        * ``True`` – the attribute must be present or greater than zero.
        * ``False`` – the attribute must be absent or zero.
        * ``int`` – the attribute must equal this integer.

    Returns
    -------
    bool
        ``True`` if all requested conditions are met; otherwise ``False``.

    Raises
    ------
    NotSupportedFormError
        If ``molecular_system`` is provided in an unsupported form.
    ArgumentError
        If argument values are inconsistent.

    Notes
    -----
    - See :ref:`Introduction_Forms` for valid molecular-system formats.
    - Selection strings must follow one of the syntaxes in
      :ref:`Introduction_Selection`.

    See Also
    --------
    :func:`molsysmt.basic.get`
        Obtain attributes of a molecular system.
    :func:`molsysmt.basic.select`
        Select elements from a molecular system.
    :func:`molsysmt.basic.is_composed_of`
        Check whether a system is composed of specific molecule types.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems.demo['T4 lysozyme L99A']['181l.mmtf']
    >>> msm.contains(molsys, waters=True, ions=True)
    True
    >>> msm.contains(molsys, selection='atom_name=="Cl"')
    True
    >>> msm.contains(molsys, selection='molecule_type!="water"', waters=True)
    False

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use
       this function, along with additional examples:
       :ref:`Tutorial_Contains`.

    .. versionadded:: 1.0.0
    """

    from . import get

    atts_required = {}
    aux_atts = {}
    for key in kwargs.keys():
        atts_required[key] = kwargs[key]
        aux_atts[key] = True

    n_atts_required = len(atts_required)

    if n_atts_required:

        atts_values = get(molecular_system, selection=selection, syntax=syntax, **aux_atts)

        if n_atts_required==1:
            atts_values = [atts_values]

        for att, att_value in zip(aux_atts.keys(), atts_values):
            if not _evaluation(atts_required[att], att_value):
                return False

    else:

        n_atoms = get(molecular_system, element='atom', selection=selection, syntax=syntax, n_atoms=True)

        if not n_atoms:
            return False

    return True

