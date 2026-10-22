"""Normalize assembly operations independently of coordinate/structure axes."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError

functions_where_boolean = (
    "molsysmt.basic.get.get",
    "molsysmt.basic.compare.compare",
    "molsysmt.basic.iterator.__init__",
    ".iterators.__init__",
)


def _chain_set(values):
    if not isinstance(values, (np.ndarray, list, tuple)):
        raise ValueError("Assembly chain indices must be integer sequences.")
    array = np.asarray(values)
    if array.ndim != 1 or (array.size and array.dtype.kind not in "iu"):
        raise ValueError("Assembly chain indices must be one-dimensional integers.")
    if any(isinstance(value, (bool, np.bool_)) for value in values):
        raise ValueError("Assembly chain indices cannot be boolean.")
    if np.any(array < 0) or (
        array.dtype.kind == "u" and np.any(array > np.iinfo(np.int64).max)
    ):
        raise ValueError("Assembly chain indices must be nonnegative int64 values.")
    return array.astype(np.int64, copy=True)


def _operation(assembly):
    from .rotations import digest_rotations
    from .translations import digest_translations

    if not isinstance(assembly, dict) or set(assembly) != {
        "chain_indices",
        "rotations",
        "translations",
    }:
        raise ValueError(
            "An assembly requires chain_indices, rotations and translations."
        )
    rotations = digest_rotations(assembly["rotations"], caller="digest_bioassembly")
    translations = digest_translations(
        assembly["translations"], caller="digest_bioassembly"
    )
    if len(rotations) != len(translations):
        raise ValueError("Assembly rotation and translation counts must match.")
    chains = assembly["chain_indices"]
    if not isinstance(chains, (np.ndarray, list, tuple)):
        raise ValueError("Assembly chain indices must be a sequence.")
    if len(chains) and isinstance(chains[0], (np.ndarray, list, tuple)):
        if len(chains) != len(rotations):
            raise ValueError(
                "Per-operation chain scopes must match the operation count."
            )
        chains = [_chain_set(values) for values in chains]
    else:
        chains = _chain_set(chains)
    return {
        "chain_indices": chains,
        "rotations": rotations,
        "translations": translations,
    }


def digest_bioassembly(bioassembly, caller=None):
    if caller is not None and caller.endswith(functions_where_boolean):
        if isinstance(bioassembly, bool):
            return bioassembly
        raise ArgumentError("bioassembly", value=bioassembly, caller=caller)
    if bioassembly is None:
        return None
    single = caller == "molsysmt.build.make_bioassembly.make_bioassembly"
    if single and isinstance(bioassembly, str):
        return bioassembly
    try:
        if single:
            return _operation(bioassembly)
        if not isinstance(bioassembly, dict):
            raise ValueError("Bioassemblies must be a mapping of names to operations.")
        result = {}
        for name, assembly in bioassembly.items():
            name = str(name)
            if not name or name in result:
                raise ValueError(
                    "Assembly names must be nonempty and unique as strings."
                )
            result[name] = _operation(assembly)
        return result
    except (TypeError, ValueError, OverflowError) as error:
        raise ArgumentError(
            "bioassembly", value=bioassembly, caller=caller, message=str(error)
        ) from error
