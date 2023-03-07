from molsysmt._private.digestion import digest

def is_a_molecular_system(molecular_system):

    from . import get_form
    from ..form import _dict_modules

    if not isinstance(molecular_system, (list, tuple)):

        try:
            _ = get_form(molecular_system)
            return True
        except:
            return False

    else:

        output = True

        list_n_atoms = []

        for item in molecular_system:

            form_in = get_form(item)

            list_n_atoms.append(_dict_modules[form_in].get_n_atoms_from_system(item))

        set_n_atoms = set([ii for ii in list_n_atoms if ii is not None])

        if len(set_n_atoms)>1:
            output = False


        return output

