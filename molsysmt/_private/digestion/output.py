from ..lists_and_tuples import is_list_or_tuple

def digest_output(output):

    if is_list_or_tuple(output):
        if len(output)==1:
            output = output[0]

    return output

