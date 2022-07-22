from ._argument_error import ArgumentError

class EntityIndexError(ArgumentError):

    def __init__(self, entity_index, caller=None, message=None):

        super().__init__('entity_index', caller=caller, message=message)

