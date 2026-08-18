from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Topology')
def to_molsysmt_MolSys(item, atom_indices='all', coordinates=None, box=None, skip_digestion=False):
    """
    Converting from openmm.Topology to molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : object, default=None
        Argument coordinates.
    box : object, default=None
        Argument box.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.structures import Structures
    from .to_molsysmt_Topology import to_molsysmt_Topology as to_molsysmt_Topology
    from . import get_box_from_system

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item.structures = Structures()
    if box is None:
        box = get_box_from_system(item)
    tmp_item.structures.append(coordinates=coordinates, box=box, skip_digestion=True)

    return tmp_item

