from .is_string_aminoacids3 import is_string_aminoacids3
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_string_aminoacids1(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_string_aminoacids3(item)
        except:
            raise WrongFormError('string:aminoacids3')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    if item.startswith('aminoacids3:'):
        item = item[12:]

    from molsysmt.element.group.aminoacid import get_1letter_code_from_name
    from molsysmt.element.group.terminal_capping import names as terminal_capping_names

    tmp_item = ''

    chunks = [item[ii:ii+3].upper() for ii in range(0, len(item), 3)]

    for chunk in chunks:
        if chunk not in terminal_capping_names:
            tmp_item += get_1letter_code_from_name(chunk)

    return tmp_item

