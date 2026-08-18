from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='MDAnalysis.Topology')
@dep_digest('MDAnalysis')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of elements or structures from form MDAnalysis.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    copy_if_all : object, default=True
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    MDAnalysis.Topology
        Resulting object in MDAnalysis.Topology form.


    .. versionadded:: 1.0.0
    """

    if not is_all(structure_indices):
        from molsysmt._private.smonitor import NotCompatibleConversionError

        raise NotCompatibleConversionError(
            'MDAnalysis.Topology',
            'MDAnalysis.Topology',
            {'structure_indices'},
            caller='molsysmt.form.MDAnalysis_Topology.extract',
            message='MDAnalysis.Topology does not contain structures.',
        )

    if is_all(atom_indices):
        return item.copy() if copy_if_all else item

    import MDAnalysis as mda

    universe = mda.Universe(item)
    return mda.Merge(universe.atoms[atom_indices])._topology
