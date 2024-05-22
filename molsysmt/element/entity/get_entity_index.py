from molsysmt._private.digestion import digest

@digest()
def get_entity_index(molecular_system, element='atom', selection='all',
                     redefine_molecules=False, redefine_indices=False, syntax='MolSysMT',
                     skip_digestion=False):

    if redefine_molecules or redefine_indices:

        from ..molecule import get_molecule_name, get_molecule_type

        if redefine_molecules:

            molecule_name_from_molecules = get_molecule_name(molecular_system, element='molecule',
                    selection=selection, redefine_indices=True, syntax=syntax, skip_digestion=True)

            molecule_type_from_molecules = get_molecule_type(molecular_system, element='molecule',
                    selection=selection, redefine_indices=True, syntax=syntax, skip_digestion=True)

        else:

            molecule_name_from_molecules = get_molecule_name(molecular_system, element='molecule',
                    selection=selection, redefine_indices=False, redefine_names=False, syntax=syntax,
                                                            skip_digestion=True)

            molecule_type_from_molecules = get_molecule_type(molecular_system, element='molecule',
                    selection=selection, redefine_indices=False, redefine_types=False, syntax=syntax,
                                                            skip_digestion=True)

        count = 0
        output = []
        aux_dict = {}

        for molecule_name, molecule_type in zip(molecule_name_from_molecules, molecule_type_from_molecules):

            if molecule_type == 'water':
                if 'water' not in aux_dict:
                    aux_dict['water'] = count
                    entity_index = count
                    count += 1
                else:
                    entity_index = aux_dict['water']
            elif molecule_type == 'ion':
                if molecule_name not in aux_dict:
                    aux_dict[molecule_name] = count
                    entity_index = count
                    count += 1
                else:
                    entity_index = aux_dict[molecule_name]
            elif molecule_type == 'lipid':
                if molecule_name not in aux_dict:
                    aux_dict[molecule_name] = count
                    entity_index = count
                    count += 1
                else:
                    entity_index = aux_dict[molecule_name]
            elif molecule_type == 'small molecule':
                if molecule_name not in aux_dict:
                    aux_dict[molecule_name] = count
                    entity_index = count
                    count += 1
                else:
                    entity_index = aux_dict[molecule_name]
            elif molecule_type == 'peptide':
                if molecule_name not in aux_dict:
                    aux_dict[molecule_name] = count
                    entity_index = count
                    count += 1
                else:
                    entity_index = aux_dict[molecule_name]
            elif molecule_type == 'protein':
                if molecule_name not in aux_dict:
                    aux_dict[molecule_name] = count
                    entity_index = count
                    count += 1
                else:
                    entity_index = aux_dict[molecule_name]
            else:
                if 'unknown' in aux_dict:
                    aux_dict['unknown'] = count
                    entity_index = count
                    count += 1
                else:
                    entity_index = aux_dict['unknown']

            output.append(entity_index)

    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     entity_index=True, skip_digestion=True)

    return output

