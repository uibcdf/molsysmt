from molsysmt._private.exceptions import ArgumentError

def digest_bond_type(bond_type, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(bond_type, bool):
            return bond_type

    raise ArgumentError('bond_type', value=bond_type, caller=caller, message=None)

