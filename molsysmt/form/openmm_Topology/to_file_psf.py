from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Topology')
def to_file_psf(item, atom_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from openmm.Topology to file.psf.

    Parameters
    ----------
    item : openmm.Topology
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file.psf
        Converted molecular system representation.
    """

    from molsysmt.form.parmed_Structure.to_parmed_Structure import to_parmed_Structure as openmm_Topology_to_parmed_Structure
    from molsysmt.form.parmed_Structure.to_file_psf import to_file_psf as openmm_Structure_to_file_psf

    tmp_item = openmm_Topology_to_parmed_Structure(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = openmm_Structure_to_file_psf(tmp_item, output_filename=output_filename, skip_digestion=True)

    return tmp_item

