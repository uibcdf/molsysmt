
def parse_form_name(form):

    if form in ['mdtraj','MDTraj']:
        return 'mdtraj.Trajectory'
    elif form in ['openmm','OpenMM']:
        return 'openmm.Modeller'
    elif form  in ['pdbfixer', 'PDBFixer']:
        return 'pdbfixer.PDBFixer'
    else:
        return form

def digest_forms(item, to_form=None):

    from molmodmt import get_form

    form_in = get_form(item)

    if to_form is not None:
        form_out = parse_form_name(to_form)
        return form_in, form_out
    else:
        return form_in, form_in

