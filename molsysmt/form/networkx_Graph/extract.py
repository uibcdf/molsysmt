from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='networkx.Graph')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of atoms or structures from form networkx.Graph.

    Parameters
    ----------
    item : networkx.Graph
        Source item.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices to extract.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    networkx.Graph
        Extracted subset in the same form.
    """

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:
         tmp_item = item.copy()
        else:
            tmp_item = item.subgraph(atom_indices).copy()
    else:

        tmp_item = item
        if not is_all(atom_indices):
            tmp_item = tmp_item.atom_slice(atom_indices)
        if not is_all(structure_indices):
            tmp_item = tmp_item.slice(structure_indices)

    return tmp_item

