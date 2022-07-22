from ._argument_error import ArgumentError

class AtomIdError(ArgumentError):

    def __init__(self, atom_id, caller=None, message=None):

        super().__init__('atom_id', caller=caller, message=message)

