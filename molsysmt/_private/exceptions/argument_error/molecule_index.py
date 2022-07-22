from ._argument_error import ArgumentError

class MoleculeIndexError(ArgumentError):

    def __init__(self, molecule_index, caller=None, message=None):

        super().__init__('molecule_index', caller=caller, message=message)

