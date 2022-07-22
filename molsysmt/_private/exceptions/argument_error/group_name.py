from ._argument_error import ArgumentError

class GroupNameError(ArgumentError):

    def __init__(self, group_name, caller=None, message=None):

        super().__init__('group_name', caller=caller, message=message)

