"""Stage one typed-state mutation using the existing native assignment boundary."""

from ._chemical_dict_queries import header
from ._chemical_scope import active_index
from .chemical_states_dict import (
    ChemicalStatesDict,
    _decode_chemical_states,
    _encode_chemical_states,
)


def assign(item, operation, indices, value):
    """Publish one encoded state only after native validation and staging succeed."""
    from molsysmt.form.molsysmt_ChemicalStates import set as setters

    data, _, _, _ = header(item)
    index = item._resolve_index(active_index(item))
    # Unrequested records remain opaque and shared. The selected codec owns all
    # typed validation; the native setter owns chemistry and field semantics.
    selected = {
        **data,
        "states": [data["states"][index]],
        "reference_chemical_state_index": 0,
    }
    native = _decode_chemical_states(ChemicalStatesDict(selected))
    getattr(setters, operation)(
        native, indices=indices, value=value, skip_digestion=True
    )
    record = _encode_chemical_states(native).data["states"][0]
    records = list(data["states"])
    records[index] = {**data["states"][index], **record}
    item.data = {**data, "states": records}
