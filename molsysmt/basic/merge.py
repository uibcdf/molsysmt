from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import inspect

@digest()
def merge(molecular_systems,
          selections='all',
          structure_indices='all',
          syntax='MolSysMT',
          to_form=None,
          ):

    """merge(items=None, selection='all', structure_indices='all', syntax='MolSysMT' to_form=None)

    XXX

    Paragraph with detailed explanation.

    Parameters
    ----------

    item: molecular model
        Molecular model in any of the supported forms by MolSysMT. (See: XXX)

    to_form: str, default='molsysmt.MolSys'
        Any accepted form by MolSysMt for the output object.

    selection: str, list, tuple or np.ndarray, defaul='all'
       Atoms selection over which this method applies. The selection can be given by a
       list, tuple or numpy array of integers (0-based), or by means of a string following any of
       the selection syntax parsable by MolSysMT (see: :func:`molsysmt.select`).

    syntax: str, default='MolSysMT'
       Syntaxis used in the argument `selection` (in case it is a string). The
       current options supported by MolSysMt can be found in section XXX (see: :func:`molsysmt.select`).

    Returns
    -------
    None
        The method prints out a pandas dataframe with relevant information depending on the element
        and the form of the item.

    Examples
    --------

    See Also
    --------

    :func:`molsysmt.get`, :func:`molsysmt.select`
    Notes
    -----

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
                aux_atom_indices.append(selection(tmp_molecular_system, selection=selection, syntax=syntax))
            aux_structure_indices.append(tmp_structure_indices)
        else:
            aux = convert(tmp_molecular_system, to_form=to_form, selection=tmp_selection,
                    structure_indices=tmp_structure_indices)
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

    output = merge_function(aux_molecular_systems, **merge_arguments)

    return output

