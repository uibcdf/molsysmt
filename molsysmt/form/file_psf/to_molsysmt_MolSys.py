from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='file:psf')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all',
        coordinates=None, structure_id=None, box=None, time=None):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.structures import Structures
    from .to_molsysmt_Topology import to_molsysmt_Topology

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices)
    tmp_item.structures = Structures()
    tmp_item.structures.append_structures(coordinates=coordinates, structure_id=structure_id, box=box, time=time)

    return tmp_item

def _to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt import convert, has_attribute

    if has_attribute(molecular_system, 'structural'):

        molsysmt_structures = convert(molecular_system, selection=atom_indices, structure_indices=structure_indices,
            to_form='molsysmt.Structures')

        coordinates = molsysmt_structures.coordinates
        time = molsysmt_structures.time
        box = molsysmt_structures.box
        structure_id = molsysmt_structures.structure_id

        tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, coordinates=coordinates,
            time=time, box=box, structure_id=structure_id)
    else:

        tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices)

    return tmp_item

