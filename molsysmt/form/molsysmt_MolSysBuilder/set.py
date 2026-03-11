from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

form = "molsysmt.MolSysBuilder"


@arg_digest(form=form)
def set_atom_name_to_atom(item, indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Topology.set import set_atom_name_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_atom_id_to_atom(item, indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Topology.set import set_atom_id_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_atom_type_to_atom(item, indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Topology.set import set_atom_type_to_atom as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_group_name_to_group(item, indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Topology.set import set_group_name_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_group_id_to_group(item, indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Topology.set import set_group_id_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_group_type_to_group(item, indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Topology.set import set_group_type_to_group as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_chain_name_to_chain(item, indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Topology.set import set_chain_name_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_chain_id_to_chain(item, indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Topology.set import set_chain_id_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_chain_type_to_chain(item, indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Topology.set import set_chain_type_to_chain as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_molecule_name_to_molecule(item, indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Topology.set import set_molecule_name_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_molecule_id_to_molecule(item, indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Topology.set import set_molecule_id_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_molecule_type_to_molecule(item, indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Topology.set import set_molecule_type_to_molecule as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_entity_name_to_entity(item, indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Topology.set import set_entity_name_to_entity as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_entity_id_to_entity(item, indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Topology.set import set_entity_id_to_entity as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_entity_type_to_entity(item, indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Topology.set import set_entity_type_to_entity as aux_set

    return aux_set(item.topology, indices=indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_coordinates_to_atom(item, indices="all", structure_indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Structures.set import set_coordinates_to_atom as aux_set

    if is_all(indices):
        n_atoms = item.topology.n_atoms
        if n_atoms != value.shape[1]:
            raise ValueError("Coordinates has a different atoms number.")

    return aux_set(
        item.structures,
        indices=indices,
        structure_indices=structure_indices,
        value=value,
        skip_digestion=True,
    )


@arg_digest(form=form)
def set_coordinates_to_system(item, indices="all", structure_indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Structures.set import set_coordinates_to_system as aux_set

    return aux_set(
        item.structures,
        indices=indices,
        structure_indices=structure_indices,
        value=value,
        skip_digestion=True,
    )


@arg_digest(form=form)
def set_box_to_system(item, structure_indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Structures.set import set_box_to_system as aux_set

    return aux_set(item.structures, structure_indices=structure_indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_time_to_system(item, structure_indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Structures.set import set_time_to_system as aux_set

    return aux_set(item.structures, structure_indices=structure_indices, value=value, skip_digestion=True)


@arg_digest(form=form)
def set_structure_id_to_system(item, structure_indices="all", value=None, skip_digestion=False):
    from ..molsysmt_Structures.set import set_structure_id_to_system as aux_set

    return aux_set(item.structures, structure_indices=structure_indices, value=value, skip_digestion=True)
