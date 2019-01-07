from os.path import basename as _basename
from os import remove as _remove

form_name=_basename(__file__).split('.')[0][4:].replace('_',':')

is_form = {
    'pdb:id': form_name,
    'PDB:id': form_name
    }

def to_pdb(form_id,output_file=None):
    from molmodmt.utils.miscellanea import download_pdb as _download_pdb
    return _download_pdb(form_id.split(':')[-1],output_file)

def to_native_Native(form_id):
    from molmodmt.formats.files.api_pdb import to_native_Native as _pdb_to_native_Native
    tmp_file = to_pdb(form_id)
    tmp_form = _pdb_to_native_Native(tmp_file)
    _remove(tmp_file)
    del(_pdb_to_native_Native)
    return tmp_form

def to_mdtraj_Topology(form_id):
    from molmodmt.formats.files.api_pdb import to_mdtraj_Topology as _pdb_to_mdtraj_Topology
    _tmp_file=to_pdb(form_id)
    _tmp_form=_pdb_to_mdtraj_Topology(_tmp_file)
    _remove(_tmp_file)
    del(_pdb_to_mdtraj_Topology)
    return _tmp_form

def to_mdtraj(form_id):
    from molmodmt.utils.miscellanea import download_pdb as _download_pdb
    from molmodmt.formats.files.api_pdb import to_mdtraj as _pdb_to_mdtraj
    _tmp_file=_download_pdb(form_id.split(':')[-1])
    _tmp_form=_pdb_to_mdtraj(_tmp_file)
    _remove(_tmp_file)
    return _tmp_form

def to_parmed_Structure(form_id):
    from molmodmt.formats.files.api_pdb import to_parmed_Structure as _pdb_to_parmed_Structure
    _tmp_file=to_pdb(form_id)
    _tmp_form=_pdb_to_parmed_Structure(_tmp_file)
    _remove(_tmp_file)
    del(_pdb_to_parmed_Structure)
    return _tmp_form

def to_parmed(form_id):
    return to_parmed_Structure(form_id)

def to_pdbfixer_PDBFixer(form_id):
    return to_pdbfixer(form_id)

def to_pdbfixer(form_id):
    from molmodmt.utils.miscellanea import download_pdb as _download_pdb
    from pdbfixer.pdbfixer import PDBFixer as _pdbfixer_loader
    _tmp_file=_download_pdb(form_id.split(':')[-1])
    _tmp_form=_pdbfixer_loader(_tmp_file)
    _remove(_tmp_file)
    return _tmp_form

def to_yank_Topography(form_id):
    from molmodmt.formats.files.api_pdb import to_yank_Topography as _pdb_to_yank_Topography
    _tmp_file=to_pdb(form_id)
    _tmp_form=_pdb_to_yank_Topography(_tmp_file)
    _remove(_tmp_file)
    del(_pdb_to_yank_Topography)
    return _tmp_form

def to_mdanalysis(form_id):
    from molmodmt.formats.files.api_pdb import to_mdanalysis as _pdb_to_mdanalysis
    _tmp_file=to_pdb(form_id)
    _tmp_form=_pdb_to_mdanalysis(_tmp_file)
    _remove(_tmp_file)
    del(_pdb_to_mdanalysis)
    return _tmp_form


def to_nglview(form_id):
    # from nglview import show_pdbid as _nglview_show_pdbid
    # return _nglview_show_pdbid(form_id.split(':')[-1])
    from molmodmt.utils.miscellanea import download_pdb as _download_pdb
    from nglview import show_file as _nglview_show_file
    tmp_pdb_file = _download_pdb(form_id.split(':')[-1])
    tmp_view = _nglview_show_file(tmp_pdb_file)
    _remove(tmp_pdb_file)
    return tmp_view

def select_with_mdtraj(item, selection):
    tmp_form=to_mdtraj(item)
    tmp_sel=tmp_form.topology.select(selection)
    del(tmp_form)
    return tmp_sel
