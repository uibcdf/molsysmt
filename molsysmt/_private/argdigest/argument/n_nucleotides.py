from molsysmt._private.smonitor import ArgumentError

def digest_n_nucleotides(n_nucleotides, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_nucleotides, bool):
            return n_nucleotides
    elif caller=='molsysmt.basic.contains.contains':
        if isinstance(n_nucleotides, (bool, int)):
            return n_nucleotides
    elif caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(n_nucleotides, (bool, int)):
            return n_nucleotides

    raise ArgumentError('n_nucleotides', value=n_nucleotides, caller=caller, message=None)
