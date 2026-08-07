from molsysmt._private.smonitor import ArgumentError

def digest_rigid_water(rigid_water, caller=None):


    if caller is not None and caller.startswith('molsysmt.form.') and '.to_' in caller:
        return rigid_water

    raise ArgumentError('rigid_water', value=rigid_water, caller=caller, message=None)

