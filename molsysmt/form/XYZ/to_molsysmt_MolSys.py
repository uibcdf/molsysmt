from molsysmt._private.argdigest import arg_digest

@arg_digest(form='XYZ')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from XYZ to molsysmt.MolSys.

    Parameters
    ----------
    item : XYZ
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolSys
        Converted molecular system representation.
    """

    from molsysmt.native.molsys import MolSys
    from .to_molsysmt_Topology import to_molsysmt_Topology
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from .to_molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanics

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices, skip_digestion=True)
    tmp_item.molecular_mechanics = to_molsysmt_MolecularMechanics(item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

