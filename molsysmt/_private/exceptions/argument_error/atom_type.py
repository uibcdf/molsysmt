from ._argument_error import ArgumentError

class AtomTypeError(ArgumentError):

    def __init__(self, atom_type, caller=None, message=None):

        super().__init__('atom_type', caller=caller, message=message)

