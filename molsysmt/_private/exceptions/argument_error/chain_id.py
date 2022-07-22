from ._argument_error import ArgumentError

class ChainIdError(ArgumentError):

    def __init__(self, chain_id, caller=None, message=None):

        super().__init__('chain_id', caller=caller, message=message)

