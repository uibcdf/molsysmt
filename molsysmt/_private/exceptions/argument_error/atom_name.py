from ._argument_error import ArgumentError

class AtomNameError(ArgumentError):

    def __init__(self, atom_name, caller=None, message=None):

        super().__init__('atom_name', caller=caller, message=message)

