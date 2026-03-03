from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.PDBFile')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native.molsys_old import MolSys
    from ..molsysmt_TopologyOld.to_molsysmt_Topology import to_molsysmt_Topology
    from ..molsysmt_StructuresOld.to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

