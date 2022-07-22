from ._argument_error import ArgumentError

class GroupIndexError(ArgumentError):

    def __init__(self, group_index, caller=None, message=None):

        super().__init__('group_index', caller=caller, message=message)

