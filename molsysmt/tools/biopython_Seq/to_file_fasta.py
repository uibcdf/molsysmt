from molsysmt.tools.biopython_Seq.is_biopython_Seq import is_biopython_Seq
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError
from molsysmt._private_tools.exceptions import NotImplementedMethodError
from molsysmt._private_tools.atom_indices import digest_atom_indices

def to_file_fasta(item, atom_indices='all', structure_indices='all', output_filename=None,
                  check=True):

    if check:

        try:
            is_biopython_Seq(item)
        except:
            raise WrongFormError('biopython.Seq')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    from molsysmt.tools.biopython_Seq import to_biopython_SeqRecord as biopython_Seq_to_biopython_SeqRecord
    from molsysmt.tools.biopython_SeqRecord import to_file_fasta as biopython_SeqRecord_to_file_fasta

    tmp_item = biopython_Seq_to_biopython_SeqRecord(item, atom_indices=atom_indices,
                                      structure_indices=structure_indices, check=False)
    tmp_item = biopython_SeqRecord_to_file_fasta(tmp_item, output_filename=output_filename,
                                                 check=False)

    return tmp_item

