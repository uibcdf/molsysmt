from ..functions import caller_name
from ..webs import github_issues, api_doc

class WrongFormError(ValueError):

    def __init__(self, form, message=None, caller=None):

        if not caller:
            caller = caller_name(skip=3)

        full_message = f"Error in {caller} due to the `form` argument."

        if message:
            full_message += message

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )
        super().__init__(full_message)

class WrongToFormError(ValueError):

    def __init__(self, to_form, message=None, caller=None):

        if not caller:
            caller = caller_name(skip=3)

        full_message = f"Error in {caller} due to the `to_form` argument."

        if message:
            full_message += message

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )
        super().__init__(full_message)


class NotSupportedFormError(ValueError):
    """ Exception raised when the item's form is unknown and thereby not supported.

        This exception is raised when Sabueso does not recognize the item as a supported form.
    """

    def __init__(self, form_type, caller=None):

        if not caller:
            caller = caller_name(skip=3)

        full_message = f"The input molecular system or item has a not supported form: {form_type} "

        if message:
            full_message += message

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )
        super().__init__(full_message)

