from molsysmt._private.digestion import digest

@digest(form='pdbfixer.PDBfixer')
def to_biopython_Seq(item, atom_indices='all'):

    from . import to_string_aminoacids1
    from ..string_aminoacids1 import to_biopython_Seq as string_aminoacids1_to_biopython_Seq

    tmp_item = to_string_aminoacids1(item, atom_indices=atom_indices)
    tmp_item = string_aminoacids1_to_biopython_Seq(tmp_item)

    return tmp_item

def _to_biopython_Seq(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_biopython_Seq(item, atom_indices=atom_indices, structure_indices=structure_indices)

