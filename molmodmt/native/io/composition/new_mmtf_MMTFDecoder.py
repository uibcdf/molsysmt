def from_mmtf_MMTFDecoder(item, atom_indices='all', frame_indices='all'):

    from molmodmt.native.composition import Composition
    from molmodmt.native import elements
    from molmodmt.utils.composition.classification as elements_classification
    import numpy as np

    tmp_item = Composition()

    id_bioassembly = 0
    for mmtf_bioassembly in mmtf.bio_assembly:

        bioassembly = elements.BioAssembly()

        bioassembly.id = id_bioassembly
        bioassembly.index = None
        bioassembly.name = mmtf_bioassembly['name']
        bioassembly.type = None

        bioassembly.mmtf_transform_list = mmtf_bioassembly['transformList']

        tmp_item.bioassembly.append(bioassembly)
