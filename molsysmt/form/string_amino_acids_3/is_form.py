from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def is_form(item):

    output = False

    if type(item) is str:

        if item.startswith('amino_acids_3:'):

            output = True

        elif not ' ' in item:

            from molsysmt.element.group.amino_acid import group_names as aminoacid_names
            from molsysmt.element.group.terminal_capping import group_names as terminal_capping_names

            tmp_item = item.upper()

            valid_patterns = aminoacid_names+terminal_capping_names+['HOH']

            output = _aux_routine(tmp_item, valid_patterns)

    return output

def _aux_routine(tmp_item, valid_patterns):

    not_found_string = 0

    len_tmp_item=len(tmp_item)

    output = True
    runner = 0

    while runner<len_tmp_item:

        found = False

        for pattern in valid_patterns:
            if tmp_item[runner:(runner+len(pattern))]==pattern:
                runner += len(pattern)
                found = True
                break

        if not found:
            not_found_string += 1
            runner += 1

        if (not_found_string/len_tmp_item)>=0.05 or not_found_string>500:
            output=False
            break

    return output

