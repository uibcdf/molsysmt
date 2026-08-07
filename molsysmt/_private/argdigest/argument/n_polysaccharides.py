from molsysmt._private.smonitor import ArgumentError

def digest_n_polysaccharides(n_polysaccharides, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(n_polysaccharides, bool):
            return n_polysaccharides
    elif caller=='molsysmt.basic.contains.contains':
        if isinstance(n_polysaccharides, (bool, int)):
            return n_polysaccharides
    elif caller=='molsysmt.basic.is_composed_of.is_composed_of':
        if isinstance(n_polysaccharides, (bool, int)):
            return n_polysaccharides

    raise ArgumentError('n_polysaccharides', value=n_polysaccharides, caller=caller, message=None)

