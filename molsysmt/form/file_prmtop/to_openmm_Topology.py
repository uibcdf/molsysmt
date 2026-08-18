from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:prmtop')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:prmtop to openmm.Topology.

    Parameters
    ----------
    item : file:prmtop
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.Topology
        Converted molecular system representation.
    """

    from .to_openmm_AmberPrmtopFile import to_openmm_AmberPrmtopFile
    from molsysmt.form.openmm_AmberPrmtopFile.to_openmm_Topology import to_openmm_Topology as openmm_AmberPrmtopFile_to_openmm_Topology

    tmp_item = to_openmm_AmberPrmtopFile(item, skip_digestion=True)
    tmp_item = openmm_AmberPrmtopFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

