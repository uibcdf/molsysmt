from ._argument_error import ArgumentError

class MoleculeIndicesError(ArgumentError):

    def __init__(self, molecule_indices, caller=None, message=None):

        super().__init__('molecule_indices', caller=caller, message=message)

