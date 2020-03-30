

def parse_form_name(form):

    fields = form.split('.')

    if len(fields) == 1:

        form_lower = form.lower()

        if form_lower == 'mdtraj':
            return 'mdtraj.Trajectory'
        elif form_lower == 'openmm':
            return 'openmm.Modeller'
        elif form_lower == 'pdbfixer':
            return 'pdbfixer.PDBFixer'
        elif form_lower == 'molsysmt':
            return 'molsysmt.MolSys'
        else:
            return form

    elif len(fields)==2:

        return fields[0]+'.'+fields[1]

    else:

        return form

def digest(item, to_form=None):

    from molsysmt import get_form

    form_in = get_form(item)

    if to_form is not None:
        form_out = parse_form_name(to_form)
        return form_in, form_out
    else:
        return form_in, form_in

