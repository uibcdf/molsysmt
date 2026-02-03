from ...exceptions import ArgumentError

functions_with_boolean = (
        'merge.merge',
        'add.add',
        'add_missing_terminal_cappings.add_missing_terminal_cappings'
        )


def digest_keep_ids(keep_ids, caller=None):

    if caller.endswith(functions_with_boolean):
        if isinstance(keep_ids, bool):
            return keep_ids

    raise ArgumentError('keep_ids', value=keep_ids, caller=caller, message=None)
