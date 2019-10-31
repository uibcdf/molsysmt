
def from_bioassembly(bioassembly):

    list_entities = []

    if type(bioassembly) in ['list','tuple']:
        bioassemblies = bioassembly
    else:
        bioassemblies = list(bioassembly)

    for tmp_bioassembly in bioassemblies:
        for tmp_entity in tmp_bioassembly.entity:
            list_entities.append(tmp_entity)

    return list_entities

