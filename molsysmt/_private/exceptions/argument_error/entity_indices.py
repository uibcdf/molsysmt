from ._argument_error import ArgumentError

class EntityIndicesError(ArgumentError):

    def __init__(self, entity_indices, caller=None, message=None):

        super().__init__('entity_indices', caller=caller, message=message)

