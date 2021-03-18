def to_gro(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filepath=None):

    raise NotImplementedError

def from_gro(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.files.api_gro import to_parmed_Structure as gro_to_parmed_Structure
    from molsysmt.native.io.topology.classes import from_parmed_Structure as parmed_Structure_to_molsysmt_Topology

    tmp_item = gro_to_parmed_Structure(item)
    tmp_item = parmed_Structure_to_molsysmt_Topology(tmp_item)

    return tmp_item

