from molsysmt._private.digestion import digest

@digest(form='pdbfixer.PDBfixer')
def to_biopython_Seq(item, atom_indices='all', digest=True):

    from . import to_string_aminoacids1
    from ..string_aminoacids1 import to_biopython_Seq as string_aminoacids1_to_biopython_Seq

    tmp_item = to_string_aminoacids1(item, atom_indices=atom_indices, digest=False)
    tmp_item = string_aminoacids1_to_biopython_Seq(tmp_item, digest=False)

    return tmp_item

