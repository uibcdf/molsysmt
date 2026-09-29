"""Experimental interaction-only H5MSM 0.5 boundary for schema probes."""

from pathlib import Path

from ._hdf5_collection import read_named_analyses, write_named_analyses


def write_interactions_file(filename, analyses):
    """Write an interaction-only 0.5 probe file without overwriting a path."""
    import h5py

    with h5py.File(Path(filename), "x") as file:
        file.attrs["type"] = "h5msm"
        file.attrs["version"] = "0.5"
        file.attrs["creator"] = "MolSysMT"
        if analyses is not None:
            write_named_analyses(file.create_group("interactions"), analyses)


def read_interactions_file(filename):
    """Read an optional interaction layer from an experimental 0.5 file."""
    import h5py

    with h5py.File(Path(filename), "r") as file:
        if file.attrs.get("type") != "h5msm" or file.attrs.get("version") != "0.5":
            raise ValueError("expected an H5MSM 0.5 file")
        if "interactions" not in file:
            return None
        return read_named_analyses(file["interactions"])
