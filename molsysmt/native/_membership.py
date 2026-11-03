"""Pack positional children by parent without inventing missing memberships."""

import numpy as np


def pack(parents, count):
    """Group nonmissing in-range parent links, preserving child order per parent."""
    valid = np.flatnonzero((parents >= 0) & (parents < count))
    order = valid[np.argsort(parents[valid], kind="stable")]
    offsets = np.concatenate(
        ([0], np.cumsum(np.bincount(parents[valid], minlength=count)))
    )
    return offsets, order


def lookup(index, packed):
    """Return the child positions of one validated parent, including empty rows."""
    offsets, children = packed
    return children[offsets[index] : offsets[index + 1]]
