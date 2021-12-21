def has_small_molecules(molecular_system):

    from molsysmt.basic import get

    output = False

    n_small_molecules = get(molecular_system, target='system', n_small_molecules=True)

    if n_small_molecules>0:
        output = True

    return output

