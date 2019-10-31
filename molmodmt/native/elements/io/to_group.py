
def from_bioassembly(bioassembly):

    list_groups = []

    if type(bioassembly) in ['list','tuple']:
        bioassemblies = bioassembly
    else:
        bioassemblies = list(bioassembly)

    for tmp_bioassembly in bioassemblies:
        for tmp_group in tmp_bioassembly.group:
            list_groups.append(tmp_group)

    return list_groups

