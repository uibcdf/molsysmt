def to_gro(item, output_filepath=None, trajectory_item=None, atom_indices='all',
           frame_indices='all'):

    raise NotImplementedError

def from_gro(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.api_gro import to_parmed_Structure as gro_to_parmed_Structure
    from molsysmt.native.io.topology import from_parmed_Structure as parmed_Structure_to_molsysmt_Topology

    tmp_item = gro_to_parmed_Structure(item)
    tmp_item = parmed_Structure_to_molsysmt_Topology(tmp_item)

    return tmp_item

