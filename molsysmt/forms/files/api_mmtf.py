from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'mmtf': form_name
    }

info=["",""]
with_topology=True
with_trajectory=True

def to_mmtf_MMTFDecoder(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import extract as extract_mmtf_MMTFDecoder
    from mmtf import parse
    tmp_item = parse(item)
    tmp_item = extract_mmtf_MMTFDecoder(tmp_item, atom_indices='all', frame_indices='all')
    return tmp_item

def to_molsysmt_MolSys(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import to_molsysmt_MolSys as mmtf_MMTFDecoder_to_molsysmt_MolSys
    tmp_item = to_mmtf_MMTFDecoder(item, atom_indices='all', frame_indices='all')
    tmp_item = mmtf_MMTFDecoder_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Topology(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import to_molsysmt_Topology as mmtf_MMTFDecoder_to_molsysmt_Topology
    tmp_item = to_mmtf_MMTFDecoder(item, atom_indices='all', frame_indices='all')
    tmp_item = mmtf_MMTFDecoder_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Trajectory(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import to_molsysmt_Trajectory as mmtf_MMTFDecoder_to_molsysmt_Trajectory
    tmp_item = to_mmtf_MMTFDecoder(item, atom_indices='all', frame_indices='all')
    tmp_item = mmtf_MMTFDecoder_to_molsysmt_Trajectory(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_aminoacids1_seq(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import to_aminoacids1_seq as molsysmt_Topology_to_aminoacids1_seq
    tmp_item = to_molsysmt_Topology(item, atom_indices=atom_indices)
    tmp_item = molsysmt_Topology_to_aminoacids1_seq(tmp_item)
    return tmp_item

def to_mdanalysis_Universe(item, atom_indices='all', frame_indices='all'):

    from MDAnalysis import Universe
    from molsysmt.forms.classes.api_mdanalysis_Universe import extract as extract_mdanalysis_Universe

    tmp_item = Universe(item)
    tmp_item = extract_mdanalysis_Universe(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def select_with_MDAnalysis(item, selection):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import select_with_MDTraj as select_mmtf_MMTFDecoder_with_MDTraj
    tmp_item = to_mmtf_MMTFDecoder(item)
    return select_mmtf_MMTFDecoder_with_MDTraj(tmp_item, selection)

def select_with_MolSysMT(item, selection):

    from molsysmt.forms.classes.api_mmtf_MMTFDecoder import select_with_MolSysMT as select_mmtf_MMTFDecoder_with_MolSysMT
    tmp_item = to_mmtf_MMTFDecoder(item)
    return select_mmtf_MMTFDecoder_with_MolSysMT(tmp_item, selection)

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

##### Get

# System

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    from mmtf import parse
    tmp_item=parse(filename)
    n_frames = tmp_item.num_models
    del(tmp_item)
    return n_frames

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    from mmtf import parse
    tmp_item=parse(filename)
    n_atoms = tmp_item.num_atoms
    del(tmp_item)
    return n_atoms

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

