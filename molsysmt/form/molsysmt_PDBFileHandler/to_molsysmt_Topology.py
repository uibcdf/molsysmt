import os
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.PDBFileHandler')
def to_molsysmt_Topology(item, atom_indices='all', get_missing_bonds=True, skip_digestion=False):
    """
    Converting from molsysmt.PDBFileHandler to molsysmt.Topology.

    Parameters
    ----------
    item : molsysmt.PDBFileHandler
        Source item in molsysmt.PDBFileHandler form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    get_missing_bonds : object
        Argument get_missing_bonds.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler
    from .to_molsysmt_MolSys import _build_topology_from_content

    if isinstance(item, (str, os.PathLike)):
        item = to_molsysmt_PDBFileHandler(str(item), skip_digestion=True)
        opened_here = True
    else:
        opened_here = False

    tmp_item = _build_topology_from_content(item, get_missing_bonds=get_missing_bonds)
    tmp_item = tmp_item.extract(atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)

    if opened_here:
        item.close()

    return tmp_item
