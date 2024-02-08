from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_molsysmt_MolSys(item, atom_indices='all', coordinates=None, box=None, skip_digestion=False):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.structures import Structures
    from . import to_molsysmt_Topology as to_molsysmt_Topology
    from . import get_box_from_system

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item.structures = Structures()
    if box is None:
        box = get_box_from_system(item)
    tmp_item.structures.append_structures(coordinates=coordinates, box=box, skip_digestion=True)

    return tmp_item

