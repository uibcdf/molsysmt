from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='openmm.CharmmCrdFile')
@dep_digest('openmm')
def to_openmm_CharmmCrdFile(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from openmm.CharmmCrdFile to openmm.CharmmCrdFile.

    Parameters
    ----------
    item : openmm.CharmmCrdFile
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.CharmmCrdFile
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, skip_digestion=True)

