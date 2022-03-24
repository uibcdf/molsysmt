from molsysmt._private.exceptions import BadCallError

arguments = [
        'all',
        'info',
        'info_no_form',
        'n_elements',
        'n_molecules',
        'n_structures',
        'form',
        ]


argument_synonyms = {
        'n_element': 'n_elements',
        'n_molecule': 'n_molecules',
        'n_frame': 'n_structures',
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

