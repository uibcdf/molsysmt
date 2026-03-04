from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.PDBFile')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from openmm.app import PDBFile
    import os

    if isinstance(item, (str, os.PathLike)):
        item = PDBFile(str(item))

    from molsysmt.form.openmm_Topology.extract import extract as extract_openmm_Topology

    tmp_item = item.topology
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item
