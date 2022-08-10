from ...exceptions import ArgumentError

def digest_with_blocks(with_blocks, caller=None):

    if isinstance(with_blocks, bool):
        return with_blocks

    raise ArgumentError('with_blocks', value=with_blocks, caller=caller, message=None)

