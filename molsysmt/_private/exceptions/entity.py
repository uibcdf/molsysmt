from ..functions import caller_name
from ..webs import github_issues, api_doc

class WrongEntityIndexError(ValueError):

    def __init__(self, entity_index, message=None, caller=None):

        if not caller:
            caller = caller_name(skip=3)

        full_message = f"Error in {caller} due to the `entity_index` argument."

        if message:
            full_message += message

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )
        super().__init__(full_message)

class WrongEntityIdError(ValueError):

    def __init__(self, entity_id, message=None, caller=None):

        if not caller:
            caller = caller_name(skip=3)

        full_message = f"Error in {caller} due to the `entity_id` argument."

        if message:
            full_message += message

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )
        super().__init__(full_message)

class WrongEntityNameError(ValueError):

    def __init__(self, entity_name, message=None, caller=None):

        if not caller:
            caller = caller_name(skip=3)

        full_message = f"Error in {caller} due to the `entity_name` argument."

        if message:
            full_message += message

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )
        super().__init__(full_message)

class WrongEntityIdError(ValueError):

    def __init__(self, entity_type, message=None, caller=None):

        if not caller:
            caller = caller_name(skip=3)

        full_message = f"Error in {caller} due to the `entity_type` argument."

        if message:
            full_message += message

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )
        super().__init__(full_message)

class WrongEntityIndicesError(ValueError):

    def __init__(self, entity_indices, message=None, caller=None):

        if not caller:
            caller = caller_name(skip=3)

        full_message = f"Error in {caller} due to the `entity_indices` argument."

        if message:
            full_message += message

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )
        super().__init__(full_message)

