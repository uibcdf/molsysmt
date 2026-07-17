from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='parmed.Structure')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    import numpy as np

    from molsysmt.native.molsys import MolSys
    from molsysmt.native import MolecularMechanics
    from molsysmt._private.variables import is_all
    from .to_molsysmt_Topology import to_molsysmt_Topology
    from .to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = MolSys()

    tmp_item.topology = to_molsysmt_Topology(item, skip_digestion=True)
    tmp_item.structures = to_molsysmt_Structures(item, skip_digestion=True)
    partial_charge = np.asarray(
        [atom.charge for atom in item.atoms], dtype=np.float64
    )
    tmp_item.molecular_mechanics = MolecularMechanics(
        partial_charge=partial_charge
    )

    if not is_all(atom_indices) or not is_all(structure_indices):
        from molsysmt.form.molsysmt_MolSys.extract import extract

        tmp_item = extract(
            tmp_item,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            skip_digestion=True,
        )

    return tmp_item
