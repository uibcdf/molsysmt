from molsysmt._private.argdigest import arg_digest
from molsysmt.native._chemical_fields import (
    ATOM_FIELDS,
    BOND_FIELDS,
    COMPONENT_FIELDS,
    has_field,
)


@arg_digest(form="molsysmt.ChemicalStates")
def has_attribute(
    molecular_system, attribute, include_none=False, skip_digestion=False
):
    """Checking whether a chemical-state attribute is available."""

    from .attributes import attributes

    if not attributes[attribute]:
        return False
    if attribute == "reference_chemical_state_index":
        return (
            include_none or molecular_system.reference_chemical_state_index is not None
        )
    if attribute in {"n_atoms", "n_chemical_states"}:
        return True
    if include_none:
        return True
    if attribute == "chemical_state_index":
        return molecular_system.n_chemical_states > 0
    if attribute == "chemical_state_id":
        return any(state.state_id is not None for state in molecular_system._states)
    if attribute == "atom_index":
        return molecular_system.n_atoms > 0
    if not molecular_system.n_chemical_states:
        return False
    state = molecular_system._resolve_chemical_state()
    if (
        attribute in ATOM_FIELDS
        or attribute in BOND_FIELDS
        or attribute in COMPONENT_FIELDS
    ):
        return bool(has_field(state, attribute))
    if attribute == "bond_index":
        return len(state.bonds) > 0
    if attribute == "component_index":
        return bool(len(state.components) > 0 or state.component_indices.notna().any())
    return True
