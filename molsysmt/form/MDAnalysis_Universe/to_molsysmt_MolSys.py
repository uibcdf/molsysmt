from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='MDAnalysis.Universe')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native.molsys import MolSys
    from .to_molsysmt_Topology import to_molsysmt_Topology
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt._private.variables import is_all
    import numpy as np

    if not is_all(atom_indices):
        atom_indices = np.unique(np.asarray(atom_indices, dtype=np.int64))

    tmp_item = MolSys()

    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices, skip_digestion=True)

    return tmp_item
