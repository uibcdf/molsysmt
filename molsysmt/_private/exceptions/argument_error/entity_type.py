from ._argument_error import ArgumentError

class EntityTypeError(ArgumentError):

    def __init__(self, entity_type, caller=None, message=None):

        super().__init__('entity_type', caller=caller, message=message)

