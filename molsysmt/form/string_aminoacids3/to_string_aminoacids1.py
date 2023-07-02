from molsysmt._private.digestion import digest

@digest(form='string:aminoacids3')
def to_string_aminoacids1(item, group_indices='all'):

    if item.startswith('aminoacids3:'):
        item = item[12:]

    from molsysmt.element.group.amino_acid import get_1_letter_code_from_name
    from molsysmt.element.group.terminal_capping import names as terminal_capping_names

    tmp_item = ''

    chunks = [item[ii:ii+3].upper() for ii in range(0, len(item), 3)]

    for chunk in chunks:
        if chunk not in terminal_capping_names:
            tmp_item += get_1_letter_code_from_name(chunk)

    return tmp_item

