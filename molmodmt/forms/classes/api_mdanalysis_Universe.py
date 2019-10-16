from os.path import basename as _basename
from os import remove as _remove
from MDAnalysis import Universe as _mdanalysis_Universe

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdanalysis_Universe : form_name,
    'mdanalysis.Universe' : form_name
}

def to_nglview(item, atom_indices=None, frame_indices=None):

    from nglview import show_mdtraj as _nglview_show_mdanalysis
    return _nglview_show_mdanalysis(item)

def to_pdb(item, atom_indices=None, frame_indices=None, output_file=None, multiframe=False):

    item.atoms.write(output_file, multiframe=multiframe)

    pass

def to_MDTraj(item, atom_indices=None, frame_indices=None, multiframe=False):

    import tempfile as _tempfile
    from molmodmt.forms.files.api_pdb import to_mdtraj as _pdb_to_mdtraj
    output_file=_tempfile.NamedTemporaryFile(suffix=".pdb").name
    to_pdb(item,output_file,multiframe)
    tmp_form=_pdb_to_mdtraj(output_file)
    _remove(output_file)

    return tmp_form

def select_with_MDTraj(item, selection):

    tmp_form=to_mdtraj(item,multiframe=True)

    return tmp_form.topology.select(selection)

def select_with_MDAnalysis(item, selection):

    tmp_atomgroup=item.select_atoms(selection)
    tmp_sel = tmp_atomgroup.atoms.ids
    del(tmp_atomgroup)

    return tmp_sel

###### Get

## system

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import _get_form
    return _get_form(item)

