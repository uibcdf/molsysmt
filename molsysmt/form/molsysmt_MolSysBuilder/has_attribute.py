from molsysmt._private.arg_digestion import arg_digest


@arg_digest(form="molsysmt.MolSysBuilder")
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):

    from .attributes import attributes

    output = attributes[attribute]

    if not include_none:
        if attribute in ["atom_index", "atom_id", "atom_name", "atom_type", "group_index"]:
            output = molecular_system.n_atoms > 0
        elif attribute in ["group_id", "group_name", "group_type", "molecule_index"]:
            output = molecular_system.n_groups > 0
        elif attribute in ["chain_id", "chain_name", "chain_type"]:
            output = molecular_system.n_chains > 0
        elif attribute in ["chain_index"]:
            output = molecular_system.n_atoms > 0 or molecular_system.n_groups > 0
        elif attribute in ["molecule_id", "molecule_name", "molecule_type"]:
            output = molecular_system.n_molecules > 0
        elif attribute in ["entity_index"]:
            output = molecular_system.n_molecules > 0
        elif attribute in ["entity_id", "entity_name", "entity_type"]:
            output = molecular_system.n_entities > 0
        elif attribute in ["n_atoms", "n_groups", "n_bonds", "n_molecules", "n_chains", "n_entities"]:
            output = True
        elif attribute in ["coordinates", "time", "box", "structure_id", "n_structures"]:
            output = molecular_system.n_structures > 0 or attribute == "n_structures"
        elif attribute == "bonded_atom_pairs":
            output = molecular_system.n_bonds > 0

    return output
