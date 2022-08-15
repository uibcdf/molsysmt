from molsysmt._private.exceptions import ArgumentError

def digest_peptides(peptides, caller=None):

    if caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(peptides, (bool, int)):
            return peptides
    if caller=='molsysmt.basic.contains.contains':
        if isinstance(peptides, (bool, int)):
            return peptides
        elif peptides is None:
            return None

    raise ArgumentError('peptides', value=peptides, caller=caller, message=None)

