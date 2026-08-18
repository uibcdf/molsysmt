from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Topology')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from openff.Topology to molsysmt.Structures.

    Parameters
    ----------
    item : openff.Topology
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Structures
        Converted molecular system representation.
    """

    from molsysmt.native import Structures

    tmp_item = Structures()
    return tmp_item
