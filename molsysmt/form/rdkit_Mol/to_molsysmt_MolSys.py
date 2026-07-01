from molsysmt._private.arg_digestion import arg_digest


@arg_digest(form='rdkit.Mol')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import MolSys, MolecularMechanics
    from molsysmt._private.variables import is_all
    from .to_molsysmt_Topology import to_molsysmt_Topology
    from .to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                 structure_indices=structure_indices, skip_digestion=True)

    formal_charge = [atom.GetFormalCharge() for atom in item.GetAtoms()]
    if not is_all(atom_indices):
        formal_charge = [formal_charge[ii] for ii in atom_indices]
    tmp_item.molecular_mechanics = MolecularMechanics(formal_charge=formal_charge)

    return tmp_item
