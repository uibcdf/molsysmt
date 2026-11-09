"""Read bounded 0.5 queries without changing the public file form.

One lexical query scope owns its handles and decoded static domains. Nothing is
cached across public calls, and resident conversion keeps its separate reader.
"""

from contextlib import ExitStack, contextmanager
from contextvars import ContextVar
from pathlib import Path

import h5py

from molsysmt._private.attribute_catalog import mechanical_attributes as _MECHANICAL
from molsysmt._private.h5msm_storage.versions import MODULAR_VERSIONS
from molsysmt._private.variables import is_all

from .._h5msm05_associations import read_associations
from .._h5msm05_structures import (
    _FIELDS,
    read_independent_structures,
    validate_structures_metadata,
)

_ACTIVE = ContextVar("molsysmt_h5msm_query", default=None)
_DERIVED = {
    "box_shape": {"box"},
    "box_lengths": {"box"},
    "box_angles": {"box"},
    "box_volume": {"box"},
    "total_energy": {"potential_energy", "kinetic_energy"},
    "n_bioassemblies": {"bioassembly"},
}
_STRUCTURAL = set(_FIELDS) | set(_DERIVED) | {"bioassembly", "alternate_location"}


def _paths(source):
    if isinstance(source, (list, tuple)):
        for item in source:
            yield from _paths(item)
    elif isinstance(source, (str, Path)) and str(source).endswith(".h5msm"):
        yield str(Path(source).resolve())


@contextmanager
def query_scope(source):
    """Share real file readers only for the duration of a public query."""
    active = _ACTIVE.get()
    if active is not None:
        _open_queries(source, *active)
        yield [
            active[0][path]
            for path in dict.fromkeys(_paths(source))
            if active[0][path] is not None
        ]
        return
    with ExitStack() as stack:
        queries = {}
        token = _ACTIVE.set((queries, stack))
        try:
            _open_queries(source, queries, stack)
            yield [query for query in queries.values() if query is not None]
        finally:
            _ACTIVE.reset(token)


def _open_queries(source, queries, stack):
    for path in _paths(source):
        if path in queries:
            continue
        file = h5py.File(path, "r")
        stack.callback(file.close)
        version = file.attrs.get("version")
        if isinstance(version, bytes):
            version = version.decode()
        if version not in MODULAR_VERSIONS:
            file.close()
            queries[path] = None
            continue
        queries[path] = _ModularQuery(file)


def _current(item):
    return _ACTIVE.get()[0].get(str(Path(item).resolve()))


def current_queries(source):
    """Return distinct file readers owned by the enclosing query scope."""
    active = _ACTIVE.get()
    return (
        []
        if active is None
        else [
            active[0][path]
            for path in dict.fromkeys(_paths(source))
            if active[0].get(path) is not None
        ]
    )


def route_getter(legacy, item, **kwargs):
    """Route already validated file arguments to the actual stored schema."""
    with query_scope(item):
        query = _current(item)
        if query is None:
            return legacy(item, skip_digestion=True, **kwargs)
        return query.get(legacy.__name__, **kwargs)


def route_mechanical_getter(target, item, **kwargs):
    """Read stored mechanics, retaining absence in legacy files."""
    with query_scope(item):
        query = _current(item)
        if query is not None:
            return query.get(target.__name__, **kwargs)
        from molsysmt.native import H5MSMFileHandler

        handler = H5MSMFileHandler(item)
        handler.close()
        return None


def query_has_attribute(item, attribute, include_none):
    """Return None only for a non-modular file, retaining legacy dispatch."""
    with query_scope(item):
        query = _current(item)
        return None if query is None else query.has(attribute, include_none)


class _ModularQuery:
    def __init__(self, file):
        from molsysmt._private.h5msm_storage.modular import (
            _DOMAINS,
            _declared_sizes,
            _header,
        )

        self.version = _header(file)
        if self.version == "0.5" and set(file) - {
            "topology",
            "chemical_states",
            "structures",
            "interactions",
            "associations",
        }:
            raise ValueError("Expected an H5MSM 0.5 modular file.")
        self.layers = (
            _DOMAINS
            if self.version == "0.6"
            else set(_DOMAINS) - {"molecular_mechanics"}
        )
        self.file = file
        validate_structures_metadata(file)
        self.sizes = _declared_sizes(file)
        if any(value < 0 for value in self.sizes.values()):
            raise ValueError("Invalid modular layer axis cardinality.")
        self._domains = {}
        self._views = {}
        self._links = None
        self._axes_checked = False

    @property
    def n_atoms(self):
        self._validate_axes()
        for layer in (
            "topology",
            "chemical_states",
            "structures",
            "molecular_mechanics",
        ):
            if (layer, None, "atom") in self.sizes:
                return self.sizes[layer, None, "atom"]
        return self._interaction_axis("atom")

    @property
    def n_structures(self):
        count = self.sizes.get(("structures", None, "structure"))
        return self._interaction_axis("structure") if count is None else count

    def _interaction_axis(self, axis):
        values = {
            size
            for (layer, _, kind), size in self.sizes.items()
            if layer == "interactions" and kind == axis
        }
        if len(values) > 1:
            raise ValueError("Named analyses do not declare one shared query axis.")
        return next(iter(values), None)

    def _validate_axes(self):
        if self._axes_checked:
            return
        links = (
            read_associations(self.file, self.sizes, axes={"atom"}, layers=self.layers)
            or []
        )
        if self.version == "0.6":
            from molsysmt._private.h5msm_storage.modular import _require_shared_axes

            _require_shared_axes(links, self.sizes, axes=("atom",))
            self._links = links
            self._axes_checked = True
            return
        required = []
        if "topology" in self.file and "chemical_states" in self.file:
            required.append(("chemical_states", "topology"))
        if ("structures", None, "atom") in self.sizes:
            if "topology" in self.file:
                required.append(("structures", "topology"))
            elif "chemical_states" in self.file:
                required.append(("structures", "chemical_states"))
        for source, target in required:
            if not any(
                link["axis"] == "atom"
                and link["source"] == source
                and link["target"] == target
                and link["source_name"] is None
                and link["target_name"] is None
                and isinstance(link["indices"], str)
                and link["indices"] == "identity"
                for link in links
            ):
                raise ValueError(
                    "File queries require declared identity links for shared atom axes."
                )
        self._links = links
        self._axes_checked = True

    def domain(self, name):
        if name not in self._domains:
            if name == "topology":
                from .._h5msm05_topology import read_independent_topology

                value = read_independent_topology(self.file)
            elif name == "molecular_mechanics":
                from molsysmt._private.h5msm_storage.mechanics import read_mechanics

                value = read_mechanics(self.file)
            else:
                from .._h5msm_chemical_states import read_independent_chemical_states

                value = read_independent_chemical_states(self.file)
            self._domains[name] = value
            if (
                name == "topology"
                and value is not None
                and self.file["topology"].attrs.get("schema_version") in (1, 2)
            ):
                states = self.domain("chemical_states")
                reference = (
                    None if states is None else states.reference_chemical_state_index
                )
                if reference is not None:
                    from molsysmt.native._legacy_molecule_membership import restore

                    with states._using_chemical_state(reference):
                        restore(value, states)
        return self._domains[name]

    def static(self, attribute, element="system"):
        from molsysmt.attribute.attributes import attributes
        from molsysmt.native import MolSys

        self._validate_axes()
        chemical = attributes[attribute]["chemical_state"] or element in {
            "bond",
            "component",
        }
        chemical |= attribute in {"n_bonds", "n_inner_bonds", "n_components"}
        inventory = not chemical or element not in {"atom", "bond", "system"}
        # Early topology schemas stored molecule membership through the reference state.
        legacy = "topology" in self.file and self.file["topology"].attrs.get(
            "schema_version"
        ) in (1, 2)
        chemical |= inventory and legacy and "chemical_states" in self.file
        key = (inventory, chemical)
        if key not in self._views:
            topology = self.domain("topology") if inventory else None
            states = self.domain("chemical_states") if chemical else None
            if states is not None:
                from molsysmt.native._query_domains import compose_query_domains

                self._views[key] = compose_query_domains(
                    [states] if topology is None else [topology, states]
                )
            else:
                self._views[key] = (
                    None
                    if topology is None
                    else MolSys._from_partial_domains(topology=topology)
                )
        return self._views[key]

    def has(self, attribute, include_none=False):
        from molsysmt.form import molsysmt_MolecularMechanics, molsysmt_MolSys

        if attribute in _MECHANICAL:
            self._validate_axes()
            mechanics = self.domain("molecular_mechanics")
            return mechanics is not None and molsysmt_MolecularMechanics.has_attribute(
                mechanics, attribute, include_none=include_none, skip_digestion=True
            )
        if attribute in {"n_atoms", "atom_index"}:
            return self.n_atoms is not None
        if attribute in {"n_structures", "structure_index"}:
            return self.n_structures is not None
        if attribute in _STRUCTURAL:
            if "structures" not in self.file:
                return False
            return include_none or all(
                name in self.file["structures"]
                for name in _DERIVED.get(attribute, {attribute})
            )
        if attribute == "structure_chemical_state_index":
            if self.n_structures is None or "chemical_states" not in self.file:
                return False
            return include_none or all(
                value is not None for value in self.state_indices("all")
            )
        source = self.static(attribute)
        return source is not None and molsysmt_MolSys.has_attribute(
            source,
            attribute,
            include_none=include_none,
            skip_digestion=True,
        )

    def _indices(self, value, size, name):
        from molsysmt.basic._index_validation import validate_element_indices

        if value is None:
            return None
        return validate_element_indices(
            str(self.file.filename),
            value,
            "structure" if name == "structure_indices" else "atom",
            name,
            "file:h5msm",
            count_getter=lambda element: size,
        )

    def state_indices(self, structures):
        self._validate_axes()
        indices = self._indices(structures, self.n_structures, "structure_indices")
        if is_all(indices):
            indices = range(self.n_structures)
        states = self.domain("chemical_states")
        for link in (
            read_associations(
                self.file, self.sizes, axes={"structure_state"}, layers=self.layers
            )
            or []
        ):
            if (
                link["axis"] == "structure_state"
                and link["source"] == "structures"
                and link["target"] == "chemical_states"
            ):
                mapping = link["indices"]
                return [
                    int(i)
                    if isinstance(mapping, str)
                    else None
                    if mapping[i] < 0
                    else int(mapping[i])
                    for i in indices
                ]
        return [
            0 if states is not None and states.n_chemical_states == 1 else None
            for _ in indices
        ]

    def _resolve_structure_chemical_state_index(self, structures):
        from molsysmt._private.smonitor import StructuralInconsistencyError

        values = self.state_indices(structures)
        reason = None
        if not values:
            reason = "No structures are available to resolve a chemical state."
        elif any(value is None for value in values):
            reason = (
                "At least one selected structure has no chemical-state association."
            )
        elif len(set(values)) != 1:
            reason = "The selected structures span multiple chemical states and cannot resolve one state-dependent result."
        if reason:
            raise StructuralInconsistencyError(reason=reason, caller="file:h5msm")
        return values[0]

    def get(self, name, **kwargs):
        from molsysmt.form import molsysmt_MolSys, molsysmt_Structures

        attribute, element = name[4:].rsplit("_from_", 1)
        indices = kwargs.get("indices", "all")
        structures = kwargs.get("structure_indices", "all")
        if attribute == "n_atoms" and element == "system":
            return self.n_atoms
        if attribute == "atom_index" and element == "atom":
            indices = self._indices(indices, self.n_atoms, "indices")
            return list(range(self.n_atoms)) if is_all(indices) else list(indices)
        if attribute in {"n_structures", "structure_index"}:
            structures = self._indices(
                structures, self.n_structures, "structure_indices"
            )
            if structures is None:
                return None
            values = range(self.n_structures) if is_all(structures) else structures
            return len(values) if attribute == "n_structures" else list(values)
        if attribute == "structure_chemical_state_index":
            return self.state_indices(structures)
        if attribute in _STRUCTURAL:
            self._validate_axes()
            if "structures" not in self.file:
                return None
            if structures is None or indices is None:
                return None
            structures = self._indices(
                structures, self.n_structures, "structure_indices"
            )
            atoms = (
                self._indices(indices, self.n_atoms, "indices")
                if element == "atom"
                else "all"
            )
            if attribute == "alternate_location":
                from .._h5msm05_alternate_location import read_alternate_location

                return read_alternate_location(
                    self.file["structures"],
                    self.n_structures,
                    self.n_atoms,
                    None if is_all(structures) else structures,
                    None if is_all(atoms) else atoms,
                    remap_atoms=False,
                )
            source = read_independent_structures(
                self.file,
                structure_indices=None if is_all(structures) else structures,
                atom_indices=None if is_all(atoms) else atoms,
                fields=_DERIVED.get(attribute, {attribute}),
            )
            target = getattr(molsysmt_Structures, name)
            canonical = {
                key: "all" for key in kwargs if key in {"indices", "structure_indices"}
            }
            return target(source, skip_digestion=True, **canonical)
        from molsysmt.form import molsysmt_MolecularMechanics

        if attribute in _MECHANICAL:
            self._validate_axes()
            mechanics = self.domain("molecular_mechanics")
            if element == "atom":
                selected = self._indices(indices, self.n_atoms, "indices")
                if selected is None:
                    return None
                kwargs = {**kwargs, "indices": selected}
            target_name = (
                f"get_{attribute}_from_atom"
                if element == "system"
                and attribute in {"partial_charge", "atom_ff_type"}
                else name
            )
            return (
                None
                if mechanics is None
                else getattr(molsysmt_MolecularMechanics, target_name)(
                    mechanics, skip_digestion=True, **kwargs
                )
            )
        source = self.static(attribute, element)
        return (
            None
            if source is None
            else getattr(molsysmt_MolSys, name)(source, skip_digestion=True, **kwargs)
        )
