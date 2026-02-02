from molsysmt.dependencies import requires
from molsysmt._private.digestion import digest

@digest(form='file:prmtop')
@requires('mdtraj')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):

    from mdtraj import load_prmtop

    tmp_item = load_prmtop(item)

    return tmp_item

