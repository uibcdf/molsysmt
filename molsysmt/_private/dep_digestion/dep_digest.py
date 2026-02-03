from depdigest import dep_digest as _dep_digest_lib

def dep_digest(*args, **kwargs):
    """
    MolSysMT dependency digestion decorator.
    Delegates to the external DepDigest library.
    """
    return _dep_digest_lib(*args, **kwargs)
