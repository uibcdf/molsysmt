from molsysmt._private.exceptions import ArgumentError

def digest_rigid_water(rigid_water, caller=None):


    if caller.startswith('molsysmt.form.') and caller.count('.to_')==2:
        return rigid_water

    raise ArgumentError('rigid_water', value=rigid_water, caller=caller, message=None)

