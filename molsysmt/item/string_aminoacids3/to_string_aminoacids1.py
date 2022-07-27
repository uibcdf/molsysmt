from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_string_aminoacids1(item, group_indices='all'):

    if check:

        digest_item(item, 'string:aminoacids3')
        group_indices = digest_group_indices(group_indices)

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

