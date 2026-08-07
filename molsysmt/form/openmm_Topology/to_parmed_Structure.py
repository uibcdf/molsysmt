from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Topology')
def to_parmed_Structure(item, atom_indices='all', skip_digestion=False):

    from parmed.openmm import load_topology as openmm_Topology_to_parmed_Structure
    from .extract import extract

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)
    tmp_item = openmm_Topology_to_parmed_Structure(tmp_item)
    return tmp_item

