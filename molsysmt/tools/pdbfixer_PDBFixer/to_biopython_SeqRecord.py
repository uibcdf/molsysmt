from molsysmt.tools.mmtf_MMTFDecoder.is_pdbfixer_PDBFixer import is_pdbfixer_PDBFixer
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError
from molsysmt._private_tools.exceptions import NotImplementedMethodError
from molsysmt._private_tools.atom_indices import digest_atom_indices

def to_biopython_SeqRecord(item, atom_indices='all', check=True):

    if check:

        try:
            is_pdbfixer_PDBFixer(item)
        except:
            raise WrongFormError('pdbfixer.PDBFixer')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    from molsysmt.tools.pdbfixer_PDBFixer import to_string_aminoacids1 as pdbfixer_PDBFixer_to_string_aminoacids1
    from molsysmt.tools.string_aminoacids1 import to_biopython_SeqRecord as string_aminoacids1_to_biopython_SeqRecord

    tmp_item = pdbfixer_PDBFixer_to_string_aminoacids1(item, atom_indices=atom_indices, check=False)
    tmp_item = string_aminoacids1_to_biopython_SeqRecord(tmp_item, check=False)

    return tmp_item

