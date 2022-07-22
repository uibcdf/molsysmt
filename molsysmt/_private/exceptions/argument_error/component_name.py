from ._argument_error import ArgumentError

class ComponentNameError(ArgumentError):

    def __init__(self, component_name, caller=None, message=None):

        super().__init__('component_name', caller=caller, message=message)

