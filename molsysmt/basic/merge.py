from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import inspect

@digest()
def merge(molecular_systems,
          selections='all',
          structure_indices='all',
          keep_ids = True,
          syntax='MolSysMT',
          to_form=None,
          skip_digestion=False
          ):
    """
    Merge elements from multiple molecular systems into a new one.

    This function creates a new molecular system by merging selected elements from a list of input
    molecular systems. All systems must contain the same number of structures. If this is not the
    case, the `structure_indices` argument must be used to align the structures selected for merging.

    Parameters
    ----------
    molecular_systems : list of molecular systems
        A list of molecular systems in any of the :ref:`supported forms <Introduction_Forms>`.
        Elements from these systems will be merged into a new system.

    selections : list of (tuple, list, numpy.ndarray, or str), or 'all', default 'all'
        Atom selections for each molecular system. If `'all'`, all atoms are included.
        If a list is provided, it must match the length of `molecular_systems`, and each element
        can be a list, tuple, NumPy array of atom indices (0-based), or a selection string in a
        :ref:`supported syntax <Introduction_Selection>`.

    structure_indices : list of (tuple, list, numpy.ndarray, or 'all'), or 'all', default 'all'
        Indices of structures (0-based) to include from each molecular system. If a list is provided,
        it must match the length of `molecular_systems`.

    syntax : str, default 'MolSysMT'
        The syntax used to interpret any string-based selections (see :ref:`Introduction_Selection`).

    keep_ids : bool, default True
        Whether to preserve original atom, group, and molecule IDs. If `False`, IDs will be reset
        in the merged system.

    to_form : str or None, default None
        Output form of the new molecular system. If `None`, the form of the first input system is used.

    Returns
    -------
    molecular system
        A new molecular system composed of the selected elements from the input systems.
        The output form is controlled via the `to_form` argument.

    Raises
    ------
    NotSupportedFormError
        If any input molecular system has an unsupported form.

    ArgumentError
        If input arguments are invalid or inconsistent in length or compatibility.

    Notes
    -----
    All input molecular systems must be structurally aligned in terms of number of structures,
    or explicitly aligned via `structure_indices`.

    For more information on supported forms and syntaxes, see:

    - :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`
    - :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`

    See Also
    --------
    :func:`molsysmt.basic.select`
        Select elements from a molecular system.

    :func:`molsysmt.basic.add`
        Add elements from one system to another.

    :func:`molsysmt.basic.append_structures`
        Append structures from one system to another.

    :func:`molsysmt.basic.concatenate_structures`
        Concatenate structures across multiple systems.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    >>> molsys_A = msm.convert(molsys)
    >>> molsys_B = msm.structure.translate(molsys_A, translation='[0.1, 0.1, 0.1] nanometers')
    >>> molsys_merged = msm.basic.merge([molsys_A, molsys_B])
    >>> msm.basic.get(molsys_merged, n_peptides=True)
    2

    .. admonition:: User guide

       For a tutorial on how to use this function, see:
       :ref:`User Guide > Tools > Basic > Merge <Tutorial_Merge>`

    .. versionadded:: 0.1.0
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
    merge_arguments['keep_ids']=keep_ids

    output = merge_function(aux_molecular_systems, **merge_arguments)

    return output

