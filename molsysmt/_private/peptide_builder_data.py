"""Read the bounded bundled peptide-construction data without loading an engine."""

import gzip
import json
from functools import lru_cache
from hashlib import sha256
from importlib.resources import files


@lru_cache(maxsize=1)
def templates():
    """Retain the builder's explicit historical-data fallback when loading fails."""
    try:
        path = files("molsysmt.data.databases.peptide_builder").joinpath(
            "amber14sb.json.gz"
        )
        return json.loads(gzip.decompress(path.read_bytes()))["templates"]
    except (OSError, ValueError, KeyError, EOFError):
        return {}


@lru_cache(maxsize=None)
def reference(
    package="molsysmt.data.databases.peptide_builder",
    filename="amber14sb.json.gz",
    title="Bundled MolSysMT peptide construction data derived from AmberClassic LEaP libraries",
):
    """Identify the bundled bytes without inventing a pinned upstream revision."""
    digest = sha256(files(package).joinpath(filename).read_bytes()).hexdigest()
    return dict(
        id=f"dataset:molsysmt-peptide-builder:{digest}",
        type="dataset",
        title=title,
        url=f"https://github.com/uibcdf/molsysmt/blob/main/{package.replace('.', '/')}/{filename}",
        roles=["chemical_reference_data"],
    )


def atom_variant(name):
    """Express one exact construction layout as named atoms and edges."""
    record = templates().get(name)
    if record is None:
        return None
    names = record["atom_names"]
    return dict(
        atoms=list(names),
        bonds=[(names[a], names[b]) for a, b in record["bonds"]],
        _resource="molsysmt.data.databases.peptide_builder/amber14sb.json.gz",
    )
