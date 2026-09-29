"""Private HDF5 group codec for named sparse interaction analyses."""

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


def read_named_analyses(group, names=None):
    """Read selected named analyses from a versioned HDF5 collection."""

    if (group.attrs.get("schema") != _SCHEMA
            or group.attrs.get("schema_version") != _VERSION):
        raise ValueError("unsupported interaction collection schema or version")
    count = int(group.attrs["n_analyses"])
    if count < 0 or set(group) != {str(index) for index in range(count)}:
        raise ValueError("interaction collection has inconsistent analysis groups")
    requested = None if names is None else ({names} if isinstance(names, str) else set(names))
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
