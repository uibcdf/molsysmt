from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.ChemicalStates")
def get_n_atoms_from_system(item, skip_digestion=False):
    """Getting the atom-domain size from chemical states."""

    return item.n_atoms


@arg_digest(form="molsysmt.ChemicalStates")
def get_n_chemical_states_from_system(item, skip_digestion=False):
    """Getting the number of chemical states."""

    return item.n_chemical_states


@arg_digest(form="molsysmt.ChemicalStates")
def get_reference_chemical_state_index_from_system(item, skip_digestion=False):
    """Getting the reference chemical-state index."""

    return item.reference_chemical_state_index
