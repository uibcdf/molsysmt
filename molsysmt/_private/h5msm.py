"""Detecting modular H5MSM files at public query boundaries."""

from pathlib import Path

MODULAR_HANDLER_REASON = (
    "H5MSM 0.5 cannot be opened as molsysmt.H5MSMFileHandler; "
    "that handler supports only H5MSM 0.3 and 0.4. "
    "Use molsysmt.convert(path, to_form='molsysmt.MolSys') for a resident load, "
    "or molsysmt.h5msm.read_layers(path, layers=...) to load selected domains."
)


def has_h5msm_path(item):
    """Recognize file-query candidates without importing their adapter or reading."""
    if isinstance(item, (list, tuple)):
        return any(has_h5msm_path(part) for part in item)
    return isinstance(item, (str, Path)) and str(item).endswith(".h5msm")


def query_inventory_candidates(item):
    """Supply real static file domains to selectors without resident conversion."""
    candidates = item if isinstance(item, (list, tuple)) else [item]
    if not has_h5msm_path(item):
        return candidates, False
    from molsysmt.form.file_h5msm._modular_query import current_queries

    readers = {
        str(Path(query.file.filename).resolve()): query
        for query in current_queries(item)
    }
    result = []
    for candidate in candidates:
        query = (
            readers.get(str(Path(candidate).resolve()))
            if isinstance(candidate, (str, Path))
            else None
        )
        if query is None:
            result.append(candidate)
            continue
        query._validate_axes()
        result.extend(
            domain
            for name in ("topology", "chemical_states")
            if (domain := query.domain(name)) is not None
        )
    return result, bool(readers)


def validate_h5msm_handler_target(item, to_form):
    """Reject a legacy-handler target before materializing any 0.5 domains."""
    targets = to_form if isinstance(to_form, (list, tuple)) else [to_form]
    if "molsysmt.H5MSMFileHandler" not in targets:
        return
    if isinstance(item, (list, tuple)):
        for part in item:
            validate_h5msm_handler_target(part, to_form)
        return
    if not isinstance(item, (str, Path)) or not str(item).endswith(".h5msm"):
        return
    if not Path(item).is_file():
        return

    import h5py

    from molsysmt._private.smonitor import FormatError

    with h5py.File(item, "r") as file:
        version = file.attrs.get("version")
    if isinstance(version, bytes):
        version = version.decode()
    if version == "0.5":
        raise FormatError(reason=MODULAR_HANDLER_REASON, caller="molsysmt.convert")


def modular_h5msm_axes(item):
    """Read present 0.5 layer axes without materializing any domain arrays."""
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
        return _axis_sizes_from_file(file)


def modular_h5msm_dimensions(item):
    """Return source axis sizes from 0.5 metadata without loading domain arrays.

    Return None for other forms. This preflight is not a schema validation;
    the materializing reader remains responsible for domain associations.
    """
    sizes = modular_h5msm_axes(item)
    if sizes is None:
        return None
    n_atoms = sizes.get(
        ("structures", None, "atom"),
        sizes.get(
            ("topology", None, "atom"), sizes.get(("chemical_states", None, "atom"), 0)
        ),
    )
    return n_atoms, sizes.get(("structures", None, "structure"), 0)


def maybe_read_modular_h5msm(item, *, topology_only=False):
    """Read an admitted topology projection or the ordinary resident domains."""
    if isinstance(item, (list, tuple)):
        converted = [
            maybe_read_modular_h5msm(part, topology_only=topology_only) for part in item
        ]
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

    if topology_only:
        from molsysmt.h5msm import read_layers

        topology = read_layers(str(path), layers=["topology"])["topology"]
        if topology is None:
            raise ValueError("This MolSys has no topology domain to convert.")
        return topology

    from molsysmt.form._h5msm05_modular import read_molsys_file

    return read_molsys_file(path)
