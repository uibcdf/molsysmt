"""Series helpers implemented by the bundled Rust extension."""

import numpy as np

from molsysmt._private.rust_backend import (
    chunks_to_serie,
    jit_serialize as _jit_serialize,
    occurrence_order,
    occurrence_order_sorted_serie,
    serie_to_chunks,
)


class serialized_lists:
    """Serializing a sequence or mapping of integer sequences."""

    def __init__(self, item=None, dtype=None):
        self.values = None
        self.starts = None
        self.indices = None
        self.n_values = None
        self.n_indices = None

        if isinstance(item, (list, np.ndarray)):
            segments = item
            self.indices = np.arange(len(item))
        elif isinstance(item, dict):
            self.indices = np.sort(list(item))
            segments = [sorted(item[index]) for index in self.indices]
        else:
            return

        self.starts, self.values = _jit_serialize(segments)
        self.n_values = self.values.shape[0]
        self.n_indices = self.indices.shape[0]


__all__ = [
    "chunks_to_serie",
    "occurrence_order",
    "occurrence_order_sorted_serie",
    "serie_to_chunks",
    "serialized_lists",
]
