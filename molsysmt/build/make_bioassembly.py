from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_iterable_of_iterables
import numpy as np
from molsysmt import pyunitwizard as puw

@digest()
def make_bioassembly(molecular_system, bioassembly=None, structure_indices=0, to_form=None, skip_digestion=False):
    """
    To be written soon...
    """

    from molsysmt.basic import extract, merge, get, copy
    from molsysmt.structure import rotate, translate

    if bioassembly is None:

        aux_bioassemblies = get(molecular_system, bioassembly=True)
        bioassembly = list(aux_bioassemblies.keys())[0]
        bioassembly = aux_bioassemblies[bioassembly]

    elif isinstance(bioassembly, str):

        aux_bioassemblies = get(molecular_system, bioassembly=True)
        bioassembly = aux_bioassemblies[bioassembly]

    aux_rotations = []
    for rotation in bioassembly['rotations']:
        rotation = rotation[np.newaxis,np.newaxis,:,:]
        aux_rotations.append(rotation)

    aux_translations = []
    for translation in bioassembly['translations']:
        value, unit = puw.get_value_and_unit(translation)
        translation = puw.quantity(value[np.newaxis, np.newaxis, :], unit, standardized=True)
        aux_translations.append(translation)

    units = []

    if _all_chains_equal(bioassembly):

        chains = bioassembly['chain_indices'][0]

        subsystem = extract(molecular_system, structure_indices=[0], selection='chain_index in @chains',
                            syntax='MolSysMT', skip_digestion=True)

        for rotation, translation in zip(aux_rotations, aux_translations):

            unit = copy(subsystem, skip_digestion=True)
            unit = rotate(unit, rotation=rotation, skip_digestion=True)
            unit = translate(unit, translation=translation, skip_digestion=True)

            units.append(unit)

    else:

        if not is_iterable_of_iterables(bioassembly['chain_indices']):

            chains = bioassembly['chain_indices']
            subsystem = extract(molecular_system, structure_indices=[0], selection='chain_index in @chains',
                                syntax='MolSysMT', skip_digestion=True)

            for rotation, translation in zip(aux_rotations, aux_translations):

                unit = copy(subsystem, skip_digestion=True)
                unit = rotate(unit, rotation=rotation, skip_digestion=True)
                unit = translate(unit, translation=translation, skip_digestion=True)
            
                units.append(unit)

        else:

            raise NotImplementedError

    output = merge(units, to_form=to_form, skip_digestion=True)

    return output

def _all_chains_equal(bioassembly):

    output = True

    first_chains = bioassembly['chain_indices'][0]

    for chains in bioassembly['chain_indices']:
        if not np.all(chains==first_chains):
            output = False
            break

    return output
