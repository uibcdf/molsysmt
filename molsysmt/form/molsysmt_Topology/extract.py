from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.Topology')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of atoms or structures from form molsysmt.Topology.

    Parameters
    ----------
    item : molsysmt.Topology
        Source item.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices to extract.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Topology
        Extracted subset in the same form.
    """

    from molsysmt.native import Topology
    if not isinstance(item, Topology):
        from molsysmt.basic import convert
        item = convert(item, to_form='molsysmt.Topology', skip_digestion=True)

    if is_all(atom_indices):
        if copy_if_all:
            tmp_item = item.copy()
        else:
            tmp_item = item
    else:
        tmp_item = item.extract(atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

