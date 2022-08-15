from ..functions import caller_name
from ..webs import github_issues, api_doc

class NotImplementedMethodError(Exception):

    def __init__(self, method=None, arguments=None, caller=None, message=None):

        if not caller:
            caller = caller_name()

        full_message = f"This method was not implemented yet."

        if message:
            full_message += message

        super().__init__(full_message)

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )

