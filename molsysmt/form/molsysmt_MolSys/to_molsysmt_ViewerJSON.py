from molsysmt._private.digestion import digest
from molsysmt.native import ViewerJSON
from molsysmt.form.molsysmt_Topology import to_molsysmt_ViewerJSON as topology_to_viewer
from molsysmt.form.molsysmt_Structures import to_molsysmt_ViewerJSON as structures_to_viewer


@digest(form='molsysmt.MolSys')
def to_molsysmt_ViewerJSON(item, skip_digestion=False):
    """Convert a native MolSys into a ViewerJSON container."""

    topo_vjson = topology_to_viewer(item.topology, skip_digestion=True)
    struct_vjson = structures_to_viewer(item.structures, skip_digestion=True)

    data = {
        "version": topo_vjson.data.get("version", "0.1"),
        "atoms": topo_vjson.data.get("atoms", {}),
        "bonds": topo_vjson.data.get("bonds", {}),
        "estructures": struct_vjson.data.get("estructures", struct_vjson.data.get("frames", [])),
    }

    return ViewerJSON(data=data)
