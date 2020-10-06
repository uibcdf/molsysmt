from os.path import basename as _basename
from os import remove as _remove
from MDAnalysis import Universe as _mdanalysis_Universe

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdanalysis_Universe : form_name,
    'mdanalysis.Universe' : form_name
}

info=["",""]
with_topology=True
with_trajectory=True

def to_nglview(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from nglview import show_mdtraj as _nglview_show_mdanalysis

    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return _nglview_show_mdanalysis(tmp_item)

def to_pdb(item, output_filepath=None, trajectory_item=None, atom_indices='all', frame_indices='all', multiframe=False):

    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item.atoms.write(output_filepath, multiframe=multiframe)

def to_mdtraj_Trajectory (item, trajectory_item=None, atom_indices='all', frame_indices='all', multiframe=False):

    from molsysmt.utils.pdb import tmp_pdb_filename
    from molsysmt.forms.files.api_pdb import to_mdtraj_Trajectory as pdb_to_mdtraj_Trajectory

    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_file = tmp_pdb_filename()
    to_pdb(tmp_item=item, output_filepath=tmp_file, multiframe=multiframe)
    tmp_item=pdb_to_mdtraj_Trajectory(tmp_file)
    _remove(tmp_file)

    return tmp_item

def select_with_MDTraj(item, selection):

    tmp_form=to_mdtraj(item,multiframe=True)

    return tmp_form.topology.select(selection)

def select_with_MDAnalysis(item, selection):

    tmp_atomgroup=item.select_atoms(selection)
    tmp_sel = tmp_atomgroup.atoms.ids
    del(tmp_atomgroup)

    return tmp_sel

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

###### Get

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

