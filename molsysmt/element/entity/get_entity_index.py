from molsysmt._private.arg_digestion import arg_digest
import numpy as np

@arg_digest()
def get_entity_index(molecular_system, element='entity', selection='all',
                     redefine_indices=False, syntax='MolSysMT',
                     skip_digestion=False):

    if redefine_indices:

        from ..molecule import get_molecule_name, get_molecule_type, get_molecule_index

        molecule_index_from_atoms = get_molecule_index(molecular_system, element='atom',
                selection=selection, redefine_indices=True, syntax=syntax, skip_digestion=True)

        molecule_name_from_molecules = get_molecule_name(molecular_system, element='molecule',
                selection='all', redefine_indices=True, redefine_names=True,
                syntax=syntax, skip_digestion=True)

        molecule_type_from_molecules = get_molecule_type(molecular_system, element='molecule',
                selection='all', redefine_indices=True, redefine_types=True,
                syntax=syntax, skip_digestion=True)

        count = 0
        molecule_to_entity = []
        aux_dict = {}

        for molecule_name, molecule_type in zip(molecule_name_from_molecules, molecule_type_from_molecules):

            if molecule_type == 'water':
                key = 'water'
            else:
                key = molecule_name

            if key not in aux_dict:
                aux_dict[key] = count
                entity_index = count
                count += 1
            else:
                entity_index = aux_dict[key]

            molecule_to_entity.append(entity_index)

        match element:
            case 'atom':
                output=[molecule_to_entity[ii] for ii in molecule_index_from_atoms]
            case 'molecule':
                output=molecule_to_entity
            case 'entity':
                n_entities = len(aux_dict)
                output=list(range(n_entities))
            case _:
                raise ValueError(f"Element '{element}' is not supported.")

    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     entity_index=True, skip_digestion=True)

    return output
