from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def is_string_aminoacids3(item):

    output = False

    if type(item) is str:

        if item.startswith('aminoacids3:'):

            output = True

        else:

            from molsysmt.element.group.aminoacid import names as aminoacid_names
            from molsysmt.element.group.terminal_capping import names as terminal_capping_names

            chunks = [item[ii:ii+3].upper() for ii in range(0, len(item), 3)]

            valid_chunks = aminoacid_names+terminal_capping_names

            output = True

            for chunk in chunks:
                if chunk not in valid_chunks:
                    output = False
                    break

    return output

