from molsysmt._private.smonitor import ArgumentError
from argdigest.core.caller import caller_matches

def digest_bond_order(bond_order, caller=None):

    if bond_order is None and caller_matches(caller, 'add_bond'):
        return None

    if caller=='molsysmt.basic.get.get':
        if isinstance(bond_order, bool):
            return bond_order
    elif caller=='molsysmt.basic.compare.compare':
        if isinstance(bond_order, bool):
            return bond_order

    raise ArgumentError('bond_order', value=bond_order, caller=caller, message=None)
