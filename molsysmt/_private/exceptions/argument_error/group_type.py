from ._argument_error import ArgumentError

class GroupTypeError(ArgumentError):

    def __init__(self, group_type, caller=None, message=None):

        super().__init__('group_type', caller=caller, message=message)

