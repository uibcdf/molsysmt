"""Embedding native structural data in a partial molecular system."""

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="molsysmt.Structures")
def to_molsysmt_MolSys(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """Converting structures to an independent MolSys without invented chemistry.

    Parameters
    ----------
    item : molecular system
        Native Structures containing structural series in their stored units.
    atom_indices : int, list, tuple or numpy.ndarray, default='all'
        Positional atom indices to retain, following native structural extraction.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Positional structure indices to retain in the requested order.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Independent structural domain. Topology and ChemicalStates remain absent.
        Physical series, units and supported structural metadata are preserved.

    Notes
    -----
    The conversion establishes no atom identities or chemical bonds. Full-axis
    copying shares protected immutable geometry through independent handles.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.native import Structures
    >>> structures = Structures(coordinates=msm.pyunitwizard.quantity([[[0., 1., 2.]]], 'nm'))
    >>> molsys = msm.convert(structures, to_form='molsysmt.MolSys')
    >>> molsys.topology is None and molsys.chemical_states is None
    True

    .. versionadded:: 1.0.0
    """
    from molsysmt.native import MolSys

    from .extract import extract

    if is_all(atom_indices) and is_all(structure_indices):
        structures = item.copy(deep=False, skip_digestion=True)
    else:
        structures = extract(
            item,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            copy_if_all=True,
            skip_digestion=True,
        )
    return MolSys._from_partial_domains(structures=structures)
