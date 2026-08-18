from molsysmt._private.argdigest import arg_digest
import numpy as np
import pandas as pd

@arg_digest()
def get_molecule_type(molecular_system, element='molecule', selection='all',
        redefine_indices=False, redefine_types=False, syntax='MolSysMT',
        skip_digestion=False):
    """
    Getting molecule types from a molecular system.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to query, in any of the :ref:`supported forms <Introduction_Forms>`.
    element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity'}, default='atom'
        Structural element level at which the molecule types are returned.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection of elements to query.
    redefine_indices : bool, default=False
        Whether to recalculate molecule indices locally prior to type assignment.
    redefine_types : bool, default=False
        Whether to re-infer molecule types from constituent components.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection`.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    list of str
        List of molecule type classifications ('protein', 'dna', 'water', 'small molecule', etc.).

    .. versionadded:: 1.0.0
    """

    if isinstance(selection, str) and selection == 'all':
        from molsysmt.native import MolSys, Topology
        from molsysmt.native._topology_infer import project_molecule_type_from_topology

        if isinstance(molecular_system, Topology):
            return project_molecule_type_from_topology(
                molecular_system,
                element=element,
                redefine_indices=redefine_indices,
                redefine_types=redefine_types,
            )
        if isinstance(molecular_system, MolSys):
            return project_molecule_type_from_topology(
                molecular_system.topology,
                element=element,
                redefine_indices=redefine_indices,
                redefine_types=redefine_types,
            )

    from molsysmt.basic import get

    if redefine_indices:

        from ..component import get_component_type

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

        from . import get_molecule_index

        molecule_indices = get_molecule_index(molecular_system, element='atom',
                                              selection='all', redefine_indices=True,
                                              skip_digestion=True)

        group_index_per_atom = get(molecular_system, element='atom', selection='all', group_index=True,
                                   skip_digestion=True)

        group_names, group_types = get(molecular_system, element='group', selection='all', group_name=True,
                                       group_type=True, skip_digestion=True)

        group_names = np.array(group_names)
        group_types = np.array(group_types)

        aux_df = pd.DataFrame({'molecule_indices':molecule_indices, 'group_indices':group_index_per_atom})
        aux_dict = aux_df.groupby('molecule_indices')['group_indices'].unique().to_dict()

        molecule_types={}

        for molecule_index, group_indices in aux_dict.items():

            molecule_type = _get_molecule_type_from_group_names_and_types(group_names[group_indices],
                                                                          group_types[group_indices])

            molecule_types[molecule_index]=molecule_type

        if element == 'atom':
            aux = get(molecular_system, element='atom', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = [molecule_types.get(ii, 'unknown') for ii in aux]
        elif element == 'group':
            aux = get(molecular_system, element='group', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = [molecule_types.get(ii, 'unknown') for ii in aux]
        elif element == 'component':
            aux = get(molecular_system, element='component', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = [molecule_types.get(ii, 'unknown') for ii in aux]
        elif element == 'molecule':
            from molsysmt.basic import get as msm_get
            n_molecules = msm_get(molecular_system, element='system', n_molecules=True, skip_digestion=True)
            output = [molecule_types.get(ii, 'unknown') for ii in range(n_molecules)]
        elif element == 'chain':
            aux = get(molecular_system, element='chain', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = []
            for molecules_in_chain in aux:
                output.append([molecule_types.get(ii, 'unknown') for ii in molecules_in_chain])
        elif element == 'entity':
            aux = get(molecular_system, element='entity', selection=selection, syntax=syntax,
                      molecule_index=True)
            output = []
            for molecules_in_entity in aux:
                output.append([molecule_types.get(ii, 'unknown') for ii in molecules_in_entity])
        else:
            raise NotImplementedError

    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     molecule_type=True)

    return output


def _get_molecule_type_from_group_names_and_types(group_names, group_types):

    from ..group.nucleotide import rna_names, dna_names
    from ..group.water.water_names import water_names
    from molsysmt.configure import min_length_protein

    n_groups = len(group_types)
    first_group_type = group_types[0]
    last_group_type = group_types[-1]
    first_group_name = group_names[0]

    if first_group_type in ['water', 'ion', 'small molecule', 'lipid']:
        tmp_type = first_group_type
    elif (first_group_type == 'amino acid') or (first_group_type == 'terminal capping'):
        if first_group_type == 'terminal capping':
            n_groups -= 1
        if last_group_type == 'terminal capping':
            n_groups -= 1
        if n_groups >= min_length_protein:
            tmp_type = 'protein'
        else:
            tmp_type = 'peptide'
    elif first_group_type == 'nucleotide':
        if first_group_name in rna_names:
            tmp_type = 'rna'
        elif first_group_name in dna_names:
            tmp_type = 'dna'
    elif first_group_type == 'saccharide':
        tmp_type = 'polysaccharide'
    else:
        if first_group_name in water_names:
            tmp_type = 'water'
        else:
            tmp_type = 'unknown'

    return tmp_type
