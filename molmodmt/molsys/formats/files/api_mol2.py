from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'mol2': form_name,
    'MOL2': form_name
    }

def to_parmed(item):

    from parmed import load_file as _parmed_file_loader
    tmp_form = _parmed_file_loader(item)
    return tmp_form.to_structure()

def to_pdb(item,out_file):

    from parmed import load_file as _parmed_file_loader
    tmp_form = _parmed_file_loader(item)
    tmp_form.save(out_file)
    pass

def to_nglview(item):
    from nglview import show_file as _nglview_show_file
    return _nglview_show_file(item)
