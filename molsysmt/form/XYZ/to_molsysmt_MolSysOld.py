from molsysmt._private.digestion import digest

@digest(form='XYZ')
def to_molsysmt_MolSysOld(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native.molsys_old import MolSysOld
    from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
    from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
    from .to_molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanics

    tmp_item = MolSysOld()
    tmp_item.topology = to_molsysmt_TopologyOld(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item.structures = to_molsysmt_StructuresOld(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices, skip_digestion=True)
    tmp_item.molecular_mechanics = to_molsysmt_MolecularMechanics(item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

