from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_molecule_type(molecular_system, element='atom', selection='all',
        redefine_indices=False, redefine_types=False, syntax='MolSysMT',
        skip_digestion=False):

    from ..component import get_component_type
    from molsysmt.basic import get

    if redefine_indices:

        molecule_types_from_molecule = get_component_type(molecular_system, element='component', selection=selection,
                redefine_indices=True, syntax=syntax)

        if element == 'atom':
            aux = get(molecular_system, element='atom', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = np.array(molecule_types_from_molecule, dtype=object)[aux].tolist()
        elif element == 'group':
            aux = get(molecular_system, element='group', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = np.array(molecule_types_from_molecule, dtype=object)[aux].tolist()
        elif element == 'component':
            aux = get(molecular_system, element='component', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = np.array(molecule_types_from_molecule, dtype=object)[aux].tolist()
        elif element == 'molecule':
            output = molecule_types_from_molecule
        else:
            aux = get(molecular_system, element='chain', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = []
            for aux_mols_chain in aux:
                output.append([molecule_types_from_molecule[ii] for ii in aux_mols_chain])

    elif redefine_types:

        molecule_types_from_molecule = get_component_type(molecular_system, element='component', selection=selection,
                redefine_indices=False, redefine_types=False, syntax=syntax)

        if element == 'atom':
            aux = get(molecular_system, element='atom', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = np.array(molecule_types_from_molecule, dtype=object)[aux].tolist()
        elif element == 'group':
            aux = get(molecular_system, element='group', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = np.array(molecule_types_from_molecule, dtype=object)[aux].tolist()
        elif element == 'component':
            aux = get(molecular_system, element='component', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = np.array(molecule_types_from_molecule, dtype=object)[aux].tolist()
        elif element == 'molecule':
            output = molecule_types_from_molecule
        elif element == 'entity':
            aux = get(molecular_system, element='entity', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = []
            for molecules_in_entity in aux:
                output.append(np.array(molecule_types_from_molecule,
                    dtype=object)[molecules_in_entity].tolist())
        else:
            raise NotImplementedError

    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     molecule_type=True)

    return output

def _get_molecule_type_from_group_names_and_types(group_names, group_types, skip_digestion=False):

    from ..component.get_component_type import _get_component_type_from_group_names_and_types

    return _get_component_type_from_group_names_and_types(group_names, group_types)

