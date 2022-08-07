from molsysmt._private.exceptions import ArgumentError

def digest_n_peptides(n_peptides, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_peptides, bool):
            return n_peptides

    raise ArgumentError('n_peptides', value=n_peptides, caller=caller, message=None)

