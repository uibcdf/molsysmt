from ._argument_error import ArgumentError

class ChainIndicesError(ArgumentError):

    def __init__(self, chain_indices, caller=None, message=None):

        super().__init__('chain_indices', caller=caller, message=message)

