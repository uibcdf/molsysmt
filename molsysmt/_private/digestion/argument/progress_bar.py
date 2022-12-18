from molsysmt._private.exceptions import ArgumentError

def digest_progress_bar(progress_bar, caller=None):

    if isinstance(progress_bar, bool):
        return progress_bar

    raise ArgumentError('progress_bar', value=progress_bar, caller=caller, message=None)

