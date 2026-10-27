"""Representing missing native hierarchy only in an MDTraj conversion target."""

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native._topology_infer import molecule_indices_from_atoms


def target_residues_for_atoms(source, target):
    """Preserve declared parents and supply documented external-only placeholders."""
    groups = source.atoms["group_index"].to_numpy(dtype=np.int64, na_value=-1)
    chains = source.atoms["chain_index"].to_numpy(dtype=np.int64, na_value=-1)
    if np.any((groups < -1) | (groups >= source.n_groups)) or np.any(
        (chains < -1) | (chains >= source.n_chains)
    ):
        raise StructuralInconsistencyError(
            caller="molsysmt.form.molsysmt_Topology.to_mdtraj_Topology",
            reason="Native group/chain membership references an undefined parent.",
        )
    group_chains = np.full(source.n_groups, -1, dtype=np.int64)
    for group, chain in zip(groups, chains):
        if group >= 0 and chain >= 0:
            if group_chains[group] >= 0 and group_chains[group] != chain:
                raise StructuralInconsistencyError(
                    caller="molsysmt.form.molsysmt_Topology.to_mdtraj_Topology",
                    reason="MDTraj cannot represent one native group across multiple chains.",
                )
            group_chains[group] = chain

    target_chains = [
        target.add_chain(chain_id=str(row.chain_id))
        for row in source.chains.itertuples(index=False)
    ]
    fallback_chain = None

    def chain_for(index):
        nonlocal fallback_chain
        if index >= 0:
            return target_chains[index]
        if fallback_chain is None:
            fallback_chain = target.add_chain()
        return fallback_chain

    declared_groups = [
        target.add_residue(
            row.group_name if pd.notna(row.group_name) else "UNL",
            chain_for(group_chains[row.Index]),
            resSeq=str(row.group_id) if pd.notna(row.group_id) else None,
        )
        for row in source.groups.itertuples(index=True)
    ]
    molecules = molecule_indices_from_atoms(source)
    placeholders = {}
    output = []
    for atom, (group, chain) in enumerate(zip(groups, chains)):
        if group >= 0:
            output.append(declared_groups[group])
        else:
            # No source group identity is implied. Known molecules get one
            # placeholder per target chain; atoms without one stay separate.
            owner = (
                ("molecule", int(molecules[atom]))
                if molecules[atom] >= 0
                else ("atom", atom)
            )
            key = (owner, int(chain))
            if key not in placeholders:
                placeholders[key] = target.add_residue("UNL", chain_for(chain))
            output.append(placeholders[key])
    return output
