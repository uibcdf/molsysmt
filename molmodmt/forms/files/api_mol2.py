from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'mol2': form_name,
    'MOL2': form_name
    }

def to_parmed_Structure(item, atom_indices=None, frame_indices=None):

    from parmed import load_file as _parmed_file_loader
    tmp_form = _parmed_file_loader(item)
    return tmp_form.to_structure()

def to_mdtraj_Trajectory(item, atom_indices=None, frame_indices=None):

    from mdtraj import load_mol2 as _mdtraj_load_mol2
    tmp_form = _mdtraj_load_mol2(item)
    del(_mdtraj_load_mol2)
    return tmp_form

def to_openmm_Modeller(item, atom_indices=None, frame_indices=None):

    from molmodmt.forms.engines.api_parmed import to_modeller as _parmed_to_modeller
    tmp_form = to_parmed(item)
    tmp_form = _parmed_to_modeller(tmp_form)
    del(_parmed_to_modeller)
    return tmp_form

def to_pdb(item, out_file, atom_indices=None, frame_indices=None):

    from parmed import load_file as _parmed_file_loader
    tmp_form = _parmed_file_loader(item)
    tmp_form.save(out_file)
    pass

def to_nglview(item, atom_indices=None, frame_indices=None):
    from nglview import show_file as _nglview_show_file
    return _nglview_show_file(item)

###### Get

## system

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import get_form
    return get_form(item)

