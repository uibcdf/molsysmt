from ._argument_error import ArgumentError

class ComponentIndicesError(ArgumentError):

    def __init__(self, component_indices, caller=None, message=None):

        super().__init__('component_indices', caller=caller, message=message)

