def has_ions(molecular_system):

    from molsysmt.basic import get

    output = False

    n_ions = get(molecular_system, target='system', n_ions=True)

    if n_ions>0:
        output = True

    return output

