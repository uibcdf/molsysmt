from ._argument_error import ArgumentError

class ChainNameError(ArgumentError):

    def __init__(self, chain_name, caller=None, message=None):

        super().__init__('chain_name', caller=caller, message=message)

