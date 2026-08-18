from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:prmtop')
def to_file_pdb(item, atom_indices='all', coordinates=None, output_filename=None, skip_digestion=False):
    """
    Converting from file:prmtop to file.pdb.

    Parameters
    ----------
    item : file:prmtop
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file.pdb
        Converted molecular system representation.
    """

    from .to_openmm_Topology import to_openmm_Topology
    from molsysmt.form.openmm_Topology.to_file_pdb import to_file_pdb as openmm_Topology_to_file_pdb

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = openmm_Topology_to_file_pdb(tmp_item, coordinates=coordinates, output_filename=output_filename,
                                           skip_digestion=True)

    return tmp_item

