from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="mdtraj.Topology")
@dep_digest("parmed")
@dep_digest("openmm")
def to_parmed_Structure(item, atom_indices="all", skip_digestion=False):
    """
    Converting from mdtraj.Topology to parmed.Structure.


    Parameters
    ----------
    item : molecular system
        MDTraj topology to convert. It contains no coordinates or force-field parameters.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include. Selected atoms retain source order.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    parmed.Structure
        Converted topology without coordinates or assigned force-field parameters.

    Examples
    --------
    >>> import molsysmt as msm
    >>> source = msm.convert(msm.systems['Trp-Cage']['1l2y.pdb'],
    ...                      to_form='mdtraj.Topology')
    >>> converted = to_parmed_Structure(source)
    >>> len(converted.atoms) == source.n_atoms and converted.coordinates is None
    True

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.openmm_Topology.to_parmed_Structure import (
        to_parmed_Structure as openmm_Topology_to_parmed_Structure,
    )

    from .to_openmm_Topology import to_openmm_Topology

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = openmm_Topology_to_parmed_Structure(tmp_item, skip_digestion=True)

    return tmp_item
