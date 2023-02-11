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

        # same n_atoms

        same_n_atoms = True

        list_n_atoms = []

        for item in items:
            tmp_n_atoms = get(item, element='system', n_atoms=True)
            list_n_atoms.append(tmp_n_atoms)

        set_n_atoms = set([ii for ii in list_n_atoms if ii is not None])
        if len(set_n_atoms)>1:
            same_n_atoms = False

        # if same_n_atoms and group_indices is an attribute of more than a single item
        # same_n_groups should be computed

        output=same_n_atoms

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

