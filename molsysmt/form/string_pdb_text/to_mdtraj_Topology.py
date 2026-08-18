from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='string:pdb_text')
@dep_digest('mdtraj')
def to_mdtraj_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from string:pdb_text to mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Topology
        Resulting object in mdtraj.Topology form.


    .. versionadded:: 1.0.0
    """

    from mdtraj import load_topology as mdtraj_load_topology

    from io import StringIO
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    tmp_io = StringIO()
    tmp_io.write(tmp_item)
    tmp_io.close()

    tmp_item = mdtraj_load_topology(tmp_io)

    return tmp_item
