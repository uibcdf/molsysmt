from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_molsysmt_MolSysOld(item, atom_indices='all', coordinates=None, box=None, skip_digestion=False):

    from molsysmt.native.molsys_old import MolSysOld
    from molsysmt.native.structures_old import StructuresOld
    from . import to_molsysmt_Topology as to_molsysmt_Topology
    from . import get_box_from_system

    tmp_item = MolSysOld()
    tmp_item.topology = to_molsysmt_TopologyOld(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item.structures = StructuresOld()
    if box is None:
        box = get_box_from_system(item, skip_digestion=True)
    tmp_item.structures.append_structures(coordinates=coordinates, box=box, skip_digestion=True)

    return tmp_item

