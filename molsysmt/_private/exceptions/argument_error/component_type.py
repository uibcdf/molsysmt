from ._argument_error import ArgumentError

class ComponentTypeError(ArgumentError):

    def __init__(self, component_type, caller=None, message=None):

        super().__init__('component_type', caller=caller, message=message)

