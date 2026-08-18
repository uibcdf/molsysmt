from molsysmt._private.argdigest import arg_digest
@arg_digest(form='file:psf')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:psf to molsysmt.Topology.

    Parameters
    ----------
    item : file:psf
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Topology
        Converted molecular system representation.
    """

    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    return to_molsysmt_MolSys(
        item, atom_indices=atom_indices, skip_digestion=True
    ).topology
