from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
def to_molsysmt_MolSys(item, coordinates=None, box=None, atom_indices='all', digest=True):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.structures import Structures
    from . import extract

    tmp_item = MolSys()
    tmp_item.topology = extract(item, atom_indices=atom_indices, copy_if_all=False, digest=False)
    tmp_item.structures = Structures()
    tmp_item.structures.append_structures(coordinates=coordinates, box=box, digest=False)

    return tmp_item

