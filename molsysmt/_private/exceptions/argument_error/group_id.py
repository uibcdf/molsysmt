from ._argument_error import ArgumentError

class GroupIdError(ArgumentError):

    def __init__(self, group_id, caller=None, message=None):

        super().__init__('group_id', caller=caller, message=message)

