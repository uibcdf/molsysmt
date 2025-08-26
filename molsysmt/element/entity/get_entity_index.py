from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_entity_index(molecular_system, element='atom', selection='all',
                     redefine_indices=False, syntax='MolSysMT',
                     skip_digestion=False):

    if redefine_indices:

        from ..molecule import get_molecule_name, get_molecule_type, get_molecule_index

        molecule_index_from_atoms = get_molecule_index(molecular_system, element='atom',
                selection=selection, redefine_indices=False, syntax=syntax, skip_digestion=True)

        molecule_name_from_molecules = get_molecule_name(molecular_system, element='molecule',
                selection='all', redefine_indices=False, syntax=syntax, skip_digestion=True)

        molecule_type_from_molecules = get_molecule_type(molecular_system, element='molecule',
                selection='all', redefine_indices=False, syntax=syntax, skip_digestion=True)

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
                    entity_index = aux_dict['unknown']
                else:
                    aux_dict['unknown'] = count
                    entity_index = count
                    count += 1

            output.append(entity_index)

        match element:
            case 'atom':
                output=[output[ii] for ii in molecule_index_from_atoms]
            case 'molecule':
                output=output
            case 'entity':
                output=np.unique(output).tolist()
            case _:
                raise ValueError(f"Element '{element}' is not supported.")

    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     entity_index=True, skip_digestion=True)

    return output


#molecule_names = self.molecules['molecule_name'].to_numpy()
#molecule_types = self.molecules['molecule_type'].to_numpy()
#
#count = 0
#entity_indices = []
#aux_dict = {}
#
#for molecule_name, molecule_type in zip(molecule_names, molecule_types):
#    if molecule_type == 'water':
#        if 'water' not in aux_dict:
#            aux_dict['water'] = count
#            entity_index = count
#            count += 1
#        else:
#            entity_index = aux_dict['water']
#    elif molecule_type == 'ion':
#        if molecule_name not in aux_dict:
#            aux_dict[molecule_name] = count
#            entity_index = count
#            count += 1
#        else:
#            entity_index = aux_dict[molecule_name]
#    elif molecule_type == 'lipid':
#        if molecule_name not in aux_dict:
#            aux_dict[molecule_name] = count
#            entity_index = count
#            count += 1
#        else:
#            entity_index = aux_dict[molecule_name]
#    elif molecule_type == 'small molecule':
#        if molecule_name not in aux_dict:
#            aux_dict[molecule_name] = count
#            entity_index = count
#            count += 1
#        else:
#            entity_index = aux_dict[molecule_name]
#    elif molecule_type == 'saccharide':
#        if molecule_name not in aux_dict:
#            aux_dict[molecule_name] = count
#            entity_index = count
#            count += 1
#        else:
#            entity_index = aux_dict[molecule_name]
#    elif molecule_type == 'peptide':
#        if molecule_name not in aux_dict:
#            aux_dict[molecule_name] = count
#            entity_index = count
#            count += 1
#        else:
#            entity_index = aux_dict[molecule_name]
#    elif molecule_type == 'protein':
#        if molecule_name not in aux_dict:
#            aux_dict[molecule_name] = count
#            entity_index = count
#            count += 1
#        else:
#            entity_index = aux_dict[molecule_name]
#    else:
#        if 'unknown' not in aux_dict:
#            aux_dict['unknown'] = count
#            entity_index = count
#            count += 1
#        else:
#            entity_index = aux_dict['unknown']
#
#    entity_indices.append(entity_index)
#
#del molecule_names, molecule_types

