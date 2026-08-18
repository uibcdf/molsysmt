from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.AmberRestartFile')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.AmberRestartFile to molsysmt.MolSys.

    Parameters
    ----------
    item : mdtraj.AmberRestartFile
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolSys
        Converted molecular system representation.
    """

    from molsysmt.native import Topology, MolSys
    from .to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = MolSys()
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                 structure_indices=structure_indices, skip_digestion=True)
    tmp_item.topology = Topology(n_atoms=item._n_atoms)

    return tmp_item
