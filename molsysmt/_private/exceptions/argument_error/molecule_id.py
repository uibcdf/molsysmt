from ._argument_error import ArgumentError

class MoleculeIdError(ArgumentError):

    def __init__(self, molecule_id, caller=None, message=None):

        super().__init__('molecule_id', caller=caller, message=message)

