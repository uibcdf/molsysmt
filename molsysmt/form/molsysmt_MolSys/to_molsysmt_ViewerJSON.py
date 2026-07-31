from molsysmt._private.arg_digestion import arg_digest
from molsysmt.native import ViewerJSON
from molsysmt.form.molsysmt_Topology.to_molsysmt_ViewerJSON import to_molsysmt_ViewerJSON as topology_to_viewer
from molsysmt.form.molsysmt_Structures.to_molsysmt_ViewerJSON import to_molsysmt_ViewerJSON as structures_to_viewer


def _json_list(values):
    if values is None:
        return []
    output = []
    for value in list(values):
        try:
            if value is None:
                output.append(None)
            elif float(value).is_integer():
                output.append(int(value))
            else:
                output.append(float(value))
        except Exception:
            output.append(value)
    return output


@arg_digest(form='molsysmt.MolSys')
def to_molsysmt_ViewerJSON(item, skip_digestion=False):
    """Converting a native MolSys into a ViewerJSON container."""

    topo_vjson = topology_to_viewer(item.topology, skip_digestion=True)
    struct_vjson = structures_to_viewer(item.structures, skip_digestion=True)

    viewer = ViewerJSON()
    # Both intermediates were built two lines above, are local, and are discarded
    # on return: their containers are handed to `viewer`, so ownership transfers
    # and the default deep copy of `to_dict()` would protect nothing.
    topo_data = topo_vjson.to_dict(copy=False)
    struct_data = struct_vjson.to_dict(copy=False)

    viewer.data["atoms"] = topo_data.get("atoms", {})
    viewer.data["bonds"] = topo_data.get("bonds", {})
    viewer.data["structures"] = struct_data.get("structures", struct_data.get("estructures", struct_data.get("frames", [])))

    formal_charge = _json_list(item.molecular_mechanics.formal_charge)
    if formal_charge:
        viewer.data["atoms"]["formal_charge"] = formal_charge
    partial_charge = _json_list(item.molecular_mechanics.partial_charge)
    if partial_charge:
        viewer.data["atoms"]["partial_charge"] = partial_charge

    return viewer
