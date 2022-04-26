from molsysmt._private.digestion import digest_item, digest_atom_indices

def to_molsysmt_Topology(item, atom_indices='all', check=True):

    if check:

        digest_item(item, 'file:msmpk')
        atom_indices = digest_atom_indices(atom_indices)

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item = molsysmt_MolSys_to_molsysmt_Topology(tmp_item, check=False)

    return tmp_item

