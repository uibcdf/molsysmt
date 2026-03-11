import numpy as np

from molsysmt._private.atom_indices import complementary_atom_indices
from molsysmt._private.smonitor import ArgumentConflictError, InternalAlgorithmError


def assign_selection_to_new_chain(molecular_system, selection='all', chain_id=None, chain_name=None, syntax='MolSysMT'):
    """Assign selected atoms to a new chain in a native topology-backed system."""

    from molsysmt.basic import get, get_form, select, set
    from molsysmt.element.chain import all_chain_names
    from molsysmt._private.variables import is_all

    chain_id = str(chain_id) if chain_id is not None else None
    chain_name = str(chain_name) if chain_name is not None else None

    if is_all(selection):
        chain_id = 'A' if chain_id is None else chain_id
        chain_name = 'A' if chain_name is None else chain_name

        set(molecular_system, element='atom', selection='all', chain_index=0, skip_digestion=True)
        set(
            molecular_system,
            element='chain',
            selection='all',
            chain_id=[chain_id],
            chain_name=[chain_name],
            skip_digestion=True,
        )
        return

    atom_indices = select(molecular_system, selection=selection, syntax=syntax, skip_digestion=True)
    rest_atom_indices = complementary_atom_indices(molecular_system, atom_indices)

    former_chain_ids, former_chain_names = get(
        molecular_system,
        selection=rest_atom_indices,
        chain_id=True,
        chain_name=True,
        skip_digestion=True,
    )
    former_chain_ids = np.asarray(former_chain_ids, dtype=str)
    former_chain_names = np.asarray(former_chain_names, dtype=str)

    aux_chain_ids = sorted(np.unique(former_chain_ids).tolist())
    aux_chain_names = sorted(np.unique(former_chain_names).tolist())

    if chain_id is None:
        for value in all_chain_names:
            if value not in aux_chain_ids:
                chain_id = value
                break
        if chain_id is None:
            chain_id = str(len(aux_chain_ids))
    elif chain_id in aux_chain_ids:
        raise ArgumentConflictError(
            arg1="chain_id",
            arg2="molecular_system",
            reason=f"There is already a chain with chain_id={chain_id}.",
            caller="molsysmt.build._private.assign_selection_to_new_chain",
        )

    if chain_name is None:
        for value in all_chain_names:
            if value not in aux_chain_names:
                chain_name = value
                break
        if chain_name is None:
            raise InternalAlgorithmError(
                reason="MolSysMT run out of chain names.",
                caller="molsysmt.build._private.assign_selection_to_new_chain",
            )
    elif chain_name in aux_chain_names:
        raise ArgumentConflictError(
            arg1="chain_name",
            arg2="molecular_system",
            reason=f"There is already a chain with chain_name={chain_name}.",
            caller="molsysmt.build._private.assign_selection_to_new_chain",
        )

    all_atom_indices = np.array(atom_indices + rest_atom_indices)
    all_chain_ids = np.array([chain_id for _ in atom_indices] + former_chain_ids.tolist(), dtype=str)
    all_chain_names = np.array([chain_name for _ in atom_indices] + former_chain_names.tolist(), dtype=str)
    sorted_indices = np.argsort(all_atom_indices)
    all_atom_indices = all_atom_indices[sorted_indices]
    all_chain_ids = all_chain_ids[sorted_indices]
    all_chain_names = all_chain_names[sorted_indices]

    chain_index = -1
    chain_ids_done = []
    new_chain_indices = []
    new_chain_ids = []
    new_chain_names = []
    chain_id_to_index = {}
    for atom_index, current_chain_id, current_chain_name in zip(all_atom_indices, all_chain_ids, all_chain_names):
        if current_chain_id not in chain_ids_done:
            chain_index += 1
            chain_id_to_index[current_chain_id] = chain_index
            chain_ids_done.append(current_chain_id)
            new_chain_ids.append(str(current_chain_id))
            new_chain_names.append(str(current_chain_name))
        new_chain_indices.append(chain_id_to_index[current_chain_id])

    n_chains = chain_index + 1
    form_in = get_form(molecular_system)
    if form_in == 'molsysmt.MolSys':
        molecular_system.topology.reset_chains(n_chains=n_chains)
    elif form_in == 'molsysmt.Topology':
        molecular_system.reset_chains(n_chains=n_chains)

    set(molecular_system, element='atom', selection='all', chain_index=new_chain_indices, skip_digestion=True)
    set(
        molecular_system,
        element='chain',
        selection='all',
        chain_id=new_chain_ids,
        chain_name=new_chain_names,
        skip_digestion=True,
    )

    if form_in == 'molsysmt.MolSys':
        molecular_system.topology.rebuild_chains(
            redefine_indices=False, redefine_ids=False, redefine_types=True, redefine_names=False
        )
    elif form_in == 'molsysmt.Topology':
        molecular_system.rebuild_chains(
            redefine_indices=False, redefine_ids=False, redefine_types=True, redefine_names=False
        )
