def traj(to_form='molsysmt.TrajectoryDict'):

    from molsysmt.demo import files
    from molsysmt.basic import convert
    molsys = convert(files['two_lj_particles_traj.trjpk'], to_form=to_form)
    return molsys

