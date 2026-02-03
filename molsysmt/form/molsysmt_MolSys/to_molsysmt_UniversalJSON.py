from molsysmt._private.digestion import arg_digest
from molsysmt.native import UniversalJSON
from molsysmt.form.molsysmt_Topology import to_molsysmt_UniversalJSON as topology_to_universal
from molsysmt.form.molsysmt_Structures import to_molsysmt_UniversalJSON as structures_to_universal


@arg_digest(form='molsysmt.MolSys')
def to_molsysmt_UniversalJSON(item, skip_digestion=False):
    """Converting a native MolSys into a UniversalJSON container."""

    topo_ujson = topology_to_universal(item.topology, skip_digestion=True)
    struct_ujson = structures_to_universal(item.structures, skip_digestion=True)

    data = topo_ujson.to_dict(copy=True)
    struct_data = struct_ujson.to_dict(copy=True)
    data["coordinates"] = struct_data.get("coordinates", {"collections": []})

    return UniversalJSON(data=data)
