from molsysmt._private.smonitor import ArgumentError

# The unit kept whole when wrapping. `False` wraps every atom independently, which is
# what a simulation engine does and what leaves a molecule straddling a boundary drawn
# with bonds crossing the whole cell. A string names the element that is moved as one
# piece instead.
#
# `'molecule'` is not offered yet: the wrapping kernels reconstruct blocks from bonded
# pairs, and grouping by molecule instead needs its own partition. Adding a value to
# this list later is additive and breaks nothing — see uibcdf/molsysmt#173.
_compact_values = [
    "component",
]


def digest_compact(compact, caller=None):

    if compact is False:
        return False

    if isinstance(compact, str):
        if compact.lower() in _compact_values:
            return compact.lower()

    raise ArgumentError('compact', value=compact, caller=caller, message=None)
