from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:crd')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', get_missing_bonds=False,
                       skip_digestion=False):
    """
    Converting from file:crd to molsysmt.MolSys.

    Parameters
    ----------
    item : file:crd
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolSys
        Converted molecular system representation.
    """

    from molsysmt.native.molsys import MolSys
    from .to_molsysmt_Topology import to_molsysmt_Topology
    from .to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

