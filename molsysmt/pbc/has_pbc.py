from molsysmt._private.digestion import digest

@digest()
def has_pbc(molecular_system):
    """
    To be written soon...
    """

    from molsysmt import get

    box = get(molecular_system, structure_indices=0, box=True)

    output = True

    if box is None:
        output = False

    return output
