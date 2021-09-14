def in_pdbid_181l(to_form='molsysmt.MolSys'):

    from molsysmt.demo import files
    from molsysmt.basic import convert
    molsys = convert(files['in_pdbid_181l.msmpk'], to_form=to_form)
    return molsys

