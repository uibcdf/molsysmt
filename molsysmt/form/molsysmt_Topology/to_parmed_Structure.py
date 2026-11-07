from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.Topology")
@dep_digest("parmed")
def to_parmed_Structure(item, atom_indices="all", skip_digestion=False):
    """
    Converting stable native inventory to an unparameterized ParmEd structure.


    Parameters
    ----------
    item : molecular system
        Stable inventory. Attached chemistry, geometry and mechanics are not
        recovered; convert the owning MolSys to include those domains.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    parmed.Structure
        Detached atom, group and chain inventory, without bonds or coordinates.

    Raises
    ------
    LibraryNotFoundError
        If the optional ParmEd provider is unavailable.
    NotCompatibleConversionError
        If atom/group labels or chemical element symbols cannot be represented.

    Examples
    --------
    >>> from molsysmt.native import Topology
    >>> len(to_parmed_Structure(Topology()).atoms)
    0


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.parmed_Structure._from_native import export_native

    from .extract import extract

    selected = extract(
        item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True
    )
    return export_native(selected)
