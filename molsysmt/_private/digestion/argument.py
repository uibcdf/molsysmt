from molsysmt.attribute.attributes import attribute_synonyms, attributes
from ..exceptions import WrongGetArgumentError


def digest_argument(argument, element):
    """ Helper function to check keyword arguments passed to get function.
    """
    output_argument = argument.lower()
    if output_argument in ['index', 'indices', 'name', 'names', 'id', 'ids', 'type', 'types', 'order']:
        output_argument = '_'.join([element, output_argument])
    if output_argument in attribute_synonyms:
        output_argument = attribute_synonyms[output_argument]
    if output_argument in attributes:
        return output_argument
    else:
        raise WrongGetArgumentError(argument)
