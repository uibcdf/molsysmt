from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import numpy as np


@arg_digest()
def get_component_index(molecular_system, element='component', selection='all', redefine_indices=False,
                        syntax='MolSysMT', skip_digestion=False):
    """
    Getting 0-based component indices from a molecular system.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='component'
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
        List of 0-based component indices.


    .. versionadded:: 1.0.0
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

        from molsysmt._private.rust_backend import get_component_index_from_bonded_atom_pairs
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
