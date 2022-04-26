class MolecularSystemNeededError(ValueError):
    def __init__(self, message=None):
        if message is None:
            message = (
                    f"The method \"{caller_name}\" works over a molecular system. "
                    f"Either no molecular system or multiple systems were provided."
                    f"Check {api_doc} for more information. "
                    f"Write a new issue in {__github_issues_web__} asking for its implementation."
                    )

        super().__init__(message)


