from molsysmt._private.argdigest import arg_digest
from molsysmt.form.molsysmt_Structures.to_molsysmt_ViewerJSON import (
    to_molsysmt_ViewerJSON as structures_to_viewer,
)
from molsysmt.form.molsysmt_ViewerJSON._from_native import (
    export_native as topology_to_viewer,
)
from molsysmt.native import ViewerJSON


def _json_list(values):
    """Normalize nullable numerical fields with the topology export's JSON rules."""
    from molsysmt.form.molsysmt_ViewerJSON._from_native import _series_to_list

    return [] if values is None else _series_to_list(values)


@arg_digest(form="molsysmt.MolSys")
def to_molsysmt_ViewerJSON(item, skip_digestion=False):
    """
    Converting from molsysmt.MolSys to molsysmt.ViewerJSON.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.ViewerJSON
        Resulting object in molsysmt.ViewerJSON form.


    .. versionadded:: 1.0.0
    """

    topo_vjson = topology_to_viewer(
        item.topology, chemical_states=item.chemical_states, skip_digestion=True
    )
    struct_vjson = structures_to_viewer(item.structures, skip_digestion=True)

    viewer = ViewerJSON()
    # Both intermediates were built two lines above, are local, and are discarded
    # on return: their containers are handed to `viewer`, so ownership transfers
    # and the default deep copy of `to_dict()` would protect nothing.
    topo_data = topo_vjson.to_dict(copy=False)
    struct_data = struct_vjson.to_dict(copy=False)

    viewer.data["atoms"] = topo_data.get("atoms", {})
    viewer.data["bonds"] = topo_data.get("bonds", {})
    viewer.data["structures"] = struct_data.get(
        "structures", struct_data.get("estructures", struct_data.get("frames", []))
    )

    partial_charge = (
        []
        if item.molecular_mechanics is None
        else _json_list(item.molecular_mechanics.partial_charge)
    )
    if partial_charge:
        viewer.data["atoms"]["partial_charge"] = partial_charge

    return viewer
