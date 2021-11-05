import re

def replace_HETATM_by_ATOM_in_terminal_cappings (molecular_system):

    from molsysmt import get_form

    form_in = get_form(molecular_system)

    if form_in == 'string:pdb':

        tmp_molecular_system = re.sub(r'HETATM+(\s+\d+\s+\w+\s+(ACE||NME)+\s+\w+\s)', r'ATOM  \1', molecular_system)

    elif form_in == 'file:pdb':

        with open(molecular_system, 'r+') as f:
            text = f.read()
            out = re.sub(r'HETATM+(\s+\d+\s+\w+\s+(ACE||NME)+\s+\w+\s)', r'ATOM  \1', text)
            f.seek(0)
            f.write(out)
            f.truncate()

        tmp_molecular_system = molecular_system

    return tmp_molecular_system

