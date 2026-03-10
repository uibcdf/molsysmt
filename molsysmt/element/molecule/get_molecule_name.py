from molsysmt._private.arg_digestion import arg_digest
import numpy as np


@arg_digest()
def get_molecule_name(molecular_system, element='molecule', selection='all', redefine_indices=False,
                       redefine_names=False, syntax='MolSysMT', skip_digestion=False):
    """Returning molecule names for a molecular system.

    Notes
    -----
    Explicit names are preserved when available. If names are redefined,
    molecule names follow the canonical local fallback rules; in particular,
    when molecules fall back to components, `molecule_name` falls back to
    `component_name`.
    """

    if isinstance(selection, str) and selection == 'all':
        from molsysmt.native import MolSys, Topology
        from molsysmt.native._hierarchy import project_molecule_name_from_topology

        if isinstance(molecular_system, Topology):
            return project_molecule_name_from_topology(
                molecular_system,
                element=element,
                redefine_indices=redefine_indices,
                redefine_names=redefine_names,
            )
        if isinstance(molecular_system, MolSys):
            return project_molecule_name_from_topology(
                molecular_system.topology,
                element=element,
                redefine_indices=redefine_indices,
                redefine_names=redefine_names,
            )

    if redefine_indices or redefine_names:

        from ..component import get_component_name, get_component_index

        component_names_from_component = get_component_name(molecular_system, element='component',
                            selection='all', redefine_names=True, syntax='MolSysMT')

        molecule_names_from_component = component_names_from_component

        if element == 'atom':

            component_indices_from_atom = get_component_index(molecular_system, element='atom',
                    selection=selection, redefine_indices=True, syntax=syntax)

            output = [molecule_names_from_component[ii] for ii in component_indices_from_atom]

        elif element == 'group':

            component_indices_from_group = get_component_index(molecular_system, element='group',
                    selection=selection, redefine_indices=True, syntax=syntax)

            output = [molecule_names_from_component[ii] for ii in component_indices_from_group]

        elif element == 'component':

            component_indices_from_component = get_component_index(molecular_system,
                    element='component', selection=selection, redefine_indices=True,
                    syntax=syntax)

            output = [molecule_names_from_component[ii] for ii in component_indices_from_component]

        elif element == 'molecule':

            from molsysmt.basic import get
            n_molecules = get(molecular_system, element='system', n_molecules=True, skip_digestion=True)
            output = [molecule_names_from_component[ii] for ii in range(n_molecules)]

        elif element == 'entity':

            component_indices_from_entity = get_component_index(molecular_system,
                    element='entity', selection=selection, redefine_indices=True,
                    syntax=syntax)

            output = []
            for aux in component_indices_from_entity:
                output.append([molecule_names_from_component[ii] for ii in aux])

        else:

            raise NotImplementedError

    else:

        from molsysmt.basic import get

        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     molecule_name=True)

    return output
