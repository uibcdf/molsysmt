from molsysmt._private.argdigest import arg_digest
import types

form='openmm.AmberPrmtopFile'

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):
    return 0

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):
    from molsysmt.form.openmm_Topology import get_box_from_system as aux_get

    return aux_get(
        item.topology,
        structure_indices=structure_indices,
        skip_digestion=True,
    )

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
