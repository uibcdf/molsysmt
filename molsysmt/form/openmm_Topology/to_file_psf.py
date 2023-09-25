from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_file_psf(item, atom_indices='all', output_filename=None):

    from .to_parmed_Structure import to_parmed_Structure as openmm_Topology_to_parmed_Structure
    from ..parmed_Structure.to_file_psf import to_file_psf as openmm_Structure_to_file_psf

    tmp_item = openmm_Topology_to_parmed_Structure(item, atom_indices=atom_indices)
    tmp_item = openmm_Structure_to_file_psf(tmp_item, output_filename=output_filename)

    return tmp_item

