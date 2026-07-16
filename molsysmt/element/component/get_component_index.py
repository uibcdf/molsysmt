from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
import numpy as np


@arg_digest()
def get_component_index(molecular_system, element='component', selection='all', redefine_indices=False,
                        syntax='MolSysMT', skip_digestion=False):
    """Returning component indices for a molecular system.

    Notes
    -----
    This is a public form-agnostic helper. When the input is already a native
    `molsysmt.Topology` or `molsysmt.MolSys` and `selection='all'`, the
    function delegates to the native hierarchy layer instead of recomputing the
    same semantics through the generic dispatch path.
    """

    if isinstance(selection, str) and selection == 'all':
        from molsysmt.native import MolSys, Topology
        from molsysmt.native._topology_infer import project_component_index_from_topology

        if isinstance(molecular_system, Topology):
            return project_component_index_from_topology(
                molecular_system, element=element, redefine_indices=redefine_indices
            )
        if isinstance(molecular_system, MolSys):
            return project_component_index_from_topology(
                molecular_system.topology, element=element, redefine_indices=redefine_indices
            )

    if redefine_indices:

        from molsysmt.lib.topology import get_component_index_from_bonded_atom_pairs
        from molsysmt.basic import get_form

        form = get_form(molecular_system)

        if form == 'molsysmt.Topology':
            n_atoms = molecular_system.n_atoms
            bonds = molecular_system._get_chemical_state_bonds()
            if 'joins_components' in bonds.columns:
                participates = ~bonds['joins_components'].eq(False).fillna(False)
                bonds = bonds.loc[participates]
            bonded_atom_pairs = bonds[['atom1_index', 'atom2_index']].to_numpy()
        else:
            from molsysmt import get
            n_atoms, bonded_atom_pairs = get(
                molecular_system,
                element='atom',
                selection='all',
                syntax=syntax,
                n_atoms=True,
                bonded_atom_pairs=True,
                skip_digestion=True,
            )

        bonded_atom_pairs = np.asarray(bonded_atom_pairs, dtype=np.int64)
        if bonded_atom_pairs.size == 0:
            bonded_atom_pairs = np.empty((0, 2), dtype=np.int64)
        else:
            bonded_atom_pairs = bonded_atom_pairs.reshape((-1, 2))

        component_index_of_atoms = get_component_index_from_bonded_atom_pairs(
            bonded_atom_pairs, np.int64(n_atoms)
        )
        aux_n_components = int(component_index_of_atoms[-1]) + 1 if n_atoms > 0 else 0

        if element == 'atom':

            if is_all(selection):
                output = component_index_of_atoms.tolist()
            else:
                output = component_index_of_atoms[selection].tolist()

        elif element == 'group':

            if form == 'molsysmt.Topology':
                group_index_of_atoms = molecular_system.atoms['group_index'].to_numpy()
            else:
                from molsysmt import get
                group_index_of_atoms = get(molecular_system, element='atom', selection='all', syntax=syntax,
                                           group_index=True, skip_digestion=True)

            group_index, first_atom_indices = np.unique(group_index_of_atoms, return_index=True)
            output = component_index_of_atoms[first_atom_indices]
            del group_index, group_index_of_atoms

            if is_all(selection):

                output = output.tolist()

            else:

                output = output[selection].tolist()

        elif element == 'component':

            if is_all(selection):

                output = list(np.arange(aux_n_components, dtype=int))
                del component_index_of_atoms

            else:

                output = selection

        else:

            raise NotImplementedError

    else:

        from molsysmt import get

        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     component_index=True, skip_digestion=True)

    return output
