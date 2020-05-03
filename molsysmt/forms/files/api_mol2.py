from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'mol2': form_name,
    'MOL2': form_name
    }

info=["",""]

def to_parmed_Structure(item, atom_indices='all', frame_indices='all'):

    from parmed import load_file as _parmed_file_loader
    tmp_form = _parmed_file_loader(item)
    return tmp_form.to_structure()

def to_mdtraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    from mdtraj import load_mol2 as _mdtraj_load_mol2
    tmp_form = _mdtraj_load_mol2(item)
    del(_mdtraj_load_mol2)
    return tmp_form

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    from mdtraj import load_mol2 as _mdtraj_load_mol2
    tmp_form = _mdtraj_load_mol2(item).topology
    del(_mdtraj_load_mol2)
    return tmp_form

def to_openmm_Topology(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdtraj_Topology import to_openmm_Topology as mdtraj_Topology_to_openmm_Topology
    tmp_form = to_mdtraj_Topology(item, atom_indices=atom_indices, frame_indices=atom_indices)
    tmp_form = mdtraj_Topology_to_openmm_Topology(tmp_form)
    return tmp_form

def to_openmm_Modeller(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdtraj_Trajectory import to_openmm_Modeller as mdtraj_Trajectory_to_openmm_Modeller
    tmp_form = to_mdtraj_Trajectory(item, atom_indices=atom_indices, frame_indices=atom_indices)
    tmp_form = mdtraj_Trajectory_to_openmm_Modeller(tmp_form)
    return tmp_form

    #from molsysmt.forms.engines.api_parmed import to_modeller as _parmed_to_modeller
    #tmp_form = to_parmed(item)
    #tmp_form = _parmed_to_modeller(tmp_form)
    #del(_parmed_to_modeller)
    #return tmp_form

def to_pdb(item, output_file_path=None, atom_indices='all', frame_indices='all'):

    from parmed import load_file as _parmed_file_loader
    tmp_form = _parmed_file_loader(item)
    tmp_form.save(output_file_path)
    pass

def to_nglview(item, atom_indices='all', frame_indices='all'):
    from nglview import show_file as _nglview_show_file
    return _nglview_show_file(item)

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

