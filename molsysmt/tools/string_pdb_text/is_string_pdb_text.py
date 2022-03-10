import re

def is_string_pdb_text(string):

    output = False

    if type(string) is str:

        pattern_1 = r'((ATOM||HETATM)+\s+\d+\s+\w+\s+\w+\s+\w+\s+\d+(\s+[+-]?([0-9]+([.][0-9]*))){5})'
        pattern_2 = r'((ATOM||HETATM)+\s+\d+\s+\w+\s+\w+\s+\w+\s+(\s+[+-]?([0-9]+([.][0-9]*))){5})'

        for pattern in [pattern_1, pattern_2]:

            n_good_lines = len(re.findall(pattern, string))
            output = (n_good_lines>0)

            if output:
                break

    return output

