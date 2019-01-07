from os.path import basename as _basename
from parmed.structure import Structure as _parmed_Structure

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _parmed_Structure : form_name
}

def to_mdtraj(item):

    from mdtraj.core.trajectory import Trajectory as mdtraj_trajectory
    from mdtraj.core.topology import Topology as mdtraj_topology

    return mdtraj_trajectory(item.positions._value,mdtraj_topology.from_openmm(item.topology))

def to_nglview(item):

    from nglview import show_parmed as _nglview_show_parmed
    return _nglview_show_parmed(item)

def to_pdb(item,output_file):

    return item.save(output_file)

def to_mol2(item,output_file):

    return item.save(output_file)

def select_with_mdtraj(item, selection):
    tmp_form=to_mdtraj(item)
    tmp_sel=tmp_form.topology.select(selection)
    del(tmp_form)
    return tmp_sel

def select_with_parmed(item, selection):
    from parmed.amber import AmberMask as _AmberMask
    tmp_sel = list(_AmberMask(item,selection).Selected())
    del(_AmberMask)
    return tmp_sel

