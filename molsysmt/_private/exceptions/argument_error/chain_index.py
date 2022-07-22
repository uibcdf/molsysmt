from ._argument_error import ArgumentError

class ChainIndexError(ArgumentError):

    def __init__(self, chain_index, caller=None, message=None):

        super().__init__('chain_index', caller=caller, message=message)

