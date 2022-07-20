from ..functions import caller_name
from ..webs import github_issues, api_doc

class WrongComponentIndexError(ValueError):

    def __init__(self, component_index, message=None, caller=None):

        if not caller:
            caller = caller_name(skip=3)

        full_message = f"Error in {caller} due to the `component_index` argument."

        if message:
            full_message += message

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )
        super().__init__(full_message)

class WrongComponentIdError(ValueError):

    def __init__(self, component_id, message=None, caller=None):

        if not caller:
            caller = caller_name(skip=3)

        full_message = f"Error in {caller} due to the `component_id` argument."

        if message:
            full_message += message

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )
        super().__init__(full_message)

class WrongComponentNameError(ValueError):

    def __init__(self, component_name, message=None, caller=None):

        if not caller:
            caller = caller_name(skip=3)

        full_message = f"Error in {caller} due to the `component_name` argument."

        if message:
            full_message += message

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )
        super().__init__(full_message)

class WrongComponentIdError(ValueError):

    def __init__(self, component_type, message=None, caller=None):

        if not caller:
            caller = caller_name(skip=3)

        full_message = f"Error in {caller} due to the `component_type` argument."

        if message:
            full_message += message

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )
        super().__init__(full_message)

class WrongComponentIndicesError(ValueError):

    def __init__(self, component_indices, message=None, caller=None):

        if not caller:
            caller = caller_name(skip=3)

        full_message = f"Error in {caller} due to the `component_indices` argument."

        if message:
            full_message += message

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )
        super().__init__(full_message)

