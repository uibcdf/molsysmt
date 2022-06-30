from molsysmt.attribute.attributes import attribute_synonyms, attributes
from ..exceptions import WrongGetArgumentError


def digest_argument(argument, element):
    """ Helper function to check the names of keyword
        arguments passed to get function.

        Parameters
        ----------
        argument : str
            Name of the keyword argument.

        element: str
            The name of an element.

        Returns
        -------
        str
            The digested name of the keyword argument.
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
