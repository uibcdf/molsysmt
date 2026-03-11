from __future__ import annotations

import numpy as np
import pandas as pd
from smonitor import signal

from molsysmt._private.smonitor import StructuralInconsistencyError


class MolSysBuilder:
    """Building a native molecular system incrementally from declared elements."""

    @signal(tags=["native", "builder"])
    def __init__(self, molecular_system=None, skip_digestion=False):

        from .molsys import MolSys
        from .structures import Structures
        from .topology import Topology

        if molecular_system is None:
            self.topology = Topology(skip_digestion=True)
            self.structures = Structures(skip_digestion=True)
        elif isinstance(molecular_system, MolSys):
            self.topology = molecular_system.topology.copy()
            self.structures = molecular_system.structures.copy()
        else:
            raise TypeError("MolSysBuilder can only be initialized from None or molsysmt.MolSys.")

    @property
    def n_atoms(self):
        return self.topology.n_atoms

    @property
    def n_groups(self):
        return self.topology.n_groups

    @property
    def n_bonds(self):
        return self.topology.n_bonds

    @property
    def n_chains(self):
        return self.topology.n_chains

    @property
    def n_molecules(self):
        return self.topology.n_molecules

    @property
    def n_entities(self):
        return self.topology.n_entities

    @property
    def n_structures(self):
        for attribute in ("coordinates", "velocities", "box", "time", "structure_id"):
            values = getattr(self.structures, attribute)
            if values is not None:
                return len(values)
        return 0

    def copy(self):
        tmp_item = MolSysBuilder(skip_digestion=True)
        tmp_item.topology = self.topology.copy()
        tmp_item.structures = self.structures.copy()
        return tmp_item

    def _ensure_atom_editable(self):
        if (
            self.structures.coordinates is not None
            or self.structures.velocities is not None
            or self.structures.b_factor is not None
        ):
            raise StructuralInconsistencyError(
                caller="molsysmt.native.MolSysBuilder",
                reason="Atoms cannot be added after atom-dependent structural arrays have been assigned.",
            )

    @staticmethod
    def _normalize_optional_string(value, default=None):
        if value is None:
            return default
        return str(value)

    @staticmethod
    def _normalize_optional_float(value):
        if value is None:
            return pd.NA
        return value

    @staticmethod
    def _indices_array(indices):
        values = np.asarray(indices, dtype=int)
        if values.ndim != 1:
            raise ValueError("Indices must define a one-dimensional collection.")
        return values

    def _validate_existing_indices(self, indices, *, upper_bound, element_name):
        if len(indices) == 0:
            raise ValueError(f"{element_name} membership cannot be empty.")
        if np.any(indices < 0) or np.any(indices >= upper_bound):
            raise ValueError(f"{element_name} membership references undefined lower-level indices.")

    @staticmethod
    def _fill_missing_string_ids(values):
        output = values.astype("string").copy()
        for index in range(len(output)):
            if pd.isna(output.iloc[index]):
                output.iloc[index] = str(index)
        return output

    @signal(tags=["native", "builder"])
    def add_atom(self, atom_id=None, atom_name=None, atom_type=None, skip_digestion=False):

        from molsysmt.element.atom import get_atom_type_from_atom_name

        self._ensure_atom_editable()

        atom_index = self.topology.n_atoms
        self.topology.atoms.loc[atom_index, "atom_id"] = self._normalize_optional_string(atom_id, default=str(atom_index))
        atom_name = self._normalize_optional_string(atom_name, default="UNK")
        self.topology.atoms.loc[atom_index, "atom_name"] = atom_name

        if atom_type is None:
            atom_type = get_atom_type_from_atom_name(atom_name)
        self.topology.atoms.loc[atom_index, "atom_type"] = self._normalize_optional_string(atom_type, default="UNK")

        self.topology.atoms.loc[atom_index, "group_index"] = pd.NA
        self.topology.atoms.loc[atom_index, "component_index"] = pd.NA
        self.topology.atoms.loc[atom_index, "chain_index"] = pd.NA

        return atom_index

    @signal(tags=["native", "builder"])
    def add_group(self, atom_indices, group_id=None, group_name=None, group_type=None, skip_digestion=False):

        atom_indices = self._indices_array(atom_indices)
        self._validate_existing_indices(atom_indices, upper_bound=self.topology.n_atoms, element_name="Group")

        current_group_index = self.topology.atoms.loc[atom_indices, "group_index"]
        if current_group_index.notna().any():
            raise ValueError("Atoms already assigned to a group cannot be reassigned.")

        group_index = self.topology.n_groups
        self.topology.groups.loc[group_index, "group_id"] = self._normalize_optional_string(group_id, default=str(group_index))
        self.topology.groups.loc[group_index, "group_name"] = self._normalize_optional_string(group_name, default="UNK")
        if group_type is None:
            self.topology.groups.loc[group_index, "group_type"] = pd.NA
        else:
            self.topology.groups.loc[group_index, "group_type"] = str(group_type)
        self.topology.groups.loc[group_index, "molecule_index"] = pd.NA
        self.topology.atoms.loc[atom_indices, "group_index"] = int(group_index)

        return group_index

    @signal(tags=["native", "builder"])
    def add_bond(self, atom_index_1, atom_index_2, bond_order=None, bond_type=None, skip_digestion=False):

        atom_indices = np.asarray([atom_index_1, atom_index_2], dtype=int)
        self._validate_existing_indices(atom_indices, upper_bound=self.topology.n_atoms, element_name="Bond")

        bond_index = self.topology.n_bonds
        self.topology.bonds.loc[bond_index, "atom1_index"] = int(atom_index_1)
        self.topology.bonds.loc[bond_index, "atom2_index"] = int(atom_index_2)
        self.topology.bonds.loc[bond_index, "order"] = self._normalize_optional_string(bond_order, default=pd.NA)
        self.topology.bonds.loc[bond_index, "type"] = self._normalize_optional_string(bond_type, default=pd.NA)
        self.topology.bonds._sort_bonds()
        self.topology.bonds.reset_index(drop=True, inplace=True)

        return bond_index

    @signal(tags=["native", "builder"])
    def add_chain(self, group_indices, chain_id=None, chain_name=None, chain_type=None, skip_digestion=False):

        group_indices = self._indices_array(group_indices)
        self._validate_existing_indices(group_indices, upper_bound=self.topology.n_groups, element_name="Chain")

        current_chain_index = self.topology.groups.get("chain_index", pd.Series(dtype="Int64"))
        if len(current_chain_index) and current_chain_index.iloc[group_indices].notna().any():
            raise ValueError("Groups already assigned to a chain cannot be reassigned.")

        chain_index = self.topology.n_chains
        self.topology.chains.loc[chain_index, "chain_id"] = self._normalize_optional_string(chain_id, default=str(chain_index))
        self.topology.chains.loc[chain_index, "chain_name"] = self._normalize_optional_string(chain_name, default=pd.NA)
        self.topology.chains.loc[chain_index, "chain_type"] = self._normalize_optional_string(chain_type, default=pd.NA)

        if "chain_index" not in self.topology.groups.columns:
            self.topology.groups["chain_index"] = pd.Series(pd.array([pd.NA] * self.topology.n_groups, dtype="Int64"))
        self.topology.groups.loc[group_indices, "chain_index"] = int(chain_index)
        self.topology.atoms["chain_index"] = pd.Series(pd.array([pd.NA] * self.topology.n_atoms, dtype="Int64"))
        for group_index in range(self.topology.n_groups):
            if pd.isna(self.topology.groups.loc[group_index, "chain_index"]):
                continue
            atom_mask = self.topology.atoms["group_index"] == group_index
            self.topology.atoms.loc[atom_mask, "chain_index"] = int(self.topology.groups.loc[group_index, "chain_index"])

        return chain_index

    @signal(tags=["native", "builder"])
    def add_molecule(self, group_indices, molecule_id=None, molecule_name=None, molecule_type=None, skip_digestion=False):

        group_indices = self._indices_array(group_indices)
        self._validate_existing_indices(group_indices, upper_bound=self.topology.n_groups, element_name="Molecule")

        current_molecule_index = self.topology.groups.loc[group_indices, "molecule_index"]
        if current_molecule_index.notna().any():
            raise ValueError("Groups already assigned to a molecule cannot be reassigned.")

        molecule_index = self.topology.n_molecules
        self.topology.molecules.loc[molecule_index, "molecule_id"] = self._normalize_optional_string(molecule_id, default=str(molecule_index))
        self.topology.molecules.loc[molecule_index, "molecule_name"] = self._normalize_optional_string(molecule_name, default=pd.NA)
        self.topology.molecules.loc[molecule_index, "molecule_type"] = self._normalize_optional_string(molecule_type, default=pd.NA)
        self.topology.molecules.loc[molecule_index, "entity_index"] = pd.NA
        self.topology.groups.loc[group_indices, "molecule_index"] = int(molecule_index)

        return molecule_index

    @signal(tags=["native", "builder"])
    def add_entity(self, molecule_indices, entity_id=None, entity_name=None, entity_type=None, skip_digestion=False):

        molecule_indices = self._indices_array(molecule_indices)
        self._validate_existing_indices(molecule_indices, upper_bound=self.topology.n_molecules, element_name="Entity")

        current_entity_index = self.topology.molecules.loc[molecule_indices, "entity_index"]
        if current_entity_index.notna().any():
            raise ValueError("Molecules already assigned to an entity cannot be reassigned.")

        entity_index = self.topology.n_entities
        self.topology.entities.loc[entity_index, "entity_id"] = self._normalize_optional_string(entity_id, default=str(entity_index))
        self.topology.entities.loc[entity_index, "entity_name"] = self._normalize_optional_string(entity_name, default=pd.NA)
        self.topology.entities.loc[entity_index, "entity_type"] = self._normalize_optional_string(entity_type, default=pd.NA)
        self.topology.molecules.loc[molecule_indices, "entity_index"] = int(entity_index)

        return entity_index

    @signal(tags=["native", "builder"])
    def set_coordinates(self, coordinates, skip_digestion=False):
        from molsysmt import pyunitwizard as puw

        value = puw.get_value(coordinates)
        if value.ndim == 2:
            value = value[np.newaxis, :, :]
            coordinates = puw.quantity(value, puw.get_unit(coordinates))
        if value.shape[1] != self.topology.n_atoms:
            raise ValueError("Coordinates must match the current number of atoms.")
        self.structures.coordinates = coordinates

    @signal(tags=["native", "builder"])
    def set_box(self, box, skip_digestion=False):
        from molsysmt import pyunitwizard as puw

        value = puw.get_value(box)
        if value.ndim == 2:
            value = value[np.newaxis, :, :]
            box = puw.quantity(value, puw.get_unit(box))
        if self.n_structures not in (0, value.shape[0]):
            raise ValueError("Box must match the current number of structures.")
        self.structures.box = box

    @signal(tags=["native", "builder"])
    def set_time(self, time, skip_digestion=False):
        from molsysmt import pyunitwizard as puw

        value = puw.get_value(time)
        if value.ndim == 0:
            value = value[np.newaxis]
            time = puw.quantity(value, puw.get_unit(time))
        if self.n_structures not in (0, len(value)):
            raise ValueError("Time must match the current number of structures.")
        self.structures.time = time

    @signal(tags=["native", "builder"])
    def set_structure_id(self, structure_id, skip_digestion=False):

        structure_id = np.asarray(structure_id)
        if structure_id.ndim == 0:
            structure_id = structure_id.reshape((1,))
        if self.n_structures not in (0, len(structure_id)):
            raise ValueError("Structure ids must match the current number of structures.")
        self.structures.structure_id = structure_id.astype(int)

    def _ensure_group_membership(self, topology):
        orphan_atom_indices = topology.atoms.index[topology.atoms["group_index"].isna()].to_numpy(dtype=int)
        for atom_index in orphan_atom_indices:
            group_index = topology.n_groups
            topology.groups.loc[group_index, "group_id"] = str(group_index)
            topology.groups.loc[group_index, "group_name"] = "UNK"
            topology.groups.loc[group_index, "group_type"] = pd.NA
            topology.groups.loc[group_index, "molecule_index"] = pd.NA
            if "chain_index" not in topology.groups.columns:
                topology.groups["chain_index"] = pd.Series(pd.array([pd.NA] * topology.n_groups, dtype="Int64"))
            topology.atoms.loc[atom_index, "group_index"] = int(group_index)

    def _fill_chain_fallbacks(self, topology):
        from ._hierarchy import infer_chain_indices_from_topology

        if "chain_index" not in topology.groups.columns:
            topology.groups["chain_index"] = pd.Series(pd.array([pd.NA] * topology.n_groups, dtype="Int64"))
        if topology.n_groups > 0 and topology.groups["chain_index"].isna().any() and topology.n_atoms > 0:
            atom_chain_index, group_chain_index = infer_chain_indices_from_topology(topology)
            missing = topology.groups["chain_index"].isna().to_numpy()
            topology.groups.loc[missing, "chain_index"] = group_chain_index[missing].astype(int)
            if "chain_index" not in topology.atoms.columns or topology.atoms["chain_index"].isna().any():
                topology.atoms["chain_index"] = pd.Series(atom_chain_index.astype(int), dtype="Int64")
        assigned_chain_index = topology.groups["chain_index"].dropna()
        if len(assigned_chain_index) > 0:
            required_n_chains = int(assigned_chain_index.astype(int).max()) + 1
            for chain_index in range(topology.n_chains, required_n_chains):
                topology.chains.loc[chain_index, "chain_id"] = str(chain_index)
                topology.chains.loc[chain_index, "chain_name"] = pd.NA
                topology.chains.loc[chain_index, "chain_type"] = pd.NA
        if topology.n_groups == 0:
            return
        unassigned = topology.groups["chain_index"].isna()
        if unassigned.any():
            chain_index = topology.n_chains
            topology.chains.loc[chain_index, "chain_id"] = str(chain_index)
            topology.chains.loc[chain_index, "chain_name"] = pd.NA
            topology.chains.loc[chain_index, "chain_type"] = pd.NA
            topology.groups.loc[unassigned, "chain_index"] = int(chain_index)
        topology.atoms["chain_index"] = pd.Series(pd.array([pd.NA] * topology.n_atoms, dtype="Int64"))
        for group_index in range(topology.n_groups):
            atom_mask = topology.atoms["group_index"] == group_index
            topology.atoms.loc[atom_mask, "chain_index"] = int(topology.groups.loc[group_index, "chain_index"])

    def _fill_molecule_fallbacks(self, topology):
        from ._hierarchy import infer_component_indices_from_topology, infer_molecule_names_from_topology, infer_molecule_types_from_topology

        if topology.n_groups == 0:
            return
        atom_component_index, group_component_index = infer_component_indices_from_topology(topology)
        topology.atoms["component_index"] = atom_component_index.astype(int)
        topology.groups["component_index"] = group_component_index.astype(int)
        n_components = int(np.max(atom_component_index)) + 1 if len(atom_component_index) > 0 else 0
        topology.reset_components(n_components=n_components)
        topology.rebuild_components(redefine_indices=False, redefine_ids=True, redefine_types=True, redefine_names=True)

        unassigned = topology.groups["molecule_index"].isna()
        if unassigned.any():
            unassigned_components = sorted(set(topology.groups.loc[unassigned, "component_index"].astype(int).tolist()))
            component_to_molecule = {}
            for component_index in unassigned_components:
                molecule_index = topology.n_molecules
                topology.molecules.loc[molecule_index, "molecule_id"] = str(molecule_index)
                topology.molecules.loc[molecule_index, "molecule_name"] = pd.NA
                topology.molecules.loc[molecule_index, "molecule_type"] = pd.NA
                topology.molecules.loc[molecule_index, "entity_index"] = pd.NA
                component_to_molecule[component_index] = molecule_index
            for group_index in topology.groups.index[unassigned]:
                component_index = int(topology.groups.loc[group_index, "component_index"])
                topology.groups.loc[group_index, "molecule_index"] = int(component_to_molecule[component_index])

        topology.molecules["molecule_id"] = self._fill_missing_string_ids(topology.molecules["molecule_id"])
        inferred_names = infer_molecule_names_from_topology(topology)
        inferred_types = infer_molecule_types_from_topology(topology)
        for molecule_index in range(topology.n_molecules):
            if pd.isna(topology.molecules.loc[molecule_index, "molecule_name"]):
                topology.molecules.loc[molecule_index, "molecule_name"] = inferred_names[molecule_index]
            if pd.isna(topology.molecules.loc[molecule_index, "molecule_type"]):
                topology.molecules.loc[molecule_index, "molecule_type"] = inferred_types[molecule_index]

    def _fill_entity_fallbacks(self, topology):
        from ._hierarchy import infer_entity_indices_from_topology, infer_entity_names_from_topology, infer_entity_types_from_topology

        unassigned = topology.molecules["entity_index"].isna()
        if unassigned.any():
            temp_topology = topology.copy()
            temp_topology.rebuild_entities(redefine_indices=True, redefine_ids=True, redefine_names=True, redefine_types=True)
            fallback_entity_index = temp_topology.molecules.loc[unassigned, "entity_index"].to_numpy(dtype=int)
            unique_fallback = sorted(set(fallback_entity_index.tolist()))
            fallback_to_declared = {}
            for fallback_index in unique_fallback:
                entity_index = topology.n_entities
                topology.entities.loc[entity_index, "entity_id"] = str(entity_index)
                topology.entities.loc[entity_index, "entity_name"] = pd.NA
                topology.entities.loc[entity_index, "entity_type"] = pd.NA
                fallback_to_declared[fallback_index] = entity_index
            for molecule_index, tmp_entity_index in zip(topology.molecules.index[unassigned], fallback_entity_index):
                topology.molecules.loc[molecule_index, "entity_index"] = int(fallback_to_declared[int(tmp_entity_index)])

        topology.entities["entity_id"] = self._fill_missing_string_ids(topology.entities["entity_id"])
        inferred_names = infer_entity_names_from_topology(topology)
        inferred_types = infer_entity_types_from_topology(topology)
        for entity_index in range(topology.n_entities):
            if pd.isna(topology.entities.loc[entity_index, "entity_name"]):
                topology.entities.loc[entity_index, "entity_name"] = inferred_names[entity_index]
            if pd.isna(topology.entities.loc[entity_index, "entity_type"]):
                topology.entities.loc[entity_index, "entity_type"] = inferred_types[entity_index]

    def _finalize_topology(self):
        topology = self.topology.copy()
        topology._coerce_id_columns_to_string()
        if not hasattr(topology.bonds, "_sort_bonds"):
            tmp_bonds = topology.bonds.copy()
            topology.reset_bonds(n_bonds=tmp_bonds.shape[0])
            for column in tmp_bonds.columns:
                topology.bonds[column] = tmp_bonds[column].values
        topology.bonds._sort_bonds()
        self._ensure_group_membership(topology)
        topology.groups["group_id"] = self._fill_missing_string_ids(topology.groups["group_id"])
        topology.rebuild_groups(redefine_ids=False, redefine_types=True)
        self._fill_molecule_fallbacks(topology)
        self._fill_chain_fallbacks(topology)
        topology.chains["chain_id"] = self._fill_missing_string_ids(topology.chains["chain_id"])
        topology.rebuild_chains(redefine_indices=False, redefine_ids=False, redefine_names=True, redefine_types=True)
        self._fill_entity_fallbacks(topology)
        topology._coerce_id_columns_to_string()
        return topology

    def _validate_structures(self):
        n_structures = self.n_structures
        if n_structures == 0:
            return

        if self.structures.coordinates is not None and self.structures.coordinates.shape[1] != self.topology.n_atoms:
            raise StructuralInconsistencyError(
                caller="molsysmt.native.MolSysBuilder",
                reason="Coordinates do not match the declared number of atoms.",
            )

        for attribute in ("box", "time", "structure_id"):
            values = getattr(self.structures, attribute)
            if values is not None and len(values) != n_structures:
                raise StructuralInconsistencyError(
                    caller="molsysmt.native.MolSysBuilder",
                    reason=f"{attribute} does not match the declared number of structures.",
                )

    @signal(tags=["native", "builder"])
    def build(self, skip_digestion=False):

        from .molsys import MolSys

        self._validate_structures()

        output = MolSys(skip_digestion=True)
        output.topology = self._finalize_topology()
        output.structures = self.structures.copy()

        return output

    def info(self, element="system", selection="all", syntax="MolSysMT", skip_digestion=False):
        from molsysmt.basic import info as _info
        return _info(self, element=element, selection=selection, syntax=syntax, skip_digestion=True)

    def get(
        self,
        element="system",
        selection="all",
        structure_indices="all",
        mask=None,
        syntax="MolSysMT",
        get_missing_bonds=True,
        output_type="values",
        skip_digestion=False,
        **kwargs,
    ):
        from molsysmt.basic import get as _get
        return _get(
            self,
            element=element,
            selection=selection,
            structure_indices=structure_indices,
            mask=mask,
            syntax=syntax,
            get_missing_bonds=get_missing_bonds,
            output_type=output_type,
            skip_digestion=True,
            **kwargs,
        )
