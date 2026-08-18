from molsysmt._private.argdigest import arg_digest
import types

form = 'MDAnalysis.AtomGroup'


@arg_digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting atom name from atom in form MDAnalysis.AtomGroup.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology.get_topological_attributes import get_atom_name_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
