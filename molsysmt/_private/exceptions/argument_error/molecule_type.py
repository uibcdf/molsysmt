from ._argument_error import ArgumentError

class MoleculeTypeError(ArgumentError):

    def __init__(self, molecule_type, caller=None, message=None):

        super().__init__('molecule_type', caller=caller, message=message)

