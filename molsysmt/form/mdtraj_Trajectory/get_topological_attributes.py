from molsysmt._private.argdigest import arg_digest
import types

form='mdtraj.Trajectory'

## From atom

@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_atom_id_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_atom_name_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_atom_type_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False):
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_group_index_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_component_index_from_atom(item, indices='all', skip_digestion=False):
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_component_index_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_chain_index_from_atom(item, indices='all', skip_digestion=False):
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_chain_index_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_molecule_index_from_atom(item, indices='all', skip_digestion=False):
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_molecule_index_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_entity_index_from_atom(item, indices='all', skip_digestion=False):
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_entity_index_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_inner_bonded_atoms_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_n_inner_bonds_from_atom as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

## From system

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_n_atoms_from_system as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_n_groups_from_system as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

@arg_digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_n_components_from_system as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

@arg_digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_n_chains_from_system as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

@arg_digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_n_molecules_from_system as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

@arg_digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_n_entities_from_system as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

@arg_digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):
    from molsysmt.form.mdtraj_Trajectory.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.get_topological_attributes import get_n_bonds_from_system as aux_get
    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
