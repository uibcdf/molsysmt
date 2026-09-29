from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.ChemicalStatesDict")
def get_n_atoms_from_system(item, skip_digestion=False):
    """Getting the atom-domain size from typed chemical-state columns."""

    return item.data["n_atoms"]


@arg_digest(form="molsysmt.ChemicalStatesDict")
def get_n_chemical_states_from_system(item, skip_digestion=False):
    """Getting the number of typed chemical-state records."""

    return len(item.data["states"])


@arg_digest(form="molsysmt.ChemicalStatesDict")
def get_reference_chemical_state_index_from_system(item, skip_digestion=False):
    """Getting the reference chemical-state index from typed columns."""

    index = item.data["reference_chemical_state_index"]
    return 0 if index is None and len(item.data["states"]) == 1 else index
