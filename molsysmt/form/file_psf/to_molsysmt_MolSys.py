from molsysmt._private.arg_digestion import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest(form='file:psf')
def to_molsysmt_MolSys(item, atom_indices='all',
        coordinates=None, structure_id=None, box=None, time=None, skip_digestion=False):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.structures import Structures
    from ..molsysmt_Topology.to_molsysmt_Topology import to_molsysmt_Topology

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item.structures = Structures()
    tmp_item.structures.append(coordinates=coordinates, structure_id=structure_id, box=box, time=time,
                               skip_digestion=True)

    return tmp_item

