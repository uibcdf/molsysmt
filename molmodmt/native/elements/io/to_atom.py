
def from_bioassembly(bioassembly):

    list_atoms = []

    if type(bioassembly) in ['list','tuple']:
        bioassemblies = bioassembly
    else:
        bioassemblies = list(bioassembly)

    for tmp_bioassembly in bioassemblies:
        for tmp_atom in tmp_bioassembly.atom:
            list_atoms.append(tmp_atom)

    return list_atoms

