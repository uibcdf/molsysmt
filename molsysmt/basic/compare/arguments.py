from molsysmt._private_tools.exceptions import BadCallError

arguments = [
        'all',
        'molecules'
        ]


argument_synonyms = {
        'molecule': 'molecules',
}


def digest_argument(argument):

    output_argument = argument.lower()
    if output_argument in argument_synonym:
        output_argument = argument_synonym[output_argument]
    if output_argument in arguments:
        return output_argument
    else:
        raise BadCallError()

