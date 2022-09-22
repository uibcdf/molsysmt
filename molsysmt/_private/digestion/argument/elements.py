from molsysmt._private.exceptions import ArgumentError

methods_where_bool = [
    'molsysmt.basic.compare.compare'
]

def digest_elements(elements, caller=None):

    if caller in methods_where_bool:

        if isinstance(elements, bool):
            return elements

    raise ArgumentError('elements', value=elements, caller=caller, message=None)

