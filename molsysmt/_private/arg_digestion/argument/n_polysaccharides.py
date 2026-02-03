from molsysmt._private.exceptions import ArgumentError

def digest_n_polysaccharides(n_polysaccharides, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_polysaccharides, bool):
            return n_polysaccharides
    elif caller=='molsysmt.basic.contains.contains':
        if isinstance(n_molecules, (bool, int)):
            return n_molecules
    elif caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(n_molecules, (bool, int)):
            return n_molecules

    raise ArgumentError('n_polysaccharides', value=n_polysaccharides, caller=caller, message=None)

