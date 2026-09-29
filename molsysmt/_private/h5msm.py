"""Detecting modular H5MSM files at public query boundaries."""

from pathlib import Path


def maybe_read_modular_h5msm(item):
    """Materialize a 0.5 file when a legacy file adapter cannot query its schema."""
    if isinstance(item, (list, tuple)):
        converted = [maybe_read_modular_h5msm(part) for part in item]
        if all(new is old for new, old in zip(converted, item)):
            return item
        return type(item)(converted)
    if not isinstance(item, (str, Path)) or not str(item).endswith(".h5msm"):
        return item
    path = Path(item)
    if not path.is_file():
        return item

    import h5py

    with h5py.File(path, "r") as file:
        version = file.attrs.get("version")
    if isinstance(version, bytes):
        version = version.decode()
    if version != "0.5":
        return item

    from molsysmt.form._h5msm05_modular import read_molsys_file

    return read_molsys_file(path)
