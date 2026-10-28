from molsysmt._private.smonitor import ArgumentError


def digest_fasta_text(fasta_text, caller=None):
    if isinstance(fasta_text, str):
        return fasta_text
    raise ArgumentError("fasta_text", value=fasta_text, caller=caller)
