from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:uniprot_id')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from .to_file_fasta import to_file_fasta
    from molsysmt.form.file_fasta.to_molsysmt_Topology import to_molsysmt_Topology as file_fasta_to_molsysmt_Topology

    tmp_item = to_file_fasta(item, skip_digestion=True)
    tmp_item = file_fasta_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
