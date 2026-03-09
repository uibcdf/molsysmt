from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.PDBFile')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all', get_missing_bonds=True, skip_digestion=False):

    from openmm.app import PDBFile
    import os
    from io import StringIO

    if isinstance(item, str):
        is_file = False
        if len(item) < 1024:
            try:
                if os.path.isfile(item):
                    is_file = True
            except:
                pass
        
        if is_file:
            item = PDBFile(item)
        else:
            item = PDBFile(StringIO(item))
    elif isinstance(item, os.PathLike):
        item = PDBFile(str(item))

    from molsysmt.form.openmm_Topology.extract import extract as extract_openmm_Topology
    from molsysmt.form.openmm_Topology.to_molsysmt_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = item.topology
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False, skip_digestion=True)

    # Note: If we are converting from openmm.PDBFile to openmm.Topology, we already have it.
    # But usually this is called from convert to molsysmt.Topology.
    
    return tmp_item
