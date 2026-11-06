"""Validate an explicit reproducibility seed without accepting booleans."""


def digest_random_seed(random_seed, caller=None):
    if random_seed is None:
        return None
    from molsysmt.build._ion_replacement import nonnegative_integer

    return nonnegative_integer(random_seed, "random_seed", caller=caller)
