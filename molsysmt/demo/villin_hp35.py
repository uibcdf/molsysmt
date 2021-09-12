def vacuum(to_form='molsysmt.MolSys'):

    from molsysmt.demo import files
    from molsysmt.basic import convert
    molsys = convert(files['villin_hp35_vacuum.msmpk'], to_form=to_form)
    return molsys

def solvated(to_form='molsysmt.MolSys'):

    from molsysmt.demo import files
    from molsysmt.basic import convert
    molsys = convert(files['villin_hp35_solvated.msmpk'], to_form=to_form)
    return molsys

def explicit_solvent_traj(to_form='molsysmt.MolSys'):

    from molsysmt.demo import files
    from molsysmt.basic import convert
    molsys = convert(files['villin_hp35_solvated.h5'], to_form=to_form)
    return molsys

