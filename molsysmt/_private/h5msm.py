"""Detecting modular H5MSM files at public query boundaries."""

from pathlib import Path


def modular_h5msm_dimensions(item):
    """Return source axis sizes from 0.5 metadata without loading domain arrays.

    Return None for other forms. This preflight is not a schema validation;
    the materializing reader remains responsible for domain associations.
    """
    if not isinstance(item, (str, Path)) or not str(item).endswith(".h5msm"):
        return None
    import h5py

    from molsysmt.form._h5msm05_associations import _axis_sizes_from_file

    with h5py.File(item, "r") as file:
        version = file.attrs.get("version")
        if isinstance(version, bytes):
            version = version.decode()
        if version != "0.5":
            return None
        sizes = _axis_sizes_from_file(file)
    n_atoms = sizes.get(
        ("structures", None, "atom"),
        sizes.get(
            ("topology", None, "atom"), sizes.get(("chemical_states", None, "atom"), 0)
        ),
    )
    return n_atoms, sizes.get(("structures", None, "structure"), 0)


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
