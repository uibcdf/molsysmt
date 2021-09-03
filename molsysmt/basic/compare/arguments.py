from molsysmt._private_tools.exceptions import BadCallError

arguments = [
        'all',
        'info',
        'n_elements',
        'n_molecules',
        'n_frames',
        'form',
        ]


argument_synonyms = {
        'n_element': 'n_elements',
        'n_molecule': 'n_molecules',
        'n_frame': 'n_frames',
        'forms': 'form',
}


def digest_argument(argument):

    output_argument = argument.lower()
    if output_argument in argument_synonyms:
        output_argument = argument_synonyms[output_argument]
    if output_argument in arguments:
        return output_argument
    else:
        raise BadCallError()

