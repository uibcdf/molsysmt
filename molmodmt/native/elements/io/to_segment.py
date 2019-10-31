
def from_bioassembly(bioassembly):

    list_segments = []

    if type(bioassembly) in ['list','tuple']:
        bioassemblies = bioassembly
    else:
        bioassemblies = list(bioassembly)

    for tmp_bioassembly in bioassemblies:
        for tmp_segment in tmp_bioassembly.segment:
            list_segments.append(tmp_segment)

    return list_segments

