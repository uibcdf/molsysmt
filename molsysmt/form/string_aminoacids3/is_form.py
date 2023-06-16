from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def is_form(item):

    output = False

    if type(item) is str:

        if item.startswith('aminoacids3:'):

            output = True

        else:

            from molsysmt.element.group.aminoacid import names as aminoacid_names
            from molsysmt.element.group.terminal_capping import names as terminal_capping_names

            tmp_item = item.upper()

            valid_patterns = aminoacid_names+terminal_capping_names+['HOH']

            not_found_string = ''

            while len(tmp_item):

                found = False

                for pattern in valid_patterns:
                    if tmp_item.startswith(pattern):
                        tmp_item = tmp_item[len(pattern):]
                        found = True
                        break

                if not found:
                    not_found_string += tmp_item[0]
                    tmp_item = tmp_item[1:]

            output = (len(not_found_string)/len(item) <0.05)

    return output

