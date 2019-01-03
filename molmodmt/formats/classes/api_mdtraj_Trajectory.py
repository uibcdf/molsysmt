from os.path import basename as _basename
from mdtraj.core.trajectory import Trajectory as _mdtraj_Trajectory

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_Trajectory:form_name
    }

def to_native_Native(item):

    from molsysmt.native import Native as _Native
    tmp_form = _Native(item)
    del(_Native)
    return tmp_form

def to_mdtraj_Topology(item):

    return item.topology

def to_openmm_Topology(item):

    from .api_mdtraj_Topology import to_openmm_Topology as _mdtraj_Topology_to_openmm_Topology

    tmp_form = to_mdtraj_Topology(item)
    tmp_form = _mdtraj_Topology_to_openmm_Topology(tmp_form)
    del(_mdtraj_Topology_to_openmm_Topology)
    return tmp_form

def to_yank_Topography(item):

    from .api_openmm_Topology import to_yank_Topography as _openmm_Topology_to_yank_Topography

    tmp_form = to_openmm_Topology(item)
    tmp_form = _openmm_Topology_to_yank_Topography(tmp_form)
    del(_openmm_Topology_to_yank_Topography)
    return tmp_form

def to_parmed_Structure(item):

    from .api_openmm_Topology import to_parmed_Structure as _openmm_Topology_to_parmed_Structure

    tmp_form = to_openmm_Topology(item)
    tmp_form = _openmm_Topology_to_parmed_Structure(tmp_form)
    del(_openmm_Topology_to_parmed_Structure)
    return tmp_form

def to_pdb(item,output_file):

    return item.save(output_file)

def to_nglview(item):

    from nglview import show_mdtraj as _show_mdtraj
    tmp_view = _show_mdtraj(item)
    return tmp_view

def get_shape(item):

    return item.n_frames, item.n_atoms

def select_with_mdtraj(item, selection):

    return item.topology.select(selection)
