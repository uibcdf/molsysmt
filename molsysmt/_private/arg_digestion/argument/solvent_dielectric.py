from molsysmt._private.smonitor import ArgumentError

def digest_solvent_dielectric(solvent_dielectric, caller=None):


    if caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return solvent_dielectric

    raise ArgumentError('solvent_dielectric', value=solvent_dielectric, caller=caller, message=None)

