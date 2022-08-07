from molsysmt._private.exceptions import ArgumentError

def digest_peptides(peptides, caller=None):

    if caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(peptides, (bool, int)):
            return peptides

    raise ArgumentError('peptides', value=peptides, caller=caller, message=None)

