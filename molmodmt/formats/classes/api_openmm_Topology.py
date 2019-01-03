from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={}

def to_native(item):

    from molsysmt import Native as _molsysmt_native
    tmp_form = _molsysmt_native(item)
    del(_molsysmt_native)
    return tmp_form

def to_mdtraj_Topology(item):

    from mdtraj.Topology import from_openmm as _mdtraj_Topology_from_openmm
    tmp_form = _mdtraj_Topology_from_openmm(item)
    del(_mdtraj_Topology_from_openmm)
    return tmp_form

def to_parmed_Structure(item):

    from parmed.openmm import load_topology as _openmm_Topology_to_parmed_Estructure

    tmp_form = _openmm_Topology_to_parmed_Estructure(item)
    del(_openmm_Topology_to_parmed_Estructure)
    return tmp_form

def to_yank_Topography(item):

    from yank import Topography as _yank_Topography
    tmp_form = _yank_Topography(item)
    del(_yank_Topography)
    return tmp_form
