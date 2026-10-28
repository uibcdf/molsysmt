"""Transport a complete declared atom axis through built-in native domains."""

from collections import deque
from collections.abc import Mapping
from copy import deepcopy

import numpy as np
import pandas as pd

from molsysmt._private.argdigest.argument._correspondence_axes import flat_axis
from molsysmt._private.smonitor import (
    ArgumentError,
    MemoryBudgetExceededError,
    StructuralInconsistencyError,
)

CALLER = "molsysmt.basic.permute_atoms"
_FIELDS = {
    "MolSys": "_chemical_states_domain _interactions _structure_chemical_state_indices _structures _topology molecular_mechanics",
    "Topology": "_chain_group_membership _atoms_dirty _chains_dirty _chemical_states_domain _components_dirty _entities_dirty _groups_dirty _molecules_dirty _molsys_owner_ref atoms chains entities groups molecules",
    "Structures": "_b_factor _box _coordinates _kinetic_energy _molsys_owner_ref _occupancy _potential_energy _temperature _time _time_step _velocities alternate_location bioassembly constant_box constant_id_step constant_time_step id_step structure_id",
    "ChemicalStates": "_molsys_owner_ref _n_atoms _reference_index _states",
    "_ChemicalStateStorage": "_component_completeness _component_evidence _connectivity_completeness _preparation_history _provenance_index atom_attributes bonds component_indices components state_id",
    "MolecularMechanics": "atom_type_assignment atoms_ff constraints cutoff_distance dispersion_correction ewald_error_tolerance flexible_constraints forcefield hydrogen_mass implicit_solvent kappa non_bonded_method partial_charge_assignment rigid_water salt_concentration solute_dielectric solvent_dielectric switch_distance water_model",
}


def _fail(reason):
    raise StructuralInconsistencyError(reason=reason, caller=CALLER)


def _profile(value, cls):
    if value is None:
        return
    if type(value) is not cls or set(vars(value)) - set(_FIELDS[cls.__name__].split()):
        _fail(
            f"Unsupported extension of {cls.__name__}; an explicit domain remapper is required."
        )


def _table(value, label, *, rows=None, columns=None, complete=False):
    if not isinstance(value, (pd.DataFrame, pd.Series)) or value.attrs:
        _fail(f"{label} requires a native table without untyped metadata.")
    if not value.index.equals(pd.RangeIndex(len(value))):
        _fail(f"{label} must use positional row indices.")
    if rows is not None and len(value) != rows:
        _fail(f"{label} is not aligned with the atom axis.")
    if isinstance(value, pd.DataFrame):
        if not value.columns.is_unique or (
            columns is not None
            and (set(value) - set(columns) or (complete and set(value) != set(columns)))
        ):
            _fail(f"{label} contains unsupported columns.")
        for column in value:
            if column.endswith("_id") and any(
                not isinstance(x, str) for x in value[column].dropna()
            ):
                _fail(f"{label}.{column} must contain string IDs.")


def _references(value, size, label):
    present = value.dropna()
    if any(
        isinstance(x, (bool, np.bool_))
        or not isinstance(x, (int, np.integer))
        or not 0 <= x < size
        for x in present
    ):
        _fail(f"{label} contains an invalid positional reference.")


def _validate(source, n_atoms):
    from .chemical_states import ChemicalStates
    from .molecular_mechanics import MolecularMechanics
    from .molsys import MolSys
    from .structures import Structures
    from .topology import (
        _ATOMS_COLUMNS,
        _BOND_ALLOWED_COLUMNS,
        _BOND_ATOM_REFERENCE_COLUMNS,
        _CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES,
        _GROUPS_COLUMNS,
        Topology,
        _ChemicalStateStorage,
    )

    _profile(source, MolSys)
    top, states, structures, mechanics = (
        source.topology,
        source.chemical_states,
        source.structures,
        source.molecular_mechanics,
    )
    for value, cls in (
        (top, Topology),
        (states, ChemicalStates),
        (structures, Structures),
        (mechanics, MolecularMechanics),
    ):
        _profile(value, cls)
    if top is not None:
        if top._chain_group_membership is not None:
            from ._chain_groups import by_chain, pack

            pack(top, by_chain(top))
        _table(
            top.atoms,
            "Topology.atoms",
            rows=n_atoms,
            columns=_ATOMS_COLUMNS,
            complete=True,
        )
        _table(top.groups, "Topology.groups", columns=_GROUPS_COLUMNS, complete=True)
        for name in ("molecules", "chains", "entities"):
            # These tables stay on their original axes; reject unknown reference columns.
            columns = {
                "molecules": (
                    "molecule_id",
                    "molecule_name",
                    "molecule_type",
                    "entity_index",
                ),
                "chains": ("chain_id", "chain_name", "chain_type"),
                "entities": ("entity_id", "entity_name", "entity_type"),
            }[name]
            _table(
                getattr(top, name), f"Topology.{name}", columns=columns, complete=True
            )
        for table, column, target in (
            (top.atoms, "group_index", top.groups),
            (top.atoms, "chain_index", top.chains),
            (top.groups, "molecule_index", top.molecules),
            (top.molecules, "entity_index", top.entities),
        ):
            if column in table:
                _references(table[column], len(target), column)
    if states is not None:
        if states.n_atoms != n_atoms:
            _fail("ChemicalStates has a different atom axis.")
        if top is not None and top._chemical_states_domain is not states:
            _fail("Topology must share the owning chemical-state domain.")
        for state in states._states:
            _profile(state, _ChemicalStateStorage)
            _table(
                state.atom_attributes,
                "chemical atom attributes",
                rows=n_atoms,
                columns=_CHEMICAL_STATE_ATOM_ATTRIBUTE_DTYPES,
            )
            _table(
                state.component_indices, "chemical component membership", rows=n_atoms
            )
            _table(
                state.components,
                "chemical components",
                columns=("component_id", "component_name", "component_type"),
                complete=True,
            )
            _references(
                state.component_indices, len(state.components), "component_indices"
            )
            _table(state.bonds, "chemical bonds", columns=_BOND_ALLOWED_COLUMNS)
            if not {"atom1_index", "atom2_index"}.issubset(state.bonds.columns):
                _fail("Chemical bonds require both endpoint columns.")
            if state.bonds[["atom1_index", "atom2_index"]].isna().any().any():
                _fail("Bond endpoints cannot be missing.")
            for column in _BOND_ATOM_REFERENCE_COLUMNS:
                if column in state.bonds:
                    _references(state.bonds[column], n_atoms, column)
    if structures is not None:
        structures._validate_alignment()
        size = structures._atom_axis_size()
        if size is not None and size != n_atoms:
            _fail("Structures has a different atom axis.")
        if structures.alternate_location is not None:
            for sites in structures.alternate_location:
                if not isinstance(sites, dict):
                    _fail("Alternate locations require sparse atom-index dictionaries.")
                _references(
                    pd.Series(list(sites), dtype=object), n_atoms, "alternate_location"
                )
    if mechanics is not None:
        from molsysmt import pyunitwizard as puw

        for name, value in vars(mechanics).items():
            if (
                name
                in ("atoms_ff", "partial_charge_assignment", "atom_type_assignment")
                or value is None
            ):
                continue
            if (
                name == "forcefield"
                and isinstance(value, (list, tuple))
                and all(isinstance(item, str) for item in value)
            ):
                continue
            if isinstance(value, (str, bool, int, float, np.number)) or (
                puw.is_quantity(value) and np.ndim(puw.get_value(value)) == 0
            ):
                continue
            _fail(
                f"Mechanics setting {name!r} is outside the supported scalar profile."
            )
    if mechanics is not None and mechanics.atoms_ff is not None:
        _table(
            mechanics.atoms_ff,
            "mechanics atoms",
            rows=n_atoms,
            columns=("formal_charge", "partial_charge", "atom_ff_type"),
        )
    for analysis in source.interactions.values():
        from molsysmt.interactions.result import Interactions

        if (
            type(analysis) is not Interactions
            or not analysis._is_full
            or analysis.n_atoms != n_atoms
        ):
            _fail("Named interactions require full built-in results on this atom axis.")
        if structures is not None and analysis.n_structures != structures.n_structures:
            _fail("Named interactions have a different structure axis.")


def _budget(source, identity):
    from molsysmt import configure

    # This estimates resident numeric payload, not Python object overhead or RSS.
    # Protected boxes and identity coordinates share immutable bytes.
    seen = set()
    structures = source.structures
    if structures is not None:
        seen.update(
            id(value)
            for value in (
                structures._box,
                structures._coordinates if identity else None,
            )
            if value is not None
        )
    from ._structure_array import _StructureArray

    def size(value):
        if id(value) in seen:
            return 0
        seen.add(id(value))
        if isinstance(value, _StructureArray):
            return int(np.prod(value.shape)) * 8
        if isinstance(value, np.ndarray):
            return value.nbytes
        if isinstance(value, (pd.DataFrame, pd.Series)):
            return int(np.sum(value.memory_usage(index=True, deep=False)))
        if isinstance(value, Mapping):
            return sum(size(item) for item in value.values())
        if isinstance(value, (list, tuple)):
            return sum(size(item) for item in value)
        if type(value).__module__.startswith(
            ("molsysmt.native.", "molsysmt.interactions.")
        ) and hasattr(value, "__dict__"):
            return sum(size(item) for item in vars(value).values())
        return 0

    total = size(source) + 16 * source._get_n_atoms()
    if total > configure.max_ram_usage:
        raise MemoryBudgetExceededError(
            reason="Resident permuted numeric output exceeds the configured budget.",
            predicted_bytes=total,
            available_bytes=configure.max_ram_usage,
            caller=CALLER,
        )


def _coordinates(structures, order):
    from molsysmt._private.execution import ChunkedExecutor, Reducer

    from ._structure_array import _BLOCK_BYTES, _StructureArray

    class Capture(Reducer):
        def initialize(self, metadata):
            self.blocks = deque()

        def consume(self, chunk):
            self.blocks.append(chunk["coordinates"])

        def finalize(self):
            def read(start, stop):
                pieces, needed = [], stop - start
                while needed:
                    block = self.blocks.popleft()
                    take = min(needed, len(block))
                    pieces.append(block[:take])
                    if take < len(block):
                        self.blocks.appendleft(block[take:])
                    needed -= take
                return pieces[0] if len(pieces) == 1 else np.concatenate(pieces)

            return _StructureArray._from_reader(structures._coordinates.shape, read)

    size = max(1, _BLOCK_BYTES // max(1, len(order) * 3 * 8))
    return ChunkedExecutor(
        structures,
        "molsysmt.Structures",
        "permute_atoms",
        reducer=Capture(),
        atom_indices=order,
        heavy_mode="force",
        chunk_size=size,
        max_chunk_size=size,
    ).execute()


def permute(source, atom_indices, *, return_report=False):
    """Validate before allocation and preserve native graph ownership when cloning."""
    from ._copy import _deferred_geometry_memo
    from .structures import _remap_alternate_atom_indices
    from .topology import Topology

    order = flat_axis(atom_indices, "atom_indices", CALLER)
    n_atoms = source._get_n_atoms()
    if (
        order is None
        or isinstance(order, str)
        or np.ndim(atom_indices) != 1
        or n_atoms is None
        or len(order) != n_atoms
        or np.any(order >= n_atoms)
        or not np.all(np.bincount(order, minlength=n_atoms) == 1)
    ):
        raise ArgumentError(
            "atom_indices",
            caller=CALLER,
            message="A complete atom-index bijection is required.",
        )
    _validate(source, n_atoms)
    inverse = np.empty(n_atoms, dtype=np.int64)
    inverse[order] = np.arange(n_atoms, dtype=np.int64)
    identity = np.array_equal(order, np.arange(n_atoms))
    _budget(source, identity)
    memo = _deferred_geometry_memo(source.structures)

    def rows(table):
        if table is not None and id(table) not in memo:
            result = table.iloc[order].copy()
            result.index = pd.RangeIndex(n_atoms)
            memo[id(table)] = result

    if source.topology is not None:
        rows(source.topology.atoms)
    if source.chemical_states is not None:
        mapping = dict(enumerate(inverse.tolist()))
        for state in source.chemical_states._states:
            rows(state.atom_attributes)
            rows(state.component_indices)
            memo[id(state.bonds)] = Topology._remap_bond_atom_indices(
                state.bonds, mapping, canonical_order=True
            )
    structures = source.structures
    if structures is not None:
        if not identity and structures._coordinates is not None:
            memo[id(structures._coordinates)] = _coordinates(structures, order)
        for values in (
            structures._velocities,
            structures._b_factor,
            structures._occupancy,
        ):
            if values is not None:
                output = np.empty_like(values)
                size = max(1, 1024 * 1024 // max(1, values[0:1].nbytes))
                for start in range(0, len(values), size):
                    output[start : start + size] = values[start : start + size][
                        :, order
                    ]
                memo[id(values)] = output
        if structures.alternate_location is not None:
            memo[id(structures.alternate_location)] = _remap_alternate_atom_indices(
                deepcopy(structures.alternate_location), order
            )
    if source.molecular_mechanics is not None:
        rows(source.molecular_mechanics.atoms_ff)
    for analysis in source.interactions.values():
        if id(analysis) not in memo:
            memo[id(analysis)] = analysis.remap(atom_indices=order)
    output = source.__deepcopy__(memo)
    from molsysmt._private.autodock_assignment import (
        project_assignment as project_types,
    )
    from molsysmt._private.partial_charges import project_assignment as project_charge

    if source.molecular_mechanics is not None:
        project_charge(source, output, order)
        project_types(source, output, order)
        for field in ("partial_charge_assignment", "atom_type_assignment"):
            assignment = getattr(output.molecular_mechanics, field)
            if assignment is not None:
                assignment["atom_order_transform"] = {
                    "operation": "permute_atoms",
                    "output_to_input_atom_indices": order.copy(),
                }
    if not return_report:
        return output, None

    from molsysmt import __version__
    from molsysmt._private.atom_maps import SCHEMA, direct

    report = dict(
        schema=SCHEMA,
        n_source_atoms=n_atoms,
        n_output_atoms=n_atoms,
        source_to_output_atom_indices=inverse,
        output_to_source_atom_indices=order,
        operation="permute_atoms",
        software={"molsysmt": __version__},
    )
    if source.topology is not None:
        for axis, table in (
            ("source", source.topology.atoms),
            ("output", output.topology.atoms),
        ):
            for column, label in (("atom_id", "ids"), ("atom_name", "names")):
                report[f"{axis}_atom_{label}"] = (
                    table[column]
                    .astype(object)
                    .where(table[column].notna(), None)
                    .to_numpy(copy=True)
                )
    return output, direct(report)
