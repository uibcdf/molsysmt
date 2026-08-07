from molsysmt._private.argdigest import arg_digest
import types

form = 'MDAnalysis.AtomGroup'


@arg_digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):
    from .to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology.get_topological_attributes import get_atom_name_from_atom as aux_get

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
