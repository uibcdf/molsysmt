from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
def to_string_pdb_text(item, atom_indices='all', coordinates=None, box=None, skip_digestion=False):

    from molsysmt.native import MolSys, Structures
    from . import extract
    from ..molsysmt_MolSys import to_string_pdb_text as molsysmt_MolSys_to_string_pdb_text

    tmp_item =  MolSys()
    tmp_item.topology = extract(item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)
    tmp_item.structures.append(coordinates=coordinates, box=box, skip_digestion=True)
    tmp_item = molsysmt_MolSys_to_string_pdb_text(tmp_item, skip_digestion=True)

    return tmp_item


