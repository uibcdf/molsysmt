"""Expanding hierarchical topology columns to atom rows without DataFrame joins."""

import numpy as np
import pandas as pd


def _integer_links(series):
    return series.to_numpy(dtype=np.int64, na_value=-1)


def _gather_series(source, links, valid, index):
    if len(source) == 0:
        return pd.Series(pd.array([pd.NA] * len(index), dtype=source.dtype), index=index)

    safe_links = np.clip(links, 0, len(source) - 1)
    output = source.iloc[safe_links].reset_index(drop=True)
    output.index = index
    if not np.all(valid):
        output.loc[~valid] = pd.NA
    return output


def _add_gathered_columns(output, table, columns, links, valid, gathered_dtypes):
    for column in columns:
        gathered = _gather_series(table[column], links, valid, output.index)
        if column in output:
            output[column] = output[column].where(~output[column].isna(), gathered)
        else:
            output[column] = gathered
            gathered_dtypes[column] = table[column].dtype


def expand_atom_dataframe(
    topology,
    *,
    atom_columns=(),
    group_columns=(),
    component_columns=(),
    molecule_columns=(),
    entity_columns=(),
    chain_columns=(),
):
    """Gather requested hierarchy columns into an atom-indexed DataFrame.

    Invalid hierarchy links are excluded when the corresponding hierarchy
    level is requested, matching the inner-join behavior of the former merge
    pipeline.
    """

    requested_atom_columns = list(atom_columns)
    needs_component_index = 'component_index' in requested_atom_columns
    stable_atom_columns = [column for column in requested_atom_columns if column != 'component_index']
    output = topology.atoms[stable_atom_columns].copy()
    if needs_component_index:
        output['component_index'] = topology._get_component_indices().copy()
        output = output[requested_atom_columns]
    n_atoms = len(topology.atoms)
    required = np.ones(n_atoms, dtype=bool)
    gathered_dtypes = {}

    group_links = None
    group_valid = None
    if group_columns or molecule_columns or entity_columns:
        group_links = _integer_links(topology.atoms['group_index'])
        group_valid = (group_links >= 0) & (group_links < len(topology.groups))
        required &= group_valid
        if group_columns:
            _add_gathered_columns(
                output,
                topology.groups,
                group_columns,
                group_links,
                group_valid,
                gathered_dtypes,
            )

    molecule_links = None
    molecule_valid = None
    if molecule_columns or entity_columns:
        molecule_links = np.full(n_atoms, -1, dtype=np.int64)
        if len(topology.groups):
            safe_groups = np.clip(group_links, 0, len(topology.groups) - 1)
            molecule_links[group_valid] = _integer_links(
                topology.groups['molecule_index'].iloc[safe_groups[group_valid]]
            )
        molecule_valid = group_valid & (molecule_links >= 0) & (molecule_links < len(topology.molecules))
        required &= molecule_valid
        if molecule_columns:
            _add_gathered_columns(
                output,
                topology.molecules,
                molecule_columns,
                molecule_links,
                molecule_valid,
                gathered_dtypes,
            )

    if entity_columns:
        entity_links = np.full(n_atoms, -1, dtype=np.int64)
        if len(topology.molecules):
            safe_molecules = np.clip(molecule_links, 0, len(topology.molecules) - 1)
            entity_links[molecule_valid] = _integer_links(
                topology.molecules['entity_index'].iloc[safe_molecules[molecule_valid]]
            )
        entity_valid = molecule_valid & (entity_links >= 0) & (entity_links < len(topology.entities))
        required &= entity_valid
        _add_gathered_columns(
            output,
            topology.entities,
            entity_columns,
            entity_links,
            entity_valid,
            gathered_dtypes,
        )

    if component_columns:
        component_links = _integer_links(topology._get_component_indices())
        component_valid = (component_links >= 0) & (component_links < len(topology.components))
        required &= component_valid
        _add_gathered_columns(
            output,
            topology.components,
            component_columns,
            component_links,
            component_valid,
            gathered_dtypes,
        )

    if chain_columns:
        chain_links = _integer_links(topology.atoms['chain_index'])
        chain_valid = (chain_links >= 0) & (chain_links < len(topology.chains))
        required &= chain_valid
        _add_gathered_columns(
            output,
            topology.chains,
            chain_columns,
            chain_links,
            chain_valid,
            gathered_dtypes,
        )

    output = output.loc[required]
    for column, dtype in gathered_dtypes.items():
        output[column] = output[column].astype(dtype)
    return output
