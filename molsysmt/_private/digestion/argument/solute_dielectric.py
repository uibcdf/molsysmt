from molsysmt._private.exceptions import ArgumentError

def digest_solute_dielectric(solute_dielectric, caller=None):


    if caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return solute_dielectric

    raise ArgumentError('solute_dielectric', value=solute_dielectric, caller=caller, message=None)

