from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import inspect

@digest()
def merge(molecular_systems,
          selections='all',
          structure_indices='all',
          syntax='MolSysMT',
          to_form=None,
          skip_digestion=False
          ):

    """
    Merging the elements of different molecular systems.

    Elements coming from a list of molecular systems are merged into a new molecular system.
    Every molecular system must have the same number of structures.
    Otherwise, the input argument `structure_indices` needs to be used to
    specify the indices to extract the structural attributes of the elements to
    be added.


    Parameters
    ----------
    molecular_systems : molecular systems
        List of  molecular systems in any of :ref:`the supported forms <Introduction_Forms>`.
        Elements from these systems will be merged into a new system by this function.

    selections : list of (tuple, list, numpy.ndarrays, str), or 'all', default 'all'
        Selections of atoms to which this function applies. The default value is 'all' to indicate
        that all elements in all systems will be merged. If different sets of elements need
        to be specified to be merge from the list of systems, a list of selections given
        by lists, tuples, numpy arrays of atom indices (0-based
        integers), or strings following any of :ref:`the selection
        syntaxes parsable by MolSysMT <Introduction_Selection>` must be provided. This former list
        will be applied to the list of molecular systems in the same order.

    structure_indices : list of (tuple, list, numpy.ndarray, 'all'), or 'all', default 'all'
        List of indices of structures (0-based integers) to which this function applies. The
        default value is 'all' to indicate that all structures in all systems will be merged.
        If a list of different indices of structures is introduced, they
        will be read and applied to the list of molecular systems in the same order.

    syntax : str, default 'MolSysMT'
        :ref:`Supported syntax <Introduction_Selection>` used in the argument
        `selections` (in case they contain strings).

    to_form: str or None, default None
        Form of the output molecular system. If no form is indicated, with the default value None, the
        output form will be the same as the first molecular system found in ``molecular_systems``.


    Returns
    -------
    molecular system
        A molecular system composed of elements extracted from the input molecular
        systems. The form of this output system can be chosen making use
        of the `to_form` input argument.


    Raises
    ------

    NotSupportedFormError
        The function raises a NotSupportedFormError in case a molecular system
        is introduced with a not supported form.

    ArgumentError
        The function raises an ArgumentError in case an input argument value
        does not meet the required conditions.

    SyntaxError
        The function raises a SyntaxError in case the syntax argument takes a not supported value.


    .. versionadded:: 0.1.0

    Notes
    -----

    The list of supported molecular systems' forms is detailed in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.

    The list of supported selection syntaxes can be checked in the documentation section
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`.


    See Also
    --------

    :func:`molsysmt.basic.select`
        Selecting elements of a molecular system

    :func:`molsysmt.basic.add`
        Adding elements of a molecular system into another molecular system.

    :func:`molsysmt.basic.append_structures`
        Adding structures from a molecular system to another molecular system.

    :func:`molsysmt.basic.concatenate_structures`
        Concatenating the structures found in a list of molecular systems.


    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> molecular_system = msm.systems.demo['alanine dipeptide']['alanine_dipeptide.msmpk']
    >>> molecular_system_1 = msm.convert(molecular_system)
    >>> molecular_system_2 = msm.structure.translate(molecular_system_1, translation='[0.1, 0.1, 0.1] nanometers')
    >>> molecular_system_3 = msm.basic.merge([molecular_system_1, molecular_system_2])
    >>> msm.basic.get(molecular_system_3, n_peptides=True)
    2


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Merge <Tutorial_Merge>`.


    """

    from . import convert, get_form, select
    from molsysmt.form import _dict_modules

    n_molecular_systems = len(molecular_systems)

    if not isinstance(selections, (list, tuple)):
        selections = [selections for ii in range(n_molecular_systems)]
    elif len(selections)!=n_molecular_systems:
        raise ValueError("The length of the lists items and selections need to be equal.")

    if not isinstance(structure_indices, (list, tuple)):
        structure_indices = [structure_indices for ii in range(n_molecular_systems)]
    elif len(structure_indices)!=n_molecular_systems:
        raise ValueError("The length of the lists items and structure_indices need to be equal.")

    aux_molecular_systems = []
    aux_atom_indices = []
    aux_structure_indices = []
    to_form = get_form(molecular_systems[0])
    for tmp_molecular_system, tmp_selection, tmp_structure_indices in zip(molecular_systems,
            selections, structure_indices):
        tmp_form = get_form(tmp_molecular_system)
        if tmp_form == to_form:
            aux_molecular_systems.append(tmp_molecular_system)
            if is_all(tmp_selection):
                aux_atom_indices.append(tmp_selection)
            else:
                aux_atom_indices.append(selection(tmp_molecular_system, selection=selection, syntax=syntax, skip_digestion=True))
            aux_structure_indices.append(tmp_structure_indices)
        else:
            aux = convert(tmp_molecular_system, to_form=to_form, selection=tmp_selection,
                    structure_indices=tmp_structure_indices, skip_digestion=True)
            aux_molecular_systems.append(aux)
            aux_atom_indices.append('all')
            aux_structure_indices.append('all')

    merge_arguments = {}
    merge_function = _dict_modules[to_form].merge
    input_arguments = set(inspect.signature(merge_function).parameters)

    if 'atom_indices' in input_arguments:
        merge_arguments['atom_indices']=aux_atom_indices

    if 'structure_indices' in input_arguments:
        merge_arguments['structure_indices']=aux_structure_indices

    merge_arguments['skip_digestion']=True

    output = merge_function(aux_molecular_systems, **merge_arguments)

    return output

