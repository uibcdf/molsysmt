
def from_bioassembly(bioassembly):

    list_chains = []

    if type(bioassembly) in ['list','tuple']:
        bioassemblies = bioassembly
    else:
        bioassemblies = list(bioassembly)

    for tmp_bioassembly in bioassemblies:
        for tmp_chain in tmp_bioassembly.chain:
            list_chains.append(tmp_chain)

    return list_chains

