from molsysmt._private.argdigest import arg_digest

@arg_digest(form='nglview.NGLWidget')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', get_missing_bonds=True, 
                       skip_digestion=False):
    """
    Converting from nglview.NGLWidget to molsysmt.MolSys.

    Parameters
    ----------
    item : nglview.NGLWidget
        Source item in nglview.NGLWidget form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    get_missing_bonds : object
        Argument get_missing_bonds.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.native.molsys import MolSys
    from .to_molsysmt_Topology import to_molsysmt_Topology
    from .to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, get_missing_bonds=get_missing_bonds,
                                             skip_digestion=True)
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                 structure_indices=structure_indices, skip_digestion=True)
    return tmp_item

