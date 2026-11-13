"""Private HDF5 group codec for named sparse interaction analyses."""

from molsysmt._private.hdf5_validation import numbered_group_count, schema_version

from .result import Interactions

_SCHEMA = "molsysmt.interactions_collection"
_VERSION = 1


def write_named_analyses(group, analyses):
    """Write a validated collection into an empty HDF5 group."""

    if len(group):
        raise ValueError("The interaction collection group must be empty")
    analyses = dict(analyses)
    for name, result in analyses.items():
        if not isinstance(name, str) or not name:
            raise ValueError("Interaction analysis names must be nonempty strings")
        if not isinstance(result, Interactions) or not result._is_full:
            raise ValueError("Named analyses require full Interactions results")

    group.attrs["schema"] = _SCHEMA
    group.attrs["schema_version"] = _VERSION
    group.attrs["n_analyses"] = len(analyses)
    for index, name in enumerate(sorted(analyses)):
        child = group.create_group(str(index))
        child.attrs["name"] = name
        analyses[name]._write_group(child)


def _collection_count(group, *, schema_versions=(_VERSION,)):
    """Validate collection headers without interpreting analysis payloads."""
    if group.attrs.get("schema") != _SCHEMA:
        raise ValueError("unsupported interaction collection schema or version")
    try:
        schema_version(group, schema_versions, "interaction collection")
    except ValueError as error:
        raise ValueError(
            "unsupported interaction collection schema or version"
        ) from error
    return numbered_group_count(group, "n_analyses", "interaction collection")


def read_named_analyses(group, names=None):
    """Read selected named analyses from a versioned HDF5 collection."""
    count = _collection_count(group)
    requested = (
        None if names is None else ({names} if isinstance(names, str) else set(names))
    )
    if requested is not None and any(
        not isinstance(name, str) or not name for name in requested
    ):
        raise ValueError("Requested analysis names must be nonempty strings")
    analyses = {}
    seen = set()
    for index in range(count):
        child = group[str(index)]
        name = child.attrs.get("name")
        if isinstance(name, bytes):
            name = name.decode("utf-8")
        if not isinstance(name, str) or not name or name in seen:
            raise ValueError("interaction collection contains an invalid analysis name")
        seen.add(name)
        if requested is None or name in requested:
            analyses[name] = Interactions._read_group(child)
    if requested is not None and requested - seen:
        raise KeyError(f"Unknown interaction analyses: {sorted(requested - seen)}")
    return analyses
