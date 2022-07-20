from ..functions import caller_name
from ..webs import github_issues, api_doc

class WrongComparisonError(ValueError):

    def __init__(self, comparison, message=None, caller=None):

        if not caller:
            caller = caller_name(skip=3)

        full_message = f"Error in {caller} due to the `comparison` argument."

        if message:
            full_message += message

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )
        super().__init__(full_message)

