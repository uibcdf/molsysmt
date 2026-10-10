"""Bounded endpoint delivery and reduction for directed molecular geometry."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private import rust_backend as kernels
from molsysmt._private.execution import ChunkedExecutor, Reducer
from molsysmt._private.h5msm import modular_h5msm_dimensions
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt._private.variables import is_all, is_iterable_of_iterables
from molsysmt._private.weighted_geometry import prepare_weights
from molsysmt.pbc._whole_participants import (
    require_whole_participants,
    validate_periodic_boxes,
)

CALLER = "molsysmt.structure.get_vectors"


def evaluate_endpoint_vectors(first, second, box, pairs, details, *, caller):
    """Compute projected nm endpoints with the shared kernel and error contract.

    Callers own source projection, memory planning and periodic-box validation.
    The Rust kernel checks endpoint axes, finiteness and image representability.
    No form discovery, argument digestion or unit presentation occurs per block.
    """
    try:
        return kernels.get_vectors(first, second, box, pairs, details)
    except ValueError as error:
        raise StructuralInconsistencyError(reason=str(error), caller=caller) from error


class Endpoint:
    """Resolve ordered source memberships once, preserving repeated endpoints."""

    def __init__(self, source, selection, structures, center, weights, syntax):
        from molsysmt.basic import get, get_form, select
        from molsysmt.form import _dict_modules

        self.source = source
        dimensions = modular_h5msm_dimensions(source)
        if dimensions is None:
            dimensions = get(source, n_atoms=True, n_structures=True)
        n_atoms, n_structures = map(int, dimensions)
        self.n_atoms = n_atoms
        self.frames = (
            np.arange(n_structures, dtype=np.int64)
            if is_all(structures)
            else np.atleast_1d(np.asarray(structures))
        )
        if self.frames.size == 0:
            self.frames = np.empty(0, dtype=np.int64)
        if (
            self.frames.ndim != 1
            or self.frames.dtype.kind not in "iu"
            or np.any((self.frames < 0) | (self.frames >= n_structures))
        ):
            raise ArgumentError("structure_indices", caller=CALLER)
        self.frames = self.frames.astype(np.int64, copy=False)
        multiple = is_iterable_of_iterables(selection) or (
            isinstance(selection, (list, tuple))
            and len(selection) > 0
            and all(isinstance(item, str) for item in selection)
        )
        self.center = bool(center or multiple)
        raw_groups = selection if multiple else [selection]
        groups = []
        for group in raw_groups:
            if is_all(group):
                atoms = np.arange(n_atoms, dtype=np.int64)
            elif not isinstance(group, str) and group is not None:
                atoms = np.asarray(group)
                if atoms.size == 0:
                    atoms = np.empty(0, dtype=np.int64)
            else:
                atoms = np.asarray(
                    select(
                        source,
                        selection=group,
                        structure_indices=self.frames,
                        syntax=syntax,
                    ),
                    dtype=np.int64,
                )
            if (
                atoms.ndim != 1
                or atoms.dtype.kind not in "iu"
                or np.any((atoms < 0) | (atoms >= n_atoms))
            ):
                raise ArgumentError("selection", caller=CALLER)
            if self.center:
                if len(atoms) == 0:
                    raise ArgumentError(
                        "selection",
                        caller=CALLER,
                        message="A center requires at least one atom.",
                    )
                groups.append(atoms.astype(np.int64, copy=False))
            else:
                groups.append(atoms.astype(np.int64, copy=False))
        self.atoms = np.concatenate(groups) if groups else np.empty(0, dtype=np.int64)
        self.sizes = (
            np.asarray([len(group) for group in groups], dtype=np.int64)
            if self.center
            else np.ones(len(self.atoms), dtype=np.int64)
        )
        self.offsets = np.r_[0, np.cumsum(self.sizes)].astype(np.int64)
        ordered = len(self.atoms) < 2 or np.all(self.atoms[1:] > self.atoms[:-1])
        self.universe = self.atoms if ordered else np.unique(self.atoms)
        self.positions = (
            np.arange(len(self.atoms), dtype=np.int64)
            if ordered
            else np.searchsorted(self.universe, self.atoms)
        )
        self.identity = np.array_equal(self.positions, np.arange(len(self.universe)))
        self.weights = None
        if self.center and len(groups):
            if (
                weights is not None
                and not isinstance(weights, str)
                and is_iterable_of_iterables(weights)
            ):
                weights = np.concatenate(weights)
            self.weights = prepare_weights(
                weights,
                len(self.atoms),
                molecular_system=source,
                selection=self.atoms,
                group_sizes=self.sizes,
                syntax=syntax,
                caller=CALLER,
            )
        elif weights is not None:
            raise ArgumentError(
                "weights", caller=CALLER, message="Weights require centers."
            )
        self.form = get_form(source)
        self.streaming = isinstance(self.form, str) and getattr(
            _dict_modules[self.form], "_heavy_support", {}
        ).get("coordinates", False)

    @property
    def count(self):
        return len(self.sizes)

    def geometry(self, coordinates, box):
        if not np.isfinite(coordinates).all():
            raise StructuralInconsistencyError(
                reason="Endpoint coordinates must be finite.", caller=CALLER
            )
        if self.center:
            if box is not None:
                for frame, cell in zip(coordinates, box):
                    require_whole_participants(
                        frame, cell, self.offsets, self.positions, CALLER
                    )
            if self.count == 0:
                return np.empty((len(coordinates), 0, 3), dtype=np.float64)
            return kernels.get_center_groups_of_atoms(
                np.ascontiguousarray(coordinates[:, self.positions]),
                self.sizes,
                self.weights,
            )
        return np.ascontiguousarray(
            coordinates if self.identity else coordinates[:, self.positions]
        )


class CoordinateReducer(Reducer):
    """Collect just one requested second-endpoint block without concatenation."""

    def __init__(self, n_atoms):
        self.n_atoms = n_atoms

    def initialize(self, metadata):
        self.coordinates = np.empty((metadata["n_structures"], self.n_atoms, 3))
        self.offset = 0

    def consume(self, chunk):
        end = self.offset + len(chunk["coordinates"])
        self.coordinates[self.offset : end] = chunk["coordinates"]
        self.offset = end

    def finalize(self):
        return self.coordinates


def read_coordinates(endpoint, frames, heavy):
    """Read a bounded second-endpoint projection through its declared route."""
    if endpoint.streaming:
        return ChunkedExecutor(
            endpoint.source,
            endpoint.form,
            "get_vectors",
            reducer=CoordinateReducer(len(endpoint.universe)),
            atom_indices="all"
            if len(endpoint.universe) == endpoint.n_atoms
            else endpoint.universe,
            structure_indices=frames,
            attributes=["coordinates"],
            heavy_mode="force" if heavy else "off",
            max_chunk_size=max(1, len(frames)),
        ).execute()
    from molsysmt.basic import get

    return np.asarray(
        puw.get_value(
            get(
                endpoint.source,
                selection=endpoint.universe,
                structure_indices=frames,
                coordinates=True,
            ),
            to_unit="nm",
            dtype=np.float64,
        )
    )


class VectorsReducer(Reducer):
    """Write each computed block into the final resident output arrays."""

    def __init__(self, first, second, universe, pairs, pbc, details, heavy):
        self.first, self.second, self.universe = first, second, universe
        self.pairs, self.pbc, self.details, self.heavy = pairs, pbc, details, heavy
        self.shared = first.source is second.source and np.array_equal(
            first.frames, second.frames
        )
        self.first_positions = np.searchsorted(universe, first.universe)
        self.first_identity = np.array_equal(
            self.first_positions, np.arange(len(universe))
        )
        self.second_positions = (
            np.searchsorted(universe, second.universe) if self.shared else None
        )
        self.second_identity = self.shared and np.array_equal(
            self.second_positions, np.arange(len(universe))
        )

    def initialize(self, metadata):
        ns = len(self.first.frames)
        nv = self.first.count if self.pairs else self.first.count * self.second.count
        self.vectors = np.empty((ns, nv, 3))
        self.distances = np.empty((ns, nv)) if self.details else None
        self.directions = np.empty((ns, nv, 3)) if self.details else None
        self.images = np.empty((ns, nv, 3), dtype=np.int32) if self.details else None
        self.offset = 0

    def consume(self, chunk):
        size = len(chunk["coordinates"])
        end = self.offset + size
        box = chunk.get("box") if self.pbc else None
        if self.pbc:
            if box is None:
                raise StructuralInconsistencyError(
                    reason="PBC requires a box for every first-endpoint structure.",
                    caller=CALLER,
                )
            validate_periodic_boxes(box, size, caller=CALLER)
        first = (
            chunk["coordinates"]
            if self.first_identity
            else chunk["coordinates"][:, self.first_positions]
        )
        second = (
            (
                chunk["coordinates"]
                if self.second_identity
                else chunk["coordinates"][:, self.second_positions]
            )
            if self.shared
            else read_coordinates(
                self.second, self.second.frames[self.offset : end], self.heavy
            )
        )
        first = self.first.geometry(first, box)
        second = self.second.geometry(second, box)
        vectors, distances, directions, images = evaluate_endpoint_vectors(
            first, second, box, self.pairs, self.details, caller=CALLER
        )
        self.vectors[self.offset : end] = vectors
        if self.details:
            self.distances[self.offset : end] = distances
            self.directions[self.offset : end] = directions
            self.images[self.offset : end] = images
        self.offset = end

    def finalize(self):
        if self.offset != len(self.first.frames):
            raise StructuralInconsistencyError(
                reason="Missing requested vector structures.", caller=CALLER
            )
        shape = (len(self.first.frames), self.first.count)
        if not self.pairs:
            shape += (self.second.count,)
        return (
            self.vectors.reshape(shape + (3,)),
            self.distances.reshape(shape) if self.details else None,
            self.directions.reshape(shape + (3,)) if self.details else None,
            self.images.reshape(shape + (3,)) if self.details else None,
        )
