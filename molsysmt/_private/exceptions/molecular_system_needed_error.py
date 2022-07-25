from ..functions import caller_name
from ..webs import github_issues, api_doc

class MolecularSystemNeededError(Exception):

    def __init__(self, caller=None, message=None):

        if not caller:
            caller = caller_name()

        full_message = (f"The function or method {caller} works over a molecular system. "
                       f"Either no molecular system or multiple systems were provided.")

        if message:
            full_message += message

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )

        super().__init__(full_message)

