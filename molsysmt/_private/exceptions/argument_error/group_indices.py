from ._argument_error import ArgumentError

class GroupIndicesError(ArgumentError):

    def __init__(self, group_indices, caller=None, message=None):

        super().__init__('group_indices', caller=caller, message=message)

