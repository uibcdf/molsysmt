from depdigest import dep_digest
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:prmtop')
@dep_digest('mdtraj')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):

    from mdtraj import load_prmtop

    tmp_item = load_prmtop(item)

    return tmp_item

