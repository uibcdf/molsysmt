from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Topology')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import MolSys, MolecularMechanics
    from molsysmt._private.variables import is_all
    from .get_mechanical_attributes import _partial_charges
    from .to_molsysmt_Topology import to_molsysmt_Topology
    from .to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                 structure_indices=structure_indices, skip_digestion=True)
    partial_charge = _partial_charges(item)
    if partial_charge is not None and not is_all(atom_indices):
        partial_charge = partial_charge[atom_indices]
    tmp_item.molecular_mechanics = MolecularMechanics(
        partial_charge=partial_charge
    )
    return tmp_item
