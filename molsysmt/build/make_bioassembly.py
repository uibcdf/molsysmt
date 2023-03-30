from molsysmt._private.digestion import digest
import numpy as np

@digest()
def make_bioassembly(molecular_system, bioassembly, structure_indices=0, to_form=None):

    from molsysmt.basic import extract, merge, get
    from molsysmt.structure import rotate, translate

    if isinstance(bioassembly, str):
        aux_bioassemblies = get(molecular_system, bioassembly=True)
        bioassembly = aux_bioassemblies[bioassembly]

    units = []

    if _all_chains_equal(bioassembly):

        chains = bioassembly['chain_indices'][0]

        unit_0 = extract(molecular_system, structure_indices=0, selection='chain_index in @chains', syntax='MolSysMT')

        for rotation, translation in zip(bioassembly['rotations'], bioassembly['translations']):

            unit = rotate(unit_0, rotation=rotation)
            unit = translate(unit, translation=translation)

            units.append(unit)

    else:

        for chains, rotation, translation in zip(bioassembly['chain_indices'], bioassembly['rotations'], bioassembly['translations']):

            unit = extract(molecular_system, structure_indices=0, selection='chain_index in @chains', syntax='MolSysMT')
            unit = rotate(unit, rotation=rotation)
            unit = translate(unit, translation=translation)

            units.append(unit)

    output = merge(units, to_form=to_form)

    return output

def _all_chains_equal(bioassembly):

    output = True

    first_chains = bioassembly['chain_indices'][0]

    for chains in bioassembly['chain_indices']:
        if not np.all(chains==first_chains):
            output = False
            break

    return output
