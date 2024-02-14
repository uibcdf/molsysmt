from molsysmt._private.digestion import digest

@digest(form='molsysmt.TopologyOld')
def to_molsysmt_MolSysOld(item, coordinates=None, box=None, atom_indices='all', skip_digestion=False):

    from molsysmt.native.molsys_old import MolSysOld
    from molsysmt.native.structures_old import StructuresOld
    from . import extract

    tmp_item = MolSysOld()
    tmp_item.topology = extract(item, atom_indices=atom_indices, copy_if_all=False)
    tmp_item.structures = StructuresOld()
    tmp_item.structures.append_structures(coordinates=coordinates, box=box)

    return tmp_item

