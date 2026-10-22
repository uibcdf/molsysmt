import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_bonded_atom_pairs(
    bonded_atom_pairs, caller=None, native_topology_bonds=False
):

    if native_topology_bonds:
        try:
            values = np.asarray(bonded_atom_pairs)
            booleans = any(
                isinstance(value, (bool, np.bool_))
                for value in np.asarray(bonded_atom_pairs, dtype=object).flat
            )
            if values.shape in {(0,), (0, 2)}:
                return np.empty((0, 2), dtype=np.int64)
            if (
                values.ndim == 2
                and values.shape[1] == 2
                and values.dtype.kind in "iu"
                and not booleans
            ):
                return values
        except (TypeError, ValueError):
            pass
        raise ArgumentError("bonded_atom_pairs", value=bonded_atom_pairs, caller=caller)

    if caller == "molsysmt.basic.get.get":
        if isinstance(bonded_atom_pairs, bool):
            return bonded_atom_pairs
    elif caller == "molsysmt.basic.compare.compare":
        if isinstance(bonded_atom_pairs, bool):
            return bonded_atom_pairs
    elif caller.endswith("add_bonds.add_bonds"):
        if isinstance(bonded_atom_pairs, list):
            for sublist in bonded_atom_pairs:
                if not (isinstance(sublist, list) and len(sublist) == 2):
                    raise ArgumentError(
                        "bonded_atom_pairs",
                        value=bonded_atom_pairs,
                        caller=caller,
                        message=None,
                    )
                if not all(isinstance(item, (int, np.integer)) for item in sublist):
                    raise ArgumentError(
                        "bonded_atom_pairs",
                        value=bonded_atom_pairs,
                        caller=caller,
                        message=None,
                    )
            return np.array(bonded_atom_pairs)
        elif isinstance(bonded_atom_pairs, np.ndarray):
            if len(bonded_atom_pairs.shape) == 2 and bonded_atom_pairs.shape[1] == 2:
                return bonded_atom_pairs
            else:
                raise ArgumentError(
                    "bonded_atom_pairs",
                    value=bonded_atom_pairs,
                    caller=caller,
                    message=None,
                )

    raise ArgumentError(
        "bonded_atom_pairs", value=bonded_atom_pairs, caller=caller, message=None
    )
