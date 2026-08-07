from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.PDBFile')
def to_molsysmt_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from openmm.app import PDBFile
    import os

    if isinstance(item, (str, os.PathLike)):
        item = PDBFile(str(item))

    from molsysmt.form.openmm_Topology.to_molsysmt_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = item.topology
    tmp_item = openmm_Topology_to_molsysmt_Topology(
        tmp_item,
        atom_indices=atom_indices,
        skip_digestion=True,
    )

    return tmp_item
