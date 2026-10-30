import os

import numpy as np
import pandas as pd

from molsysmt._private.variables import is_all


def _read_strings(dataset):
    """Reading legacy text or numeric datasets as strings."""

    if dataset.dtype.kind in {"O", "S", "U"}:
        return dataset.asstr()[:]
    return dataset[:].astype(str)


def _read_indices(dataset):
    """Restore unknown legacy parent memberships from their negative sentinel."""
    values = pd.array(dataset[:], dtype="Int64")
    values[values < 0] = pd.NA
    return values


def read_native(item, atom_indices="all", skip_digestion=False):
    """
    Converting from molsysmt.H5MSMFileHandler to molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler.to_molsysmt_H5MSMFileHandler import (
        to_molsysmt_H5MSMFileHandler,
    )
    from molsysmt.native import MolSys

    if isinstance(item, (str, os.PathLike)):
        item = to_molsysmt_H5MSMFileHandler(str(item), skip_digestion=True)
        opened_here = True
    else:
        opened_here = False

    topology_ds = item.file["topology"]
    format_version = item.format_version

    native = MolSys(n_atoms=len(topology_ds["atoms"]["atom_id"]))

    tmp_item = native.topology

    # Atoms
    tmp_item.atoms["atom_id"] = _read_strings(topology_ds["atoms"]["atom_id"])
    tmp_item.atoms["atom_type"] = _read_strings(topology_ds["atoms"]["atom_type"])
    tmp_item.atoms["atom_name"] = _read_strings(topology_ds["atoms"]["atom_name"])
    if "isotope" in topology_ds["atoms"]:
        isotope = topology_ds["atoms"]["isotope"][:]
        tmp_item.atoms["isotope"] = pd.array(
            [pd.NA if value == 0 else int(value) for value in isotope],
            dtype="UInt16",
        )
    tmp_item.atoms["group_index"] = _read_indices(topology_ds["atoms"]["group_index"])
    if format_version == "0.3":
        component_indices = topology_ds["atoms"]["component_index"][:].astype("int64")
        native.chemical_states._set_component_indices(
            [pd.NA if value < 0 else value for value in component_indices]
        )
    tmp_item.atoms["chain_index"] = _read_indices(topology_ds["atoms"]["chain_index"])

    # Groups
    tmp_item.groups["group_id"] = _read_strings(topology_ds["groups"]["group_id"])
    tmp_item.groups["group_name"] = _read_strings(topology_ds["groups"]["group_name"])
    tmp_item.groups["group_type"] = _read_strings(topology_ds["groups"]["group_type"])
    tmp_item.groups["molecule_index"] = _read_indices(
        topology_ds["groups"]["molecule_index"]
    )

    # Molecules
    tmp_item.molecules["molecule_id"] = _read_strings(
        topology_ds["molecules"]["molecule_id"]
    )
    tmp_item.molecules["molecule_name"] = _read_strings(
        topology_ds["molecules"]["molecule_name"]
    )
    tmp_item.molecules["molecule_type"] = _read_strings(
        topology_ds["molecules"]["molecule_type"]
    )
    tmp_item.molecules["entity_index"] = _read_indices(
        topology_ds["molecules"]["entity_index"]
    )

    # Entities
    tmp_item.entities["entity_id"] = _read_strings(topology_ds["entities"]["entity_id"])
    tmp_item.entities["entity_name"] = _read_strings(
        topology_ds["entities"]["entity_name"]
    )
    tmp_item.entities["entity_type"] = _read_strings(
        topology_ds["entities"]["entity_type"]
    )

    # Components in 0.3 belong to the migrated reference state. In 0.4 they
    # are loaded together with every chemical state below.
    if format_version == "0.3":
        native.chemical_states._resolve_chemical_state().components["component_id"] = (
            _read_strings(topology_ds["components"]["component_id"])
        )
        native.chemical_states._resolve_chemical_state().components[
            "component_name"
        ] = _read_strings(topology_ds["components"]["component_name"])
        native.chemical_states._resolve_chemical_state().components[
            "component_type"
        ] = _read_strings(topology_ds["components"]["component_type"])

    # Chains
    tmp_item.chains["chain_id"] = _read_strings(topology_ds["chains"]["chain_id"])
    tmp_item.chains["chain_name"] = _read_strings(topology_ds["chains"]["chain_name"])
    tmp_item.chains["chain_type"] = _read_strings(topology_ds["chains"]["chain_type"])

    if format_version == "0.3":
        atom1_index = topology_ds["bonds"]["atom1_index"][:].astype("int64")
        atom2_index = topology_ds["bonds"]["atom2_index"][:].astype("int64")
        bond_orders = None
        bond_types = None
        if topology_ds["bonds"]["order"].size:
            values = topology_ds["bonds"]["order"].asstr()[:]
            bond_orders = [pd.NA if value == "<NA>" else value for value in values]
        if topology_ds["bonds"]["type"].size:
            values = topology_ds["bonds"]["type"].asstr()[:]
            bond_types = [pd.NA if value == "<NA>" else value for value in values]
        native.chemical_states._append_chemical_state_bonds(
            np.column_stack((atom1_index, atom2_index)),
            orders=bond_orders,
            types=bond_types,
            sort=False,
        )
        state = native.chemical_states._resolve_chemical_state()
        state.connectivity_completeness = "complete"
        state.component_completeness = (
            "partial"
            if native.chemical_states._get_component_indices().isna().any()
            else "complete"
        )
        state.component_evidence = "unknown"
    else:
        from molsysmt.form._h5msm_chemical_states import (
            read_chemical_states,
        )

        states, reference_index = read_chemical_states(topology_ds, tmp_item.n_atoms)
        native.chemical_states._replace_states(states, reference_index)

    from molsysmt.native._legacy_molecule_membership import restore

    restore(native.topology, native.chemical_states)

    if not is_all(atom_indices):
        native = native.extract(atom_indices=atom_indices, skip_digestion=True)

    if opened_here:
        item.close()

    return native
