def has_waters(molecular_system):

    from molsysmt.basic import get

    output = False

    n_waters = get(molecular_system, target='system', n_waters=True)

    if n_waters>0:
        output = True

    return output

