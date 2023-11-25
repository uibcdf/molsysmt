from molsysmt._private.digestion import digest


@digest()
def get_entity_index(molecular_system, element='atom', selection='all',
        redefine_molecules=False, redefine_indices=False, syntax='MolSysMT'):

    if redefine_molecules or redefine_indices:

        if redefine_molecules:

            molecule_name_from_molecules = get_molecule_name(molecular_system, element='molecule',
                    selection=selection, redefine_molecules=True, syntax=syntax)

            molecule_type_from_molecules = get_molecule_type(molecular_system, element='molecule',
                    selection=selection, redefine_molecules=True, syntax=syntax)

        else:

            molecule_name_from_molecules = get_molecule_name(molecular_system, element='molecule',
                    selection=selection, redefine_molecules=False, redefine_names=False, syntax=syntax)

            molecule_type_from_molecules = get_molecule_type(molecular_system, element='molecule',
                    selection=selection, redefine_molecules=False, redefine_types=False, syntax=syntax)

        count = 0
        entity_index_from_molecule = []
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

            


    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     entity_index=True)

    return output

def _get_entity_name_from_molecule_name
