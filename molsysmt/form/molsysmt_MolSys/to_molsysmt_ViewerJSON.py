from molsysmt._private.arg_digestion import arg_digest
from molsysmt.native import ViewerJSON
from molsysmt.form.molsysmt_Topology.to_molsysmt_ViewerJSON import to_molsysmt_ViewerJSON as topology_to_viewer
from molsysmt.form.molsysmt_Structures.to_molsysmt_ViewerJSON import to_molsysmt_ViewerJSON as structures_to_viewer


@arg_digest(form='molsysmt.MolSys')
def to_molsysmt_ViewerJSON(item, skip_digestion=False):
    """Converting a native MolSys into a ViewerJSON container."""

    topo_vjson = topology_to_viewer(item.topology, skip_digestion=True)
    struct_vjson = structures_to_viewer(item.structures, skip_digestion=True)

    viewer = ViewerJSON()
    topo_data = topo_vjson.to_dict()
    struct_data = struct_vjson.to_dict()

    viewer.data["atoms"] = topo_data.get("atoms", {})
    viewer.data["bonds"] = topo_data.get("bonds", {})
    viewer.data["structures"] = struct_data.get("structures", struct_data.get("estructures", struct_data.get("frames", [])))

    return viewer
