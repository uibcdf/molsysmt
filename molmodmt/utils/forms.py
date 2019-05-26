
def parse_form_name(form):

    if form in ['mdtraj','MDTraj']:
        return 'mdtraj.Trajectory'
    elif form in ['openmm','OpenMM']:
        return 'openmm.Modeller'
    elif form  in ['pdbfixer', 'PDBFixer']:
        return 'pdbfixer.PDBFixer'
    else:
        return form
