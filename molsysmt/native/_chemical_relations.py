"""Project stored bond endpoints without stable topology or graph perception."""

import numpy as np

from molsysmt._private.variables import is_all


def relation(item, element, attribute, selected="all"):
    """Read selected edges/participants under the same native/dictionary scope."""
    from .chemical_states_dict import ChemicalStatesDict

    if isinstance(item, ChemicalStatesDict):
        from ._chemical_dict_queries import _pairs, _positions, _state

        pairs = _pairs(item, _state(item))
        positions = None if is_all(selected) else _positions(item, element, selected)
    else:
        from ._chemical_queries import indices

        pairs = (
            item._resolve_chemical_state()
            .bonds[["atom1_index", "atom2_index"]]
            .to_numpy(dtype=np.int64)
        )
        positions = None if is_all(selected) else indices(item, element, selected)
    if positions is None and not is_all(selected):
        return None
    if element == "bond" and positions is not None:
        pairs = pairs[positions]
    elif element == "atom" and positions is not None:
        mask = np.isin(pairs, positions)
        pairs = pairs[
            mask.all(axis=1) if attribute.startswith("inner_") else mask.any(axis=1)
        ]
    if attribute == "bonded_atoms":
        return np.unique(pairs).tolist()
    return pairs.tolist()
