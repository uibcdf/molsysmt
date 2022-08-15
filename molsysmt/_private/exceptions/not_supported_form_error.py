from ..functions import caller_name
from ..webs import github_issues, api_doc

class NotSupportedFormError(Exception):

    def __init__(self, form, caller=None, message=None):

        if not caller:
            caller = caller_name()

        full_message = f"The form {form} used in {caller} is not supported by MolSysMT."

        if message:
            full_message += message

        super().__init__(full_message)

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )

