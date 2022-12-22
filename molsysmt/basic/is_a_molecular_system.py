from molsysmt._private.digestion import digest

@digest()
def is_a_molecular_system(items):

    from . import get_form, get
    from molsysmt.api_forms import dict_attributes

    if isinstance(items, (list, tuple)):
        for item in items:
            if isinstance(item, (list, tuple)):
                return False

    output = True

    if not isinstance(items, (list, tuple)):
        items=[items]

    if len(items)>1:

        list_n_atoms = []
        list_n_groups = []
        list_forms = []

        for item in items:
            tmp_form = get_form(item)
            tmp_n_atoms, tmp_n_groups = get(item, element='system', n_atoms=True, n_groups=True, digest=False)
            list_forms.append(tmp_form)
            list_n_atoms.append(tmp_n_atoms)
            list_n_groups.append(tmp_n_groups)

        set_n_atoms = set([ii for ii in list_n_atoms if ii is not None])
        if len(set_n_atoms)>1:
            output = False

        if output:

            set_n_groups = set([ii for ii in list_n_groups if ii is not None])
            if len(set_n_groups)>1:
                output = False

    if output:

        if isinstance(items, (list, tuple)):

            if len(items)>1:

                with_atoms_and_coordinates=0
                for item in items:
                    form_in = get_form(item)
                    has_atoms = dict_attributes[form_in]["atom_index"]
                    has_coordinates = dict_attributes[form_in]["coordinates"]
                    if has_atoms and has_coordinates:
                        with_atoms_and_coordinates+=1

                if with_atoms_and_coordinates>1:
                    output = False

    return output

