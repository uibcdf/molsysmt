from ._argument_error import ArgumentError

class ComponentIdError(ArgumentError):

    def __init__(self, component_id, caller=None, message=None):

        super().__init__('component_id', caller=caller, message=message)

