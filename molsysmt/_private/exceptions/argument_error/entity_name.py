from ._argument_error import ArgumentError

class EntityNameError(ArgumentError):

    def __init__(self, entity_name, caller=None, message=None):

        super().__init__('entity_name', caller=caller, message=message)

