from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:prmtop')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import MolSys
    from .to_molsysmt_Topology import to_molsysmt_Topology

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    # Note: prmtop only has topology, so we return a MolSys without structures unless they are added later
    # but we can initialize an empty structures object.
    from molsysmt.native import Structures
    tmp_item.structures = Structures()

    return tmp_item
