from molsysmt._private.argdigest import arg_digest


@arg_digest()
def get_molecule_index(molecular_system, element='molecule', selection='all',
                       redefine_indices=False, syntax='MolSysMT', skip_digestion=False):
    """
    Getting 0-based molecule indices from a molecular system.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='molecule'
        Structural element level to query ('atom', 'group', 'component', 'molecule', 'chain', 'entity').
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    redefine_indices : bool, default=False
        Whether to reassign contiguous 0-based indices.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of int
        List of 0-based molecule indices.


    .. versionadded:: 1.0.0
    """

    if isinstance(selection, str) and selection == 'all':
        from molsysmt.native import MolSys, Topology
        from molsysmt.native._topology_infer import project_molecule_index_from_topology

        if isinstance(molecular_system, Topology):
            return project_molecule_index_from_topology(
                molecular_system, element=element, redefine_indices=redefine_indices
            )
        if isinstance(molecular_system, MolSys):
            return project_molecule_index_from_topology(
                molecular_system.topology, element=element, redefine_indices=redefine_indices
            )

    if redefine_indices:

        from ..component import get_component_index

        component_indices_from_component = get_component_index(molecular_system, element='component',
                            selection='all', redefine_indices=True, syntax='MolSysMT')

        molecule_indices_from_component = component_indices_from_component

        comp_to_mol = {ii: jj for ii, jj in enumerate(molecule_indices_from_component)}

        if element == 'atom':

            component_indices_from_atom = get_component_index(molecular_system, element='atom',
                    selection=selection, redefine_indices=True, syntax=syntax)

            output = [comp_to_mol.get(ii, None) for ii in component_indices_from_atom]

        elif element == 'group':

            component_indices_from_group = get_component_index(molecular_system, element='group',
                    selection=selection, redefine_indices=True, syntax=syntax)

            output = [comp_to_mol.get(ii, None) for ii in component_indices_from_group]

        elif element == 'component':

            component_indices_from_component = get_component_index(molecular_system,
                    element='component', selection=selection, redefine_indices=True,
                    syntax=syntax)

            output = [comp_to_mol.get(ii, None) for ii in component_indices_from_component]

        elif element == 'molecule':

            output = component_indices_from_component

        elif element == 'entity':

            component_indices_from_entity = get_component_index(molecular_system,
                    element='entity', selection=selection, redefine_indices=True,
                    syntax=syntax)

            output = []
            for aux in component_indices_from_entity:
                output.append([comp_to_mol.get(ii, None) for ii in aux])

        else:

            raise NotImplementedError

    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     molecule_index=True)

    return output
