from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_molsysmt_MolSys(item, atom_indices='all', coordinates=None, box=None):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.structures import Structures
    from . import to_molsysmt_Topology as to_molsysmt_Topology
    from . import get_box_from_system

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices)
    tmp_item.structures = Structures()
    if box is None:
        box = get_box_from_system(item)
    tmp_item.structures.append_structures(coordinates=coordinates, box=box)

    return tmp_item

def _to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.basic import get

    coordinates = get(molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
                      coordinates=True)

    box = get(molecular_system, structure_indices=structure_indices, box=True)

    return to_molsysmt_MolSys(item, atom_indices=atom_indices, coordinates=coordinates, box=box)

