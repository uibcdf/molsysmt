from molsysmt._private.digestion import digest

@digest(form='mmtf.MMTFDecoder')
def to_string_pdb_text(item, atom_indices='all', structure_indices='all'):

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_string_pdb_text as molsysmt_MolSys_to_string_pdb_text

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices,
            structure_indices=structure_indices)
    tmp_item = molsysmt_MolSys_to_string_pdb_text(tmp_item)

    return tmp_item

def _to_string_pdb_text(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices)


