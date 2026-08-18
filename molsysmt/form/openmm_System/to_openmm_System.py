from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.System')
def to_openmm_System(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from openmm.System to openmm.System.

    Parameters
    ----------
    item : openmm.System
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.System
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, skip_digestion=True)

