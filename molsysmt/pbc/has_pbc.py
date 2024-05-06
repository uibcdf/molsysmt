from molsysmt._private.digestion import digest

@digest()
def has_pbc(molecular_system, skip_digestion=False):
    """
    To be written soon...
    """

    from molsysmt import get

    box = get(molecular_system, structure_indices=0, box=True, skip_digestion=True)

    output = True

    if box is None:
        output = False

    return output
