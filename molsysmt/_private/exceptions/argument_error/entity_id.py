from ._argument_error import ArgumentError

class EntityIdError(ArgumentError):

    def __init__(self, entity_id, caller=None, message=None):

        super().__init__('entity_id', caller=caller, message=message)

