from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import StructuralInconsistencyError, InternalAlgorithmError, FormatError, ArgumentChoiceError


@arg_digest()
def get_entity_name(molecular_system, element='entity', selection='all', redefine_indices=False,
                    redefine_names=False, syntax='MolSysMT', skip_digestion=False):
    """
    Getting entity names from a molecular system.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='entity'
        Structural element level to query ('atom', 'group', 'component', 'molecule', 'chain', 'entity').
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    redefine_indices : bool, default=False
        Whether to reassign contiguous 0-based indices.
    redefine_names : bool, default=False
        Whether to assign normalized element names.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of str
        List of entity names.


    .. versionadded:: 1.0.0
    """

    if isinstance(selection, str) and selection == 'all':
        from molsysmt.native import MolSys, Topology
        from molsysmt.native._topology_infer import project_entity_name_from_topology

        if isinstance(molecular_system, Topology):
            return project_entity_name_from_topology(
                molecular_system,
                element=element,
                redefine_indices=redefine_indices,
                redefine_names=redefine_names,
            )
        if isinstance(molecular_system, MolSys):
            return project_entity_name_from_topology(
                molecular_system.topology,
                element=element,
                redefine_indices=redefine_indices,
                redefine_names=redefine_names,
            )

    if redefine_indices or redefine_names:

        from ..molecule import get_molecule_name, get_molecule_type, get_molecule_index

        if redefine_indices:
            redefine_names = True
            redefine_types = True
        else:
            redefine_types = False

        molecule_index_from_atoms = get_molecule_index(molecular_system, element='atom',
                selection=selection, redefine_indices=redefine_indices, syntax=syntax, skip_digestion=True)

        molecule_name_from_molecules = get_molecule_name(molecular_system, element='molecule',
                selection='all', redefine_indices=redefine_indices, redefine_names=redefine_names,
                syntax=syntax, skip_digestion=True)

        molecule_type_from_molecules = get_molecule_type(molecular_system, element='molecule',
                selection='all', redefine_indices=redefine_indices, redefine_types=redefine_types,
                syntax=syntax, skip_digestion=True)

        count = 0
        molecule_to_entity = []
        entity_names = {}
        aux_dict = {}

        for molecule_name, molecule_type in zip(molecule_name_from_molecules, molecule_type_from_molecules):

            if molecule_type == 'water':
                key = 'water'
            else:
                key = molecule_name

            if key not in aux_dict:
                aux_dict[key] = count
                entity_index = count
                entity_names[count] = key
                count += 1
            else:
                entity_index = aux_dict[key]

            molecule_to_entity.append(entity_index)

        match element:
            case 'atom':
                output=[entity_names[molecule_to_entity[ii]] for ii in molecule_index_from_atoms]
            case 'molecule':
                output=[entity_names[ii] for ii in molecule_to_entity]
            case 'entity':
                n_entities = len(entity_names)
                output=[entity_names[ii] for ii in range(n_entities)]
            case _:
                raise ArgumentChoiceError(argument='element', value=element,
                                           choices=['atom', 'group', 'component', 'molecule', 'chain', 'entity'],
                                           caller='molsysmt.element.entity.get_entity_name')

    else:

        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     entity_name=True, skip_digestion=True)

    return output
