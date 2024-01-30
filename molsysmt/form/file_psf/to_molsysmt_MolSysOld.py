from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='file:psf')
def to_molsysmt_MolSysOld(item, atom_indices='all',
        coordinates=None, structure_id=None, box=None, time=None, skip_digestion=False):

    from molsysmt.native.molsys_old import MolSysOld
    from molsysmt.native.structures_old import StructuresOld
    from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld

    tmp_item = MolSysOld()
    tmp_item.topology = to_molsysmt_TopologyOld(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item.structures = StructuresOld()
    tmp_item.structures.append_structures(coordinates=coordinates, structure_id=structure_id, box=box, time=time,
                                          skip_digestion=True)

    return tmp_item

