from molsysmt._private.variables import is_all
from molsysmt._private.arg_digestion import arg_digest
import numpy as np
import pandas as pd
from smonitor import signal

class MolSys:
    """Container holding native topology, structures, and molecular mechanics data."""

    @signal(tags=['native'])
    @arg_digest()
    def __init__(self, n_atoms=0, n_groups=0, n_components=0, n_molecules=0, n_entities=0, n_chains=0, n_bonds=0,
                skip_digestion=False):

        from .topology import Topology
        from .structures import Structures
        from .molecular_mechanics import MolecularMechanics

        self.topology = Topology(n_atoms=n_atoms, n_groups=n_groups, n_components=n_components,
                                 n_molecules=n_molecules, n_entities=n_entities, n_chains=n_chains,
                                 n_bonds=n_bonds, skip_digestion=True)
        self.structures = Structures(skip_digestion=True)
        self.molecular_mechanics = MolecularMechanics()
        self._structure_chemical_state_indices = None

    def __setstate__(self, state):
        """Restore a molecular system and finish coordinated legacy migration."""

        self.__dict__.update(state)
        if '_structure_chemical_state_indices' not in self.__dict__:
            legacy_indices = getattr(self.structures, '_chemical_state_indices', None)
            self._structure_chemical_state_indices = (
                None
                if legacy_indices is None
                else pd.array(
                    [
                        pd.NA if pd.isna(value) or int(value) < 0 else int(value)
                        for value in legacy_indices
                    ],
                    dtype='Int64',
                )
            )
        self.structures.__dict__.pop('_chemical_state_indices', None)
        topology_formal_charge = getattr(
            self.topology, '_legacy_formal_charge', None
        )
        mechanics_formal_charge = getattr(
            self.molecular_mechanics, '_legacy_formal_charge', None
        )
        if topology_formal_charge is not None and mechanics_formal_charge is not None:
            topology_values = np.asarray(topology_formal_charge)
            mechanics_values = np.asarray(mechanics_formal_charge)
            if topology_values.shape != mechanics_values.shape or not np.array_equal(
                topology_values, mechanics_values
            ):
                from molsysmt._private.smonitor import StructuralInconsistencyError

                raise StructuralInconsistencyError(
                    reason=(
                        'Legacy formal charge is present with conflicting values in topology '
                        'and molecular mechanics; explicit resolution is required.'
                    ),
                    caller='molsysmt.native.MolSys.__setstate__',
                )

        formal_charge = topology_formal_charge
        formal_charge_origin = 'legacy_topology'
        if formal_charge is None:
            formal_charge = mechanics_formal_charge
            formal_charge_origin = 'legacy_molecular_mechanics'
        if formal_charge is not None:
            self.topology._set_chemical_state_atom_attribute(
                'formal_charge', formal_charge
            )
            self.topology._reference_chemical_state._formal_charge_migration_origin = (
                formal_charge_origin
            )

        topology_partial_charge = getattr(
            self.topology, '_legacy_partial_charge', None
        )
        mechanics_partial_charge = getattr(
            self.molecular_mechanics, '_legacy_partial_charge', None
        )
        partial_charge = mechanics_partial_charge
        if partial_charge is None:
            partial_charge = topology_partial_charge
        if partial_charge is not None:
            self.molecular_mechanics.partial_charge = partial_charge

        for owner in (self.topology, self.molecular_mechanics):
            owner.__dict__.pop('_legacy_formal_charge', None)
            owner.__dict__.pop('_legacy_partial_charge', None)

    def _get_structure_chemical_state_indices(self, structure_indices='all', resolved=True):
        """Return explicit or implicitly resolved state indices aligned to structures."""

        n_structures = self.structures.n_structures
        if is_all(structure_indices):
            indices = np.arange(n_structures, dtype=np.int64)
        else:
            indices = np.asarray(structure_indices, dtype=np.int64)
            if indices.ndim != 1 or np.any(indices < 0) or np.any(indices >= n_structures):
                from molsysmt._private.smonitor import StructuralInconsistencyError

                raise StructuralInconsistencyError(
                    reason='Structure indices for chemical-state association are out of range.',
                    caller='molsysmt.native.MolSys',
                )

        if self._structure_chemical_state_indices is None:
            if resolved and len(self.topology._chemical_states) == 1:
                return pd.array(np.zeros(len(indices), dtype=np.int64), dtype='Int64')
            return pd.array([pd.NA] * len(indices), dtype='Int64')

        values = self._structure_chemical_state_indices[indices]
        n_states = len(self.topology._chemical_states)
        known = pd.Series(values).dropna()
        if not known.empty and ((known < 0).any() or (known >= n_states).any()):
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason='Structure-to-state association contains an invalid chemical-state index.',
                caller='molsysmt.native.MolSys',
            )
        return pd.array(values, dtype='Int64')

    def _set_structure_chemical_state_indices(self, values, structure_indices='all'):
        """Set nullable state indices for all or selected structures."""

        n_structures = self.structures.n_structures
        if is_all(structure_indices):
            indices = np.arange(n_structures, dtype=np.int64)
        else:
            indices = np.asarray(structure_indices, dtype=np.int64)
            if indices.ndim != 1 or np.any(indices < 0) or np.any(indices >= n_structures):
                from molsysmt._private.smonitor import StructuralInconsistencyError

                raise StructuralInconsistencyError(
                    reason='Structure indices for chemical-state association are out of range.',
                    caller='molsysmt.native.MolSys',
                )

        if values is None and is_all(structure_indices):
            self._structure_chemical_state_indices = None
            return

        if values is None or values is pd.NA:
            normalized = [pd.NA] * len(indices)
        elif np.isscalar(values):
            normalized = [values] * len(indices)
        else:
            normalized = list(values)
            if len(normalized) != len(indices):
                from molsysmt._private.smonitor import ArgumentLengthError

                raise ArgumentLengthError(
                    argument='structure_chemical_state_index',
                    expected=len(indices),
                    actual=len(normalized),
                    caller='molsysmt.native.MolSys',
                )

        array = pd.array(normalized, dtype='Int64')
        n_states = len(self.topology._chemical_states)
        known = pd.Series(array).dropna()
        if not known.empty and ((known < 0).any() or (known >= n_states).any()):
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason=(
                    'Structure-to-state association values must reference existing '
                    'chemical-state indices.'
                ),
                caller='molsysmt.native.MolSys',
            )

        if self._structure_chemical_state_indices is None:
            self._structure_chemical_state_indices = pd.array(
                [pd.NA] * n_structures, dtype='Int64'
            )
        self._structure_chemical_state_indices[indices] = array

    def _resolve_structure_chemical_state_index(self, structure_indices='all'):
        """Resolve one state shared by the requested structures or fail closed."""

        values = self._get_structure_chemical_state_indices(
            structure_indices=structure_indices, resolved=True
        )
        if len(values) == 0:
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason='No structures are available to resolve a chemical state.',
                caller='molsysmt.native.MolSys',
            )
        if pd.isna(values).any():
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason='At least one selected structure has no chemical-state association.',
                caller='molsysmt.native.MolSys',
            )
        unique = np.unique(np.asarray(values, dtype=np.int64))
        if len(unique) != 1:
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason=(
                    'The selected structures span multiple chemical states and cannot '
                    'resolve one state-dependent result.'
                ),
                caller='molsysmt.native.MolSys',
            )
        return int(unique[0])

    @signal(tags=['native'])
    @arg_digest()
    def extract(self, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
        """Return a copy or subset of the molecular system."""

        if is_all(atom_indices) and is_all(structure_indices):

            if copy_if_all:
                return self.copy()
            else:
                return self

        else:

            if not is_all(atom_indices):
                atom_indices = np.sort(np.asarray(atom_indices, dtype=int))

            tmp_item = MolSys()
            tmp_item.topology = self.topology.extract(atom_indices=atom_indices, copy_if_all=True, skip_digestion=True)
            tmp_item.structures = self.structures.extract(atom_indices=atom_indices,
                                                          structure_indices=structure_indices, copy_if_all=True,
                                                          skip_digestion=True)
            if (
                not is_all(atom_indices)
                and tmp_item.structures.bioassembly is not None
            ):
                selected_chain_indices = (
                    self.topology.atoms.iloc[atom_indices]["chain_index"]
                    .dropna()
                    .astype(int)
                    .unique()
                    .tolist()
                )
                chain_index_map = {
                    old_index: new_index
                    for new_index, old_index in enumerate(selected_chain_indices)
                }
                retained_assemblies = {}
                for assembly_id, assembly in tmp_item.structures.bioassembly.items():
                    chain_indices = assembly["chain_indices"]
                    if chain_indices and isinstance(chain_indices[0], (list, tuple, np.ndarray)):
                        retained_operations = [
                            operation_index
                            for operation_index, operation_chains in enumerate(chain_indices)
                            if all(
                                int(chain_index) in chain_index_map
                                for chain_index in operation_chains
                            )
                        ]
                        if not retained_operations:
                            continue
                        retained_assemblies[assembly_id] = {
                            **assembly,
                            "chain_indices": [
                                [
                                    chain_index_map[int(chain_index)]
                                    for chain_index in chain_indices[operation_index]
                                ]
                                for operation_index in retained_operations
                            ],
                            "rotations": assembly["rotations"][retained_operations],
                            "translations": assembly["translations"][retained_operations],
                        }
                    else:
                        if not all(
                            int(chain_index) in chain_index_map
                            for chain_index in chain_indices
                        ):
                            continue
                        retained_assemblies[assembly_id] = {
                            **assembly,
                            "chain_indices": [
                                chain_index_map[int(chain_index)]
                                for chain_index in chain_indices
                            ],
                        }
                tmp_item.structures.bioassembly = retained_assemblies or None
            tmp_item.molecular_mechanics = self.molecular_mechanics.copy()
            if (
                not is_all(atom_indices)
                and tmp_item.molecular_mechanics is not None
                and tmp_item.molecular_mechanics.atoms_ff is not None
            ):
                tmp_item.molecular_mechanics.atoms_ff = (
                    tmp_item.molecular_mechanics.atoms_ff
                    .iloc[atom_indices]
                    .reset_index(drop=True)
                    .copy()
                )
            if self._structure_chemical_state_indices is not None:
                if is_all(structure_indices):
                    tmp_item._structure_chemical_state_indices = (
                        self._structure_chemical_state_indices.copy()
                    )
                else:
                    tmp_item._structure_chemical_state_indices = pd.array(
                        self._structure_chemical_state_indices[structure_indices],
                        dtype='Int64',
                    )

            return tmp_item


    @signal(tags=['native'])
    @arg_digest()
    def remove(self, atom_indices=None, structure_indices=None, copy_if_None=False, skip_digestion=False):
        """Remove atoms and/or structures by index and return the resulting MolSys."""

        if (atom_indices is None) and (structure_indices is None):

            if copy_if_None:
                return self.copy()
            else:
                return self

        else:

            if atom_indices is not None:
                atom_indices_to_be_kept = np.setdiff1d(np.arange(self.topology.n_atoms), atom_indices)
            else:
                atom_indices_to_be_kept = 'all'

            if structure_indices is not None:
                structure_indices_to_be_kept = np.setdiff1d(np.arange(self.structures.n_structures), structure_indices)
            else:
                structure_indices_to_be_kept = 'all'

            tmp_item = self.extract(atom_indices=atom_indices_to_be_kept,
                                    structure_indices=structure_indices_to_be_kept, skip_digestion=True)

            return tmp_item

    @signal(tags=['native'])
    @arg_digest(form='molsysmt.MolSys')
    def add(self, item, atom_indices='all', structure_indices='all', keep_ids=True, skip_digestion=False):
        """Adding topology and atom-aligned structures from another MolSys."""

        candidate_topology = self.topology.copy()
        candidate_structures = self.structures.copy()
        candidate_topology.add(
            item.topology,
            atom_indices=atom_indices,
            keep_ids=keep_ids,
            skip_digestion=True,
        )
        candidate_structures.add(
            item.structures,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            skip_digestion=True,
        )
        self.topology = candidate_topology
        self.structures = candidate_structures

    @arg_digest(form='molsysmt.MolSys')
    def append_structures(
        self,
        item,
        atom_indices='all',
        structure_indices='all',
        attribute_policy='intersection',
        skip_digestion=False,
    ):
        """Append structures from another MolSys while aligning atom indices."""

        source_topology = item.topology.extract(
            atom_indices=atom_indices, copy_if_all=True, skip_digestion=True
        )
        if self.topology.n_atoms != source_topology.n_atoms:
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason=(
                    f'Source structures contain {source_topology.n_atoms} selected atoms, '
                    f'but the target contains {self.topology.n_atoms} atoms.'
                ),
                caller='molsysmt.native.MolSys.append_structures',
            )

        inventories_match = self.topology._chemical_state_inventory_equals(source_topology)
        target_state_indices = self._get_structure_chemical_state_indices(
            resolved=True
        )
        other = item.structures.extract(atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=True, skip_digestion=True)
        if inventories_match:
            source_state_indices = item._get_structure_chemical_state_indices(
                structure_indices=structure_indices, resolved=True
            )
        elif len(self.topology._chemical_states) == 1:
            source_state_indices = pd.array(
                np.zeros(other.n_structures, dtype=np.int64), dtype='Int64'
            )
        else:
            source_state_indices = pd.array(
                [pd.NA] * other.n_structures, dtype='Int64'
            )
        self.structures.append(
            structure_id=other.structure_id,
            time=other.time,
            coordinates=other.coordinates,
            velocities=other.velocities,
            box=other.box,
            temperature=other.temperature,
            potential_energy=other.potential_energy,
            kinetic_energy=other.kinetic_energy,
            b_factor=other.b_factor,
            alternate_location=other.alternate_location,
            occupancy=other.occupancy,
            atom_indices='all',
            structure_indices='all',
            attribute_policy=attribute_policy,
            skip_digestion=True,
        )
        if (
            len(self.topology._chemical_states) > 1
            or self._structure_chemical_state_indices is not None
            or (
                inventories_match
                and item._structure_chemical_state_indices is not None
            )
        ):
            combined = pd.array(
                list(target_state_indices) + list(source_state_indices), dtype='Int64'
            )
            self._structure_chemical_state_indices = None
            self._set_structure_chemical_state_indices(combined)

    @signal(tags=['native'])
    def copy(self):
        """Deep-copy the MolSys."""

        tmp_item = MolSys()
        tmp_item.topology = self.topology.copy()
        tmp_item.structures = self.structures.copy()
        tmp_item.molecular_mechanics = self.molecular_mechanics.copy()
        if self._structure_chemical_state_indices is not None:
            tmp_item._structure_chemical_state_indices = (
                self._structure_chemical_state_indices.copy()
            )
        return tmp_item


    def add_missing_bonds(self, threshold='2 angstroms', selection='all', structure_indices=0, syntax='MolSysMT',
                          engine='MolSysMT', with_templates=True, with_distances=True, skip_digestion=False):
        """Fill missing bonds inferred from the current coordinates."""

        from molsysmt.build import get_missing_bonds as _get_missing_bonds

        bonds = _get_missing_bonds(self, threshold=threshold, selection=selection, structure_indices=structure_indices,
                                   syntax=syntax, engine='MolSysMT', with_templates=True, with_distances=False,
                                   skip_digestion=True)

        self.topology.add_bonds(bonds, skip_digestion=True)

    def rebuild_atoms(self, redefine_ids=True, redefine_types=True):
        """Recompute atom ids/types from the present topology."""

        self.topology.rebuild_atoms(redefine_ids=redefine_ids, redefine_types=redefine_types)

    def rebuild_groups(self, redefine_ids=True, redefine_types=True):
        """Rebuilding group ids and group types on the native topology."""

        self.topology.rebuild_groups(redefine_ids=redefine_ids, redefine_types=redefine_types)

    def rebuild_components(self, redefine_ids=True, redefine_types=True):
        """Rebuilding component metadata on the native topology."""

        self.topology.rebuild_components(redefine_ids=redefine_ids, redefine_types=redefine_types)

    def rebuild_molecules(self, redefine_ids=True, redefine_types=True):
        """Rebuilding molecule metadata on the native topology."""

        self.topology.rebuild_molecules(redefine_ids=redefine_ids, redefine_types=redefine_types)

    def rebuild_chains(self, redefine_ids=True, redefine_types=True):
        """Recompute chain ids/types from the present topology."""

        self.topology.rebuild_chains(redefine_ids=redefine_ids, redefine_types=redefine_types)

    def rebuild_entities(self, redefine_ids=True, redefine_types=True):
        """Rebuilding entity metadata on the native topology."""

        self.topology.rebuild_entities(redefine_ids=redefine_ids, redefine_types=redefine_types)

    def to_form(self, to_form, skip_digestion=False, **kwargs):
        """Convert the MolSys to a target form."""

        from molsysmt.form.molsysmt_MolSys import _convert_to

        function = _convert_to[to_form]

        if isinstance(function, str):
            from importlib import import_module
            module_name = f"molsysmt.form.molsysmt_MolSys.{function}"
            module = import_module(module_name)
            function = getattr(module, function)

        return function(self, skip_digestion=True, **kwargs)

    def info(self,
             element='system',
             selection='all',
             syntax='MolSysMT',
             skip_digestion=False
             ):
        """Return a text summary of the MolSys."""

        from molsysmt.basic import info as _info

        return _info(self, element=element, selection=selection, syntax=syntax, skip_digestion=True)

    def get(self,
        element='system',
        selection='all',
        structure_indices='all',
        mask=None,
        syntax='MolSysMT',
        get_missing_bonds=True,
        output_type='values',
        skip_digestion=False,
        **kwargs):
        """Proxy to :func:`molsysmt.get` using this MolSys as input."""

        from molsysmt.basic import get as _get

        return _get(self, element=element, selection=selection, structure_indices=structure_indices,
                    mask=mask, syntax=syntax, get_missing_bonds=get_missing_bonds, output_type=output_type,
                    skip_digestion=True, **kwargs)

    def _get_n_atoms(self):
        return self.topology._get_n_atoms()

    def get_n_atoms(self):
        return self.topology.get_n_atoms()
