from molsysmt._private.digestion import digest

@digest(form='pdbfixer.PDBFixer')
def to_molsysmt_MolSysOld(item, atom_indices='all', structure_indices='all'):

    from molsysmt.native.molsys_old import MolSysOld
    from . import to_molsysmt_TopologyOld
    from . import to_molsysmt_StructuresOld as pdbfixer_PDBFixer_to_molsysmt_StructuresOld

    tmp_item = MolSysOld()

    tmp_item.topology = to_molsysmt_TopologyOld(item, atom_indices=atom_indices)
    tmp_item.structures = pdbfixer_PDBFixer_to_molsysmt_StructuresOld(item, atom_indices=atom_indices)

    return tmp_item

