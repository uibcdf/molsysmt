from ...exceptions import ArgumentError
from string import ascii_uppercase

alternate_locations = list(ascii_uppercase)

def digest_keep(keep, caller=None):

    if caller=='molsysmt.build.remove_atoms_with_alternate_locations.remove_atoms_with_alternate_locations':

        if isinstance(keep, str):
            if keep in alternate_locations:
                return keep

    raise ArgumentError('keep', value=keep, caller=caller, message=None)
