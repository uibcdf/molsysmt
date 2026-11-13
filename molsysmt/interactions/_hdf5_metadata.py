"""Reading integral axis declarations from sparse-result HDF5 metadata."""

import json

from molsysmt._private.hdf5_validation import integer_metadata


def read_metadata(group):
    """Validate stored counts before any constructor or query can coerce them."""
    metadata = json.loads(group.attrs["metadata"])
    if not isinstance(metadata, dict):
        raise ValueError("Interactions metadata must be an object.")
    for name in ("n_atoms", "n_structures"):
        metadata[name] = integer_metadata(metadata.get(name), f"interactions.{name}")
    for name in ("source_n_atoms", "source_n_structures"):
        if metadata.get(name) is not None:
            metadata[name] = integer_metadata(metadata[name], f"interactions.{name}")
    return metadata
