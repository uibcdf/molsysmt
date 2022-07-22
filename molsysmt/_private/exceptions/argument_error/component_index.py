from ._argument_error import ArgumentError

class ComponentIndexError(ArgumentError):

    def __init__(self, component_index, caller=None, message=None):

        super().__init__('component_index', caller=caller, message=message)

