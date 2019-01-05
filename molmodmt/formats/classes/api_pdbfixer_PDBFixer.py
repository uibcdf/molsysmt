from os.path import basename as _basename
from pdbfixer.pdbfixer import PDBFixer as _pdbfixer_PDBFixer

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _pdbfixer_PDBFixer : form_name
}

def to_nglview(item):

    from nglview import show_mdtraj as _nglview_show_mdtraj
    from molmodmt.formats.engines.api_pdbfixer import to_mdtraj as _pdbfixer_to_mdtraj
    return _nglview_show_mdtraj(_pdbfixer_to_mdtraj(item))

def to_native_Native(item):

    from molsysmt.native import Native as _native_Native
    tmp_form = _native_Native(item)
    del(_native_Native)
    return tmp_form

def to_mdtraj_Topology(item):

    from mdtraj.core.topology import Topology as _mdtraj_Topology

    tmp_form = to_openmm_Topology(item)
    tmp_form = _mdtraj_Topology.from_openmm(tmp_form)
    del(_mdtraj_Topology)
    return tmp_form

def to_mdtraj_Trajectory(item):

    return to_mdtraj(item)

def to_mdtraj(item):

    from mdtraj.core.trajectory import Trajectory as _mdtraj_trajectory
    from mdtraj.core.topology import Topology as _mdtraj_topology
    tmp_form = _mdtraj_trajectory(item.positions._value,_mdtraj_topology.from_openmm(item.topology))
    del(_mdtraj_trajectory,_mdtraj_topology)
    return tmp_form

def to_modeller(item):

    from simtk.openmm.app import Modeller as _openmm_app_Modeller
    return _openmm_app_Modeller(item.topology, item.positions)

def to_openmm_Topology(item):

    return item.topology

def to_openmm_Positions(item):

    return item.positions

def to_yank_Topography(item):

    from yank import Topography as _yank_Topography
    tmp_form = to_openmm_Topology(item)
    tmp_form = _yank_Topography(tmp_form)
    del(_yank_Topography)
    return tmp_form

def to_parmed_Structure(item):

    from .api_openmm_Topology import to_parmed_Structure as _openmm_Topology_to_parmed_Structure
    tmp_form = to_openmm_Topology(item)
    tmp_form = _openmm_Topology_to_parmed_Structure(tmp_form)
    del(_openmm_Topology_to_parmed_Structure)
    return tmp_form

def to_pdb(item,output_file):

    from simtk.openmm.app import PDBFile as _openmm_app_PDBFILE
    return _openmm_app_PDBFILE.writeFile(item.topology, item.positions, open(output_file, 'w'))

def select_with_mdtraj(item, selection):

    tmp_form=to_mdtraj(item)
    tmp_sel=tmp_form.topology.select(selection)
    del(tmp_form)
    return tmp_sel
