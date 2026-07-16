from molsysmt._private.arg_digestion import arg_digest


@arg_digest(form='openff.Molecule')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import MolSys, MolecularMechanics
    from molsysmt._private.variables import is_all
    from .to_molsysmt_Topology import to_molsysmt_Topology
    from .to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                 structure_indices=structure_indices, skip_digestion=True)

    partial_charge = []
    charges = getattr(item, "partial_charges", None)
    has_partial_charge = False
    if charges is not None:
        try:
            partial_charge = list(charges.m)
            has_partial_charge = True
        except Exception:
            try:
                partial_charge = list(charges)
                has_partial_charge = True
            except Exception:
                partial_charge = []
                has_partial_charge = False

    if not is_all(atom_indices):
        if has_partial_charge:
            partial_charge = [partial_charge[ii] for ii in atom_indices]

    kwargs = {}
    if has_partial_charge:
        kwargs["partial_charge"] = partial_charge
    tmp_item.molecular_mechanics = MolecularMechanics(**kwargs)

    return tmp_item
