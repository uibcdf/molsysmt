from molsysmt._private.smonitor import ArgumentError
from argdigest.core.caller import caller_matches


def digest_atom_index_1(atom_index_1, caller=None):

    if caller_matches(caller, 'add_bond'):
        if isinstance(atom_index_1, int):
            return atom_index_1

    raise ArgumentError('atom_index_1', value=atom_index_1, caller=caller, message=None)
