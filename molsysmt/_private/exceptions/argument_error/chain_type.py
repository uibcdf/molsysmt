from ._argument_error import ArgumentError

class ChainTypeError(ArgumentError):

    def __init__(self, chain_type, caller=None, message=None):

        super().__init__('chain_type', caller=caller, message=message)

