from ._argument_error import ArgumentError

class AtomIndicesError(ArgumentError):

    def __init__(self, atom_indices, caller=None, message=None):

        super().__init__('atom_indices', caller=caller, message=message)

