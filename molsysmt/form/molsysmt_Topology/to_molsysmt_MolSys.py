from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
def to_molsysmt_MolSys(item, coordinates=None, box=None, atom_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.structures import Structures
    from . import extract

    tmp_item = MolSys()
    tmp_item.topology = extract(item, atom_indices=atom_indices, copy_if_all=False)
    tmp_item.structures = Structures()
    tmp_item.structures.append_structures(coordinates=coordinates, box=box)

    return tmp_item

def _to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all'):

    return to_molsysmt_MolSys(item, coordinates=coordinates, box=box, atom_indices=atom_indices)

