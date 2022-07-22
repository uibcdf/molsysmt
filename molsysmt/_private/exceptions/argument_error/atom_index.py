from ._argument_error import ArgumentError

class AtomIndexError(ArgumentError):

    def __init__(self, atom_index, caller=None, message=None):

        super().__init__('atom_index', caller=caller, message=message)

