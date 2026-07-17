from molsysmt.form.MDAnalysis_Topology.attributes import (
    attributes as _topology_attributes,
)

attributes = dict(_topology_attributes)
attributes['coordinates'] = True
attributes['velocities'] = True
attributes['box'] = True
attributes['time'] = True
attributes['structure_id'] = True
attributes['structure_index'] = True
attributes['n_structures'] = True

del(_topology_attributes)
