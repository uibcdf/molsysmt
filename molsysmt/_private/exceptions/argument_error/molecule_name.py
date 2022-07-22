from ._argument_error import ArgumentError

class MoleculeNameError(ArgumentError):

    def __init__(self, molecule_name, caller=None, message=None):

        super().__init__('molecule_name', caller=caller, message=message)

