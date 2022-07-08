from ..lists_and_tuples import is_list_or_tuple


def digest_output(output, caller=""):
    """ If 'output is a list or tuple with a single element, it returns that
        element. If not it returns the original 'output'.
    """
    # TODO: check this function
    if is_list_or_tuple(output):
        if len(output) == 1:
            output = output[0]

    return output
