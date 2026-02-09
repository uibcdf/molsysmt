from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
import inspect

@arg_digest()
def merge(molecular_systems,
          selections='all',
          structure_indices='all',
          keep_ids = True,
          syntax='MolSysMT',
          to_form=None,
          skip_digestion=False
          ):
    """
    Merging elements from multiple molecular systems into a new one.

    This function builds a new molecular system by merging selected elements from several
    input systems. All inputs must be compatible in their number of structures; otherwise,
    `structure_indices` must be provided to align the frames that will be merged. You can also
    provide per-system atom selections via `selections`. The output form can be set with
    `to_form` (defaults to the first system’s form).

    Parameters
    ----------
    molecular_systems : list of molecular systems
        Input systems, each in one of the :ref:`supported forms <Introduction_Forms>`.
    selections : list of (tuple, list, numpy.ndarray or str) or 'all', default 'all'
        Atom selections for each input system. A single value applies to all systems; otherwise
        provide a list with the same length as `molecular_systems`. Selection strings follow
        :ref:`Introduction_Selection`. If `'all'`, all atoms from every system are included.
    structure_indices : list of (int, tuple, list, numpy.ndarray) or 'all', default 'all'
        0-based indices of the structures to include from each system. A single value applies
        to all systems; otherwise provide a list matching `molecular_systems`.
    keep_ids : bool, default True
        Whether to preserve original ids (atom, group, molecule) from the inputs. If `False`,
        ids are reassigned in the merged system.
    syntax : str, default 'MolSysMT'
        Selection syntax used when any entry in `selections` is a string.
        See :ref:`Introduction_Selection`.
    to_form : str or None, default None
        Output form of the merged molecular system. If `None`, the output molecular system inherits the first input
        system’s form.
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
    molecular system
        New molecular system composed of the selected elements from the inputs. Its form is
        controlled by `to_form` (or inherited from the first input when `None`).

    Raises
    ------
    NotSupportedFormError
        If any input molecular system has an unsupported form.
    ArgumentError
        If input arguments are invalid or inconsistent in length or compatibility.

    Notes
    -----
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.
    - All input systems must be aligned in **number of structures** or explicitly aligned via
      `structure_indices`. Internal conversions are performed when the input forms differ from
      the chosen `to_form`.

    See Also
    --------
    :func:`molsysmt.basic.select`
        Select elements from a molecular system.
    :func:`molsysmt.basic.add`
        Add elements from one system to another.
    :func:`molsysmt.basic.append_structures` :
        Append structures from one system to another.
    :func:`molsysmt.basic.concatenate_structures` :
        Concatenate structures across multiple molecular systems.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    >>> molsys_A = msm.convert(molsys)
    >>> molsys_B = msm.structure.translate(molsys_A, translation='[0.1, 0.1, 0.1] nanometers')
    >>> molsys_merged = msm.basic.merge([molsys_A, molsys_B])
    >>> msm.basic.get(molsys_merged, n_peptides=True)
    2

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Merge`.

    .. versionadded:: 1.0.0
    """

    from . import convert, get_form, select
    from molsysmt.form import _dict_modules
    from molsysmt._private.smonitor import ArgumentLengthError

    n_molecular_systems = len(molecular_systems)

    if not isinstance(selections, (list, tuple)):
        selections = [selections for ii in range(n_molecular_systems)]
    elif len(selections) != n_molecular_systems:
        raise ArgumentLengthError(
            argument="selections",
            expected=n_molecular_systems,
            actual=len(selections),
            caller="molsysmt.basic.merge",
        )

    if not isinstance(structure_indices, (list, tuple)):
        structure_indices = [structure_indices for ii in range(n_molecular_systems)]
    elif len(structure_indices) != n_molecular_systems:
        raise ArgumentLengthError(
            argument="structure_indices",
            expected=n_molecular_systems,
            actual=len(structure_indices),
            caller="molsysmt.basic.merge",
        )

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

