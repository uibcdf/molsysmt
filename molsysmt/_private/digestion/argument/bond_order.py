from molsysmt._private.exceptions import ArgumentError

def digest_bond_order(bond_order, caller=None):

    if caller=='molsysmt.basic.get.get':
        if isinstance(bond_order, bool):
            return bond_order

    raise ArgumentError('bond_order', value=bond_order, caller=caller, message=None)

