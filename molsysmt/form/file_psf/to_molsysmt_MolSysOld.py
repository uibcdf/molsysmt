from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest(form='file:psf')
def to_molsysmt_MolSysOld(item, atom_indices='all',
        coordinates=None, structure_id=None, box=None, time=None, skip_digestion=False):
    """
    Converting from file:psf to molsysmt.MolSysOld.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : object, default=None
        Argument coordinates.
    structure_id : object, default=None
        Argument structure_id.
    box : object, default=None
        Argument box.
    time : object, default=None
        Argument time.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSysOld
        Resulting object in molsysmt.MolSysOld form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.native.molsys_old import MolSysOld
    from molsysmt.native.structures_old import StructuresOld
    from molsysmt.form.molsysmt_TopologyOld.to_molsysmt_TopologyOld import to_molsysmt_TopologyOld

    tmp_item = MolSysOld()
    tmp_item.topology = to_molsysmt_TopologyOld(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item.structures = StructuresOld()
    tmp_item.structures.append_structures(coordinates=coordinates, structure_id=structure_id, box=box, time=time,
                                          skip_digestion=True)

    return tmp_item

