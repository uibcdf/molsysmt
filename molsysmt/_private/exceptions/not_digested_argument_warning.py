from ..webs import github_issues, api_doc

class NotDigestedArgumentWarning(Warning):

    def __init__(self, argument):

        full_message = f"The {argument} argument was not digested."

        full_message += (
            f"Check {api_doc} for more information. "
            f"If you still need help, open a new issue in {github_issues}."
        )

        super().__init__(full_message)


