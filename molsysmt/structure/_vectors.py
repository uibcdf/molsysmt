"""Bounded endpoint delivery and reduction for directed molecular geometry."""

import numpy as np

from molsysmt._private import rust_backend as kernels
from molsysmt._private.execution import Reducer
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.pbc._whole_participants import validate_periodic_boxes

from ._geometry_endpoints import read_coordinates

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
