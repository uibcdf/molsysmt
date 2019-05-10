from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'dcd': form_name,
    'DCD': form_name
    }

def to_mdtraj(item,topology=None):

    if not topology:
        raise ValueError('"topology" argument is required for dcd.to_mdtraj')

    from molmodmt import convert as _molmodmt_convert
    from mdtraj import load_dcd as _mdtraj_load_dcd
    _mdtraj_topology = _molmodmt_convert(topology,'mdtraj.Topology')
    tmp_form = _mdtraj_load_dcd(item, top=_mdtraj_topology)
    del(_mdtraj_load_dcd, _mdtraj_topology, _molmodmt_convert)
    return tmp_form

def to_mdanalysis(item,topology=None):

    if not topology:
        raise ValueError('"topology" argument is required for dcd.to_mdtraj')

    from MDAnalysis import Universe as _mdanalysis_universe
    return _mdanalysis_universe(topology,item)
