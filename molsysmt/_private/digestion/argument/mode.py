from ...exceptions import ArgumentError

def digest_mode(mode, caller=None):

    if caller=='molsysmt.build.remove_atoms_with_alternate_locations.remove_atoms_with_alternate_locations':

        if isinstance(mode, str):
            if mode in ['A']:
                return mode

    raise ArgumentError('mode', value=mode, caller=caller, message=None)
