import re

def is_pdb(string):

    pattern = r'((ATOM||HETATM)+\s+\d+\s+\w+\s+\w+\s+\w+\s+\d+(\s+[+-]?([0-9]+([.][0-9]*))){5})'
    n_good_lines = len(re.findall(pattern, string))
    output = (n_good_lines>0)

    return output

