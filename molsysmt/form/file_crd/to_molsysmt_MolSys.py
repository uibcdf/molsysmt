from molsysmt._private.digestion import digest

@digest(form='file:crd')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all'):
 
    from molsysmt.native.io.molsys import from_crd as crd_to_molsysmt_MolSys
 
    tmp_item, tmp_molecular_system = crd_to_molsysmt_MolSys(item, molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)
 
    return tmp_item, tmp_molecular_system

