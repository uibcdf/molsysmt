from molsysmt._private.argdigest import arg_digest
import types

form='openmm.PDBFile'

@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting atom id from atom in form openmm.PDBFile.

    Parameters
    ----------
    item : openmm.PDBFile
        Source item in openmm.PDBFile form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.openmm_Topology import get_atom_id_from_atom as aux_get
    return aux_get(item.getTopology(), indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting atom name from atom in form openmm.PDBFile.

    Parameters
    ----------
    item : openmm.PDBFile
        Source item in openmm.PDBFile form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.openmm_Topology import get_atom_name_from_atom as aux_get
    return aux_get(item.getTopology(), indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting atom type from atom in form openmm.PDBFile.

    Parameters
    ----------
    item : openmm.PDBFile
        Source item in openmm.PDBFile form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.openmm_Topology import get_atom_type_from_atom as aux_get
    return aux_get(item.getTopology(), indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    """
    Getting n atoms from system in form openmm.PDBFile.

    Parameters
    ----------
    item : openmm.PDBFile
        Source item in openmm.PDBFile form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.getTopology().getNumAtoms()

@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):
    """
    Getting n groups from system in form openmm.PDBFile.

    Parameters
    ----------
    item : openmm.PDBFile
        Source item in openmm.PDBFile form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return item.getTopology().getNumResidues()

# ... add more if needed, or use a generic delegation loop if we want full parity ...

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
